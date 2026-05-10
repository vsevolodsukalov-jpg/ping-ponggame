from pygame import *

'''Необходимые классы'''



# класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))  # вместе 55,55 - параметры
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



# сделать так, чтобы ракетка не уходила вниз за пределы экрана
# (то-есть ракетка должна быть видна полностью при достижении конечного значения по оси y)

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed() # получаем нажатую кнопку
        # проверяем кнопку на совпадение с кнопкой "стрелка вверх" и
        # координата ракетки должна быть больше 5, чтобы ракетка не уходила за границу карты вверх
        # если true - координата y уменьшается (ракетка поднимается)
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        # проверяем кнопку на совпадение с кнопкой "стрелка вниз" и
        # координата ракетки должна быть меньше размер окна - 80, чтобы ракетка не уходила за границу карты вниз
        # если true - координата y увеличивается (ракетка опускается)
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def update_l(self):
        keys = key.get_pressed() # получаем нажатую кнопку
        # проверяем кнопку на совпадение с кнопкой "W" и
        # координата ракетки должна быть больше 5, чтобы ракетка не уходила за границу карты вверх
        # если true - координата y уменьшается (ракетка поднимается)
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        # проверяем кнопку на совпадение с кнопкой "S" и
        # координата ракетки должна быть меньше размер окна - 80, чтобы ракетка не уходила за границу карты вниз
        # если true - координата y увеличивается (ракетка опускается)
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed


# игровая сцена:
back = (200, 255, 255)  # цвет фона (background)
win_width = 600 # размер окна в ширину
win_height = 500 # размер окна в длину
window = display.set_mode((win_width, win_height)) # окно будет размером win_width и win_height
window.fill(back) # заливка цветом back = (200, 255, 255)

# флаги, отвечающие за состояние игры
game = True # игровой цикл
finish = False # Закончена ли игра
clock = time.Clock() # игровой таймер
FPS = 60 # frames per second - частота кадров в секунду

# создания мяча и ракетки
racket1 = Player('racket.png', 30, 200, 4, 50, 150)
racket2 = Player('racket.png', 520, 200, 4, 50, 150)
ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)

# с этого момента на след уроке

font.init() # Инициализация шрифтов
font = font.Font(None, 35) # Задание шрифта - None - шрифт по умолчанию
# Задаем надписи (первый параметр - надпись)
# второй параметр - Antialias - Если True, границы надписи сглаженные,
# если False - границы будут острые, углы 90 градусов
# Третий параметр - цвет - формат - rgb (смотри rgb calculator)
lose1 = font.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font.render('PLAYER 2 LOSE!', True, (180, 0, 0))

speed_x = 4 # скорость мячика по координате x
speed_y = -4 # скорость мячика по координате y

# запускается игровой цикл
while game:
    for e in event.get(): # Отлавливем событие на предмет выхода из игры (нажатие по крестику)
        if e.type == QUIT:
            game = False
            break

    if not finish: # (not finish) = (finish != True)
        window.fill(back) # заполнить цветом фон окна
        racket1.update_l() # Связываем метод обновления движения по координате y для левой ракетки
        racket2.update_r() # Связываем метод обновления движения по координате y для правой ракетки
        ball.rect.x += speed_x # Задаем перемещение мячика по координате x - горизонтально
        ball.rect.y += speed_y # Задаем перемещение мячика по координате y - вертикально

        # Блок, отвечающий за смену направления движения по горизонтальной оси (вправо/влево)
        # при соприкосновении мячика с одной из ракеток
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1

        # Блок, отвечающий за смену направления движения по вертикальной оси (вверх/вниз)
        # при соприкосновении мячика с верхней или нижней границей окна
        if ball.rect.y > win_height - 50 or ball.rect.y < 0:
            speed_y *= -1

        # если мяч улетел дальше ракетки, выводим условие проигрыша для первого игрока
        if ball.rect.x < -1:
            finish = True
            window.blit(lose1, (200, 200))
            game_over = True

        # если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока
        if ball.rect.x > win_width - 40:
            finish = True
            window.blit(lose2, (200, 200))
            game_over = True

        racket1.reset()
        racket2.reset()
        ball.reset()

    display.update()
    clock.tick(FPS)
