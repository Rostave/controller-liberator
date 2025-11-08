"""
Test GUI controls visualization
"""
import pygame
import cv2
import numpy as np
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

# 创建一个简单的 Context mock
class MockConfig:
    def get(self, section, key):
        defaults = {
            'caption': 'Game Controls Test',
            'smooth_fps_accum_frames': '10'
        }
        return defaults.get(key, 'default')
    
    def getboolean(self, section, key):
        return True
    
    def getint(self, section, key):
        return 10

class MockContext:
    def __init__(self):
        self.cfg = MockConfig()
        self.gui = None

# 导入 GUI 类
from context import Context
# 如果上面导入失败，使用 mock
try:
    ctx = Context()
except:
    ctx = MockContext()

# 导入 GUI
import importlib.util
spec = importlib.util.spec_from_file_location("gui", "gui_demo.py")
gui_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gui_module)

GUI = gui_module.GUI

# 初始化 GUI
gui = GUI(ctx, reso=(800, 600), fps=60)

# 创建一个虚拟的摄像头画面（纯色背景）
def create_dummy_frame(width=640, height=480):
    """创建一个渐变色的虚拟画面"""
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    # 创建渐变背景
    for i in range(height):
        frame[i, :] = [50 + i//3, 100 + i//4, 150 + i//5]
    return frame

# 模拟变量
brake = 0.0
throttle = 0.0
handbrake = False
time_counter = 0

print("GUI 半透明测试启动！")
print("操作说明：")
print("  W键: 油门加速")
print("  S键: 刹车减速")
print("  空格键: 切换手刹")
print("  ESC: 退出")
print("\n提示：窗口是半透明的，可以透过看到后面的桌面或应用！")

# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                handbrake = not handbrake
    
    # 键盘控制
    keys = pygame.key.get_pressed()
    
    # 油门控制（W键）
    if keys[pygame.K_w]:
        throttle = min(1.0, throttle + 0.02)
    else:
        throttle *= 0.95  # 自然衰减
    
    # 刹车控制（S键）
    if keys[pygame.K_s]:
        brake = min(1.0, brake + 0.02)
    else:
        brake *= 0.95  # 自然衰减
    
    # 清屏（黑色背景会完全透明）
    gui.clear_color()
    
    # 不渲染摄像头画面，保持背景透明
    # gui.render_webcam_capture(dummy_frame)  # 注释掉
    
    # 绘制游戏控制UI
    gui.render_game_controls(
        brake_pressure=brake,
        throttle_pressure=throttle,
        handbrake_active=handbrake
    )
    
    # 绘制提示文字（带半透明背景）
    font = pygame.font.Font(None, 24)
    hint_texts = [
        f"Throttle: {throttle:.2f} (W)",
        f"Brake: {brake:.2f} (S)",
        f"Handbrake: {'ON' if handbrake else 'OFF'} (SPACE)",
        "Press ESC to exit",
        "Window is semi-transparent!"
    ]
    
    for i, text in enumerate(hint_texts):
        # 创建半透明背景
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (10, 10 + i * 30)
        
        # 使用半透明Surface作为背景
        bg_surface = pygame.Surface((text_rect.width + 10, text_rect.height + 5), pygame.SRCALPHA)
        bg_surface.fill((255, 255, 255, 60))  # 白色半透明背景
        gui.screen.blit(bg_surface, (text_rect.x - 5, text_rect.y - 2))
        
        # 绘制文字
        gui.screen.blit(text_surface, text_rect)
    
    # 更新显示
    gui.update_display()
    gui.clock_tick()
    
    time_counter += 1

# 退出
gui.quit()
print("GUI 测试结束")
