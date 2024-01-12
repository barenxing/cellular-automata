from bitarray import bitarray
from bitarray.util import int2ba, ba2int
import pygame
from random import randint, choice

class CellWorld:
    def __init__(self, window: pygame.Surface, steps: int, cell_width: int, rule: int=0, random_seed:bool = False):
        self.window = window
        self.cell_width = cell_width
        self.steps = steps
        self.set_initial_cells(random_seed)
        self.update_rule(number=rule)


    def update_ruleset(self):
        a = int2ba(self.rule, endian='little')
        a.fill()
        self.ruleset = a.tolist()
    

    def update_rule(self, step: int|None=None, number: int|None=None):
        if step:
            self.rule = (self.rule + step) % 256
        elif type(number) == int:
            self.rule = number % 256

        self.update_ruleset()
        pygame.display.set_caption(f"Cellular Automata - rule {self.rule}")
        self.draw()


    def set_initial_cells(self, random_seed: bool=False):
        w = 2*self.steps+1
        self.initial_cells = bitarray('0'*w)
        if random_seed:
            for i in range(w):
                self.initial_cells[i] = choice([0,0,0,0,0,1])
        else:
            self.initial_cells[w//2] = 1
    
    
    def draw(self):
        self.window.fill('gray30')

        cells = self.initial_cells
        for i in range(self.steps+2):
            self.draw_at(i, cells)
            cells = self.cells_update(cells)


    def draw_at(self, row: int, cells):
        for i, value in enumerate(cells):
            color = ['gray85', 'black'][value]
            csz = self.cell_width
            pygame.draw.rect(self.window, color, (i*csz, row*csz, csz, csz))
            pygame.draw.rect(self.window, 'gray60', (i*csz, row*csz, csz, csz), 1)
                                

    def cells_update(self, cells):
        c = len(cells)
        next_cells = [None]*c

        next_cells[0] = self.next_generation((cells[-1], cells[0], cells[1]))
        next_cells[-1] = self.next_generation((cells[-2], cells[-1], cells[0]))

        for i in range(1, c-1):
            next_cells[i] = self.next_generation(cells[i-1:i+2])
        return next_cells


    def next_generation(self, cells):
        index = ba2int(bitarray(cells))
        return self.ruleset[index]

