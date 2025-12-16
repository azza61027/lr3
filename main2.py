import pygame
import random

pygame.init()

# Цвета
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
blue = (50, 153, 213)
grey = (200, 200, 200)
dark_grey = (150, 150, 150)

# Настройки по умолчанию
DEFAULT_WIDTH = 1000
DEFAULT_HEIGHT = 600
MIN_WIDTH = 600
MIN_HEIGHT = 400
MAX_WIDTH = 1600
MAX_HEIGHT = 900

# Текущие настройки
dis_width = DEFAULT_WIDTH
dis_height = DEFAULT_HEIGHT
snake_block = 10
snake_speed = 15

# Создаем окно с настройками по умолчанию
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

# Шрифты
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
menu_font = pygame.font.SysFont("bahnschrift", 40)
small_font = pygame.font.SysFont("bahnschrift", 20)

def Your_score(score):
    value = score_font.render("Счёт: " + str(score), True, black)
    dis.blit(value, [0, 0])

def snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 3 + y_offset))
    dis.blit(mesg, text_rect)

def draw_button(text, x, y, width, height, active_color, inactive_color, active=False):
    color = active_color if active else inactive_color
    pygame.draw.rect(dis, color, [x, y, width, height], border_radius=10)
    pygame.draw.rect(dis, black, [x, y, width, height], 2, border_radius=10)

    text_surf = font_style.render(text, True, black)
    text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))
    dis.blit(text_surf, text_rect)
    return pygame.Rect(x, y, width, height)


def draw_slider(x, y, width, height, value, min_val, max_val, label):
    # Фон слайдера
    pygame.draw.rect(dis, grey, [x, y, width, height], border_radius=5)

    # Текущее значение
    ratio = (value - min_val) / (max_val - min_val)
    slider_pos = x + (width * ratio)

    # Бегунок
    pygame.draw.circle(dis, red, (int(slider_pos), y + height // 2), height)

    # Текст
    label_text = small_font.render(f"{label}: {value}", True, dark_grey)
    dis.blit(label_text, (x, y - 25))

    return pygame.Rect(x, y, width, height), ratio


def show_menu():
    global dis_width, dis_height, dis

    menu = True
    selected = 0
    menu_items = ["Начать игру", "Настройки размера окна", "Выход"]

    # Настройки размера
    width_slider = dis_width
    height_slider = dis_height

    in_size_settings = False
    dragging_width = False
    dragging_height = False

    while menu:
        dis.fill(white)

        if not in_size_settings:
            # Заголовок меню
            title = menu_font.render("ЗМЕЙКА", True, yellow)
            title_rect = title.get_rect(center=(dis_width / 2, dis_height / 4))
            dis.blit(title, title_rect)

            # Элементы меню
            for i, item in enumerate(menu_items):
                color = yellow if i == selected else grey
                item_text = font_style.render(item, True, color)
                item_rect = item_text.get_rect(center=(dis_width / 2, dis_height / 2 + i * 60))
                dis.blit(item_text, item_rect)

                # Стрелка выбора
                if i == selected:
                    arrow = font_style.render(">", True, yellow)
                    dis.blit(arrow, (item_rect.left - 40, item_rect.top))


        else:
            # Экран настроек размера
            settings_title = menu_font.render("НАСТРОЙКА РАЗМЕРА ОКНА", True, yellow)
            settings_title_rect = settings_title.get_rect(center=(dis_width / 2, 100))
            dis.blit(settings_title, settings_title_rect)

            # Слайдер для ширины окна
            width_rect, width_ratio = draw_slider(dis_width // 4, 200, dis_width // 2, 20,
                                                  width_slider, MIN_WIDTH, MAX_WIDTH, "Ширина")

            # Слайдер для высоты окна
            height_rect, height_ratio = draw_slider(dis_width // 4, 280, dis_width // 2, 20,
                                                    height_slider, MIN_HEIGHT, MAX_HEIGHT, "Высота")

            # Текущий размер
            size_text = font_style.render(f"Текущий размер: {dis_width} x {dis_height}", True, white)
            size_rect = size_text.get_rect(center=(dis_width / 2, 350))
            dis.blit(size_text, size_rect)

            # Кнопка сохранения
            save_rect = draw_button("Сохранить", dis_width // 2 - 150, 400, 300, 50,
                                    blue, dark_grey)

            # Кнопка сброса
            reset_rect = draw_button("Сбросить", dis_width // 2 - 150, 470, 300, 50,
                                     yellow, dark_grey)

            # Кнопка возврата
            back_rect = draw_button("Назад", dis_width // 2 - 150, 540, 300, 50,
                                    blue, dark_grey)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if not in_size_settings:
                    if event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(menu_items)
                    elif event.key == pygame.K_UP:
                        selected = (selected - 1) % len(menu_items)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if selected == 0:  # Начать игру
                            menu = False
                            return True
                        elif selected == 1:  # Настройки размера окна
                            in_size_settings = True
                        elif selected == 2:  # Выход
                            pygame.quit()
                            quit()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                else:
                    if event.key == pygame.K_ESCAPE:
                        in_size_settings = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if in_size_settings:
                    # Проверка клика по слайдерам
                    if width_rect.collidepoint(mouse_pos):
                        dragging_width = True
                    if height_rect.collidepoint(mouse_pos):
                        dragging_height = True

                    # Проверка клика по кнопкам
                    if save_rect.collidepoint(mouse_pos):
                        # Сохраняем настройки
                        dis_width = width_slider
                        dis_height = height_slider

                        # Обновляем дисплей с новыми размерами
                        dis = pygame.display.set_mode((dis_width, dis_height))
                        in_size_settings = False

                    if reset_rect.collidepoint(mouse_pos):
                        # Сброс настроек
                        width_slider = DEFAULT_WIDTH
                        height_slider = DEFAULT_HEIGHT

                    if back_rect.collidepoint(mouse_pos):
                        in_size_settings = False

            if event.type == pygame.MOUSEBUTTONUP:
                dragging_width = False
                dragging_height = False

            if event.type == pygame.MOUSEMOTION:
                if dragging_width:
                    mouse_x = event.pos[0]
                    # Вычисляем новое значение ширины
                    ratio = (mouse_x - width_rect.left) / width_rect.width
                    ratio = max(0, min(1, ratio))
                    width_slider = int(MIN_WIDTH + ratio * (MAX_WIDTH - MIN_WIDTH))
                    # Округляем до ближайшего числа, кратного 10
                    width_slider = (width_slider // 10) * 10

                if dragging_height:
                    mouse_x = event.pos[0]
                    ratio = (mouse_x - height_rect.left) / height_rect.width
                    ratio = max(0, min(1, ratio))
                    height_slider = int(MIN_HEIGHT + ratio * (MAX_HEIGHT - MIN_HEIGHT))
                    height_slider = (height_slider // 10) * 10

        clock.tick(30)


def generate_food():
    global dis_width, dis_height, snake_block
    # Генерируем координаты, кратные размеру блока змейки
    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
    return foodx, foody

def gameLoop():
    global dis_width, dis_height, dis, clock

    game_over = False
    game_close = False
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1

    # Генерация первой еды
    foodx, foody = generate_food()

    while not game_over:
        while game_close == True:
            dis.fill(grey)
            message("Вы проиграли! Нажмите Q для выхода или C для повторной игры", black)
            message("Нажмите M для возврата в меню", black, 80)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_c:
                        gameLoop()
                    if event.key == pygame.K_m:
                        if show_menu():
                            gameLoop()
                        return
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_ESCAPE:
                    if show_menu():
                        gameLoop()
                    return

        # Проверка столкновения с границами
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(grey)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Проверка столкновения с собой
        for segment in snake_List[:-1]:
            if segment == snake_Head:
                game_close = True

        snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
            foodx, foody = generate_food()
            Length_of_snake += 1

        clock.tick(snake_speed)

if __name__ == "__main__":
    if show_menu():
        gameLoop()

pygame.quit()
quit()