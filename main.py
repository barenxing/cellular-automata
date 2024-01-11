import sys, argparse
import pygame
from cell_world import CellWorld

pygame.init()


 
def main():
    rule, steps, window_width = 0, 50, 1800
    random_seed = False
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--steps', type=int)
    parser.add_argument('-r', '--rule', type=int)
    parser.add_argument('-w', '--width', type=int)
    parser.add_argument('-x', '--random', action='store_true')
    args = parser.parse_args()

    if args.rule: rule = args.rule
    if args.steps: steps = args.steps
    if args.width: window_width = args.width
    if args.random: random_seed = args.random

    cell_width = window_width // (2*steps)
    width, height = cell_width*(2*steps+1), cell_width*(steps+1)

    window = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    world = CellWorld(window=window, steps=steps, cell_width=cell_width, rule=rule, random_seed=random_seed)

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_HOME:
                    world.update_rule(number=0)
                if event.key == pygame.K_END:
                    world.update_rule(number=255)                
                if event.key == pygame.K_PAGEUP:
                    world.update_rule(step=-10)
                if event.key == pygame.K_PAGEDOWN:
                    world.update_rule(step=10)
                                        
                if event.key == pygame.K_LEFT or event.key == pygame.K_UP:
                    world.update_rule(step=-1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                    world.update_rule(step=1)
        
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':    
    main()