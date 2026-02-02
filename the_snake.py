"""Импорты библеотек."""
import pygame

from random import choice, randint

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTRAL = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=None, body_color=None) -> None:
        """Инициализирует базовые атрибуты."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Пустышка."""


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self, occupied_pos=None, position=None, body_color=APPLE_COLOR):
        """Начальное состояние яблока."""
        super().__init__(position=position, body_color=body_color)
        self.randomize_position(occupied_pos)

    def randomize_position(self, occupied_pos=None):
        """Устанавливает случайные координаты яблока, не занятые змейкой."""
        if not occupied_pos:
            occupied_pos = []
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in occupied_pos:
                break

    def draw(self):
        """Рисует яблоко на игровом поле."""
        rect = pygame.Rect((self.position), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self, position=CENTRAL, body_color=SNAKE_COLOR):
        """Начальное состояние змейки."""
        super().__init__(position=position, body_color=body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self, direction):
        """Обновляет направление движения, предотвращая разворот."""
        tail = (self.direction[0] * -1, self.direction[1] * -1)
        if direction and tail != direction:
            self.direction = direction

    def move(self):
        """Вычисляет новую позицию головы и обновляет тело змейки."""
        x, y = self.get_head_position()
        dir_x, dir_y = self.direction

        new_head = (
            (x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self) -> None:
        """Отрисовывает все сегменты тела змейки."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает текущие координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки при столкновении с собой."""
        self.length = 1
        self.positions = [self.position]
        self.next_direction = None
        possible_directions = [(UP), (RIGHT), (DOWN), (LEFT)]
        self.direction = choice(possible_directions)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)
        elif event.type == pygame.KEYUP:
            snake.next_direction = None


def main():
    """Основной игровой цикл."""
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
