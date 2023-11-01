import pygame


class Button:
    def __init__(self, text, pos, size, action):
        self.text = text
        self.pos = pos
        self.size = size
        self.action = action
        self.color = (200, 200, 200)
        self.text_color = (0, 0, 0)

    def draw(self, win, font):
        pygame.draw.rect(win, self.color, pygame.Rect(self.pos, self.size))
        button_text = font.render(self.text, True, self.text_color)
        win.blit(button_text, (self.pos[0] + 10, self.pos[1] + 10))

    def was_clicked(self, x, y):
        return self.pos[0] <= x <= self.pos[0] + self.size[0] and self.pos[1] <= y <= self.pos[1] + self.size[1]
