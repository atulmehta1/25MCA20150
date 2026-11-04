from datetime import datetime, time, timedelta
import io
import pandas as pd
from sqlalchemy import func, or_
from database.db import db
from database.models import Student, Attendance

class AttendanceService:
    @staticmethod
    def mark_attendance(student_id: str) -> tuple:
        """
        Marks attendance for a student for the current day.
        Checks if attendance was already marked today to prevent duplicates.
        Returns:
            (success: bool, message: str)
        """
        # Find student
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return False, f"Student ID {student_id} not registered."

        # Get start and end of today
        today_start = datetime.combine(datetime.now().date(), time.min)
        today_end = datetime.combine(datetime.now().date(), time.max)

        # Check if already marked today
        existing = Attendance.query.filter(
            Attendance.student_id == student_id,
            Attendance.timestamp.between(today_start, today_end)
        ).first()

        if existing:
            # Already marked, return success but flag that it was already marked
            return False, f"Attendance already marked for {student.name} today at {existing.timestamp.strftime('%H:%M:%S')}."

        # Create new attendance record
        new_attendance = Attendance(
            student_id=student_id,
            timestamp=datetime.now(),
            status='Present'
        )
        
        try:
            db.session.add(new_attendance)
            db.session.commit()
            return True, f"Attendance marked: {student.name} ({student.student_id}) at {new_attendance.timestamp.strftime('%H:%M:%S')}"
        except Exception as e:
            db.session.rollback()
            return False, f"Error saving attendance: {str(e)}"

    @staticmethod
    def get_dashboard_stats() -> dict:
        """
        Retrieves statistics for the admin dashboard.
        """
        # Count total students
        total_students = Student.query.count()

        # Count present students today (unique students)
        today_start = datetime.combine(datetime.now().date(), time.min)
        today_end = datetime.combine(datetime.now().date(), time.max)
        
        present_today = db.session.query(func.count(func.distinct(Attendance.student_id))).filter(
            Attendance.timestamp.between(today_start, today_end)
        ).scalar() or 0

        absent_today = max(0, total_students - present_today)
        
        attendance_rate = 0.0
        if total_students > 0:
            attendance_rate = round((present_today / total_students) * 100, 1)

        # Recent activities (last 5 attendance logs)
        recent_logs = Attendance.query.order_by(Attendance.timestamp.desc()).limit(5).all()
        recent_activities = []
        for log in recent_logs:
            recent_activities.append({
                'name': log.student.name if log.student else "Unknown",
                'student_id': log.student_id,
                'time': log.timestamp.strftime('%H:%M:%S') if log.timestamp else "",
                'date': log.timestamp.strftime('%Y-%m-%d') if log.timestamp else "",
                'department': log.student.department if log.student else "N/A"
            })

        return {
            'total_students': total_students,
            'present_today': present_today,
            'absent_today': absent_today,
            'attendance_rate': attendance_rate,
            'recent_activities': recent_activities
        }

    @staticmethod
    def get_weekly_chart_data() -> dict:
        """
        Retrieves attendance counts for the last 7 calendar days.
        Returns:
            {'labels': [date_strings], 'data': [present_counts]}
        """
        labels = []
        data = []
        
        # We loop from 6 days ago to today
        for i in range(6, -1, -1):
            day = datetime.now().date() - timedelta(days=i)
            day_start = datetime.combine(day, time.min)
            day_end = datetime.combine(day, time.max)
            
            count = Attendance.query.filter(
                Attendance.timestamp.between(day_start, day_end)
            ).count()
            
            # Format label, e.g. "Mon", "Tue" or "07/13"
            labels.append(day.strftime('%a (%b %d)'))
            data.append(count)
            
        return {
            'labels': labels,
            'data': data
        }

    @staticmethod
    def export_to_excel(start_date=None, end_date=None, search_query=None) -> io.BytesIO:
        """
        Queries attendance and exports it to an Excel workbook.
        """
        query = db.session.query(
            Attendance.timestamp,
            Attendance.student_id,
            Student.name,
            Student.email,
            Student.department,
            Attendance.status
        ).join(Student, Attendance.student_id == Student.student_id)

        if start_date and str(start_date).strip():
            try:
                s_date = datetime.strptime(str(start_date).strip(), '%Y-%m-%d')
                query = query.filter(Attendance.timestamp >= s_date)
            except ValueError:
                pass
            
        if end_date and str(end_date).strip():
            try:
                # Include the entire day of the end_date
                e_date = datetime.strptime(str(end_date).strip(), '%Y-%m-%d') + timedelta(days=1)
                query = query.filter(Attendance.timestamp < e_date)
            except ValueError:
                pass

        if search_query and str(search_query).strip():
            sq = str(search_query).strip()
            query = query.filter(
                or_(
                    Student.student_id.like(f"%{sq}%"),
                    Student.name.like(f"%{sq}%"),
                    Student.department.like(f"%{sq}%")
                )
            )

        records = query.order_by(Attendance.timestamp.desc()).all()

        # Build DataFrame
        data_list = []
        for rec in records:
            data_list.append({
                'Date': rec.timestamp.strftime('%Y-%m-%d') if rec.timestamp else "",
                'Time': rec.timestamp.strftime('%H:%M:%S') if rec.timestamp else "",
                'Student ID': rec.student_id,
                'Name': rec.name,
                'Email': rec.email,
                'Department': rec.department,
                'Status': rec.status
            })

        df = pd.DataFrame(data_list)
        if df.empty:
            # Return empty DataFrame with headers
            df = pd.DataFrame(columns=['Date', 'Time', 'Student ID', 'Name', 'Email', 'Department', 'Status'])

        # Export to BytesIO
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Attendance Report')
            
            # Adjust column width automatically
            from openpyxl.utils import get_column_letter
            workbook = writer.book
            worksheet = writer.sheets['Attendance Report']
            for col in worksheet.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                col_letter = get_column_letter(col[0].column)
                worksheet.column_dimensions[col_letter].width = max(max_len + 3, 10)

        output.seek(0)
        return output
