import pygame
from random import choice

class CellWorld:
    def __init__(self, window: pygame.Surface, steps: int, cell_width: int, rule: int=0, random_seed:bool = False):
        self.window = window
        self.cell_width = cell_width
        self.steps = steps
        self.set_initial_cells(random_seed)
        self.update_rule(number=rule)


    def update_ruleset(self):
        self.ruleset = list(map(lambda x: int(x), bin(self.rule)[2:].zfill(8)[::-1]))


    def update_rule(self, step: int|None=None, number: int|None=None):
        if step:
            self.rule = (self.rule + step) % 256
        elif type(number) == int:
            self.rule = number % 256

        self.update_ruleset()
        pygame.display.set_caption(f"Cellular Automata - rule {self.rule}")
        self.draw()


    def set_initial_cells(self, random_seed: bool=False):
        self.initial_cells = [0]*self.steps + [1] + [0]*self.steps
        if random_seed:
            for i in range(len(self.initial_cells)):
                self.initial_cells[i] = choice([0, 1])
    
    
    def draw(self):
        self.window.fill('gray30')

        cells = self.initial_cells
        for i in range(self.steps+2):
            self.draw_at(i, cells)
            cells = self.cells_update(cells)


    def draw_at(self, row: int, cells: list[int]):
        for i, value in enumerate(cells):
            color = ['gray85', 'black'][value]
            csz = self.cell_width
            pygame.draw.rect(self.window, color, (i*csz, row*csz, csz, csz))
            pygame.draw.rect(self.window, 'gray60', (i*csz, row*csz, csz, csz), 1)
                                

    def cells_update(self, cells: list[int]) -> list[int]:
        c = len(cells)
        next_cells = [None]*c

        next_cells[0] = self.next_generation((cells[-1], cells[0], cells[1]))
        next_cells[-1] = self.next_generation((cells[-2], cells[-1], cells[0]))

        for i in range(1, c-1):
            next_cells[i] = self.next_generation(cells[i-1:i+2])
        return next_cells


    def next_generation(self, cells: list[str]) -> int:
        index = int("".join(map(lambda x: f"{x}", cells)), base=2)
        return self.ruleset[index]