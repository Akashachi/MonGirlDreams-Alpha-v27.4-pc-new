
init python:
    mapInteractable = True # Used to turn the map off when bringing up a choice menu - shivan
    
    locationButtonList = []  # The index list for keyboard/pad map navigation, also updates mapTT
    def populateMapButtonList():
        global locationButtonList, player, LocationDatabase, ProgressEvent
        locationButtonList = []
        for i, loc in enumerate(LocationDatabase):
            if requiresCheck(loc.requires, loc.requiresEvent, player, ProgressEvent) >= len(loc.requires) + len(loc.requiresEvent):
                locationButtonList += [[loc.exploreTitle, i]]
    def isMapIconSelected(buttonPos, i, mapButtonIndex):
        if mapButtonIndex == None:
            return False
        if buttonPos[mapButtonIndex][1] == i:
            return True
        else:
            return False

    class locationButtonTraverse(Action):
        def __init__(self, direction, mapButtonIndex):
            self.direction = direction
            self.mapButtonIndex = mapButtonIndex
        def __call__(self):
            global locationButtonList, LocationDatabase
            mapButtonIndex = self.mapButtonIndex
            if mapButtonIndex == None:
                mapButtonIndex = 0
            if mapButtonIndex != None: # Somehow user input can outrun renpy's update process for an action.
                if self.direction == "Up":
                    mapButtonIndex = len(locationButtonList) - 1
                elif self.direction == "Down":
                    mapButtonIndex = 0
                elif self.direction == "Left":
                    if mapButtonIndex != 0:
                        mapButtonIndex -= 1
                elif self.direction == "Right":
                    if mapButtonIndex != len(locationButtonList) - 1:
                        mapButtonIndex += 1
                renpy.run(SetScreenVariable("mapButtonIndex", mapButtonIndex))
                renpy.run(SetScreenVariable("mapTT", locationButtonList[mapButtonIndex][0]))
                renpy.restart_interaction()
    
init:
    transform mapIconZoom(scalingImageSize=69):
        subpixel True
        transform_anchor True
        on hover, selected_idle:
            ease .1 zoom max(1.05, 1.01 + (690 / (scalingImageSize[0] * scalingImageSize[1]))) alpha 1.0 matrixcolor ContrastMatrix(value=1.16) * BrightnessMatrix(value=0.2)
        on idle:
            ease .1 zoom 1.0 matrixcolor ContrastMatrix(value=1.0) * BrightnessMatrix(value=0.0)
    transform mapIconZoomMinimal(scalingImageSize):
        subpixel True
        transform_anchor True
        on hover, selected_idle:
            zoom max(1.05, 1.01 + (800 / (scalingImageSize[0] * scalingImageSize[1]))) alpha 1.0 matrixcolor ContrastMatrix(value=1.16) * BrightnessMatrix(value=0.2)
        on idle:
            zoom 1.0 matrixcolor ContrastMatrix(value=1.0) * BrightnessMatrix(value=0.0)
    transform mapIconNightify():
        matrixcolor TintMatrix(Color(rgb=(0.2431, 0.3294, 0.5725)))

# World map screen on "Go Adventuring!"
screen ON_MapMenu():
    on "show" action [SetScreenVariable("mapTT", ""), populateMapButtonList()]

    default mapButtonIndex = None
    default inLocationMenu = False
    default hoveredMouse = False
    default haveRefreshed = False
    default mapTT = ""
    $ ignorebuttons = 0
    
    key "K_c" action [
        ShowMenu("ON_CharacterDisplayScreen"),
        Function(cmenu_resetMenu),
        SelectedIf(_game_menu_screen=="ON_CharacterDisplayScreen")
        ]
    if not inLocationMenu:
        key ["focus_left"] action [locationButtonTraverse("Left", mapButtonIndex)]
        key ["focus_right"]  action [locationButtonTraverse("Right", mapButtonIndex)]
        key ["focus_up"] action locationButtonTraverse("Up", mapButtonIndex)
        key ["focus_down"] action [locationButtonTraverse("Down", mapButtonIndex)]
    if mapButtonIndex == 0:
        key ["K_KP_ENTER", "K_RETURN", "pad_a_press", "pad_righttrigger_pos"] action [SetScreenVariable("inLocationMenu", True), Jump("Town")]
    elif mapButtonIndex != None:
        key ["K_KP_ENTER", "K_RETURN", "pad_a_press", "pad_righttrigger_pos"] action [SetScreenVariable("inLocationMenu", True), SetVariable("targetLocation", locationButtonList[mapButtonIndex][1]), Jump("ON_ChooseAdventure")]

    if TimeOfDay in [Dusk, Evening, Midnight, MorningNight, NoonNight, AfternoonNight]:
        add "map/mapNight.png"
    else:
        add "map/map.png"
    
    # Ensure tooltip goes away when not hovering anything also also not spamming.
    if persistent.lastInput == "Mouse" and not hoveredMouse and haveRefreshed:
        $ mapButtonIndex = None
        $ haveRefreshed = False
        $ mapTT = ""
    elif persistent.lastInput in ["Keyboard", "Pad"]:
        $ haveRefreshed = True

    $ locationsWithoutIcons = []
    $ mapIconIndices = [] # array of tuples - (0, '0', True) - (index, zorder, hasReq)
    
    if renpy.variant("touch"):
        $ ignorebuttons = 1
        for i, loc in enumerate(LocationDatabase):
            $ locationsWithoutIcons.append(i)
            $ sortedIndices = sorted(mapIconIndices, key = lambda x: x[1])
    else:
        # Determine whether each location has a map icon.
        for i, loc in enumerate(LocationDatabase):
            $ hasReq = 0
            $ hasReq = requiresCheck(loc.requires, loc.requiresEvent, player, ProgressEvent)

            $ available = hasReq >=  len(loc.requires) + len(loc.requiresEvent)

            if loc.mapIcon == "" or loc.mapIcon == "None":
                if available:
                    $ locationsWithoutIcons.append(i)
            else:
                $ mapIconIndices.append((i, loc.mapIconZorder, available))
    
    # Sort icons by zorder (e.g. draw mountain icon before forest)
    $ sortedIndices = sorted(mapIconIndices, key = lambda x: x[0])
    if ignorebuttons == 0:
        # Draw all icons in order
        for i in sortedIndices:
            $ loc = LocationDatabase[i[0]]
            $ imageSize = renpy.image_size(loc.mapIcon + ".png")
            imagebutton:
                focus_mask True
                keyboard_focus False
                xpos int(loc.mapIconXpos) ypos int(loc.mapIconYpos)
                xycenter (0.5, 0.5)
                xysize ((imageSize[0]), (imageSize[1]))
                offset ((imageSize[0]/2), (imageSize[1]/2))
                if imageSize == (1920, 1080):
                    if TimeOfDay in [Dusk, Evening, Midnight, MorningNight, NoonNight, AfternoonNight]:
                        idle loc.mapIcon + ".png" at mapIconNightify
                        hover loc.mapIcon + "_Hover.png"
                    else:
                        idle loc.mapIcon + ".png"
                        hover loc.mapIcon + "_Hover.png"
                else:
                    if persistent.animatedUI:
                        if TimeOfDay in [Dusk, Evening, Midnight, MorningNight, NoonNight, AfternoonNight]:
                            if renpy.loadable( "images/" + loc.mapIcon + "Night.png"):
                                idle loc.mapIcon + "Night.png" at mapIconZoom(scalingImageSize=imageSize)
                            else:
                                idle loc.mapIcon + ".png" at mapIconZoom(scalingImageSize=imageSize)
                        else:
                            idle loc.mapIcon + ".png" at mapIconZoom(scalingImageSize=imageSize)
                    else:
                        if TimeOfDay in [Dusk, Evening, Midnight, MorningNight, NoonNight, AfternoonNight]:
                            if renpy.loadable( "images/" + loc.mapIcon + "Night.png"):
                                idle loc.mapIcon + "Night.png" at mapIconZoomMinimal(scalingImageSize=imageSize)
                            else:
                                idle loc.mapIcon + ".png" at [mapIconZoomMinimal(scalingImageSize=imageSize), mapIconNightify]
                        else:
                            idle loc.mapIcon + ".png" at mapIconZoomMinimal(scalingImageSize=imageSize)
                if loc.name == "Town":
                    hovered [SetScreenVariable("mapTT", "Return to Town"), SetScreenVariable("hoveredMouse", True)]
                    unhovered [SetScreenVariable("mapTT", ""), SetScreenVariable("hoveredMouse", False)]
                    alt "Return to Town"
                    action [SensitiveIf(mapInteractable), SelectedIf(isMapIconSelected(locationButtonList, 0, mapButtonIndex)), SetScreenVariable("inLocationMenu", True), Hide("ON_MapMenu"), Jump("Town")]
                else:
                    hovered [SetScreenVariable("mapTT", loc.exploreTitle), SetScreenVariable("hoveredMouse", True)]
                    unhovered [SetScreenVariable("mapTT", ""), SetScreenVariable("hoveredMouse", False)]
                    alt loc.exploreTitle
                    action [SensitiveIf(mapInteractable and i[2]), SelectedIf(isMapIconSelected(locationButtonList, i[0], mapButtonIndex)), SetScreenVariable("inLocationMenu", True), SetVariable("targetLocation", i[0]), Jump("ON_ChooseAdventure")]

    # Draw generic cloud cover
    #add "map/map_clouds.png"

    # Draw cloud cover for each location with an icon that CAN'T be visited
    for each in LocationDatabase:
        if each.mapIcon != "" and each.mapIcon != "None":
            $ hasReq = 0
            $ hasReq = requiresCheck(each.requires, each.requiresEvent, player, ProgressEvent)

            $ available = hasReq >=  len(each.requires) + len(each.requiresEvent)

            if not TimeOfDay in [Dusk, Evening, Midnight, MorningNight, NoonNight, AfternoonNight]:
                if not available and each.mapClouds != "":
                    add each.mapClouds:
                        xpos int(each.mapCloudsXpos) ypos int(each.mapCloudsYpos)
            else:
                if not available and each.mapClouds != "":
                    if renpy.loadable( "images/" + each.mapClouds[:each.mapClouds.rfind('.')] + "Night" + each.mapClouds[each.mapClouds.rfind('.'):]):
                        add each.mapClouds[:each.mapClouds.rfind('.')] + "Night" + each.mapClouds[each.mapClouds.rfind('.'):]:
                            xpos int(each.mapCloudsXpos) ypos int(each.mapCloudsYpos)
                    else:
                        add each.mapClouds at mapIconNightify:
                            xpos int(each.mapCloudsXpos) ypos int(each.mapCloudsYpos)

    if mapTT:
        text "[mapTT]" xalign 0.5 yalign 0.075 size fontsize

screen ON_MapMenuButtons():
    default mapTT = ""
    $ locationsWithoutIcons = []
    $ mapIconIndices = [] # array of tuples - (index, zorder, hasReq)

    $ ignorebuttons = 0
    if renpy.variant("touch"):
        $ ignorebuttons = 1
        for i, loc in enumerate(LocationDatabase):
            $ locationsWithoutIcons.append(i)
            $ sortedIndices = sorted(mapIconIndices, key = lambda x: x[1])

    # Determine whether each location has a map icon

    for i, loc in enumerate(LocationDatabase):
        $ hasReq = 0
        $ hasReq = requiresCheck(loc.requires, loc.requiresEvent, player, ProgressEvent)

        $ available = hasReq >=  len(loc.requires) + len(loc.requiresEvent)

        if loc.mapIcon == "" or loc.mapIcon == "None":
            if available:
                $ locationsWithoutIcons.append(i)
        else:
            $ mapIconIndices.append((i, loc.mapIconZorder, available))

    # in front of clouds, draw classic list of any locations that don't have icons
    if mapInteractable:
        $ yal = 0.1

        $ locationsCount = 0

        for i in locationsWithoutIcons:
            $ loc = LocationDatabase[i]

            $ hasReq = 0
            $ hasReq = requiresCheck(loc.requires, loc.requiresEvent, player, ProgressEvent)

            $ available = hasReq >= len(loc.requires) + len(loc.requiresEvent)
            if available:
                $ locationsCount += 1

        $ mapxal = 0.5
        if locationsCount > 5:
            $ mapxal = 0.35
        if locationsCount > 10:
            $ mapxal = 0.25

        for i in locationsWithoutIcons:

            $ loc = LocationDatabase[i]

            $ hasReq = 0
            $ hasReq = requiresCheck(loc.requires, loc.requiresEvent, player, ProgressEvent)


            $ available = hasReq >= len(loc.requires) + len(loc.requiresEvent)

            if available and loc.name != "Town":
                fixed:
                    yalign yal
                    xalign mapxal
                    xsize 324
                    ysize 81
                    use ON_TextButton(text=loc.exploreTitle, action=[SetVariable("targetLocation", i), Jump("ON_ChooseAdventure")])

                if locationsCount <= 5:
                    $ yal += 0.15
                elif locationsCount <= 10:
                    if mapxal == 0.35:
                        $ mapxal = 0.65
                    elif mapxal == 0.65:
                        $ mapxal = 0.35
                        $ yal += 0.15
                elif locationsCount <= 15:
                    if mapxal == 0.25:
                        $ mapxal = 0.50
                    elif mapxal == 0.50:
                        $ mapxal = 0.75
                    elif mapxal == 0.75:
                        $ mapxal = 0.25
                        $ yal += 0.15

        if renpy.variant("touch"):
            fixed:
                yalign 0.85
                xalign 0.5
                xsize 324
                ysize 81
                use ON_TextButton(text="Return to Town", action=[Jump("Town")])

    if mapTT:
        text "[mapTT]" xalign 0.5 yalign 0.15 size fontsize


# New label so you don't go into the setup screen if you're just going to do an adventure anyway
# when a location is chosen and it has adventures available, bring up a choice menu
# Option to explore (using cards), do any adventures, or return to the map
label ON_ChooseAdventure:
    default mapTT = ""
    # reset the hovered var from the setup menu since it might still be set
    $ hoveredCard = None

    # disable the map and show the location's BG
    $ mapInteractable = False
    $ bg = changeBG(LocationDatabase[targetLocation].picture)
    if bg != "":
        show screen DisplayBG onlayer master
    window hide dissolve

    python:
        loc = LocationDatabase[targetLocation]

        hasReq = 0
        hasReq = requiresCheck(loc.FullyUnlockedBy, loc.FullyUnlockedByEvent, player, ProgressEvent)
        hasExploreReq = requiresCheck(loc.ExplorationUnlockedBy, loc.ExplorationUnlockedByEvent, player, ProgressEvent)

        availableAdventures = GetAdventureNames(loc)

    if hasReq < len(loc.FullyUnlockedBy) + len(loc.FullyUnlockedByEvent):
        # if there are any adventures for this location, give the list, sans "Explore" option
        if len(availableAdventures) > 0:
            python:
                menuItems = []

                for adventureName in availableAdventures:
                    menuItems.append((adventureName, adventureName))

                menuItems.append(("Return", "__Return"))

                selection = renpy.display_menu(menuItems) # equivalent to "menu:" statement

            if selection == "__Return":
                $ mapTT = ""
                jump Adventure # Back to map
            else:
                hide screen ON_MapMenu
                hide screen ON_MapMenuButtons
                $ currentCardName = selection # Set adventure name
                jump AdventureEmbark

        else: # not fully unlocked but no adventures to go on?! Just go back to map
            jump Adventure

    else:
        # If there are any adventures to choose, use a choice menu
        if len(availableAdventures) > 0:

            python:
                menuItems = []
                if hasExploreReq == len(loc.ExplorationUnlockedBy) + len(loc.ExplorationUnlockedByEvent):
                    menuItems.append(("Explore the " + loc.name, "__Explore"))

                for adventureName in availableAdventures:
                    menuItems.append((adventureName, adventureName))

                menuItems.append(("Return", "__Return"))

                selection = renpy.display_menu(menuItems) # equivalent to "menu:" statement

            if selection == "__Explore":
                jump AdventureSetUp
            elif selection == "__Return":
                $ mapTT = ""
                jump Adventure # Back to map
            else:
                hide screen ON_MapMenu
                hide screen ON_MapMenuButtons
                $ currentCardName = selection # Set adventure name
                jump AdventureEmbark

        # If no adventures to pick from, just go straight to the setup menu
        else:
            jump AdventureSetUp

init python:
    hoveredCard = None

    # get all available adventures for a location
    def GetAdventureNames(loc):
        availableAdventures = []

        for adventureName in loc.Adventures:
            adventureIndex = getFromName(adventureName, AdventureDatabase)

            if adventureIndex >= 0:

                adventure = AdventureDatabase[adventureIndex]
                questProgress = ProgressAdventure[adventureIndex]

                hasReq = 0

                hasReq = requiresCheck(adventure.requires, adventure.requiresEvent, player, ProgressEvent)


                if questProgress.questComplete == 1:
                    hasReq = 0

                if hasReq >= len(adventure.requires) + len(adventure.requiresEvent):
                    availableAdventures.append(adventureName)

        return availableAdventures


screen ON_AdventureSetupMenu:
    add "gui/adventurecards.png" xpos 270 ypos 0

    text LocationDatabase[targetLocation].name xpos 570 ypos 60 size fontsize
    hbox:
        xpos 592
        ypos 112
        text "Pages: "
        text str(len(monsterDeck) +len(eventDeck)) + "  (minimum: " + str(LocationDatabase[targetLocation].MinimumDeckSize) + ")":
            if len(monsterDeck) + len(eventDeck) < LocationDatabase[targetLocation].MinimumDeckSize:
                color "#ff2200"

    fixed:
        xpos 255
        ypos 105
        use ON_TextButtonMid(text="Return", action=[SetScreenVariable("mapTT", ""), Jump("Adventure")])

    vbox:
        xpos 250 ypos 205
        fixed:
            xsize 300
            ysize 75
            imagebutton:
                idle "gui/tabhoriz_idle.png"
                hover "gui/tabhoriz_hover.png"
                insensitive "gui/tabhoriz_selected.png"
                action [SensitiveIf(tabToggle != 1), SetVariable ("tabToggle", 1), SetVariable("hoveredCard", None)]
            text "Monsters:" xpos 15 yalign 0.05
            text "Pages: " + str(len(monsterDeck)) + "/" + str(LocationDatabase[targetLocation].MaximumMonsterDeck) xpos 20 yalign 0.95 size 20
        fixed:
            xsize 250
            ysize 75
            imagebutton:
                idle "gui/tabhoriz_idle.png"
                hover "gui/tabhoriz_hover.png"
                insensitive "gui/tabhoriz_selected.png"
                action [SensitiveIf(tabToggle != 2), SetVariable ("tabToggle", 2), SetVariable("hoveredCard", None)]
            text "Events:" xpos 15 yalign 0.05
            text "Pages: " + str(len(eventDeck)) + "/" + str(LocationDatabase[targetLocation].MaximumEventDeck) xpos 20 yalign 0.95 size 20
        fixed:
            xsize 250
            ysize 75
            imagebutton:
                idle "gui/tabhoriz_idle.png"
                hover "gui/tabhoriz_hover.png"
                insensitive "gui/tabhoriz_selected.png"
                action [SensitiveIf(tabToggle != 3), SetVariable ("tabToggle", 3), SetVariable("hoveredCard", None)]
            text "Quest:" xpos 15 yalign 0.05
            if QuestSlot.name == "":
                $ display = "[PlayersInput] to select!"
            else:
                $ display = QuestSlot.name
            text display xpos 30 yalign 0.90 size 20

    fixed:
        xpos 255
        ypos 442
        use ON_TextButtonMid(text="Randomize", action=[Jump("RandomizeAdventure")])

    fixed:
        xpos 255
        ypos 550
        use ON_TextButtonMid(text="Embark!", action=[SensitiveIf(len(monsterDeck) + len(eventDeck) >= LocationDatabase[targetLocation].MinimumDeckSize), Jump("shuffleExploration")])

    $ hasThing = 0
    python:
        for each in player.inventory.items:
            if each.name == "Nightmare Shard":
                hasThing = 1

    if LocationDatabase[targetLocation].nightmare == 1 or hasThing == 1:
        if nightmare == 0:
            fixed:
                xpos 255
                ypos 658
                use ON_TextButtonMid(text="Nightmare?", hovered=[SetVariable("hoveredCard", None), SetScreenVariable("mapTT", "Nightmare mode! Enemies will scale up to match your level at the start of combat! Any powerups they may do from other sources will then be stacked on top of that!")], action=[SetVariable("nightmare", 1), SetScreenVariable("mapTT", "Turn off nightmare mode?")])
        else:
            fixed:
                xpos 255
                ypos 658
                use ON_TextButtonNightmare(text="Nightmare!!!", hovered=[SetVariable("hoveredCard", None), SetScreenVariable("mapTT", "Turn off nightmare mode?")], action=[SetVariable("nightmare", 0), SetScreenVariable("mapTT", "Nightmare mode! Enemies will scale up to match your level at the start of combat! Any powerups they may do from other sources will then be stacked on top of that!")])


    $ cardSel = []
    if (tabToggle == 1):
        $ cardSel = LocationDatabase[targetLocation].Monsters
        $ currentDeck = monsterDeck
    elif tabToggle == 2:
        $ cardSel = LocationDatabase[targetLocation].Events
        $ currentDeck = eventDeck
    elif tabToggle == 3:
        $ cardSel = LocationDatabase[targetLocation].Quests
        $ currentDeck = eventDeck
    else:
        $ cardSel = []

    fixed:
        xpos 562
        ypos 232
        xsize 510
        ysize 622

        use ON_Scrollbox(""):
            for each in cardSel:

                if (tabToggle == 1):
                    $ getCurrentCard = getFromName(each, MonsterDatabase)
                    $ currentCard = MonsterDatabase[getCurrentCard]
                    $ currentMax = LocationDatabase[targetLocation].MaximumMonsterDeck
                elif tabToggle == 2:
                    $ getCurrentCard = getFromName(each, EventDatabase)
                    $ currentCard = EventDatabase[getCurrentCard]
                    $ getCurrentProgCard = getFromName(each, ProgressEvent)
                    $ currentProg = ProgressEvent[getCurrentProgCard]
                    $ currentMax = LocationDatabase[targetLocation].MaximumEventDeck
                elif tabToggle == 3:
                    $ getCurrentCard = getFromName(each, EventDatabase)
                    $ currentCard = EventDatabase[getCurrentCard]
                    $ getCurrentProgCard = getFromName(each, ProgressEvent)
                    $ currentProg = ProgressEvent[getCurrentProgCard]

                $ hasReq = 0

                $ hasReq = requiresCheck(currentCard.requires, currentCard.requiresEvent, player, ProgressEvent)


                if tabToggle == 2 or tabToggle == 3:
                    if currentProg.questComplete == 1:
                        $ hasReq = 0

                $ numberInDeck = 0
                for cycle in currentDeck:
                    if (tabToggle == 1):
                        if cycle.IDname == currentCard.IDname:
                            $ numberInDeck += 1
                    else:
                        if cycle.name == currentCard.name:
                            $ numberInDeck += 1

                if hasReq >= len(currentCard.requires) + len(currentCard.requiresEvent):

                    hbox:
                        fixed:
                            if renpy.variant("touch"):
                                ysize 75
                            else:
                                ysize 60
                            xsize 120


                            imagebutton:
                                idle "gui/ListEntryBack.png"
                                hover "gui/ListEntryBack.png"
                                yalign 0.5
                                action SetVariable("hoveredCard", currentCard), SetScreenVariable("mapTT", "")
                                hovered SetVariable("hoveredCard", currentCard), SetScreenVariable("mapTT", "")

                            if tabToggle == 3:
                                if QuestSlot.name == currentCard.name:
                                    imagebutton:
                                        idle "gui/circlebuttonsmallchecked.png"
                                        hover "gui/circlebuttonsmallchecked_hover.png"
                                        xalign 0.5
                                        yalign 0.5
                                        action SetVariable("hoveredCard", currentCard), SetVariable("currentCardName", currentCard.name), Jump("RemoveFromDeck")
                                else:
                                    imagebutton:
                                        idle "gui/circlebuttonsmall.png"
                                        hover "gui/circlebuttonsmall_hover.png"
                                        xalign 0.5
                                        yalign 0.5
                                        action SetVariable("hoveredCard", currentCard), SetVariable("currentCardName", currentCard.name), Jump("AddToDeck")

                            else:
                                if renpy.variant("touch"):
                                    $ buttonIdleImgDown = "gui/Button_dec_idle_Jumbo.png"
                                    $ buttonHoverImgDown = "gui/Button_dec_hover_Jumbo.png"
                                    $ buttonIdleImgUp = "gui/Button_inc_idle_Jumbo.png"
                                    $ buttonHoverImgUp = "gui/Button_inc_hover_Jumbo.png"
                                    hbox:
                                        if tabToggle != 1:
                                            imagebutton:
                                                idle buttonIdleImgDown
                                                hover buttonHoverImgDown
                                                xalign 0.0
                                                yalign 0.5
                                                action [SensitiveIf(numberInDeck > 0), SetVariable("hoveredCard", currentCard), SetVariable("currentCardName", currentCard.name), Jump ("RemoveFromDeck")]
                                        else:
                                            imagebutton:
                                                idle buttonIdleImgDown
                                                hover buttonHoverImgDown
                                                xalign 0.0
                                                yalign 0.5
                                                action [SensitiveIf(numberInDeck > 0), SetVariable("hoveredCard", currentCard), SetVariable("currentCardName", currentCard.IDname), Jump ("RemoveFromDeck")]

                                        if tabToggle == 1:
                                            $ numText = str(numberInDeck)
                                        else:
                                            $ numText = str(numberInDeck) + "/" + str(currentCard.CardLimit)

                                        fixed:
                                            xalign 0.5
                                            yalign 0.5
                                            #add "gui/circlebuttonlarge.png"
                                            text numText xalign 0.5 yalign 0.5

                                        $ addible = False
                                        if currentMax > len(currentDeck):
                                            if tabToggle == 2:
                                                if numberInDeck < currentCard.CardLimit:
                                                    $ addible = True
                                            else:
                                                $ addible = True

                                        if tabToggle != 1:
                                            imagebutton:
                                                idle buttonIdleImgUp
                                                hover buttonHoverImgUp
                                                xalign 1.0
                                                yalign 0.5
                                                action [SensitiveIf(addible), SetVariable("hoveredCard", currentCard), SetVariable("currentCardName", currentCard.name), Jump ("AddToDeck")]
                                        else:
                                            imagebutton:
                                                idle buttonIdleImgUp
                                                hover buttonHoverImgUp
                                                xalign 1.0
                                                yalign 0.5
                                                action [SensitiveIf(addible), SetVariable("hoveredCard", currentCard), SetVariable("currentCardName", currentCard.IDname), Jump ("AddToDeck")]
                                else:
                                    $ buttonIdleImgDown = "gui/Button_dec_idle.png"
                                    $ buttonHoverImgDown = "gui/Button_dec_hover.png"
                                    $ buttonIdleImgUp = "gui/Button_inc_idle.png"
                                    $ buttonHoverImgUp = "gui/Button_inc_hover.png"
                                    if tabToggle != 1:
                                        imagebutton:
                                            idle buttonIdleImgDown
                                            hover buttonHoverImgDown
                                            xalign 0.0
                                            yalign 0.5
                                            action [SensitiveIf(numberInDeck > 0), SetVariable("hoveredCard", currentCard), SetVariable("currentCardName", currentCard.name), Jump ("RemoveFromDeck")]
                                    else:
                                        imagebutton:
                                            idle buttonIdleImgDown
                                            hover buttonHoverImgDown
                                            xalign 0.0
                                            yalign 0.5
                                            action [SensitiveIf(numberInDeck > 0), SetVariable("hoveredCard", currentCard), SetVariable("currentCardName", currentCard.IDname), Jump ("RemoveFromDeck")]

                                    if tabToggle == 1:
                                        $ numText = str(numberInDeck)
                                    else:
                                        $ numText = str(numberInDeck) + "/" + str(currentCard.CardLimit)

                                    fixed:
                                        xalign 0.5
                                        yalign 0.5
                                        #add "gui/circlebuttonlarge.png"
                                        text numText xalign 0.5 yalign 0.5

                                    $ addible = False
                                    if currentMax > len(currentDeck):
                                        if tabToggle == 2:
                                            if numberInDeck < currentCard.CardLimit:
                                                $ addible = True
                                        else:
                                            $ addible = True

                                    if tabToggle != 1:
                                        imagebutton:
                                            idle buttonIdleImgUp
                                            hover buttonHoverImgUp
                                            xalign 1.0
                                            yalign 0.5
                                            action [SensitiveIf(addible), SetVariable("hoveredCard", currentCard), SetVariable("currentCardName", currentCard.name), Jump ("AddToDeck")]
                                    else:
                                        imagebutton:
                                            idle buttonIdleImgUp
                                            hover buttonHoverImgUp
                                            xalign 1.0
                                            yalign 0.5
                                            action [SensitiveIf(addible), SetVariable("hoveredCard", currentCard), SetVariable("currentCardName", currentCard.IDname), Jump ("AddToDeck")]

                        if tabToggle == 3:
                            text currentCard.name xpos -10 yalign 0.5 size 26
                        else:
                            if renpy.variant("touch"):
                                text currentCard.name xpos 65 yalign 0.5 size 26
                            else:
                                text currentCard.name xpos 13 yalign 0.5 size 26

    if hoveredCard is not None:
        fixed:
            xpos 1090
            ypos 232
            xsize 510
            ysize 622

            text hoveredCard.name xalign 0.5

            fixed:
                ypos 52
                ysize 555
                use ON_Scrollbox(""):
                    if (tabToggle == 1):
                        if hasattr(hoveredCard, 'encyclopedia'):
                            text hoveredCard.encyclopedia size 24
                        else:
                            text hoveredCard.description size 24
                    else:
                        text hoveredCard.description size 24
    fixed:
        xpos 1090
        ypos 232
        xsize 510
        ysize 622

        fixed:
            ypos 52
            ysize 555
            use ON_Scrollbox(""):
                if mapTT:
                    text "[mapTT]" size 24
