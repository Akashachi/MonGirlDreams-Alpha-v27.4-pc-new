init offset = -1

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigationMain():

    vbox:
        style_prefix "navigation"

        xalign 0.5
        yalign 0.64

        if main_menu:
            textbutton _("Start New Game") action Start()

        else:
            textbutton _("Save") action ShowMenu("save")

        textbutton _("Load Game") action ShowMenu("load")

        textbutton _("Options") action ShowMenu("options")

        if not main_menu:
            textbutton _("History") action ShowMenu("history")

        if main_menu:
            textbutton _("Credits") action ShowMenu("credits")

        textbutton _("Links") action ShowMenu("links")

        if renpy.variant("pc"):
            textbutton _("Mods") action ShowMenu("mods")

        textbutton _("Controls") action ShowMenu("controls")


        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Main Menu") action MainMenu()

        if renpy.variant("pc"):

            ## The quit button is banned on iOS and unnecessary on Android.
            textbutton _("Quit") action Quit(confirm=not main_menu)


style navigation_button:
    is gui_button
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    is gui_button_text
    properties gui.button_text_properties("navigation_button")

screen navigation():
    fixed:
        style_prefix "navigation"

        xpos gui.navigation_xpos-35
        ypos 320 # moved down from 0.5 to fit backdrop animation
        xsize 280
        ysize 456

        vbox:
            xpos 25

            if not main_menu:
                textbutton _("Character") action [ShowMenu("ON_CharacterDisplayScreen"), Function(cmenu_resetMenu)] text_xalign 0

                textbutton _("Save") action ShowMenu("save") text_xalign 0

            textbutton _("Load") action If(persistent.genModData, true=Show("confirmModLoad"), false=ShowMenu("load")) text_xalign 0

            textbutton _("Options") action If(persistent.genModData, true=Show("confirmModLoad"), false=ShowMenu("options")) text_xalign 0

            if not main_menu:
                textbutton _("History") action ShowMenu("history") text_xalign 0

            if _in_replay:
                textbutton _("End Replay") action EndReplay(confirm=True) text_xalign 0

            textbutton _("Credits") action If(persistent.genModData, true=Show("confirmModLoad"), false=ShowMenu("credits")) text_xalign 0

            textbutton _("Links") action If(persistent.genModData, true=Show("confirmModLoad"), false=ShowMenu("links")) text_xalign 0

            if renpy.variant("pc"):
                if main_menu:
                    textbutton _("Mods") action ShowMenu("mods") text_xalign 0
                textbutton _("Controls") action If(persistent.genModData, true=Show("confirmModLoad"), false=ShowMenu("controls")) text_xalign 0

            if not main_menu:
                textbutton _("Main Menu") action MainMenu() text_xalign 0

            if renpy.variant("pc"):
                ## The quit button is banned on iOS and unnecessary on Android.
                textbutton _("Quit") action Quit(confirm=not main_menu) text_xalign 0


style navigation_button:
    is gui_button
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    is gui_button_text
    properties gui.button_text_properties("navigation_button")

## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    ## This ensures that any other menu screen is replaced.
    tag menu

    style_prefix "main_menu"

    ## This empty frame darkens the main menu.
    frame:
        pass

    if gui.show_name:

        use menu_background(mainMenu=True) # backdrop animation from on_menububblescreen.rpy

        text "Monster Girl Dreams":
            style "main_menu_title"
            xalign 0.5
            ypos 40
        fixed:
            xalign 0.5 ypos 100
            ymaximum 200 xmaximum 600
            text "[randomMenuLine]" xalign 0.5 textalign 0.5

        #vbox:
            #text "[config.name!t]":

            #text "[config.version]":
            #    style "main_menu_version"

    use navigationMain


style main_menu_frame:
    is empty
    xsize 280
    yfill True

style main_menu_vbox:
    is vbox
    xalign 0.5
    #xoffset -20
    xmaximum 800
    yalign 0.05
    #yoffset -20

style main_menu_text:
    is gui_text
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    is main_menu_text
    properties gui.text_properties("title")

style main_menu_version:
    is main_menu_text
    properties gui.text_properties("version")

## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid". When
## this screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None):

    style_prefix "game_menu"
    use menu_background # backdrop animation replaces game_menu.png and/or main_menu.png

    frame:
        style "game_menu_outer_frame"
        hbox:
            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        side_yfill True

                        vbox:
                            transclude
                elif scroll == "viewportHistory":
                    viewport:
                        yinitial 1.0
                        side_yfill True

                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        vbox:
                            transclude

                elif scroll == "vpgrid":
                    vpgrid:
                        yinitial 1.0
                        side_yfill True
                        cols 1

                        scrollbars "vertical"
                        mousewheel True
                        draggable True

                        transclude
                else:
                    transclude

    use navigation

    textbutton _("Return"):
        style "return_button"
        text_xalign 0
        action If(persistent.genModData, true=Show("confirmModLoad"), false=Return())

    label title xoffset 350 yoffset -10

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame:
    is empty
    bottom_padding 30
    top_padding 80

style game_menu_navigation_frame:
    is empty
    xsize 400
    yfill True

style game_menu_content_frame is empty:
    left_margin 20
    right_margin 20

style game_menu_viewport is gui_viewport:
    xsize 1440

style game_menu_vscrollbar is gui_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side is gui_side:
    spacing 10

style game_menu_label is gui_label:
    xpos 50
    ysize 120

style game_menu_label_text is gui_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button is navigation_button:
    xpos gui.navigation_xpos-10
    yalign 0.98
    yoffset -10

style return_button_text is navigation_button_text

## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():
    $ _game_menu_screen = "save"

    tag menu

    use file_slots(_("Save"))

screen load():
    $ _game_menu_screen = "load"

    tag menu

    use file_slots(_("Load"))

screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True
            ## The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value
            
            if config.has_sync:
                if CurrentScreenName() == "save":
                    if persistent.informedSync:
                        textbutton _("Upload Sync"):
                            action UploadSync()
                            xalign 0.92
                            yalign 0.015
                    else:
                        textbutton _("Upload Sync"):
                            action Show("sync_inform", fileMenuType="save")
                            xalign 0.92
                            yalign 0.015
                else:
                    if persistent.informedSync:
                        textbutton _("Download Sync"):
                            action DownloadSync()
                            xalign 0.92
                            yalign 0.015
                    else:
                        textbutton _("Download Sync"):
                            action Show("sync_inform", fileMenuType="load")
                            xalign 0.92
                            yalign 0.015
            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    if renpy.mobile:
                        button:
                            if isDeletingSave:
                                action FileDelete(slot)
                            elif not main_menu and FileLoadable(slot):
                                if renpy.get_screen("save"):
                                    action Show("file_prompt", fileMenu="save", slot=slot)
                                elif renpy.get_screen("load"):
                                    action Show("file_prompt", fileMenu="load", slot=slot)
                            else:
                                action FileAction(slot)

                            has vbox

                            add FileScreenshot(slot) xalign 0.5

                            if FileJson(slot, "UsableSaveName") and FileJson(slot, "UsableSaveName") != "":
                                text FileJson(slot, "UsableSaveName") style "slot_name_text"
                            else:
                                text FileSaveName(slot) style "slot_name_text"

                            text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                                style "slot_time_text"
                    else:
                        button:
                            if not main_menu and FileLoadable(slot):
                                if renpy.get_screen("save"):
                                    action Show("file_prompt", fileMenu="save", slot=slot)
                                elif renpy.get_screen("load"):
                                    action Show("file_prompt", fileMenu="load", slot=slot)
                            else:
                                action FileAction(slot)

                            has vbox

                            add FileScreenshot(slot) xalign 0.5
                            
                            if FileJson(slot, "UsableSaveName") and FileJson(slot, "UsableSaveName") != "":
                                text FileJson(slot, "UsableSaveName") style "slot_name_text"
                            else:
                                text FileSaveName(slot) style "slot_name_text"

                            text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                                style "slot_time_text"

                            key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            hbox:
                style_prefix "page"

                xalign 0.5
                spacing gui.page_spacing

                if main_menu:
                    yalign 1.0
                else:
                    yalign 1.05

                if renpy.mobile and not isDeletingSave:
                    textbutton _("Delete") action [If(isDeletingSave, true=[SetVariable("isDeletingSave", False)], false=[SetVariable("isDeletingSave", True)])]
                if isDeletingSave:
                    textbutton _("{color=#E470B2}Delete{/color}") action [If(isDeletingSave, true=[SetVariable("isDeletingSave", False)], false=[SetVariable("isDeletingSave", True)])]

                textbutton _("<") action FilePagePrevious()

                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action FilePage("quick")

                ## range(1, 10) gives the numbers from 1 to 9.
                if renpy.mobile:
                    for page in range(1, 16):
                        textbutton "[page]" action FilePage(page)
                else:
                    for page in range(1, 21):
                        textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()
                if not main_menu:
                    textbutton _("Rename\nSave") action Show("rename_save_prompt", slot=slot) yoffset -20
    on "replaced" action SetVariable("isDeletingSave", False)
    on "hide" action SetVariable("isDeletingSave", False)

screen sync_inform(fileMenuType):
    modal True
    zorder 300
    style_prefix "confirm"
    add Solid("#00000099")

    frame:
        padding (50, 50, 50, 200)
        xsize 1200
        ysize 720
        vbox:
            first_spacing 20
            xalign 0.5
            label _("Save Syncing") xalign 0.5
            text "This feature temporarily uploads all of your saves to the {a=https://sync.renpy.org/}Ren'Py Sync Server{/a}. This enables transfering saves across devices, including between desktop and mobile."
            text ""
            text "You upload your save via the 'Upload Sync' button from the in-game save menu. It provides a temporary 11 character code you should write down or screenshot. Then, go to the loading screen, and press 'Download Sync' to input your code."
            text ""
            text "This will not remove new saves made in untouched slots since last sync, but it will overwrite saves located on the same slots."
            text ""
            text "The feature and what it does with your saves is handled and maintained independently from this game and its creator. See the above link for more more privacy information."
    
    if fileMenuType == "save":
        key ["game_menu", "dismiss"] action [SetVariable("persistent.informedSync", True), Hide("sync_inform"), UploadSync()]
    else:
        key ["game_menu", "dismiss"] action [SetVariable("persistent.informedSync", True), Hide("sync_inform"), DownloadSync()]

screen file_prompt(fileMenu, slot):
    modal True
    zorder 300
    style_prefix "confirm"
    add Solid("#00000099")
    default fileMessage = ""

    frame:
        xminimum 1000
        xmaximum 1000
        yminimum 300
        ymaximum 300
        if fileMenu == "save":
            $ fileMessage = "Are you sure you want to overwrite your save?"
        elif fileMenu == "load":
            $ fileMessage = "Loading will lose unsaved progress. Are you sure you want to do this?"
        label _(fileMessage):
            style "confirm_prompt"
            xalign 0.5
            yalign 0.1

        fixed: ##Return button
            xalign 0.15
            yalign 1.0
            xsize 324
            ysize 81
            if fileMenu == "save":
                use ON_TextButton(text="Overwrite", action=[Hide("file_prompt"), FileSave(slot, confirm=False)])
            elif fileMenu == "load":
                use ON_TextButton(text="Load", action=[Hide("file_prompt"),  Function(SaveInteraction, saveNameStinky), FileLoad(slot, confirm=False)])


        fixed: ##Return button
            xalign 0.85
            yalign 1.0
            xsize 324
            ysize 81
            use ON_TextButton(text="Cancel", action=[Hide("file_prompt")])


    ## Right-click and escape answer "no".
    key "game_menu" action Hide("file_prompt")

init:
    default persistent.informedSync = False
    if persistent.informedSync == True:
        $ persistent.informedSync = False

init python:

    isDeletingSave = False
    saveNameStinky = ""
    def jsoncallbacksavestinky(d):
        d["UsableSaveName"] = saveNameStinky
    config.save_json_callbacks.append(jsoncallbacksavestinky)

    class SaveInteraction(Action):
        def __init__(self, d):
            self.d = d
        def __call__(self):
            global saveNameStinky
            renpy.retain_after_load()
            saveNameStinky = self.d
            renpy.restart_interaction()

screen rename_save_prompt(slot):
    
    modal True
    zorder 300
    style_prefix "confirm"
    add "gui/overlay/confirm.png"
    if FileJson(slot, "UsableSaveName") and FileJson(slot, "UsableSaveName") != "":
        default saveName = FileJson(slot, "UsableSaveName")
    else:
        default saveName = FileSaveName(slot)
    key "dismiss" action [Hide("rename_save_prompt")]
    key "game_menu" action [Hide("rename_save_prompt")]
    if renpy.variant("touch"):
        frame:
            default saveNameAfter = saveName
            xminimum 1000
            xmaximum 1000
            yminimum 400
            ymaximum 400
            yalign 0.0
            vbox:
                yalign 1.0
                spacing 5
                frame:
                    xminimum 900
                    xmaximum 900
                    input default "" copypaste True length 40 exclude "{}[]" value ScreenVariableInputValue("saveNameAfter") size 24
                if saveNameAfter == saveName:
                    text "Save name not yet set.\n Use text box below." text_align 0.5 xalign 0.5
                else:
                    text "Saves will be named:\n [saveNameAfter]" text_align 0.5 xalign 0.5
            fixed:
                xalign 0.15
                yalign 0.0
                yoffset 0
                xsize 324
                ysize 81
                use ON_TextButton(text="Confirm", action=[Hide("rename_save_prompt"), SaveInteraction(saveNameAfter)])
            
            fixed:
                xalign 0.85
                yalign 0.0
                xsize 324
                ysize 81
                use ON_TextButton(text="Cancel", action=[Hide("rename_save_prompt")])

    else:
        frame:
            default saveNameAfter = saveName
            xminimum 1000
            xmaximum 1000
            yminimum 400
            ymaximum 400
            vbox:
                yalign 0.1
                spacing 50
                if saveNameAfter == saveName:
                    text "Save name not yet set.\n Use text box below." text_align 0.5 xalign 0.5
                else:
                    text "Saves will be named:\n [saveNameAfter]" text_align 0.5 xalign 0.5
                frame:
                    xminimum 900
                    xmaximum 900
                    input default "" copypaste True length 40 exclude "{}[]" value ScreenVariableInputValue("saveNameAfter") size 24
                
            fixed:
                xalign 0.15
                yalign 1.0
                yoffset 0
                xsize 324
                ysize 81
                use ON_TextButton(text="Confirm", action=[Hide("rename_save_prompt"), SaveInteraction(saveNameAfter)])
            
            fixed:
                xalign 0.85
                yalign 1.0
                xsize 324
                ysize 81
                use ON_TextButton(text="Cancel", action=[Hide("rename_save_prompt")])


style page_label is gui_label:
    xpadding 50
    ypadding 3

style page_label_text is gui_label_text:
    text_align 1.0
    layout "subtitle"
    hover_color gui.hover_color

style page_button is gui_button:
    properties gui.button_properties("page_button")

style page_button_text is gui_button_text:
    properties gui.button_text_properties("page_button")

style slot_button is gui_button:
    properties gui.button_properties("slot_button")

style slot_button_text is gui_button_text:
    properties gui.button_text_properties("slot_button")

style slot_time_text is slot_button_text

style slot_name_text is slot_button_text

## Options screen ##########################################################
##
## The Options screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#Options

screen options():
    $ _game_menu_screen = "options"

    tag menu

    if renpy.mobile:
        $ cols = 2
    else:
        $ cols = 6

    use game_menu(_("Options"), scroll="viewport"):
        vbox:
            first_spacing 50
            spacing 100
            hbox:
                spacing 50
                box_wrap True
                if renpy.variant("pc"):
                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("1280 x 720") action Preference("display", 0.666666666667)
                        textbutton _("1600 x 900") action Preference("display", 0.83333333333)
                        textbutton _("1920 x 1080") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")
                vbox:
                    style_prefix "check"
                    label _("Skip") 
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))
                vbox:
                    label _("Visual")
                    style_prefix "check"

                    textbutton _("Character Images") action ToggleVariable("persistent.showCharacterImages", true_value=True, false_value=False)
                    textbutton _("Card Bubbles") action ToggleVariable("persistent.showCardBubbles", true_value=True, false_value=False)
                    textbutton _("VFX") action ToggleVariable("persistent.showVFX", true_value=True, false_value=False)
                vbox:
                    label _("")
                    xoffset -30
                    style_prefix "check"
                    textbutton _("Animated UI") action ToggleVariable("persistent.animatedUI", true_value=True, false_value=False)
            vbox:
                hbox:
                    spacing 50
                    box_wrap True
                    textbutton _("Quick Menu Settings") action [Show("quick_menu_settings")]
                    if main_menu:
                        if not renpy.android:
                            textbutton _("Debug Game Data On Startup") action ToggleVariable("persistent.validatorAtStartup", true_value=True, false_value=False) style "check_button"
                    if not main_menu:
                        vbox:
                            textbutton _("Player Appearance") action [Jump("AppearanceCreator"),  SensitiveIf(InventoryAvailable)]
                        vbox:
                            textbutton _("Update Save") action [Jump("reloadDatabase"),  SensitiveIf(InventoryAvailable)]

            hbox:
                style_prefix "slider"

                vbox:

                    label _("Text Speed")

                    bar value Preference("text speed")

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                vbox:
                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Sound Effect Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    #if config.has_voice:
                    #    label _("Voice Volume")

                    #    hbox:
                    #        bar value Preference("voice volume")

                    #        if config.sample_voice:
                    #            textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "check_button"

label reloadDatabase:
    $ renpy.retain_after_load()
    $ CurrentVersion = config.version
    $ loadingDatabaseType = 1
    hide screen CharacterDialogueScreen
    $ npcProgHolder = copy.deepcopy(ProgressNPC)
    $ eventProgHolder = copy.deepcopy(ProgressEvent)
    $ advenProgHolder = copy.deepcopy(ProgressAdventure)
    $ MenuLineSceneCheckMark = -1
    $ runAndStayInEvent = 0
    $ victoryScene = 0
    $ inChurch = 0

    $ player.Update()

    $ cmenu_columns = []
    $ cmenu_breadcrumb = []
    python:
        try:
            persistantMonSetData
        except:
            persistantMonSetData = []
    $ persistantMonSetData = persistantMonSetData

    call uncapStats from _call_uncapStats_1

    $ ProgressNPC = []
    $ ProgressEvent = []
    $ ProgressAdventure = []
    call loadDatabase from _call_loadDatabase_1
    $ npcProgHolder = []
    $ eventProgHolder = []
    $ advenProgHolder = []


    if len(FetishList) > len(TempFetishes):
        $ holdFetish = copy.deepcopy(TempFetishes)
        $ TempFetishes = copy.deepcopy(FetishList)
        python:
            for tempFet in TempFetishes:
                for pastFet in holdFetish:
                    if tempFet.name == pastFet.name:
                        tempFet.Level = pastFet.Level


    if rehauled == 0: #this is solely for updating saves to v23, and can be deleted later.
        "As you walk around town, you find a small silver ticket on the ground. It seems like you got a Guild Approved respec ticket!"
        $ player.inventory.give("Respec Ticket", amount)
        python:
            perkHolder = copy.deepcopy(player.perks)
            for eachNew in perkHolder:
                player.giveOrTakePerk(eachNew.name, -1)
            i = 0
            for each in player.FetishList:

                player.FetishList[i].Level = player.FetishList[i].Level*10 - 5
                if player.FetishList[i].Level <= 0:
                    player.FetishList[i].Level = 0

                TempFetishes[i].Level = TempFetishes[i].Level*10
                if TempFetishes[i].Level <= 0:
                    TempFetishes[i].Level = 0
                i+=1

            for eachNew in perkHolder:
                player.giveOrTakePerk(eachNew.name, 1)

    if progressionBoost == 0: #this is solely for updating saves to v23.9, and can be deleted later.
        $ progressionBoost = 1
        $ player.statPoints += copy.deepcopy(player.stats.lvl) - 1
        $ display = "Gained " + str(player.stats.lvl - 1) + " stat points!"
        "[display!i]"

        if player.stats.lvl >= 5:
            $ player.perkPoints += 1
            $ perkIncreases += 1

        if player.stats.lvl >= 10:
            $ player.perkPoints += 2
            $ perkIncreases += 2

        if player.stats.lvl >= 20:
            $ player.perkPoints += 2
            $ perkIncreases += 2
        $ display = "Gained " + str(perkIncreases) + " perk points!"
        "[display!i]"

        "As you walk around town, you find a small silver ticket on the ground. It seems like you got a Guild Approved respec ticket!"
        $ player.inventory.give("Respec Ticket", amount)

    $ progressionBoost = 1
    $ rehauled = 1
    $ player.CalculateStatBoost()
    "Save updated!"

    #$ _game_menu_screen="Options"
    #call _game_menu from _call__game_menu_1
    jump exitCombatFunction

label AutoReloadDatabase:
    $ CurrentVersion = config.version
    $ loadingDatabaseType = 1

    $ npcProgHolder = copy.deepcopy(ProgressNPC)
    $ eventProgHolder = copy.deepcopy(ProgressEvent)
    $ advenProgHolder = copy.deepcopy(ProgressAdventure)
    hide screen CharacterDialogueScreen

    $ cmenu_columns = []
    $ cmenu_breadcrumb = []
    python:
        try:
            persistantMonSetData
        except:
            persistantMonSetData = []
    $ persistantMonSetData = persistantMonSetData

    $ player.Update()

    call uncapStats from _call_uncapStats_2

    $ ProgressNPC = []
    $ ProgressEvent = []
    $ ProgressAdventure = []
    call loadDatabase from _call_loadDatabase_3
    $ npcProgHolder = []
    $ eventProgHolder = []
    $ advenProgHolder = []


    if len(FetishList) > len(TempFetishes):
        $ holdFetish = copy.deepcopy(TempFetishes)
        $ TempFetishes = copy.deepcopy(FetishList)
        python:
            for tempFet in TempFetishes:
                for pastFet in holdFetish:
                    if tempFet.name == pastFet.name:
                        tempFet.Level = pastFet.Level

    if checkCapitalProgress == 0:
        $ hasThing = 0
        python:
            for item in player.inventory.items:
                if item.name == "Slime Badge":
                    hasThing = 1
        if hasThing == 1:
            $ AdvLocation = getFromName("Proceed to the Capital", ProgressAdventure)
            $ ProgressAdventure[AdvLocation].questComplete = 1
        $ checkCapitalProgress = 1

    if rehauled == 0: #this is solely for updating saves to v23, and can be deleted later.
        "You find a small silver ticket on the ground. It seems like you got a Guild Approved respec ticket!"
        $ player.inventory.give("Respec Ticket", amount)
        python:
            perkHolder = copy.deepcopy(player.perks)
            for eachNew in perkHolder:
                player.giveOrTakePerk(eachNew.name, -1)
            i = 0
            for each in player.FetishList:
                player.FetishList[i].Level = player.FetishList[i].Level*10 - 5
                if player.FetishList[i].Level <= 0:
                    player.FetishList[i].Level = 0

                TempFetishes[i].Level = TempFetishes[i].Level*10
                if TempFetishes[i].Level <= 0:
                    TempFetishes[i].Level = 0
                i+=1

            for eachNew in perkHolder:
                player.giveOrTakePerk(eachNew.name, 1)

    if progressionBoost == 0: #this is solely for updating saves to v23.9, and can be deleted later.
        $ progressionBoost = 1
        $ player.statPoints += copy.deepcopy(player.stats.lvl) - 1
        $ display = "Gained " + str(player.stats.lvl - 1) + " stat points!"
        "[display!i]"

        if player.stats.lvl >= 5:
            $ player.perkPoints += 1
            $ perkIncreases += 1

        if player.stats.lvl >= 10:
            $ player.perkPoints += 2
            $ perkIncreases += 2

        if player.stats.lvl >= 20:
            $ player.perkPoints += 2
            $ perkIncreases += 2
        $ display = "Gained " + str(perkIncreases) + " perk points!"
        "[display!i]"

        "You find a small silver ticket on the ground. It seems like you got a Guild Approved respec ticket!"
        $ player.inventory.give("Respec Ticket", amount)

    $ player.CalculateStatBoost()
    $ rehauled = 1
    $ progressionBoost = 1

    #$ _game_menu_screen="Options"
    #call _game_menu from _call__game_menu_1
    jump exitCombatFunction

label checkData:
    $ needToUpdate = 0
    python:
        #try:
        #    CurrentVersion
        #except NameError:
        #    needToUpdate = 1
        #    CurrentVersion = config.version
        #else:
        #    if CurrentVersion != config.version:
        #        needToUpdate = 1
        #        CurrentVersion = config.version
        UpdatedGameCheck = len(SkillsDatabase) + len(ItemDatabase) + len(MonsterDatabase) + len(PerkDatabase) + len(LocationDatabase) + len(EventDatabase) + len(AdventureDatabase)

        try:
            CurrentIteration
        except NameError:
            needToUpdate = 1
            CurrentIteration = copy.deepcopy(UpdatedGameCheck)

    if CurrentIteration != UpdatedGameCheck:
        $ needToUpdate = 1
        $ CurrentIteration = copy.deepcopy(UpdatedGameCheck)


    if needToUpdate == 1 or CurrentVersion != config.version:
        $ CurrentVersion = config.version
        call AutoReloadDatabase from _call_AutoReloadDatabase

    jump exitCombatFunction

style slider_pref_vbox is vbox:
    xsize 225

## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewportHistory")):

        style_prefix "history"

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"

                        ## Take the color of the who text from the Character, if
                        ## set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                text h.what + "\n"

        if not _history_list:
            label _("The dialogue history is empty.")


style history_window is empty:
    xfill True
    ysize gui.history_height

style history_name is gui_label:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text is gui_label_text:
    min_width gui.history_name_width
    text_align gui.history_name_xalign

style history_text is gui_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label is gui_label:
    xfill True

style history_label_text is gui_label_text:
    xalign 0.5

## Links screen ##############################################################

screen links():
    $ _game_menu_screen = "links"

    tag menu

    use game_menu(_("Links"), scroll="viewport"):

        if renpy.variant("mobile"):
            vbox:
                text "Tap twice to open a link!"
                text ""
        elif renpy.variant("pc"):
            vbox:
                text "Use {i}ctrl{/i} + {i}click{/i} to open links!"
                text ""
        hbox:
            xalign 0.5
            label "{a=https://monstergirldreams.miraheze.org/wiki/Monster_Girl_Dreams_Wiki}Game Wiki{/a}"
        hbox:
            xalign 0.5
            text "Contains walkthroughs and general game information.{b} Caution of spoilers{/b}."
        text ""
        hbox:
            xalign 0.5
            label "{a=https://discord.com/invite/Md5n5KJ}Discord{/a}"
        hbox:
            text "Features a range of channels from game help, bug and typo reporting, and just socializing with other MGD fans."
        text ""
        hbox:
            xalign 0.5
            label "{a=https://monstergirldreams.blogspot.com}Game Blog{/a}"
        hbox:
            xalign 0.5
            text "Contains the most detailed archive of game changelogs."
        text ""
        hbox:
            xalign 0.5
            label "{a=https://twitter.com/ThresholdMGD}Threshold's Twitter{/a}"
        hbox:
            xalign 0.5
            text "Tweets related to the game and occasionally personal developer notes."

style links_label is gui_label

style links_label_text is gui_label_text:
    size gui.label_text_size

style links_text is gui_text

## Controls screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen controls():
    $ _game_menu_screen = "controls"

    tag menu

    default device = "keyboard"

    use game_menu(_("Controls"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 15

            hbox:

                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help

screen keyboard_help():

    hbox:
        label _("Shift")
        text _("Increment leveling up, and buying/selling options by 5.")

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys, WASD")
        text _("Navigate the interface. On world map, 'Up' goes to latest location, 'Down' the town.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Delete/Del")
        text _("Delete saves in the save menu on hover with mouse/keyboard.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label "C"
        text _("Opens the character menu.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "Shift+S, Alt+S"
        text _("Takes a screenshot.")

    hbox:
        label "Shift+A"
        text _("Opens the renpy accessibility menu.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")

screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface. On world map, 'Up' goes to latest location, 'Down' the town.")

    hbox:
        label _("Start, Guide")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()


style help_button is gui_button:
    properties gui.button_properties("help_button")
    xmargin 8

style help_button_text is gui_button_text:
    properties gui.button_text_properties("help_button")

style help_label is gui_label:
    xsize 250
    right_padding 20

style help_label_text is gui_label_text:
    size gui.text_size
    xalign 1.0
    text_align 1.0

style help_text is gui_text
