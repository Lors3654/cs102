import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen_size = life.cols * self.cell_size, life.rows * self.cell_size
        self.screen = pygame.display.set_mode(self.screen_size)
        
    def draw_lines(self) -> None:
        # Copy from previous assignment
         width, height = self.screen_size

        for x in range(0, width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, height))
        for y in range(0, height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
         for i in range(self.life.rows):
            for j in range(self.life.cols):
                cur_color = pygame.Color('white')
                if self.life.curr_generation[i][j]:
                    cur_color = pygame.Color('green')
                pygame.draw.rect(self.screen, cur_color,
                                 (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        

        pause = False
        running = True
        while running and not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYUP and event.key == K_SPACE:
                    pause = not pause
                elif event.type == MOUSEBUTTONDOWN and pause:
                    self.mouse_fill_cell()

            self.draw_grid()
            self.draw_lines()
            if not pause:
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

if __name__ == '__main__':
    life = GameOfLife((24, 24), max_generations=50)
    gui = GUI(life)
    gui.run()

