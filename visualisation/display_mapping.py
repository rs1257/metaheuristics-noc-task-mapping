from shared.constants import *
from visualisation.core import *

X_SIZE = 600
Y_SIZE = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def parse_mapping(mapping, cores):
    # for each core append which tasks are assigned to it
    for task, core in enumerate(mapping):
        cores[core].add_task(task)


def show_task_mapping(mapping):
    # Initialize the game engine
    pygame.init()
    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    myfont = pygame.font.SysFont('Arial', 12)

    # Set the height and width of the screen
    size = [X_SIZE, Y_SIZE]
    screen = pygame.display.set_mode(size)

    # Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()
    start, offset, CORE_WIDTH = 35, 150, 75
    if CORE_NUMBER == 9:
        start = 50
        CORE_WIDTH = 100
        offset = 200
    elif CORE_NUMBER == 16 or CORE_NUMBER == 12:
        start = 35
        CORE_WIDTH = 75
        offset = 150
    elif CORE_NUMBER == 25 or CORE_NUMBER == 20:
        start = 30
        CORE_WIDTH = 50
        offset = 120
    cores = []
    for i in range(SIZEX):
        x_pos = start + (i * offset)
        for j in range(SIZEY):
            y_pos = start + (j * offset)
            cores.append(Core(x_pos, y_pos, CORE_WIDTH, offset))
    while not done:

        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(10)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        # All drawing code happens after the for loop and but
        # inside the main while done==False loop.

        # Clear the screen and set the screen background
        screen.fill(WHITE)

        for i in cores:
            i.draw_core(screen, BLACK)
            i.draw_interconnect(screen, BLACK)

        parse_mapping(mapping, cores)
        for c in cores:
            c.draw_tasks(screen, myfont)

        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()
    # Be IDLE friendly
    pygame.quit()
