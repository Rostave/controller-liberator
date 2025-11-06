"""
Group: Keyboard Liberators
This program processes the pose data and maps it to control signals and send them to the virtual controller.
"""

from context import Context


class PoseFeature:
    """
    Static pose feature class
    """
    hand_left_center: float = 0.0
    hand_right_center: float = 0.0


class PoseControlMapper:
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        ctx.mapper = self

    def extract_features(self, landmarks):
        """
        Update extracted features from the given landmarks, and store them in the PoseFeature instance
        TODO: Input is the landmark features detected by MediaPipe, implement feature extraction, update the fields in the PoseFeature instance
        """

    def trigger_control(self, features: PoseFeature):
        """
        Trigger corresponding game control ti the virtual controller based on the extracted features
        TODO: Given the updated features in the PoseFeature instance, trigger the corresponding game control signal to the virtual controller ctx.gamepad
        """

