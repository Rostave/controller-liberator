# """
# Group: Keyboard Liberators
# This program processes the pose data and maps it to control signals and send them to the virtual controller.
# """
#
# from typing import List
# from context import Context
# import math
# from presets import PresetManager
#
#
# class PoseFeature:
#     """
#     Static pose feature class
#     """
#     # 姿态特征数据结构：存储提取到的手部中心、躯干角度、握拳与双手在后方等标志
#     # Features
#     hand_left_center: List = [0.0, 0.0]
#     hand_right_center: List = [0.0, 0.0]
#     hands_center: List = [0.0, 0.0]
#
#     # Trigger detection parameters
#     steering_thresh_y = 0.1
#
#
# class PoseControlMapper:
#
#     # Indices of landmarks of body parts
#     head_indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#     left_hand_indices = [15, 17, 19, 21]
#     right_hand_indices = [16, 18, 20, 22]
#     hand_indices = [15, 16, 17, 18, 19, 20, 21, 22]
#     body_left_indices = [11, 23]
#     body_right_indices = [12, 24]
#     body_up_indices = [11, 12]
#     body_indices = [11, 12, 23, 24]
#
#     def __init__(self, ctx: Context):
#         self.ctx: Context = ctx
#         ctx.mapper = self
#         self.features = PoseFeature()
#         # previous button states so we press/release only on state changes
#         self._prev_menu_pressed = False
#         self._prev_y_pressed = False
#         # 加载灵敏度配置和阈值（来自配置文件的 [mapping] 节），用于调节检测与映射灵敏度
#         # 如果配置文件没有对应项，则使用代码中的默认值
#         cfg = getattr(ctx, 'cfg', None)
#         if cfg is not None and cfg.has_section('mapping'):
#             self.max_pitch = cfg.getfloat('mapping', 'max_pitch', fallback=0.4)
#             self.fist_thresh = cfg.getfloat('mapping', 'fist_thresh', fallback=0.06)
#             self.behind_thresh = cfg.getfloat('mapping', 'behind_thresh', fallback=0.08)
#             self.joystick_deadzone = cfg.getfloat('mapping', 'joystick_deadzone', fallback=0.02)
#             self.steering_scale = cfg.getfloat('mapping', 'steering_scale', fallback=1.0)
#         else:
#             # sensible defaults when no config provided
#             self.max_pitch = 0.4
#             self.fist_thresh = 0.06
#             self.behind_thresh = 0.08
#             self.joystick_deadzone = 0.02
#             self.steering_scale = 1.0
#
#         # 预设管理器占位：用于将来注册/切换按键操作预设
#         # PresetManager 目前是空的占位实现，方便后续扩展
#         try:
#             self.preset_manager = PresetManager(ctx)
#         except Exception:
#             # 如果导入或初始化失败，仍保持程序可运行
#             self.preset_manager = None
#
#     def extract_features(self, landmarks) -> PoseFeature:
#         # 提取特征：计算手部中心、躯干俯仰角、握拳状态以及双手向后摆等标志
#         # 输入：MediaPipe返回的landmarks（归一化坐标），输出：更新的PoseFeature实例
#         """
#         Update extracted features from the given landmarks, and store them in the PoseFeature instance
#         TODO: Input is the landmark features detected by MediaPipe, implement feature extraction, update the fields in the PoseFeature instance, return the PoseFeature instance
#         """
#
#         # Reset features to defaults first
#         # 重置特征到默认值（避免上一次帧的数据遗留）
#         f = self.features
#         f.hand_left_center = [0.0, 0.0]
#         f.hand_right_center = [0.0, 0.0]
#         f.hands_center = [0.0, 0.0]
#
#         # default dynamic features
#         f.torso_pitch = 0.0  # positive = leaning forward, negative = leaning backward
#         f.left_fist = False
#         f.right_fist = False
#         f.hands_behind = False
#
#         if landmarks is None:
#             # 如果未检测到landmarks，直接返回默认特征
#             return f
#
#         # 辅助函数：获取指定landmark的归一化坐标(x, y, z)
#         def L(i):
#             lm = landmarks.landmark[i]
#             return lm.x, lm.y, lm.z
#
#     # 计算左右手中心：对指定的手部关节点取平均，作为手部中心坐标
#         left_points = [L(i) for i in self.left_hand_indices]
#         right_points = [L(i) for i in self.right_hand_indices]
#
#         def avg(points):
#             n = len(points)
#             sx = sum(p[0] for p in points)
#             sy = sum(p[1] for p in points)
#             sz = sum(p[2] for p in points)
#             return sx / n, sy / n, sz / n
#
#         lcx, lcy, lcz = avg(left_points)
#         rcx, rcy, rcz = avg(right_points)
#         f.hand_left_center = [lcx, lcy]
#         f.hand_right_center = [rcx, rcy]
#         f.hands_center = [(lcx + rcx) / 2.0, (lcy + rcy) / 2.0]
#
#     # 躯干俯仰角估算：使用双肩与双臀（或髋）中点，估计前倾/后仰角度
#         shoulder_pts = [L(i) for i in self.body_up_indices]
#         hip_pts = [L(i) for i in [23, 24]]
#         sx, sy, sz = avg(shoulder_pts)
#         hx, hy, hz = avg(hip_pts)
#
#         # vector from hips to shoulders
#         vx = sx - hx
#         vy = sy - hy
#         vz = sz - hz
#
#         # pitch: positive when shoulders are closer (leaning forward)
#         # use atan2(-vz, vy) so that more negative vz (shoulders closer) => positive pitch
#         f.torso_pitch = math.atan2(-vz, vy) if (vy != 0 or vz != 0) else 0.0
#
#         # 握拳检测：通过指尖与手腕的二维距离判断是否握拳（距离较小表示握拳）
#         # 指尖索引（近似）：左手19,21；右手20,22
#         def dist(a, b):
#             return math.hypot(a[0] - b[0], a[1] - b[1])
#
#         # left wrist is index 15, right wrist 16
#         lw = L(15)
#         rw = L(16)
#         left_tips = [L(19), L(21)]
#         right_tips = [L(20), L(22)]
#         left_avg_tip = ((left_tips[0][0] + left_tips[1][0]) / 2.0, (left_tips[0][1] + left_tips[1][1]) / 2.0)
#         right_avg_tip = ((right_tips[0][0] + right_tips[1][0]) / 2.0, (right_tips[0][1] + right_tips[1][1]) / 2.0)
#
#         left_wrist_xy = (lw[0], lw[1])
#         right_wrist_xy = (rw[0], rw[1])
#
#         left_tip_dist = dist(left_avg_tip, left_wrist_xy)
#         right_tip_dist = dist(right_avg_tip, right_wrist_xy)
#
#         # 使用配置的阈值判断是否握拳
#         f.left_fist = left_tip_dist < self.fist_thresh
#         f.right_fist = right_tip_dist < self.fist_thresh
#
#         # 双手向后摆检测：比较手的z值与躯干中点z，若都显著更大则视为向后摆
#         body_mid_z = (sz + hz) / 2.0
#         if (lcz - body_mid_z) > self.behind_thresh and (rcz - body_mid_z) > self.behind_thresh:
#             f.hands_behind = True
#         else:
#             f.hands_behind = False
#
#         return f
#
#     def trigger_control(self):
#         # 将提取到的特征映射为虚拟手柄输入：触发器、摇杆、按键等
#         """
#         Trigger corresponding game control to the virtual controller based on the extracted features.
#
#         Mappings implemented:
#         1) torso_pitch -> right_trigger (lean forward) and left_trigger (lean backward)
#         2) angle between hands -> left joystick X axis
#         3) fist (either hand) -> START button (menu)
#         4) both hands swung behind -> Y button
#         """
#
#         gp = getattr(self.ctx, 'gamepad', None)
#         if gp is None:
#             return
#
#         # 获取当前的PoseFeature实例
#         f = self.features
#
#     # --- 触发器映射：前倾映射到右触发，后仰映射到左触发（值在[0,1]之间） ---
#         pitch = f.torso_pitch
#         rt_value = 0.0
#         lt_value = 0.0
#         if pitch > 0:
#             rt_value = min(pitch / self.max_pitch, 1.0)
#             lt_value = 0.0
#         else:
#             lt_value = min((-pitch) / self.max_pitch, 1.0)
#             rt_value = 0.0
#
#         gp.right_trigger(float(rt_value))
#         gp.left_trigger(float(lt_value))
#
#     # --- 左摇杆X轴映射：根据双手相对连线的角度控制左右转向 ---
#     # 计算从左手到右手连线的角度，映射为[-1,1]区间
#         lx, ly = f.hand_left_center
#         rx, ry = f.hand_right_center
#         dx = rx - lx
#         dy = ry - ly
#         angle = math.atan2(dy, dx) if (dx != 0 or dy != 0) else 0.0
#         # map angle in [-pi/2,pi/2] to joystick [-1,1], apply steering scale
#         joy_x = max(-1.0, min(1.0, (angle / (math.pi / 2)) * self.steering_scale))
#         # 应用摇杆死区以避免抖动
#         if abs(joy_x) < self.joystick_deadzone:
#             joy_x = 0.0
#         gp.left_joystick(float(joy_x), 0.0)
#
#         # --- 按键映射：握拳触发 START（菜单键），双手向后摆触发 Y 键 ---
#         menu_pressed = (f.left_fist or f.right_fist)
#         y_pressed = f.hands_behind
#
#         # START (menu)
#         if menu_pressed and not self._prev_menu_pressed:
#             gp.press_button(gp.START)
#         if not menu_pressed and self._prev_menu_pressed:
#             gp.release_button(gp.START)
#         self._prev_menu_pressed = menu_pressed
#
#         # Y button
#         if y_pressed and not self._prev_y_pressed:
#             gp.press_button(gp.Y)
#         if not y_pressed and self._prev_y_pressed:
#             gp.release_button(gp.Y)
#         self._prev_y_pressed = y_pressed
#
