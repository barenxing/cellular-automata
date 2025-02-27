from argparse import ArgumentParser, RawTextHelpFormatter
import pygame
from cell_world import CellWorld

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

    world = CellWorld(window=window, steps=steps, cell_width=cell_width, rule_number=rule, random_seed=random_seed)

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    world.set_initial_cells(random_seed=True)
                if event.key == pygame.K_HOME:
                    world.update_rule_number(rule=0)
                if event.key == pygame.K_END:
                    world.update_rule_number(rule=255)
                if event.key == pygame.K_PAGEUP:
                    world.update_rule_number(increment=-10)
                if event.key == pygame.K_PAGEDOWN:
                    world.update_rule_number(increment=10)

                if event.key == pygame.K_LEFT or event.key == pygame.K_UP:
                    world.update_rule_number(increment=-1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                    world.update_rule_number(increment=1)

        if world.need_redraw:
            world.draw()
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
