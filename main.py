"""
Group: Keyboard Liberators
Main entrance of the program.
"""

import pygame
import cv2
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('sysconfig.ini')


pygame.init()

screen = pygame.display.set_mode((640, 480))
camera = cv2.VideoCapture(0)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    ret, frame = camera.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.rotate(frame, -90)
    screen.blit(frame, (0, 0))
    pygame.display.flip()
    clock.tick(60)
