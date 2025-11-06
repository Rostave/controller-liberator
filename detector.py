"""
Group: Keyboard Liberators
This program applies MediaPipe to detect user pose and obtain landmarks.
When receiving invocation from the main loop, it will call the detector instance for pose landmarks.
"""

from context import Context


class Detector:
    """
    Detect user pose, obtaining landmarks
    """
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        ctx.detector = self
        # TODO: Initialize the MediaPipe detector instance

    def get_landmarks(self, frame):
        """
        Use the detector instance to detect user pose of upper body, obtain and return landmarks.
        TODO: Use the detector instance to detect user pose of upper body, obtain and return landmarks.
        """



