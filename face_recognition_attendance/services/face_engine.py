import os
import threading
import urllib.request
from pathlib import Path
import cv2
import numpy as np
from config import Config

# URLs to download the pre-trained ONNX models from Hugging Face
YUNET_URL = "https://huggingface.co/opencv/face_detection_yunet/resolve/main/face_detection_yunet_2023mar.onnx"
SFACE_URL = "https://huggingface.co/opencv/face_recognition_sface/resolve/main/face_recognition_sface_2021dec.onnx"

class FaceEngine:
    def __init__(self):
        self.model_dir = Config.MODEL_DIR
        self.yunet_path = self.model_dir / "face_detection_yunet.onnx"
        self.sface_path = self.model_dir / "face_recognition_sface.onnx"
        self.lock = threading.Lock()
        
        # Ensure models are downloaded
        self._ensure_models_downloaded()
        
        # Initialize YuNet Detector using positional arguments (OpenCV C++ bindings do not accept keyword arguments)
        # Signature: create(model, config, input_size, score_threshold, nms_threshold, top_k)
        self.detector = cv2.FaceDetectorYN.create(
            str(self.yunet_path),
            "",
            (320, 320),
            float(Config.CONFIDENCE_THRESHOLD),
            0.3,
            5000
        )
        
        # Initialize SFace Recognizer using positional arguments
        # Signature: create(model, config)
        self.recognizer = cv2.FaceRecognizerSF.create(
            str(self.sface_path),
            ""
        )

    def _ensure_models_downloaded(self):
        """Downloads the ONNX models if they do not exist."""
        if not self.yunet_path.exists():
            print(f"Downloading YuNet model to {self.yunet_path}...")
            self._download_file(YUNET_URL, self.yunet_path)
            
        if not self.sface_path.exists():
            print(f"Downloading SFace model to {self.sface_path}...")
            self._download_file(SFACE_URL, self.sface_path)

    def _download_file(self, url: str, dest_path: Path):
        """Helper to download a file from a URL with basic progress reporting."""
        try:
            import requests
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Successfully downloaded: {dest_path.name}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            # Fallback to urllib if requests fails
            try:
                urllib.request.urlretrieve(url, str(dest_path))
                print(f"Successfully downloaded via urllib: {dest_path.name}")
            except Exception as e2:
                raise IOError(f"Could not download model from {url}. Error: {e2}")

    def detect_faces(self, frame: np.ndarray):
        """
        Detects faces in the given BGR image frame thread-safely.
        Updates input size dynamically to match the frame size.
        Returns:
            faces: numpy array of detected faces or None. 
                   Each face row contains: [x, y, w, h, x_re, y_re, x_le, y_le, x_nt, y_nt, x_rc, y_rc, x_lc, y_lc, score]
        """
        if frame is None or not isinstance(frame, np.ndarray) or frame.size == 0:
            return None
            
        with self.lock:
            h, w = frame.shape[:2]
            self.detector.setInputSize((int(w), int(h)))
            _, faces = self.detector.detect(frame)
            return faces

    def extract_embedding(self, frame: np.ndarray, face_coords) -> np.ndarray:
        """
        Aligns the face and extracts the 128-dimensional face embedding thread-safely.
        Args:
            frame: The original BGR frame.
            face_coords: The face detection array row returned from YuNet.
        Returns:
            embedding: 128-dimensional float32 numpy array representing face features.
        """
        if frame is None or face_coords is None:
            return np.zeros(128, dtype=np.float32)

        with self.lock:
            # Ensure face_coords is a 2D float32 numpy array with shape (1, 15) for OpenCV alignCrop
            face_coords_arr = np.asarray(face_coords, dtype=np.float32)
            if face_coords_arr.ndim == 1:
                face_coords_arr = face_coords_arr.reshape(1, -1)
                
            aligned_face = self.recognizer.alignCrop(frame, face_coords_arr)
            if aligned_face is None or getattr(aligned_face, 'size', 0) == 0:
                return np.zeros(128, dtype=np.float32)
                
            embedding = self.recognizer.feature(aligned_face)
            return embedding.flatten().astype(np.float32)

    @staticmethod
    def compute_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Computes Cosine Similarity between two face embeddings.
        Cosine similarity = (A . B) / (||A|| * ||B||)
        Since SFace embeddings are L2 normalized, it simplifies to A . B.
        """
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(embedding1, embedding2) / (norm1 * norm2))

    def match_face(self, query_embedding: np.ndarray, known_students_embeddings: list) -> tuple:
        """
        Matches a face embedding against a list of known student face embeddings.
        Args:
            query_embedding: The extracted embedding from the live camera frame (1D array).
            known_students_embeddings: List of dicts: [{'student_id': str, 'embedding': np.ndarray}]
        Returns:
            (student_id, similarity) if similarity matches the threshold, else (None, 0.0)
        """
        if not known_students_embeddings:
            return None, 0.0
            
        best_student_id = None
        best_similarity = -1.0
        
        for record in known_students_embeddings:
            student_id = record['student_id']
            known_emb = record['embedding']
            
            # Compute cosine similarity
            similarity = self.compute_similarity(query_embedding, known_emb)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_student_id = student_id
                
        # Check against match threshold
        # For Cosine Similarity, we want similarity >= MATCH_THRESHOLD (e.g. 0.363 cosine distance translation corresponds to ~0.363 similarity if using distance, or ~0.60 standard threshold for cosine similarity).
        # We make this configurable. The default MATCH_THRESHOLD is 0.60 (or 0.363 depending on distance/similarity).
        # Let's adjust: in SFace, cosine similarity >= 0.363 is generally considered a match (since its feature space is highly separated). Let's use Config.MATCH_THRESHOLD (default 0.363 or 0.40 for reliability).
        if best_similarity >= Config.MATCH_THRESHOLD:
            return best_student_id, best_similarity
            
        return None, best_similarity
