"""
使用 break.png 图标绘制刹车踏板
"""
import pygame
import os

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Break 图标显示")
clock = pygame.time.Clock()

# 加载刹车图标
# 由于文件在 Test_Scripts 文件夹，需要访问父目录的 UI_Icons
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
icon_path = os.path.join(parent_dir, "UI_Icons", "break.png")

if os.path.exists(icon_path):
    brake_icon = pygame.image.load(icon_path)
    print(f"成功加载图标: {icon_path}")
    print(f"图标尺寸: {brake_icon.get_size()}")
    
    # 如果图标太大，缩放它
    icon_width, icon_height = brake_icon.get_size()
    if icon_width > 200 or icon_height > 200:
        scale_factor = min(200/icon_width, 200/icon_height)
        new_size = (int(icon_width * scale_factor), int(icon_height * scale_factor))
        brake_icon = pygame.transform.scale(brake_icon, new_size)
        print(f"缩放后尺寸: {new_size}")
else:
    print(f"错误: 找不到文件 {icon_path}")
    brake_icon = None

# 主循环
running = True
pressure = 0.0

print("\n操作说明：")
print("  S键: 踩刹车")
print("  ESC: 退出")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # 键盘控制
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        pressure = min(1.0, pressure + 0.02)
    else:
        pressure = max(0.0, pressure - 0.03)
    
    # 清屏
    screen.fill((0, 0, 0))
    
    # 显示图标
    if brake_icon:
        # 原始图标（左侧）
        icon_rect = brake_icon.get_rect(center=(150, 200))
        screen.blit(brake_icon, icon_rect)
        
        # 带填充效果的图标（右侧）
        icon_width, icon_height = brake_icon.get_size()
        
        # 创建结果表面
        result_surface = pygame.Surface((icon_width, icon_height), pygame.SRCALPHA)
        
        # 1. 绘制半透明的完整图标作为背景（未填充部分）
        dimmed_icon = brake_icon.copy()
        dimmed_icon.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)
        result_surface.blit(dimmed_icon, (0, 0))
        
        # 2. 绘制填充部分（从下往上，几乎不透明）
        fill_height = int(icon_height * pressure)
        
        if fill_height > 0:
            # 创建一个临时表面用于填充部分
            fill_surface = pygame.Surface((icon_width, fill_height), pygame.SRCALPHA)
            
            # 复制图标的底部部分
            fill_surface.blit(brake_icon, (0, -(icon_height - fill_height)))
            
            # 设置为更透明（降低透明度）
            fill_surface.fill((255, 255, 255, 180), special_flags=pygame.BLEND_RGBA_MULT)
            
            # 绘制填充部分到结果表面
            result_surface.blit(fill_surface, (0, icon_height - fill_height))
        
        # 绘制到屏幕
        icon_rect2 = result_surface.get_rect(center=(450, 200))
        screen.blit(result_surface, icon_rect2)
        
        # 标签
        font = pygame.font.Font(None, 24)
        
        label1 = font.render("Original Icon (break.png)", True, (255, 255, 255))
        screen.blit(label1, (50, 320))
        
        label2 = font.render(f"Fill Progress: {int(pressure*100)}%", True, (255, 255, 255))
        screen.blit(label2, (340, 320))
    else:
        # 显示错误信息
        font = pygame.font.Font(None, 36)
        error_text = font.render("Icon not found!", True, (255, 100, 100))
        screen.blit(error_text, (200, 180))
        
        # 显示期望的路径
        small_font = pygame.font.Font(None, 20)
        path_text = small_font.render(f"Looking for: {icon_path}", True, (200, 200, 200))
        screen.blit(path_text, (100, 220))
    
    # 提示
    hint_font = pygame.font.Font(None, 20)
    hint = hint_font.render("Press S to brake | ESC to exit", True, (150, 150, 150))
    screen.blit(hint, (180, 360))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("程序结束")
