init python:
    on_listTitleSize = 27
    on_listTextSize = 25
    on_listEntryHeight = 34

    on_cmenu_listTextSize = 30
    on_cmenu_listEntryHeight = 40

    if renpy.variant("touch"):
        on_cmenu_listTextSize = 38
        on_cmenu_listEntryHeight = 50

screen ON_Scrollbox(name="", leftBar=False, hideBar=True, titleAlign=0.5, boxAlign=(0.0, 0.0)):

    #viewportID2 = name + str(random.random()) # prevent collisions for viewports with same name
    $ viewportID2 = name + str(renpy.random.randint(0, 1000)) + str(renpy.random.randint(0, 1000)) # prevent collisions for viewports with same name

    vbox:
        align boxAlign
        if name:
            text name size on_listTitleSize xalign titleAlign
        hbox:
            xfill True
            box_reverse leftBar

            viewport id viewportID2:
                mousewheel True
                draggable True
                vbox:
                    text "" size 0 color "#fff" ysize 0 xalign 0.5  # action [SelectedIf(False), NullAction()]
                    transclude

            vbar value YScrollValue(viewportID2):

                if hideBar:
                    unscrollable "hide"

transform flipClouds:
    xzoom -1.0

screen ON_TextButton(text="", action=[], hovered=[], unhovered=[], alt=""):
    default cloudsLeft = "TextButton_clouds" + str(renpy.random.randint(0, 7)) + ".png"
    default cloudsRight = "TextButton_clouds" + str(renpy.random.randint(0, 7)) + ".png"
    if alt == "":
        $ alt = text
    fixed:
        xsize 324
        ysize 81

        add cloudsLeft
        add cloudsRight xzoom -1.0

        imagebutton:
            idle "TextButton.png"
            hover "TextButton_hovered.png"
            insensitive "TextButton_insensitive.png"
            action action
            hovered hovered
            unhovered unhovered
            alt alt

        text text:
            xalign 0.5
            yalign 0.5

screen ON_TextButtonBackground(text=""):

    default cloudsLeft = "TextButton_clouds" + str(renpy.random.randint(0, 7)) + ".png"
    default cloudsRight = "TextButton_clouds" + str(renpy.random.randint(0, 7)) + ".png"

    fixed:
        xsize 324
        ysize 81

        add cloudsLeft
        add cloudsRight xzoom -1.0
        add "TextButton_Background.png"

        text text:
            xalign 0.5
            yalign 0.5

screen ON_TextButtonBackgroundNoClouds(text=""):

    fixed:
        xsize 324
        ysize 81

        add "TextButton_Background.png"

        text text:
            xalign 0.5
            yalign 0.5

screen ON_TextButtonSmol(text="", action=[], hovered=[]):
    default cloudsLeft = "TextButton_clouds" + str(renpy.random.randint(0, 7)) + ".png"
    default cloudsRight = "TextButton_clouds" + str(renpy.random.randint(0, 7)) + ".png"

    fixed:
        xsize 203
        ysize 68

        #add cloudsLeft ypos 2 xpos 1
        #add cloudsRight xzoom -1.0 xpos -65 ypos 2

        imagebutton:
            idle "textButtonSmol.png"
            hover "textButtonSmol_hovered.png"
            insensitive "textButtonSmol_insensitive.png"
            action action
            hovered hovered

        text text:
            xalign 0.5
            yalign 0.5

screen ON_TextButtonMid(text="", action=[], hovered=[], unhovered=[]):
    default cloudsLeft = "TextButton_clouds" + str(renpy.random.randint(0, 7)) + ".png"
    default cloudsRight = "TextButton_clouds" + str(renpy.random.randint(0, 7)) + ".png"

    fixed:
        xsize 270
        ysize 90

        add cloudsLeft ypos 2 xpos 1
        add cloudsRight xzoom -1.0 xpos -65 ypos 2

        imagebutton:
            idle "TextButtonMid.png"
            hover "TextButtonMid_hovered.png"
            insensitive "TextButtonMid_insensitive.png"
            action action
            hovered hovered
            unhovered unhovered

        text text:
            xalign 0.5
            yalign 0.5

screen ON_TextButtonNightmare(text="", action=[], hovered=[]):


    fixed:
        xsize 270
        ysize 90


        imagebutton:
            idle "TextButtonMidRed.png"
            hover "TextButtonMidRed_hovered.png"
            insensitive "TextButtonMid_insensitive.png"
            action action
            hovered hovered

        text text:
            xalign 0.5
            yalign 0.5
