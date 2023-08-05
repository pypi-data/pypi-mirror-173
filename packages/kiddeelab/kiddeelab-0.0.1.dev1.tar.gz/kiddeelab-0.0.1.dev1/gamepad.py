from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import platform

class joystick:
        def __init__(self):
            #variables used for pygame joystick
            self._joystick = None

            self.buttonA = None
            self.buttonB = None
            self.buttonX = None
            self.buttonY = None
            self.buttonL1 = None
            self.buttonR1 = None
            self.buttonSelect = None
            self.buttonStart = None
            self.buttonL3 = None
            self.buttonR3 = None
            self.buttonL2 = None
            self.buttonR2 = None
            self.leftStickX = None
            self.leftStickY = None
            self.rightStickX = None
            self.rightStickY = None
            self.hat = None
            self.home = None
        
        def update(self):
            for event in pygame.event.get():
                pass

            if platform.system() == "Darwin":
                self.buttonA = self._joystick.get_button(0)
                self.buttonB = self._joystick.get_button(1)
                self.buttonX = self._joystick.get_button(2)
                self.buttonY = self._joystick.get_button(3)
                self.buttonL1 = self._joystick.get_button(4)
                self.buttonR1 = self._joystick.get_button(5)
                self.buttonStart = self._joystick.get_button(8)
                self.buttonSelect = self._joystick.get_button(9)
                self.home = self._joystick.get_button(10)

                if self._joystick.get_axis(2) > 0.5:
                    self.buttonL2 = 1
                else:
                    self.buttonL2 = 0

                if self._joystick.get_axis(5) > 0.5:
                    self.buttonR2 = 1
                else:
                    self.buttonR2 = 0

                self.leftStickX = round(self._joystick.get_axis(0), 3)
                self.leftStickY = round(self._joystick.get_axis(1), 3)
                self.rightStickX = round(self._joystick.get_axis(3), 3)
                self.rightStickY = round(self._joystick.get_axis(4), 3)

                _hatValue = (self._joystick.get_button(14)-self._joystick.get_button(13), self._joystick.get_button(11)-self._joystick.get_button(12))
                self.hat = _hatValue
            else:
                self.buttonA = self._joystick.get_button(0)
                self.buttonB = self._joystick.get_button(1)
                self.buttonX = self._joystick.get_button(2)
                self.buttonY = self._joystick.get_button(3)
                self.buttonL1 = self._joystick.get_button(4)
                self.buttonR1 = self._joystick.get_button(5)
                self.buttonSelect = self._joystick.get_button(6)
                self.buttonStart = self._joystick.get_button(7)
                self.buttonL3 = self._joystick.get_button(8)
                self.buttonR3 = self._joystick.get_button(9)

                if self._joystick.get_axis(4) > 0.5:
                    self.buttonL2 = 1
                else:
                    self.buttonL2 = 0

                if self._joystick.get_axis(5) > 0.5:
                    self.buttonR2 = 1
                else:
                    self.buttonR2 = 0

                self.leftStickX = round(self._joystick.get_axis(0), 3)
                self.leftStickY = round(self._joystick.get_axis(1), 3)
                self.rightStickX = round(self._joystick.get_axis(2), 3)
                self.rightStickY = round(self._joystick.get_axis(3), 3)

                self.hat = self._joystick.get_hat(0)