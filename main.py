from argparse import ArgumentParser, RawTextHelpFormatter
from random import choice
import pygame
from wolfram_world import WolframWorld as CellWorld

pygame.init()

def main():
    rule, steps, window_width = 0, 20, 800
    random_seed = False

    prog_desc = """
    Displays Wolfram Cellular Automata by the rule numbers.

    LEFT or UPPER arrow key decrements the rule number by 1
    RIGHT or DOWN arrow key increments the rule number by 1
    PAGE_UP   decrements the rule number by 10
    PAGE DOWN increments the rule number by 10
    HOME changes rule number to 0
    END  changes rule number to 255
    """

    parser = ArgumentParser(description=prog_desc, formatter_class=RawTextHelpFormatter)
    parser.add_argument('-s', '--steps', type=int, default=steps, help="number of steps(rows) to calculate, default: 20")
    parser.add_argument('-r', '--rule', type=int,  default=rule,  help="rule number as defined by Wolfram Alpha, integer 0-255, default: 0")
    parser.add_argument('-w', '--width', type=int, default=window_width, help="width of the display window, default: 800")
    parser.add_argument('-x', '--random', action='store_true', default=False, help="default False: if set, uses a random array")
    args = parser.parse_args()

    if args.rule: rule = args.rule
    if args.steps: steps = args.steps
    if args.width: window_width = args.width
    if args.random: random_seed = args.random

    cell_width = window_width // (2*steps)
    width, height = cell_width*(2*steps+1), cell_width*(steps+1)

    window = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    world = CellWorld(window=window, cell_width=cell_width, rows=steps+1, cols=2*steps+1, random_seed=random_seed)
    world.update_rule_number(rule=rule)

    
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    world.update_rule_number(rule=choice(range(256)))
                if event.key == pygame.K_HOME or event.key == pygame.K_a:
                    world.update_rule_number(rule=0)
                if event.key == pygame.K_END or event.key == pygame.K_z:
                    world.update_rule_number(rule=255)
                if event.key == pygame.K_PAGEUP or event.key == pygame.K_p:
                    world.update_rule_number(increment=-10)
                if event.key == pygame.K_PAGEDOWN or event.key == pygame.K_n:
                    world.update_rule_number(increment=10)

                if event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_f:
                    world.update_rule_number(increment=-1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT or event.key == pygame.K_j:
                    world.update_rule_number(increment=1)

        if world.need_redraw:
            world.draw()
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
