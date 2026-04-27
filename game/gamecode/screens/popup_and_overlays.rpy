## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## http://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 300

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:
        xminimum 1000
        xmaximum 1000
        yminimum 300
        ymaximum 300

        label _(message):
            style "confirm_prompt"
            xalign 0.5
            yalign 0.1

        fixed: ##Return button
            xalign 0.15
            yalign 1.0
            xsize 324
            ysize 81
            use ON_TextButton(text="Yes", action=yes_action)


        fixed: ##Return button
            xalign 0.85
            yalign 1.0
            xsize 324
            ysize 81
            use ON_TextButton(text="No", action=no_action)


    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    text_align 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.button_text_properties("confirm_button")





## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 6

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"

## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text message

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")

## Input Detection #############################################################
screen input_detection():
    zorder -690
    add InputDetection

## Quick Menu screen ###########################################################

transform dropdownQuickMenu(delay=0.0):
    yalign -0.1
    on show:
        easein 0.1 yalign 0.0
    on hide:
        yalign 0.0
        pause delay
        easeout 0.1 yalign -0.1
    on appear:
        easein 0.1 yalign 0.0
init python:
    def dropdownQuickMenuControl(d):
        if renpy.get_screen_variable(quick_menu_visible, screen=quick_menu):
            return At(d, dropdownQuickMenu)
        else:
            return At(d, dropdownQuickMenu)
screen quick_menu():
    default quick_menu_visible = False
    #timer 0.2 action Hide("quick_menu", dissolve)

    ## Ensure this appears on top of other screens.
    zorder 300
    showif not minigameQuickMenuHide:
        if persistent.quickMenuVisibility == "Hover":
            fixed:
                mousearea:
                    area (0.25, 0, 1000, 81)
                    hovered SetScreenVariable("quick_menu_visible", True)
                    unhovered SetScreenVariable("quick_menu_visible", False)

        if persistent.quickMenuVisibility == "Toggle" or persistent.quickMenuVisibility == "Hover":
            if persistent.quickMenuVisibility == "Toggle":
                imagebutton:
                    xalign 0.99 yalign 0.02
                    auto "gui/button/quick/big_quickBorgar_%s_button.png"
                    if quick_menu_visible:
                        alt "Exit Quick Menu"
                    else:
                        alt "Quick Menu"
                    action [ToggleScreenVariable("quick_menu_visible")]
                showif quick_menu_visible:
                    hbox:
                        style_prefix "quick"
                        if persistent.animatedUI:
                            at dropdownQuickMenu
                        xalign 0.5 yalign 0.0
                        use quick_menu_items
            else:
                showif quick_menu_visible:
                    hbox:
                        style_prefix "quick"
                        if persistent.animatedUI:
                            at dropdownQuickMenu(delay=0.3)
                        xalign 0.5 yalign 0.0
                        use quick_menu_items
        else:
            hbox:
                style_prefix "quick"
                xalign 0.5 yalign 0.0
                use quick_menu_items
        if showTimeofDay == 1:
            hbox:
                style_prefix "quick"
                xalign 0.025 yalign 0.98
                text _(TimeOfDay) size 28 alt ""

screen quick_menu():
    default quick_menu_visible = False
    default LastTime = ""
    variant "touch"

    zorder 300
    if not minigameQuickMenuHide:
        showif persistent.quickMenuVisibility == "Toggle":
            imagebutton:
                xalign 0.98 yalign 0.02
                auto "gui/button/quick/quickBorgar_%s_button.png"
                if quick_menu_visible:
                    alt "Exit Quick Menu"
                else:
                    alt "Quick Menu"
                action [ToggleScreenVariable("quick_menu_visible")]
            showif quick_menu_visible:
                hbox:
                    style_prefix "quick"
                    if persistent.animatedUI:
                        at dropdownQuickMenu
                    xalign 0.5 yalign 0.0
                    use quick_menu_items
        else:
            hbox:
                style_prefix "quick"
                xalign 0.5 yalign 0.0
                use quick_menu_items
        if showTimeofDay == 1:
            hbox:
                style_prefix "quick"
                xalign 0.025 yalign 0.98
                text _(TimeOfDay) size 28 alt ""
        hbox:
            style_prefix "quick"
            xalign 0.975 yalign 0.98
            textbutton _("Hide-UI") action HideInterface()

style quick_button is default:
    properties gui.button_properties("quick_button")

style quick_button_text is button_text:
    properties gui.button_text_properties("quick_button")

init:
    if renpy.mobile:
        define defaultQuickMenu = ["History", "Skip", "Auto", "Menu", "Q.Save", "Q.Load"]
        default persistent.quickMenuBurger = True
        default persistent.quickMenuVisibility = "Toggle"
    else:
        define defaultQuickMenu = ["History", "Skip", "Auto", "Character", "Save", "Q.Save", "Q.Load", "Options"]
        default persistent.quickMenuBurger = False
        default persistent.quicKMenuHover = True
        default persistent.quickMenuVisibility = "Hover"
    default quick_menu = 0
    default persistent.quickMenuOrder = copy.copy(defaultQuickMenu)

init python:

    config.overlay_screens.append("quick_menu")

    class QuickButtonSelect(Action):
        def __init__(self, quickMenuOrder, rectFocus, buttonList="", buttonName="", buttonTarget=""):
            self.quickMenuOrder = quickMenuOrder
            self.rectFocus = rectFocus
            self.buttonList = buttonList
            self.buttonName = buttonName
            self.buttonTarget = buttonTarget
        def __call__(self):
            if self.buttonList == "Used":
                if self.buttonTarget == "":
                    renpy.run(CaptureFocus(self.rectFocus))
                    renpy.run(SetScreenVariable("quickTarget", self.buttonName))
                    renpy.run(SetScreenVariable("quickPop", self.buttonList))
                elif self.buttonName == self.buttonTarget:
                    renpy.run(SetScreenVariable("sortingQuickMenu", False))
                    renpy.run(SetScreenVariable("quickTarget", ""))
                    renpy.run(SetScreenVariable("quickPop", ""))
                elif self.buttonName != self.buttonTarget:
                    heldButtonName = self.quickMenuOrder.index(self.buttonName)
                    heldTargetName = self.quickMenuOrder.index(self.buttonTarget)
                    self.quickMenuOrder[heldButtonName], self.quickMenuOrder[heldTargetName] = self.quickMenuOrder[heldTargetName], self.quickMenuOrder[heldButtonName]
                    renpy.run(SetScreenVariable("sortingQuickMenu", False))
                    renpy.run(SetScreenVariable("quickTarget", ""))
                    renpy.run(SetScreenVariable("quickPop", ""))
                renpy.restart_interaction()
            else:
                renpy.run(SetScreenVariable("quickTarget", self.buttonName))
                renpy.run(CaptureFocus(self.rectFocus))
                renpy.run(SetScreenVariable("quickPop", self.buttonList))
                renpy.restart_interaction()
    class QuickButtonAction(Action):
        def __init__(self, quickMenuOrder, rectFocus, buttonTarget, buttonAction):
            self.quickMenuOrder = quickMenuOrder
            self.rectFocus = rectFocus
            self.buttonTarget = buttonTarget
            self.buttonAction = buttonAction
        def __call__(self):
            if self.buttonAction == "Sort":
                renpy.run(SetScreenVariable("sortingQuickMenu", True))
            elif self.buttonAction == "Add":
                self.quickMenuOrder.append(self.buttonTarget)
                renpy.run(SetScreenVariable("quickTarget", ""))
            elif self.buttonAction == "Remove":
                self.quickMenuOrder.remove(self.buttonTarget)
                renpy.run(SetScreenVariable("quickTarget", ""))
            renpy.run(SetScreenVariable("quickPop", ""))
            renpy.run(ClearFocus(self.rectFocus))
            renpy.restart_interaction()

    # This weird UX is specificallly to work around a bug with Ren'Py where you can only set the persistent.quickMenuOrder once.
    # No, Action classes or inline actions on the button or any combination does not work. I tried.
    def QuickMenuReset(temp, which):
        global defaultQuickMenu
        if which == "Blank":
            temp = []
            return temp
        else:
            temp = copy.copy(defaultQuickMenu)
            return temp

    def QuickMenuApply(temp):
        persistent.quickMenuOrder = copy.copy(temp)

screen quick_menu_items():
    if renpy.mobile:
        textbutton _("Menu") action [
            If(persistent.quickMenuVisibility=="Toggle", true=[SetScreenVariable("quick_menu_visible", False)]),
            ShowMenu()]
    for item in persistent.quickMenuOrder:
        if item == "History":
            textbutton _("History") action [
                If(persistent.quickMenuVisibility=="Toggle", true=[SetScreenVariable("quick_menu_visible", False)]),
                ShowMenu('history')] 
        elif item == "Skip":
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True) at dropdownQuickMenu
        elif item == "Auto":
            textbutton _("Auto") action [
                If(persistent.quickMenuVisibility=="Toggle", true=[SetScreenVariable("quick_menu_visible", False)]),
                Preference("auto-forward", "toggle")]
        elif item == "Save":
            textbutton _("Save") action [
                If(persistent.quickMenuVisibility=="Toggle", true=[SetScreenVariable("quick_menu_visible", False)]),
                ShowMenu('save')]
        elif item == "Load":
            textbutton _("Load") action [
                If(persistent.quickMenuVisibility=="Toggle", true=[SetScreenVariable("quick_menu_visible", False)]),
                ShowMenu('load')]
        elif item == "Q.Save":
            textbutton _("Q.Save") action [
                If(persistent.quickMenuVisibility=="Toggle", true=[SetScreenVariable("quick_menu_visible", False)]),
                QuickSave()]
        elif item == "Q.Load":
            textbutton _("Q.Load") action [
                If(persistent.quickMenuVisibility=="Toggle", true=[SetScreenVariable("quick_menu_visible", False)]),
                QuickLoad()]
        if (item == "Menu") and not renpy.mobile:
            textbutton _("Menu") action [
            If(persistent.quickMenuVisibility=="Toggle", true=[SetScreenVariable("quick_menu_visible", False)]),
            ShowMenu()]
        elif item == "Options" and not renpy.variant("small"):
            textbutton _("Options") action [
                If(persistent.quickMenuVisibility=="Toggle", true=[SetScreenVariable("quick_menu_visible", False)]),
                ShowMenu('options')]
        elif item == "Character":
            textbutton _("Character") action [
                If(persistent.quickMenuVisibility=="Toggle", true=[SetScreenVariable("quick_menu_visible", False)]),
                ShowMenu("ON_CharacterDisplayScreen"),
                Function(cmenu_resetMenu),
                SelectedIf(_game_menu_screen=="ON_CharacterDisplayScreen")
            ]

screen quick_menu_settings():
    modal True
    zorder 300
    style_prefix "confirm"
    add "gui/overlay/confirm.png"
    default sortingQuickMenu = False
    default quickPop = ""
    default quickTarget = ""
    default quickTargetFormatted = " (Sorting [quickTarget]):"
    default tempQuickMenuOrder = copy.copy(persistent.quickMenuOrder)

    if quickTarget:
        dismiss:
            action SetScreenVariable("quickTarget", "")
            alt "Dismiss sorting [quickTarget]"
    frame:
        if renpy.variant("small"):
            xsize 1860
        else:
            xsize 1440
        if renpy.variant("small"):
            ymaximum 800
        else:
            ymaximum 750
        vbox:
            spacing 20

            text _("Quick Menu Settings")
            if quickTarget and sortingQuickMenu:
                text _("Quick Menu" + quickTargetFormatted) xalign 0.5 size 28
            else:
                text _("Quick Menu:") xalign 0.5 size 28
            frame:
                alt "Quick Menu"
                xalign 0.5
                if renpy.variant("small"):
                    xminimum 1800
                else:
                    xminimum 1380
                yminimum 110
                hbox:
                    xalign 0.5
                    spacing 10
                    style_prefix "quick"
                    if renpy.variant("touch"):
                        textbutton _("Menu") action [SensitiveIf(False)] text_size 24
                    for item in tempQuickMenuOrder:
                        if item == "History":
                            textbutton _("History") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Used", "History", quickTarget)] text_size 24
                        elif item == "Skip":
                            textbutton _("Skip") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Used", "Skip", quickTarget)] text_size 24
                        elif item == "Auto":
                            textbutton _("Auto") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Used", "Auto", quickTarget)] text_size 24
                        elif item == "Save":
                            textbutton _("Save") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Used", "Save", quickTarget)] text_size 24
                        elif item == "Load":
                            textbutton _("Load") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Used", "Load", quickTarget)] text_size 24
                        elif item == "Q.Save":
                            textbutton _("Q.Save") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Used", "Q.Save", quickTarget)] text_size 24
                        elif item == "Q.Load":
                            textbutton _("Q.Load") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Used", "Q.Load", quickTarget)] text_size 24
                        elif (item == "Menu") and not renpy.mobile:
                            textbutton _("Menu") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Used", "Menu", quickTarget)] text_size 24
                        elif item == "Options":
                            textbutton _("Options") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Used", "Options", quickTarget)] text_size 24
                        elif item == "Character":
                            textbutton _("Character") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Used", "Character", quickTarget)] text_size 24

            hbox:
                xanchor 1.0
                if renpy.variant("small"):
                    xalign 0.73434
                else:
                    xalign 0.81
                spacing 75
                textbutton _("Visibility Mode: [persistent.quickMenuVisibility]"):
                    action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Visibility")]
                    if persistent.quickMenuVisibility == "Hover":
                        alt "Visibility Mode: [persistent.quickMenuVisibility]" + "(not compatible with keyboard navigation, select to change)"
                    else:
                        alt "Visibility Mode: [persistent.quickMenuVisibility]"
                    text_size 30
                textbutton "Set To Blank" action SetScreenVariable("tempQuickMenuOrder", copy.copy([])) text_size 30
                textbutton "Reset To Default" action SetScreenVariable("tempQuickMenuOrder", copy.copy(defaultQuickMenu)) text_size 30


            text _("Unused Buttons:") xalign 0.5 size 28
            frame:
                xalign 0.5
                if renpy.variant("small"):
                    xminimum 1800
                else:
                    xminimum 1380
                yminimum 110
                hbox:
                    xalign 0.5
                    spacing 10
                    style_prefix "quick"
                    if ("Menu" not in tempQuickMenuOrder) and not renpy.variant("touch"):
                        textbutton _("Menu") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Unused", "Menu")] text_size 24
                    if "Options" not in tempQuickMenuOrder and not renpy.variant("small"):
                        textbutton _("Options") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Unused", "Options")] text_size 24
                    if "Character" not in tempQuickMenuOrder:
                        textbutton _("Character") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Unused", "Character")] text_size 24
                    if "History" not in tempQuickMenuOrder:
                        textbutton _("History") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Unused", "History")] text_size 24
                    if "Skip" not in tempQuickMenuOrder:
                        textbutton _("Skip") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Unused", "Skip")] text_size 24
                    if "Auto" not in tempQuickMenuOrder:
                        textbutton _("Auto") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Unused", "Auto")] text_size 24
                    if "Save" not in tempQuickMenuOrder:
                        textbutton _("Save") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Unused", "Save")] text_size 24
                    if "Load" not in tempQuickMenuOrder:
                        textbutton _("Load") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Unused", "Load")] text_size 24
                    if "Q.Save" not in tempQuickMenuOrder:
                        textbutton _("Q.Save") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Unused", "Q.Save")] text_size 24
                    if "Q.Load" not in tempQuickMenuOrder:
                        textbutton _("Q.Load") action [QuickButtonSelect(tempQuickMenuOrder, "quickChoice", "Unused", "Q.Load")] text_size 24
            hbox:
                yalign 0.5
                xalign 0.5
                spacing 300
                use ON_TextButton(text="Apply", action=[Function(QuickMenuApply, tempQuickMenuOrder), Hide("quick_menu_settings")])
                use ON_TextButton(text="Cancel", action=Hide("quick_menu_settings"))
    if GetFocusRect("quickChoice"):
        dismiss:
            action [SetScreenVariable("quickPop", ""), SetScreenVariable("quickTarget", ""), ClearFocus("quickChoice")]
            alt "Dismiss " + quickTarget + " button prompt"
        nearrect:
            focus "quickChoice"
            prefer_top True
            frame:
                modal True
                has vbox
                if renpy.variant("small"):
                    spacing 34
                if quickPop == "Used":
                    textbutton _("Sort"):
                        action [QuickButtonAction(tempQuickMenuOrder, "quickChoice", quickTarget, "Sort")]
                        alt "Sort " + quickTarget + " button"

                    textbutton _("Remove"):
                        action [QuickButtonAction(tempQuickMenuOrder, "quickChoice", quickTarget, "Remove")]
                        alt "Remove " + quickTarget + " button"
                elif quickPop == "Unused":
                    textbutton _("Add"):
                        action [QuickButtonAction(tempQuickMenuOrder, "quickChoice", quickTarget, "Add")]
                        alt "Add " + quickTarget + " button"
                elif quickPop == "Visibility":
                    textbutton _("Always On"):
                        action [
                        SetVariable("persistent.quickMenuVisibility", "Always On"),
                        SetScreenVariable("quickPop", ""), ClearFocus("quickChoice")]
                        alt "Set to Always On visibility"
                    textbutton _("Toggle"):
                        action [
                        SetVariable("persistent.quickMenuVisibility", "Toggle"),
                        SetScreenVariable("quickPop", ""), ClearFocus("quickChoice")]
                        alt "Set to Toggle visibility"
                    if not renpy.variant("touch"):
                        textbutton _("Hover"):
                            action [
                            SetVariable("persistent.quickMenuVisibility", "Hover"),
                            SetScreenVariable("quickPop", ""), ClearFocus("quickChoice")]
                            alt "Set to Hover visibility (not compatible with keyboard navigation)"

## Difficulty screen ##############################################################

screen difficulty_info():
    modal True
    zorder 300
    style_prefix "confirm"
    add "gui/overlay/confirm.png"
    key "dismiss" action Hide("difficulty_info")
    key "game_menu" action Hide("difficulty_info")
    frame:
        padding (50, 50, 50, 300)
        xsize 1440
        ysize 1000
        vbox:
            text "Easy Changes" xalign 0.5
            text "- Higher starting stats."
            text "- Fully restore spirit, energy, and arousal on level ups."
            text "- Energy costs to auto pass failed checks is reduced by 25%."
            text "- Item and Eros drops rates are increased by 25%."
            text "- Gain 20% more exp."
            text "- On rest regain 1 use of Goddess' Favor."
            text ""
            text "Hard Changes" xalign 0.5
            text "- Lower starting stats."
            text "- Monsters no longer give you a grace period for stance moves, meaning group fights can lead to you getting swarmed much more rapidly."
            text "- Using an escape skill now only gives you a grace period for the remainder of the turn instead of 2 turns."
            text "- When charmed, escape skills have their odds cut down by 75% instead of 50%."
            text "- When charmed, temptation checks have their difficulty increased by 5 instead of 1."
            text "- Sleep drains 25% more energy from the player."
            text "- Paralysis' energy cost amplication is 50% higher."
            text "- Energy costs to auto pass failed checks is increased by 25%."
            text "- The minimum possible cost to auto pass a check is 25 instead of 10."
            text "- Start with 1 less Goddess' Favor."
            text "- Strain recovered on resting reduced to 25."
