"""
Group: Keyboard Liberators
This program builds a graphical user interface for visualizing pose detection and user calibration.
When receiving function calls from the main loop, the GUI instance renders corresponding graphics to the screen.
"""

from context import Context
from time import time as tm
import pygame
import cv2
import sys
import ctypes


class GUI:
    """
    Graphical user interface built using Pygame.
    """
    def __init__(self, ctx: Context, reso: tuple, fps: float):
        self.ctx: Context = ctx
        ctx.gui = self
        self.reso: tuple = reso
        self.fps: float = fps

        pygame.init()
        self.caption = ctx.cfg.get("window", "caption")
        pygame.display.set_caption(self.caption)
        self.win_resolution = self.reso
        self.screen = pygame.display.set_mode(self.win_resolution)
        self.clock = pygame.time.Clock()
        
        # 设置窗口透明（仅Windows）
        self._set_window_transparency()

        self.show_caption_fps = ctx.cfg.getboolean('window', "show_caption_fps")
        self.delta_time: float = 0.0
        self.running_time: float = 0.0
        self._running_start_time: float = tm()
        self._fps_accum_target: int = ctx.cfg.getint('window', "smooth_fps_accum_frames")
        self._fps_accum_time: int = 0
        self._fps_accum_count: int = 0
        self._smoothed_fps: int = 0

    def _set_window_transparency(self):
        """
        Set window transparency on Windows platform.
        """
        if sys.platform == 'win32':
            try:
                # 获取窗口句柄
                hwnd = pygame.display.get_wm_info()['window']
                
                # Windows API 常量
                GWL_EXSTYLE = -20
                WS_EX_LAYERED = 0x80000
                LWA_ALPHA = 0x2
                LWA_COLORKEY = 0x1
                
                # 设置窗口为分层窗口
                _winlib = ctypes.windll.user32
                _winlib.SetWindowLongA(hwnd, GWL_EXSTYLE, 
                                      _winlib.GetWindowLongA(hwnd, GWL_EXSTYLE) | WS_EX_LAYERED)
                
                # 方法1: 整体透明度 + 色键透明组合
                # 先设置黑色为完全透明
                colorkey = 0x000000  # 黑色 RGB(0,0,0)
                # 然后设置整体窗口透明度，让组件也半透明
                _winlib.SetLayeredWindowAttributes(hwnd, colorkey, 200, LWA_COLORKEY | LWA_ALPHA)
                # 200是整体透明度 (0-255)，可以看到窗口后面的内容
                
                print("窗口半透明已启用 (可以透视窗口)")
            except Exception as e:
                print(f"设置窗口透明失败: {e}")

    def clock_tick(self):
        """
        Update the clock and return the elapsed time in seconds.
        """
        self.running_time = tm() - self._running_start_time
        self.delta_time = self.clock.tick(self.fps) / 1000.0
        if self.show_caption_fps:
            self.__calc_smooth_fps()
            caption = f"{self.caption}  FPS: {self._smoothed_fps}"
            pygame.display.set_caption(caption)
        return self.delta_time

    def __calc_smooth_fps(self):
        """
        Calculate the smoothed FPS based on the accumulated FPS values.
        """
        self._fps_accum_count += 1
        self._fps_accum_time += self.delta_time
        if self._fps_accum_count >= self._fps_accum_target:
            self._smoothed_fps = round(self._fps_accum_count / self._fps_accum_time)
            pygame.display.set_caption(f"{self.caption}  FPS: {self._smoothed_fps}")
            self._fps_accum_count = 0
            self._fps_accum_time = 0.0

    def clear_color(self):
        """
        Clear the screen with black (transparent when colorkey is enabled).
        """
        self.screen.fill((0, 0, 0))  # 黑色背景将完全透明

    @staticmethod
    def update_display():
        """
        Update the display with the rendered graphics.
        """
        pygame.display.flip()

    def render_webcam_capture(self, np_frame):
        """
        Visualize the webcam capture to the screen.
        """
        frame = cv2.cvtColor(np_frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.rotate(frame, -90)
        self.screen.blit(frame, (0, 0))

    def render_pose_landmarks(self, landmarks):
        """
        Visualize the pose landmarks (links) to the screen.
        TODO: Given Mediapipe upper body pose landmarks, visualize the pose landmarks (links) to the screen.
        """

    def render_pose_features(self, features):
        """
        Visualize the pose features to the screen.
        TODO: Given PoseFeature instance, visualize the data on the screen
        """

    def render_game_controls(self, brake_pressure=0.0, throttle_pressure=0.0, 
                            handbrake_active=False):
        """
        Render game-style control UI elements in the bottom-right corner.
        Args:
            brake_pressure: 0.0-1.0, brake pedal pressure
            throttle_pressure: 0.0-1.0, throttle pedal pressure
            handbrake_active: bool, handbrake status
        """
        # 基础位置（右下角）
        base_x = self.win_resolution[0] - 250
        base_y = self.win_resolution[1] - 200
        
        # 1. 绘制左踏板（刹车）
        self._draw_pedal(base_x - 80, base_y, brake_pressure, (255, 100, 100), "Brake")
        
        # 2. 绘制右踏板（油门）
        self._draw_pedal(base_x + 20, base_y, throttle_pressure, (100, 255, 100), "Throttle")
        
        # 3. 绘制手刹指示器（中间的横条）
        handbrake_y = base_y + 120
        self._draw_handbrake(base_x - 30, handbrake_y, handbrake_active)
        
        # 4. 绘制按钮组（Y, X, B, A）
        button_x = base_x + 120
        button_y = base_y + 40
        self._draw_button_cluster(button_x, button_y)
    
    def _draw_pedal(self, x, y, pressure, color, label):
        """
        Draw a pedal with fill based on pressure (white with transparency).
        """
        pedal_width = 60
        pedal_height = 100
        
        # 创建半透明 Surface
        pedal_surface = pygame.Surface((pedal_width, pedal_height), pygame.SRCALPHA)
        
        # 背景（未按下部分 - 白色半透明）
        bg_rect = pygame.Rect(0, 0, pedal_width, pedal_height)
        pygame.draw.rect(pedal_surface, (255, 255, 255, 80), bg_rect, border_radius=10)  # 白色，透明度80
        
        # 填充（按下部分，从下往上填充 - 白色更不透明）
        fill_height = int(pedal_height * pressure)
        if fill_height > 0:
            fill_rect = pygame.Rect(0, pedal_height - fill_height, 
                                    pedal_width, fill_height)
            pygame.draw.rect(pedal_surface, (255, 255, 255, 200), fill_rect, border_radius=10)  # 白色，透明度200
        
        # 边框（白色）
        pygame.draw.rect(pedal_surface, (255, 255, 255, 255), bg_rect, 3, border_radius=10)
        
        # 贴到主屏幕
        self.screen.blit(pedal_surface, (x, y))
        
        # 标签（白色）
        font = pygame.font.Font(None, 20)
        text = font.render(label, True, (255, 255, 255))
        text_rect = text.get_rect(centerx=x + pedal_width // 2, y=y + pedal_height + 10)
        self.screen.blit(text, text_rect)
    
    def _draw_handbrake(self, x, y, active):
        """
        Draw handbrake indicator (horizontal bar - white with transparency).
        """
        bar_width = 120
        bar_height = 30
        
        # 创建半透明 Surface
        bar_surface = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
        
        # 根据激活状态设置透明度
        alpha = 220 if active else 100
        bar_rect = pygame.Rect(0, 0, bar_width, bar_height)
        pygame.draw.rect(bar_surface, (255, 255, 255, alpha), bar_rect, border_radius=15)
        
        # 边框
        pygame.draw.rect(bar_surface, (255, 255, 255, 255), bar_rect, 2, border_radius=15)
        
        # 贴到主屏幕
        self.screen.blit(bar_surface, (x, y))
        
        # 图标/文字（白色）
        font = pygame.font.Font(None, 24)
        text = font.render("HANDBRAKE" if active else "---", True, (255, 255, 255))
        text_rect = text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        self.screen.blit(text, text_rect)
    
    def _draw_button_cluster(self, x, y):
        """
        Draw Xbox-style button cluster (white with transparency).
        """
        button_radius = 20
        button_spacing = 50
        
        buttons = [
            {'pos': (x, y - button_spacing), 'label': 'Y'},  # 上
            {'pos': (x - button_spacing, y), 'label': 'X'},  # 左
            {'pos': (x + button_spacing, y), 'label': 'B'},  # 右
            {'pos': (x, y + button_spacing), 'label': 'A'},  # 下
        ]
        
        for btn in buttons:
            # 创建半透明按钮 Surface
            btn_size = (button_radius * 2 + 6) * 2
            btn_surface = pygame.Surface((btn_size, btn_size), pygame.SRCALPHA)
            center = (btn_size // 2, btn_size // 2)
            
            # 外圈（白色半透明）
            pygame.draw.circle(btn_surface, (255, 255, 255, 100), center, button_radius + 3)
            # 按钮主体（白色更不透明）
            pygame.draw.circle(btn_surface, (255, 255, 255, 180), center, button_radius)
            # 边框
            pygame.draw.circle(btn_surface, (255, 255, 255, 255), center, button_radius, 2)
            
            # 字母（白色）
            font = pygame.font.Font(None, 28)
            text = font.render(btn['label'], True, (255, 255, 255))
            text_rect = text.get_rect(center=center)
            btn_surface.blit(text, text_rect)
            
            # 贴到主屏幕
            surface_pos = (btn['pos'][0] - btn_size // 2, btn['pos'][1] - btn_size // 2)
            self.screen.blit(btn_surface, surface_pos)

    @staticmethod
    def handle_events() -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    @staticmethod
    def quit():
        """
        Close the pygame window and release resources
        """
        pygame.quit()
