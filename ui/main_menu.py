import pygame

def gradient_text(text, font, color_top, color_bottom):
    text_surf = font.render(text, True, (255,255,255))
    w, h = text_surf.get_size()
    text_surf = text_surf.convert_alpha()  

    grad_surf = pygame.Surface((w, h), pygame.SRCALPHA)

    for y in range(h):
        ratio = y / (h - 1) if h > 1 else 0

        r = color_top[0] + (color_bottom[0] - color_top[0]) * ratio
        g = color_top[1] + (color_bottom[1] - color_top[1]) * ratio
        b = color_top[2] + (color_bottom[2] - color_top[2]) * ratio
        a = 255  
        pygame.draw.line(grad_surf, (r,g,b,a), (0,y), (w,y))

    text_surf.blit(grad_surf, (0,0), special_flags=pygame.BLEND_RGBA_MULT)

    return text_surf


def main_menu(screen, background_path):
    bg_image = pygame.image.load(background_path)
    bg_image = pygame.transform.scale(bg_image, (screen.get_width(), screen.get_height()))

    clock = pygame.time.Clock()

    custom_font_path = "./ui/font/short.ttf"
    font_title = pygame.font.Font(custom_font_path, 60)
    font_msg   = pygame.font.Font(custom_font_path, 30)
    font_btn   = pygame.font.Font(custom_font_path, 40)

    title_surface = gradient_text("CHESS GAME", font_title, (0, 0, 0), (255, 128, 0))
    msg_surface   = gradient_text("develop by HCMUT student group", font_msg, (0, 0, 0), (204, 0, 102))

    play_surface  = font_btn.render("PLAY", True, (255,255,255))
    exit_surface  = font_btn.render("EXIT", True, (255,255,255))

    while True:
        screen.blit(bg_image, (0,0))

        title_w, title_h = title_surface.get_size()
        msg_w,   msg_h   = msg_surface.get_size()
        play_w,  play_h  = play_surface.get_size()
        exit_w,  exit_h  = exit_surface.get_size()

       
        padding_top    = 30
        padding_between= 20
        padding_bottom = 30
        line_gap       = 10

        btn_gap = 40
        total_btn_width = (play_w + 40) + (exit_w + 40) + btn_gap  
        content_width = max(title_w, msg_w, total_btn_width)
        
        
        box_height = (
            padding_top +
            title_h + line_gap +
            msg_h + line_gap +
            (max(play_h, exit_h) + 20) +  
            padding_bottom
        )

        box_width = content_width + 80  

        box_x = screen.get_width() // 2 - box_width // 2
        box_y = screen.get_height() // 2 - box_height // 2

        box_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        box_surf.fill((200, 200, 200, 180))  

        current_y = padding_top

        title_x = (box_width - title_w) // 2
        box_surf.blit(title_surface, (title_x, current_y))
        current_y += title_h + line_gap

        msg_x = (box_width - msg_w) // 2
        box_surf.blit(msg_surface, (msg_x, current_y))
        current_y += msg_h + line_gap

        play_rect_w = play_w + 40
        play_rect_h = play_h + 20
        exit_rect_w = exit_w + 40
        exit_rect_h = exit_h + 20
        
        total_btn_w = play_rect_w + exit_rect_w + btn_gap
        btn_start_x = (box_width - total_btn_w)//2
        btn_y = current_y

        play_rect = pygame.Rect(btn_start_x, btn_y, play_rect_w, play_rect_h)
        pygame.draw.rect(box_surf, (80,80,80), play_rect, border_radius=8)
        px = play_rect.x + (play_rect_w - play_w)//2
        py = play_rect.y + (play_rect_h - play_h)//2
        box_surf.blit(play_surface, (px, py))

        exit_rect = pygame.Rect(play_rect.right + btn_gap, btn_y, exit_rect_w, exit_rect_h)
        pygame.draw.rect(box_surf, (80,80,80), exit_rect, border_radius=8)
        ex = exit_rect.x + (exit_rect_w - exit_w)//2
        ey = exit_rect.y + (exit_rect_h - exit_h)//2
        box_surf.blit(exit_surface, (ex, ey))

        current_y += max(play_rect_h, exit_rect_h) + padding_bottom

        screen.blit(box_surf, (box_x, box_y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                local_x = mx - box_x
                local_y = my - box_y

                if play_rect.collidepoint(local_x, local_y):
                    return True
                elif exit_rect.collidepoint(local_x, local_y):
                    return False

        clock.tick(30)