"""
使用 break_icon.png 图标绘制刹车踏板
"""
import pygame
import os

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("刹车图标显示")
clock = pygame.time.Clock()

# 加载刹车图标
icon_path = "UI_Icons/break_icon.png"
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
        
        # 带颜色填充效果的图标（右侧）
        icon_width, icon_height = brake_icon.get_size()
        
        # 创建结果表面
        result_surface = pygame.Surface((icon_width, icon_height), pygame.SRCALPHA)
        
        # 1. 绘制完整的原始图标（白色轮廓）
        result_surface.blit(brake_icon, (0, 0))
        
        # 2. 在图标内部填充颜色（从下往上）
        fill_height = int(icon_height * pressure)
        
        if fill_height > 0:
            # 创建填充颜色层（绿色/红色渐变）
            fill_color = (100, 255, 100) if pressure < 0.7 else (255, 100, 100)
            
            # 创建填充表面
            fill_surface = pygame.Surface((icon_width, fill_height), pygame.SRCALPHA)
            
            # 填充纯色
            fill_surface.fill((*fill_color, 180))
            
            # 复制图标的底部作为遮罩
            mask_surface = pygame.Surface((icon_width, fill_height), pygame.SRCALPHA)
            mask_surface.blit(brake_icon, (0, -(icon_height - fill_height)))
            
            # 使用图标形状作为遮罩，只在图标内部填充颜色
            # 获取遮罩的alpha通道
            import numpy as np
            try:
                mask_alpha = pygame.surfarray.pixels_alpha(mask_surface)
                fill_alpha = pygame.surfarray.pixels_alpha(fill_surface)
                
                # 只在图标有内容的地方应用填充颜色
                fill_alpha[:] = np.minimum(fill_alpha, mask_alpha)
                
                del mask_alpha
                del fill_alpha
            except:
                # 如果numpy方法失败，使用简单混合
                pass
            
            # 绘制填充到结果表面
            result_surface.blit(fill_surface, (0, icon_height - fill_height), special_flags=pygame.BLEND_RGBA_MIN)
        
        # 绘制到屏幕
        icon_rect2 = result_surface.get_rect(center=(450, 200))
        screen.blit(result_surface, icon_rect2)
        
        # 绘制填充进度指示线
        if pressure > 0:
            line_y = 200 + icon_height//2 - fill_height
            pygame.draw.line(screen, (255, 200, 0), 
                           (450 - icon_width//2 - 10, line_y),
                           (450 + icon_width//2 + 10, line_y), 2)
        
        # 标签
        font = pygame.font.Font(None, 24)
        
        label1 = font.render("Original Icon", True, (255, 255, 255))
        screen.blit(label1, (80, 320))
        
        color_name = "Green" if pressure < 0.7 else "Red"
        label2 = font.render(f"Fill: {int(pressure*100)}% ({color_name})", True, (255, 255, 255))
        screen.blit(label2, (340, 320))
    else:
        # 显示错误信息
        font = pygame.font.Font(None, 36)
        error_text = font.render("Icon not found!", True, (255, 100, 100))
        screen.blit(error_text, (200, 180))
    
    # 提示
    hint_font = pygame.font.Font(None, 20)
    hint = hint_font.render("Press S to brake | ESC to exit", True, (150, 150, 150))
    screen.blit(hint, (180, 360))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("程序结束")
