"""
Group: Controller Liberators
Pose detection module using MediaPipe.

This module provides the Detector class for real-time human pose estimation.
It detects 33 body landmarks and returns them for gesture-based game control.

Features:
- Guarded imports with graceful degradation if dependencies missing
- Cross-platform support (macOS, Windows, Linux)
- Configurable via sysconfig.ini
- Preset-aware visualization settings

Usage:
    from detector import Detector
    from context import Context
    
    ctx = Context(config)
    detector = Detector(ctx)
    landmarks, visual_frame = detector.get_landmarks(rgb_frame)
"""
import numpy as np

try:
    import mediapipe as mp
    _HAS_MEDIAPIPE = True
except Exception:  # broad to catch import errors and version incompat
    mp = None
    _HAS_MEDIAPIPE = False

try:
    import cv2
    _HAS_CV2 = True
except Exception:
    cv2 = None
    _HAS_CV2 = False
from .context import Context


class Detector:
    """
    Detect user pose, obtaining landmarks
    """
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        ctx.detector = self
        # If mediapipe or cv2 aren't available, keep the detector in a
        # disabled state and provide clear runtime guidance when used.
        if not _HAS_MEDIAPIPE or not _HAS_CV2:
            missing = []
            if not _HAS_MEDIAPIPE:
                missing.append('mediapipe')
            if not _HAS_CV2:
                missing.append('opencv-python (cv2)')
            self.disabled = True
            self._missing_deps = missing
            self.mp_pose = None
            self.pose = None
            return

        # Initialize the MediaPipe detector instance
        self.disabled = False
        self._missing_deps = []
        self.mp_pose = mp.solutions.pose
        
        # Load config from context
        cfg = ctx.cfg["MediaPipe"]
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,  # False for video stream，True for static image
            model_complexity=cfg.getint("model_complexity"),
            smooth_landmarks=cfg.getboolean("smooth_landmarks"),
            enable_segmentation=False,
            smooth_segmentation=True,
            min_detection_confidence=cfg.getfloat("min_detection_confidence"),
            min_tracking_confidence=cfg.getfloat("min_tracking_confidence")
        )

    def get_landmarks(self, frame):
        """
        Use the detector instance to detect user pose of upper body, obtain and return landmarks.
        :param frame: frame in RGB format
        Returns:
            tuple: (landmarks, visual_frame)
                - landmarks: landmarks detected by MediaPipe, or None if no pose detected
                - visual_frame: visualized frame with detected landmarks (if enabled)
        """
        if getattr(self, 'disabled', False):
            raise RuntimeError(
                f"Detector cannot run because required packages are missing: {', '.join(self._missing_deps)}. "
                "Install them in a Python 3.12 virtualenv (MediaPipe may not support 3.13 yet): "
                "https://google.github.io/mediapipe/getting_started/python.html"
            )

        frame.flags.writeable = False
        results = self.pose.process(frame)
        frame.flags.writeable = True

        calibration_mode = self.ctx.gui.calibration_mode
        show_cam_capture = self.ctx.gui.show_cam_capture
        show_pose_estimation = self.ctx.gui.show_pose_estimation

        if results.pose_landmarks:
            if not calibration_mode:
                return results.pose_landmarks, frame

            if not show_cam_capture:
                frame[:] = 0  # Set black background
            if show_pose_estimation:
                mp_drawing = mp.solutions.drawing_utils
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            return results.pose_landmarks, frame
        else:
            if not show_cam_capture:
                frame[:] = 0
            return None, frame
    
    def close(self):
        """
        Release MediaPipe resources
        """
        if hasattr(self, 'pose') and self.pose:
            self.pose.close()



