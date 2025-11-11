"""
Group: Keyboard Liberators
This program processes the pose data and maps it to control signals and send them to the virtual controller.
"""

import math
from typing import List
from context import Context
from presets import Preset
from utils import *


class ControlFeature:
    """
    Containing process landmark features and game control parameters.
    """
    def __init__(self, ctx: Context):
        self.ctx = ctx

        # Visualizing parameters
        self.hand_left_center: List = [0.0, 0.0]  # [0,1] uniformed hands center in pygame coordinate
        self.hand_right_center: List = [0.0, 0.0]  # [0,1] uniformed hands center in pygame coordinate
        self.hands_center: List = [0.0, 0.0]  # [0,1] uniformed hands center in pygame coordinate
        self.left_pressure: float = 0.0  # [0,1] left joystick input strength (left)
        self.right_pressure: float = 0.0  # [0,1] left joystick input strength (right)
        self.steer_angle: float = 0.0  # [-180,180] estimated steering angle in degrees

        self.brake_pressure: float = 0.0  # [0,1] brake trigger strength
        self.throttle_pressure: float = 0.0  # [0,1] throttle trigger strength
        self.handbrake_active: bool = False  # whether handbrake is active

        # Control parameters
        # Steering sensitivity
        self.steering_safe_angle = ctx.tkparam.scalar("steering safe angle", 7.0, 0.0, 30.0)
        self.steering_left_border_angle = ctx.tkparam.scalar("steering left border", 45.0, 0.0, 80.0)
        self.steering_right_border_angle = ctx.tkparam.scalar("steering right border", 45.0, 0.0, 80.0)


class PoseControlMapper:
    """
    Mapping pose data to control signals.
    """

    # Indices of landmarks of body parts
    head_indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    left_hand_indices = [15, 17, 19, 21]
    right_hand_indices = [16, 18, 20, 22]
    hand_indices = [15, 16, 17, 18, 19, 20, 21, 22]
    body_left_indices = [11, 23]
    body_right_indices = [12, 24]
    body_up_indices = [11, 12]
    body_indices = [11, 12, 23, 24]

    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        ctx.mapper = self
        self.features = ControlFeature(ctx)

        # previous button states, trigger press/release only on state changes
        self._prev_menu_pressed = False
        self._prev_y_pressed = False

        ctx.preset_mgr.register_preset_update_callback(self.__on_update_preset)

    def __on_update_preset(self, preset: Preset) -> None:
        self.ctx.tkparam.load_param_from_dict(preset.mapping)

    def extract_features(self, landmarks) -> ControlFeature:
        """
        Update extracted features from the given landmarks, and store them in the PoseFeature instance
        """

        f = self.features
        if landmarks is None:
            return f

        # Get center of hands
        left_points = [L(landmarks, i) for i in self.left_hand_indices]
        right_points = [L(landmarks, i) for i in self.right_hand_indices]

        lcx, lcy, lcz = avg(left_points)
        rcx, rcy, rcz = avg(right_points)
        f.hand_left_center = [1-lcx, lcy]
        f.hand_right_center = [1-rcx, rcy]
        f.hands_center = [1-(lcx+rcx)/2.0, (lcy+rcy)/2.0]

        # Horizontal - 0 degree; Steer right to 90 degree; Steer left to -90
        f.steer_angle = math.degrees(math.atan2(rcx-lcx, rcy-lcy))+90.0
        safe_angle = f.steering_safe_angle.get()
        f.left_pressure = clamp01((-f.steer_angle-safe_angle) / f.steering_left_border_angle.get())\
            if f.steer_angle < 0 else 0.0
        f.right_pressure = clamp01((f.steer_angle-safe_angle) / f.steering_right_border_angle.get()) \
            if f.steer_angle > 0 else 0.0

        return f

        # 躯干俯仰角估算：使用双肩与双臀（或髋）中点，估计前倾/后仰角度
        # shoulder_pts = [L(i) for i in self.body_up_indices]
        # hip_pts = [L(i) for i in [23, 24]]
        # sx, sy, sz = avg(shoulder_pts)
        # hx, hy, hz = avg(hip_pts)
        #
        # # vector from hips to shoulders
        # vx = sx - hx
        # vy = sy - hy
        # vz = sz - hz
        #
        # # pitch: positive when shoulders are closer (leaning forward)
        # # use atan2(-vz, vy) so that more negative vz (shoulders closer) => positive pitch
        # f.torso_pitch = math.atan2(-vz, vy) if (vy != 0 or vz != 0) else 0.0
        #
        # # 握拳检测：通过指尖与手腕的二维距离判断是否握拳（距离较小表示握拳）
        # # 指尖索引（近似）：左手19,21；右手20,22
        # def dist(a, b):
        #     return math.hypot(a[0] - b[0], a[1] - b[1])
        #
        # # left wrist is index 15, right wrist 16
        # lw = L(15)
        # rw = L(16)
        # left_tips = [L(19), L(21)]
        # right_tips = [L(20), L(22)]
        # left_avg_tip = ((left_tips[0][0] + left_tips[1][0]) / 2.0, (left_tips[0][1] + left_tips[1][1]) / 2.0)
        # right_avg_tip = ((right_tips[0][0] + right_tips[1][0]) / 2.0, (right_tips[0][1] + right_tips[1][1]) / 2.0)
        #
        # left_wrist_xy = (lw[0], lw[1])
        # right_wrist_xy = (rw[0], rw[1])
        #
        # left_tip_dist = dist(left_avg_tip, left_wrist_xy)
        # right_tip_dist = dist(right_avg_tip, right_wrist_xy)
        #
        # # 使用配置的阈值判断是否握拳
        # fist_thresh = self.ctx.active_preset.mapping["fist_thresh"]
        # f.left_fist = left_tip_dist < fist_thresh
        # f.right_fist = right_tip_dist < fist_thresh
        #
        # # 双手向后摆检测：比较手的z值与躯干中点z，若都显著更大则视为向后摆
        # behind_thresh = self.ctx.active_preset.mapping["behind_thresh"]
        # body_mid_z = (sz + hz) / 2.0
        # if (lcz - body_mid_z) > behind_thresh and (rcz - body_mid_z) > behind_thresh:
        #     f.hands_behind = True
        # else:
        #     f.hands_behind = False
        #
        # return f

    def trigger_control(self):
        """
        Trigger corresponding game control to the virtual controller based on the extracted features.
        """

        gp = self.ctx.gamepad
        f = self.features

        # steering control
        gp.left_joystick(f.right_pressure - f.left_pressure, 0.0)

