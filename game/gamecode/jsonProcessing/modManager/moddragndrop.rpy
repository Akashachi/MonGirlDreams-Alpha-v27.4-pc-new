init 1 python:
    
    config.pygame_events = [pygame.DROPFILE]

    class ZipDragAndDrop(renpy.Displayable):
        def __init__(self, **kwargs):
            super(ZipDragAndDrop, self).__init__(**kwargs)

        def render(self, width, height, st, at):
            render = renpy.Render(1, 1)
            return render
 
        def event(self, ev, x, y, st):
            # print("Event type:", ev.type)
            if ev.type == pygame.DROPFILE:
                if ev.file.endswith(".zip"):
                    filename = os.path.basename(ev.file)
                    destination = os.path.join(os.path.dirname(renpy.config.gamedir), "Mods/") + filename
                    shutil.copy(ev.file, destination)
                    updateModMetadata(True)
                    renpy.hide_screen("urlInput")
                    renpy.notify( filename + " moved. Install below!")
                    renpy.restart_interaction()
                    
                

    modDragNDrop = ZipDragAndDrop()