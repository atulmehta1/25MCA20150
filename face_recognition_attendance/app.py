import os
import sys
from pathlib import Path

# Ensure application directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import base64
import json
import queue
import threading
import time
from datetime import datetime, timedelta, timezone
import cv2
import numpy as np
# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, jsonify, Response, send_file
from sqlalchemy import or_
from config import Config
from database.db import db
from database.models import Student, FaceEmbedding, Attendance
from services.face_engine import FaceEngine
from services.attendance_service import AttendanceService

app = Flask(__name__, template_folder=str(BASE_DIR / 'templates'), static_folder=str(BASE_DIR / 'static'))
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Initialize Face Recognition Engine
# FaceEngine downloads ONNX files automatically if not present.
face_engine = FaceEngine()

# Global Cache for Face Embeddings
# Structure: [{'student_id': str, 'name': str, 'department': str, 'embedding': np.ndarray}]
known_face_cache = []
cache_lock = threading.Lock()

# SSE Listeners queue
sse_listeners = []
listeners_lock = threading.Lock()

def refresh_face_cache():
    """
    Refreshes the in-memory face embeddings cache from the database.
    This avoids hit-testing the database on every webcam frame.
    """
    global known_face_cache
    with app.app_context():
        try:
            students = Student.query.all()
            new_cache = []
            for s in students:
                for emb in s.embeddings:
                    arr = emb.get_embedding()
                    if arr is not None and arr.size == 128:
                        new_cache.append({
                            'student_id': s.student_id,
                            'name': s.name,
                            'department': s.department,
                            'embedding': arr
                        })
            with cache_lock:
                known_face_cache = new_cache
            print(f"Face cache refreshed: {len(known_face_cache)} signatures loaded.")
        except Exception as e:
            print(f"Error refreshing face cache: {e}")

def broadcast_attendance_event(student_id, name, department, time_str):
    """
    Broadcasts a new attendance event to all active SSE listeners.
    """
    with app.app_context():
        stats = AttendanceService.get_dashboard_stats()
        weekly_chart = AttendanceService.get_weekly_chart_data()

    event_data = {
        'student_id': student_id,
        'name': name,
        'department': department,
        'time': time_str,
        'stats': stats,
        'weekly_chart': weekly_chart
    }
    
    event_str = f"data: {json.dumps(event_data)}\n\n"
    
    with listeners_lock:
        for q in list(sse_listeners):
            try:
                q.put_nowait(event_str)
            except Exception:
                sse_listeners.remove(q)

def gen_frames():
    """
    Generates video frames from the webcam, performs face detection and recognition,
    overlays bounding boxes, and streams them as an MJPEG feed.
    """
    # Use DirectShow on Windows for fast webcam initialization, fallback to default
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not camera.isOpened():
        camera = cv2.VideoCapture(0)
    
    # Try to set camera dimensions for optimization (640x480 is standard)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH if hasattr(cv2, 'CAP_PROP_FRAME_WIDTH') else 3, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT if hasattr(cv2, 'CAP_PROP_FRAME_HEIGHT') else 4, 480)

    last_recognition_time = {} # Cooldown for marking attendance per student in the current session (e.g. 10 sec)
    
    try:
        while True:
            success, frame = camera.read()
            if not success:
                # If camera is unavailable, stream a static modern placeholder
                placeholder = np.zeros((480, 640, 3), dtype=np.uint8)
                # Draw subtle dark slate background
                placeholder[:, :] = [22, 13, 9] 
                cv2.putText(placeholder, "NO CAMERA DETECTED", (150, 220), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (129, 163, 148), 2, cv2.LINE_AA)
                cv2.putText(placeholder, "Please connect a webcam or check permissions.", (80, 260), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (184, 163, 148), 1, cv2.LINE_AA)
                
                # Encode and yield
                ret, jpeg = cv2.imencode('.jpg', placeholder)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
                time.sleep(0.5)
                continue

            # Run Face Detection (YuNet is highly optimized for CPU)
            faces = face_engine.detect_faces(frame)
            
            if faces is not None:
                for face in faces:
                    # YuNet returns detection properties
                    # Bounding box is the first 4 parameters [x, y, w, h]
                    box = face[0:4].astype(int)
                    x, y, w, h = box[0], box[1], box[2], box[3]
                    
                    # Prevent drawing off screen boundaries
                    x = max(0, x)
                    y = max(0, y)

                    color = (94, 63, 244) # Rose (Default color for unrecognized face)
                    label = "Scanning..."
                    
                    # Extract Embedding and perform Match
                    try:
                        embedding = face_engine.extract_embedding(frame, face)
                        
                        with cache_lock:
                            cached_embeddings = list(known_face_cache)
                        
                        student_id, sim = face_engine.match_face(embedding, cached_embeddings)
                        
                        if student_id:
                            # Find student name from cache
                            student_info = next((item for item in cached_embeddings if item['student_id'] == student_id), None)
                            student_name = student_info['name'] if student_info else student_id
                            student_dept = student_info['department'] if student_info else "N/A"
                            
                            color = (129, 185, 16) # Emerald / Green
                            label = f"{student_name} ({sim:.2f})"
                            
                            # Mark attendance (cooldown check to avoid heavy db writes on every video frame)
                            now = datetime.now()
                            last_marked = last_recognition_time.get(student_id)
                            
                            if not last_marked or (now - last_marked).total_seconds() > 30: # 30 seconds local stream cooldown
                                last_recognition_time[student_id] = now
                                
                                # Perform DB insertion in request context thread-safely
                                with app.app_context():
                                    marked, msg = AttendanceService.mark_attendance(student_id)
                                    if marked:
                                        print(f"Attendance recorded via Live Feed: {msg}")
                                        # Push live update to dashboard
                                        broadcast_attendance_event(
                                            student_id, 
                                            student_name, 
                                            student_dept, 
                                            now.strftime('%H:%M:%S')
                                        )
                        else:
                            label = f"Unknown Face ({sim:.2f})"
                            
                    except Exception as e:
                        # Print debug details but don't break the camera loop
                        # print(f"Frame processing error: {e}")
                        pass
                    
                    # Draw Glassmorphic Bounding Box (rounded corner rectangles)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    
                    # Draw a nice semi-transparent overlay label backplate
                    overlay = frame.copy()
                    cv2.rectangle(overlay, (x, y - 25), (x + w, y), color, cv2.FILLED)
                    cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
                    
                    # Draw label text
                    cv2.putText(frame, label, (x + 5, y - 7), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)

            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
                
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                   
    finally:
        camera.release()

# ----------------- FLASK VIEW ROUTES -----------------

@app.route('/')
def dashboard():
    stats = AttendanceService.get_dashboard_stats()
    chart_data = AttendanceService.get_weekly_chart_data()
    return render_template('dashboard.html', active_page='dashboard', stats=stats, chart_data=chart_data)

@app.route('/students')
def students():
    return render_template('students.html', active_page='students')

@app.route('/history')
def history():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    search_query = request.args.get('search', '')
    
    # Query logs matching filters
    query = Attendance.query.join(Student, Attendance.student_id == Student.student_id)
    
    if start_date and start_date.strip():
        try:
            s_date = datetime.strptime(start_date.strip(), '%Y-%m-%d')
            query = query.filter(Attendance.timestamp >= s_date)
        except ValueError:
            pass
    if end_date and end_date.strip():
        try:
            e_date = datetime.strptime(end_date.strip(), '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Attendance.timestamp < e_date)
        except ValueError:
            pass
    if search_query and search_query.strip():
        sq = search_query.strip()
        query = query.filter(
            or_(
                Student.student_id.like(f"%{sq}%"),
                Student.name.like(f"%{sq}%"),
                Student.department.like(f"%{sq}%")
            )
        )
        
    logs = query.order_by(Attendance.timestamp.desc()).all()
    
    return render_template(
        'history.html', 
        active_page='history', 
        logs=logs,
        start_date=start_date,
        end_date=end_date,
        search_query=search_query
    )

# ----------------- WEB STREAM ROUTES -----------------

@app.route('/video_feed')
def video_feed():
    """
    Returns the live MJPEG camera feed response.
    """
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/attendance_stream')
def attendance_stream():
    """
    Server-Sent Events (SSE) route to push new attendance detections to dashboard.
    """
    def event_generator():
        q = queue.Queue()
        with listeners_lock:
            sse_listeners.append(q)
            
        try:
            # Send initial keepalive
            yield "data: {\"heartbeat\": true}\n\n"
            
            while True:
                try:
                    # Timeout to prevent blocking permanently when client disconnects
                    data = q.get(timeout=15)
                    yield data
                except queue.Empty:
                    # Keep-alive heartbeat
                    yield "data: {\"heartbeat\": true}\n\n"
        except GeneratorExit:
            with listeners_lock:
                if q in sse_listeners:
                    sse_listeners.remove(q)

    return Response(event_generator(), mimetype='text/event-stream')

# ----------------- REST API ENDPOINTS -----------------

@app.route('/api/students', methods=['GET'])
def api_get_students():
    """
    Returns list of all registered students.
    """
    students = Student.query.order_by(Student.student_id.asc()).all()
    result = []
    for s in students:
        s_dict = s.to_dict()
        s_dict['has_embedding'] = len(s.embeddings) > 0
        result.append(s_dict)
    return jsonify(result)

@app.route('/api/students/register', methods=['POST'])
def api_register_student():
    """
    Registers a new student and extracts face embedding details.
    Accepts JSON body: student_id, name, email, department, face_image (base64).
    """
    data = request.json
    if not data:
        return jsonify({'success': False, 'error': 'Missing JSON data payload.'}), 400
        
    student_id = data.get('student_id')
    name = data.get('name')
    email = data.get('email')
    department = data.get('department')
    face_image_base64 = data.get('face_image')
    
    if not all([student_id, name, email, department, face_image_base64]):
        return jsonify({'success': False, 'error': 'Missing required registration parameters.'}), 400
        
    # Check if student already exists
    existing = Student.query.filter_by(student_id=student_id).first()
    if existing:
        return jsonify({'success': False, 'error': f"Student ID {student_id} is already registered."}), 400

    try:
        # Decode base64 image safely handling data URL prefix if present
        if "," in face_image_base64:
            _, encoded = face_image_base64.split(",", 1)
        else:
            encoded = face_image_base64
        image_bytes = base64.b64decode(encoded)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return jsonify({'success': False, 'error': 'Failed to decode image payload.'}), 400
            
        # Detect Face & Extract Embedding
        faces = face_engine.detect_faces(img)
        if faces is None or len(faces) == 0:
            return jsonify({'success': False, 'error': 'No face detected in the image. Please try again with clear lighting.'}), 400
        
        # Take the first (largest/highest score) face
        face_details = faces[0]
        embedding_array = face_engine.extract_embedding(img, face_details)
        
        # Save Student record
        new_student = Student(
            student_id=student_id,
            name=name,
            email=email,
            department=department
        )
        db.session.add(new_student)
        
        # Save Face Embedding record
        new_embedding = FaceEmbedding(student_id=student_id)
        new_embedding.set_embedding(embedding_array)
        db.session.add(new_embedding)
        
        db.session.commit()
        
        # Update our in-memory cache thread-safely
        refresh_face_cache()
        
        return jsonify({
            'success': True, 
            'message': f"Student {name} registered and face details enrolled successfully."
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error registering student: {e}")
        return jsonify({'success': False, 'error': f"Database enrollment failure: {str(e)}"}), 500

@app.route('/api/students/delete/<student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        return jsonify({'success': False, 'error': 'Student not found.'}), 404
        
    try:
        db.session.delete(student)
        db.session.commit()
        refresh_face_cache() # update active cache
        return jsonify({'success': True, 'message': f"Student {student_id} and all related logs deleted."})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f"Failed to delete student: {str(e)}"}), 500

@app.route('/api/attendance/delete/<int:log_id>', methods=['DELETE'])
def api_delete_log(log_id):
    log = db.session.get(Attendance, log_id) if hasattr(db.session, 'get') else Attendance.query.get(log_id)
    if not log:
        return jsonify({'success': False, 'error': 'Log entry not found.'}), 404
        
    try:
        db.session.delete(log)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Log entry deleted successfully.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f"Failed to delete log: {str(e)}"}), 500

@app.route('/export_excel')
def export_excel():
    start_date = request.args.get('start_date', None)
    end_date = request.args.get('end_date', None)
    search_query = request.args.get('search', None)
    
    excel_file = AttendanceService.export_to_excel(start_date, end_date, search_query)
    
    filename = f"Attendance_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    return send_file(
        excel_file,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

# ----------------- APP INITIALIZATION -----------------

# Context Processor to inject current time into templates if needed
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Initialize DB tables and face cache on startup (supports flask run and WSGI)
with app.app_context():
    try:
        db.create_all()
        print("Database initialized (SQLite attendance.db ready).")
        refresh_face_cache()
    except Exception as e:
        print(f"Warning: Database initialization error: {e}")

if __name__ == '__main__':
    # Run the server on port 5050
    # Set host='0.0.0.0' to allow network devices to access the attendance screen
    app.run(host='0.0.0.0', port=5050, debug=True, use_reloader=False)
