import pygame

X_SIZE = 600
Y_SIZE = 600


class Core:
    def __init__(self, x, y, w, o):
        self.x_pos = x
        self.y_pos = y
        self.w = w
        self.o = o
        self.tasks = []

    def draw_core(self, screen, colour):
        pygame.draw.rect(screen, colour, [self.x_pos, self.y_pos, self.w, self.w], 2)

    def draw_interconnect(self, screen, colour):
        if self.x_pos + self.o < X_SIZE:
            pygame.draw.aaline(screen, colour, (self.x_pos + self.w, self.y_pos + self.w / 2),
                               (self.x_pos + self.o, self.y_pos + self.w / 2))
        if self.y_pos + self.o < Y_SIZE:
            pygame.draw.aaline(screen, colour, (self.x_pos + self.w / 2, self.y_pos + self.w),
                               (self.x_pos + self.w / 2, self.y_pos + self.o))

    def add_task(self, task):
        self.tasks.append(task)
        self.tasks = list(set(self.tasks))

    def draw_tasks(self, screen, myfont):
        self.tasks.sort()

        string = ""
        count = "Count: " + str(len(self.tasks))
        for t in self.tasks:
            if string != "":
                string += ", "
            string += str(t)
        textsurface = myfont.render(string, False, (0, 0, 0))
        screen.blit(textsurface, (self.x_pos + self.w / 2 - textsurface.get_width() / 2, self.y_pos + 5))

        textsurface = myfont.render(count, True, (0, 0, 0))
        screen.blit(textsurface, (
        self.x_pos + self.w / 2 - textsurface.get_width() / 2, self.y_pos + self.w / 2 - textsurface.get_height() / 2))
