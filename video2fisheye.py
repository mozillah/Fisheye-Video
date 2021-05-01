# PYGAME IS REQUIRED
try:
    import pygame
    from pygame import Color, Surface, SRCALPHA, RLEACCEL, BufferProxy
    from pygame.surfarray import pixels3d, array_alpha, pixels_alpha, array3d
    from pygame.image import frombuffer

except ImportError:
    print("\n<Pygame> library is missing on your system."
          "\nTry: \n   C:\\pip install pygame on a window command prompt.")
    raise SystemExit

from FISHEYE import fish_eye24, fish_eye32

from pygame.locals import KEYDOWN, K_ESCAPE, K_q
import pygame
import numpy as np

import cv2
import sys


def surface_to_string(surface):
    """Convert a pygame surface into string"""
    return pygame.image.tostring(surface, 'RGB')


def pygame_to_cvimage(surface):
    # cv2.Header
    """Convert a pygame surface into a cv image"""
    print(type(surface))
    cv_image =np.array(surface)
    # cv_image = cv2.CreateImageHeader(surface.get_size(), cv2.IPL_DEPTH_8U, 3)
    # image_string = surface_to_string(surface)
    # cv2.SetData(cv_image, image_string)
    return cv_image

camera = cv2.VideoCapture("/home/mazz/Desktop/Work/Videos/railway.avi")
frame_width = int(camera.get(3))
frame_height = int(camera.get(4))
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
screen = pygame.display.set_mode([frame_width, frame_height])
background = pygame.image.load('back.png').convert()
background.set_alpha(None)
try:
    while True:

        ret, frame = camera.read()
        screen.fill([0, 0, 0])
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame.swapaxes(0, 1)
        # pygame.surfarray.blit_array(screen, frame)
        # pygame.display.update()
        pygame.surfarray.blit_array(screen, frame)
        surface_ = screen
        
        surface24 = surface_.convert()
        surface32 = surface_.convert_alpha()
        i = 0
        fisheye_surface = fish_eye32(surface32)

        fisheye_surface = fish_eye24(surface24)

        screen.fill((0, 0, 0))
        # screen.blit(background, q(0, 0))
        screen.blit(fisheye_surface, (0, 0))
        screen.blit(surface32, (frame_width, 0))
        # screen.blit(fisheye_surface, (frame_width, frame_height))
        pygame.display.flip()
        cv_image = pygame.surfarray.array3d(fisheye_surface)
        # cv_image = pygame_to_cvimage(surface32)  # Create cv image from pygame image
        # cv_image = np.uint8(cv_image)
        cv_image=cv_image.swapaxes(0,1)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        print(type(cv_image))
        cv2.imshow('frame',cv_image)
        cv2.waitKey(1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    sys.exit(0)

except (KeyboardInterrupt, SystemExit):
    pygame.quit()
    cv2.destroyAllWindows()
