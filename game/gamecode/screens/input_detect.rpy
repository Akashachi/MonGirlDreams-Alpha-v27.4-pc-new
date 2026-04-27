init:
    define config.pass_controller_events = True
    define config.pass_joystick_events = True
    if renpy.android:
        default persistent.lastInput = "Touch"
    else:
        default persistent.lastInput = "Normal"
init python:
    
    class InputDetector(renpy.Displayable):
        def __init__(self, **kwargs):
            super(InputDetector, self).__init__(**kwargs)
        def render(self, width, height, st, at):
            render = renpy.Render(0, 0)
            return render
 
        def event(self, ev, x, y, st):

            # print("Event type:", ev.type)
            if ev.type == pygame.MOUSEMOTION and persistent.lastInput != "Mouse":
                persistent.lastInput = "Mouse"
                renpy.restart_interaction()
            elif ev.type == pygame.MOUSEBUTTONDOWN and persistent.lastInput != "Mouse":
                persistent.lastInput = "Mouse"
                renpy.restart_interaction()
            elif ev.type == pygame.FINGERMOTION and persistent.lastInput != "Touch":
                persistent.lastInput = "Touch"
                renpy.restart_interaction()
            elif ev.type == pygame.FINGERDOWN and persistent.lastInput != "Touch":
                persistent.lastInput = "Touch"
                renpy.restart_interaction()
            elif ev.type == pygame.KEYDOWN and persistent.lastInput != "Keyboard":
                persistent.lastInput = "Keyboard"
                renpy.restart_interaction()
            elif ev.type == pygame.JOYBUTTONDOWN and persistent.lastInput != "Pad":
                persistent.lastInput = "Pad"
                renpy.restart_interaction()
            elif ev.type == pygame.JOYAXISMOTION and persistent.lastInput != "Pad" and abs(ev.value) > 0.43:
                persistent.lastInput = "Pad"
                renpy.restart_interaction()
    
    InputDetection = InputDetector()