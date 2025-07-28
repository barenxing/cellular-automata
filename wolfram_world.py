# wolfram_cellular_automata/wolfram_world.py
# created by Richard Hu on 7/27/2025
#
# Wolfram World based on Bit Cell World.

from bitarray import bitarray
from random import choice
from cell_world.bit_cell_world import BitCellWorld # type: ignore
from bitarray.util import int2ba, ba2int
import pygame


class WolframWorld(BitCellWorld):
  """
  Wolfram Cellular Automata World based on Bit Cell World.
  """

  def __init__(self, window, cell_width=20, rows=21, cols=41, random_seed=False):
      super().__init__(window=window, cell_width=cell_width, rows=rows, cols=cols, random_seed=random_seed)
      self.rule = 0  if not random_seed else choice(range(256))
      self.ruleset = self.ruleset_for(self.rule)


  def initialize_cells(self, random_seed: bool=False):
    """Initialize the first row cells for the Wolfram World.

    Args:
        random_seed (bool): Whether to use a random seed for initialization.
    """

    # note the random_seed is required by parent class, but ignored here
    self.first_row = bitarray('0' * self.cols)
    self.first_row[self.cols//2] = 1


  def update_rule_number(self, increment: int|None=None, rule: int|None=None):
    """Update the rule number for the cellular automata by an increment or a new rule number.

    Args:
        increment (int | None, optional): The amount to change the rule by. Defaults to None.
        rule (int | None, optional): The new rule number to set. Defaults to None.
    """
    
    if type(increment) == int:
      # Increment the rule number and wrap around at 256
      self.rule = (self.rule + increment) % 256
    elif type(rule) == int:
      self.rule = rule % 256

    self.ruleset = self.ruleset_for(self.rule)
    pygame.display.set_caption(f"Cellular Automata - rule {self.rule}")
    self.need_redraw = True


  def ruleset_for(self, rule: int):
    a = int2ba(rule, endian='little')
    a.fill()
    return a.tolist()


  def cells_update(self, cells):
    cell_len = len(cells)
    next_gen_cells = [0]*cell_len

    # Iterate through each cell and apply the rule to generate the next generation
    # the cells are treated as circular array, so the first and last cells are neighbors
    # use modulo arithmetic to wrap around the edges
    for i in range(cell_len):
      next_gen_cells[i] = self.next_generation((
        cells[(i-1+cell_len) % cell_len], cells[i], cells[(i+1) % cell_len]
      ))

    return next_gen_cells


  def next_generation(self, cells):
    """Calculate the next generation of cells based on the current cells and the rule.
    
    Args:
        cells (tuple): A tuple of three cell values representing the current state.
    Returns:
        int: The next cell value based on the rule.
      """

    index = ba2int(bitarray(cells))
    return self.ruleset[index]


  def draw(self):
    self.window.fill('gray30')

    cells = self.first_row.copy()
    for row in range(self.rows+2):
      self.draw_row(row, cells)
      cells = self.cells_update(cells)

    self.need_redraw = False


  def draw_row(self, row: int, cells):
    for i, value in enumerate(cells):
      color = ['gray85', 'black'][value]
      csz = self.cell_width
      pygame.draw.rect(self.window, color, (i*csz, row*csz, csz, csz))
      pygame.draw.rect(self.window, 'gray60', (i*csz, row*csz, csz, csz), width=1)