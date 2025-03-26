import pygame

notification_text = None
notification_expires = 0
font_path = "./ui/font/short.ttf"
def show_notification(text, duration=2000):
    
    global notification_text, notification_expires
    notification_text = text
    notification_expires = pygame.time.get_ticks() + duration


def draw_notification(screen):
    global notification_text, notification_expires
    if not notification_text:
        return  

    current_time = pygame.time.get_ticks()
    if current_time > notification_expires:
        notification_text = None
        return

    font = pygame.font.SysFont(None, 30)

    text_surface = font.render(notification_text, True, (255, 255, 255))
    box_w = text_surface.get_width() + 20
    box_h = text_surface.get_height() + 10

    margin = 10
    box_x = screen.get_width() - box_w - margin
    box_y = margin

    box_rect = pygame.Rect(box_x, box_y, box_w, box_h)
    pygame.draw.rect(screen, (30, 30, 30), box_rect, border_radius=10)

    text_x = box_x + 10
    text_y = box_y + 5
    screen.blit(text_surface, (text_x, text_y))


# when end
def popup_checkmate(screen, message):
    
    # screen layer 
    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.set_alpha(180)  
    overlay.fill((0, 0, 0))  
    screen.blit(overlay, (0, 0))

    font_title = pygame.font.Font(font_path, 46)
    font_msg = pygame.font.Font(font_path, 32)
    font_btn = pygame.font.Font(font_path, 28)

    title_surface = font_title.render("CHECKMATE!", True, (255, 255, 0))
    msg_surface = font_msg.render(message, True, (255, 255, 255))

    replay_surface = font_btn.render("REPLAY", True, (255, 255, 255))
    exit_surface   = font_btn.render("EXIT", True, (255, 255, 255))

    title_w, title_h = title_surface.get_size()
    msg_w,   msg_h   = msg_surface.get_size()
    replay_w, replay_h = replay_surface.get_size()
    exit_w,   exit_h   = exit_surface.get_size()

    padding = 30
    content_width = max(title_w, msg_w, (replay_w + exit_w + 60))
    box_width = content_width + padding*2

    box_height = title_h + msg_h + replay_h + padding*4

    box_x = screen.get_width() // 2 - box_width // 2
    box_y = screen.get_height() // 2 - box_height // 2

    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
    pygame.draw.rect(screen, (50, 50, 50), box_rect, border_radius=15)

    tx = box_x + (box_width - title_w) // 2
    ty = box_y + padding
    screen.blit(title_surface, (tx, ty))

    mx = box_x + (box_width - msg_w) // 2
    my = ty + title_h + 10
    screen.blit(msg_surface, (mx, my))

    # replay? exit?
    btn_space = 20  
    btn_y = my + msg_h + padding

    replay_rect = pygame.Rect(0, 0, replay_w + 20, replay_h + 10)
    exit_rect   = pygame.Rect(0, 0, exit_w + 20,   exit_h + 10)

    total_btn_width = replay_rect.width + exit_rect.width + btn_space
    start_x = box_x + (box_width - total_btn_width)//2  

    # draw replay
    replay_rect.x = start_x
    replay_rect.y = btn_y
    pygame.draw.rect(screen, (80,80,80), replay_rect, border_radius=5)
    screen.blit(replay_surface, (replay_rect.x+10, replay_rect.y+5))

    # draw exit
    exit_rect.x = replay_rect.right + btn_space
    exit_rect.y = btn_y
    pygame.draw.rect(screen, (80,80,80), exit_rect, border_radius=5)
    screen.blit(exit_surface, (exit_rect.x+10, exit_rect.y+5))

    # update
    pygame.display.flip()

    # choose one choice
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if replay_rect.collidepoint(mouse_x, mouse_y):
                    return True   
                elif exit_rect.collidepoint(mouse_x, mouse_y):
                    return False  

# choose first step.
def choose_first_player(screen):
    
    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.set_alpha(180)  
    overlay.fill((189, 183, 107))  
    screen.blit(overlay, (0, 0))

    font_title = pygame.font.Font(font_path, 46)
    font_btn = pygame.font.Font(font_path, 32)

    title_surface = font_title.render("Choosing sides ", True, (255, 255, 0))
    white_surface = font_btn.render("White", True, (255,255,255))
    black_surface = font_btn.render("Black", True, (255,255,255))

    title_w, title_h = title_surface.get_size()
    white_w, white_h = white_surface.get_size()
    black_w, black_h = black_surface.get_size()

    padding = 30
    box_width = max(title_w, white_w+black_w+40) + padding*2
    box_height = title_h + white_h + padding*4

    box_x = screen.get_width()//2 - box_width//2
    box_y = screen.get_height()//2 - box_height//2
    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
    pygame.draw.rect(screen, (50,50,50), box_rect, border_radius=15)

    # title
    tx = box_x + (box_width - title_w)//2
    ty = box_y + padding
    screen.blit(title_surface, (tx, ty))

    # create 2 button
    btn_space = 20
    btn_y = ty + title_h + padding

    white_rect = pygame.Rect(0,0, white_w+20, white_h+10)
    black_rect = pygame.Rect(0,0, black_w+20, black_h+10)

    total_btn_width = white_rect.width + black_rect.width + btn_space
    start_x = box_x + (box_width - total_btn_width)//2

    # white button
    white_rect.x = start_x
    white_rect.y = btn_y
    pygame.draw.rect(screen, (80,80,80), white_rect, border_radius=5)
    screen.blit(white_surface, (white_rect.x+10, white_rect.y+5))

    # Black Button
    black_rect.x = white_rect.right + btn_space
    black_rect.y = btn_y
    pygame.draw.rect(screen, (80,80,80), black_rect, border_radius=5)
    screen.blit(black_surface, (black_rect.x+10, black_rect.y+5))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'white'  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = event.pos
                if white_rect.collidepoint(mx,my):
                    return 'white'
                elif black_rect.collidepoint(mx,my):
                    return 'black'
