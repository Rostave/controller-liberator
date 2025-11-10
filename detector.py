"""
Group: Keyboard Liberators
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
from context import Context


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
            static_image_mode=False,  # False表示视频流模式，True表示静态图像模式
            model_complexity=cfg.getint("model_complexity"),
            smooth_landmarks=cfg.getboolean("smooth_landmarks"),
            enable_segmentation=False,  # 不启用分割（不需要分割功能）
            smooth_segmentation=True,
            min_detection_confidence=cfg.getfloat("min_detection_confidence"),
            min_tracking_confidence=cfg.getfloat("min_tracking_confidence")
        )
        
        # Visualization settings (updated by preset callbacks)
        self.visualize_landmarks: bool = True
        self.show_cam_capture: bool = False
        ctx.preset_mgr.register_preset_update_callback(self.__on_update_preset)
    
    def __on_update_preset(self, preset) -> None:
        """Apply the new preset visual settings"""
        self.visualize_landmarks = preset.visual["show_pose_estimation"]
        self.show_cam_capture = preset.visual["show_cam_capture"]

    def get_landmarks(self, frame):
        """
        Use the detector instance to detect user pose of upper body, obtain and return landmarks.
        使用检测器实例检测用户上半身姿态，获取并返回landmarks。
        
        Args:
            frame: RGB格式的图像帧（main.py已转换为RGB）
        
        Returns:
            tuple: (landmarks, visual_frame)
                - landmarks: MediaPipe检测到的姿态landmarks，如果未检测到则返回None
                - visual_frame: 可视化后的帧（绘制了关键点和连接线）
        """
        if getattr(self, 'disabled', False):
            raise RuntimeError(
                f"Detector cannot run because required packages are missing: {', '.join(self._missing_deps)}. "
                "Install them in a Python 3.12 virtualenv (MediaPipe may not support 3.13 yet): "
                "https://google.github.io/mediapipe/getting_started/python.html"
            )

        # MediaPipe处理（frame已经是RGB格式）
        frame.flags.writeable = False
        results = self.pose.process(frame)
        frame.flags.writeable = True
        
        # 根据配置决定是否可视化
        if results.pose_landmarks:
            if not self.show_cam_capture:
                frame[:] = 0  # 黑屏背景
            # 绘制姿态landmarks
            if self.visualize_landmarks:
                mp_drawing = mp.solutions.drawing_utils
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            return results.pose_landmarks, frame
        else:
            return None, frame
    
    def close(self):
        """
        释放MediaPipe资源
        Release MediaPipe resources
        """
        if hasattr(self, 'pose') and self.pose:
            self.pose.close()



