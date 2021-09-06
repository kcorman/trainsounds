import pygame, time
pygame.init()
beep = pygame.mixer.Sound("sounds/goodchug1.wav")
beep.play()
while(True):
    beep.play()
    time.sleep(.2)
