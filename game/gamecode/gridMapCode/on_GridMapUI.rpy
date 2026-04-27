screen Gridmap():
    vbox:
        ypos mapy
        xpos mapx
        $ gridCoordX = 0
        $ gridCoordY = 0

        for Row in TheGrid:
            $ gridCoordX = 0
            hbox:
                for Tile in Row:
                    if playerCoord[0]+1 == gridCoordX and playerCoord[1] == gridCoordY:
                        imagebutton:
                            idle tileset[FindTileType(Tile, tileset)][1]
                            hover tileset[FindTileType(Tile, tileset)][1]
                            insensitive tileset[FindTileType(Tile, tileset)][1]
                            if playerGridCanMove == True:
                                hovered SetVariable("HoveringGrid", [gridCoordX, gridCoordY])
                                unhovered SetVariable("HoveringGrid", [-1, -1])
                                action [SensitiveIf(onGridMap==1),SensitiveIf(TheGrid!=[]),SetVariable("GridMovin", 1), Jump("GridXMovement")]
                    elif playerCoord[0]-1 == gridCoordX and playerCoord[1] == gridCoordY:
                        imagebutton:
                            idle tileset[FindTileType(Tile, tileset)][1]
                            hover tileset[FindTileType(Tile, tileset)][1]
                            insensitive tileset[FindTileType(Tile, tileset)][1]
                            if playerGridCanMove == True:
                                hovered SetVariable("HoveringGrid", [gridCoordX, gridCoordY])
                                unhovered SetVariable("HoveringGrid", [-1, -1])
                                action [SensitiveIf(onGridMap==1),SensitiveIf(TheGrid!=[]),SetVariable("GridMovin", -1), Jump("GridXMovement")]
                    elif playerCoord[0] == gridCoordX and playerCoord[1]+1 == gridCoordY:
                        imagebutton:
                            idle tileset[FindTileType(Tile, tileset)][1]
                            hover tileset[FindTileType(Tile, tileset)][1]
                            insensitive tileset[FindTileType(Tile, tileset)][1]
                            if playerGridCanMove == True:
                                hovered SetVariable("HoveringGrid", [gridCoordX, gridCoordY])
                                unhovered SetVariable("HoveringGrid", [-1, -1])
                                action [SensitiveIf(onGridMap==1),SensitiveIf(TheGrid!=[]),SetVariable("GridMovin", 1),  Jump("GridYMovement")]
                    elif playerCoord[0] == gridCoordX and playerCoord[1]-1 == gridCoordY:
                        imagebutton:
                            idle tileset[FindTileType(Tile, tileset)][1]
                            hover tileset[FindTileType(Tile, tileset)][1]
                            insensitive tileset[FindTileType(Tile, tileset)][1]
                            if playerGridCanMove == True:
                                hovered SetVariable("HoveringGrid", [gridCoordX, gridCoordY])
                                unhovered SetVariable("HoveringGrid", [-1, -1])
                                action [SensitiveIf(onGridMap==1),SensitiveIf(TheGrid!=[]),SetVariable("GridMovin", -1),  Jump("GridYMovement")]
                    else:
                        $ passSight = 1

                        python:
                            if PlayerGridSight > 0:
                                passSight = 0
                                for see in visibleGrid:
                                    if gridCoordX == see[0] and gridCoordY == see[1]:
                                        passSight = 1
                                        break

                        if passSight == 1:
                            imagebutton:
                                idle tileset[FindTileType(Tile, tileset)][1]
                                hover tileset[FindTileType(Tile, tileset)][1]
                                insensitive tileset[FindTileType(Tile, tileset)][1]
                                hovered SetVariable("HoveringGrid", [gridCoordX, gridCoordY])
                                unhovered SetVariable("HoveringGrid", [-1, -1])
                                action [SetVariable("playerGridCanMove", True)]
                        else:
                            imagebutton:
                                idle "GridMap/Void.png"
                                hover "GridMap/Void.png"
                                insensitive "GridMap/Void.png"
                                hovered SetVariable("HoveringGrid", [gridCoordX, gridCoordY])
                                unhovered SetVariable("HoveringGrid", [-1, -1])
                                action [SetVariable("playerGridCanMove", True)]

                    $ gridCoordX += 1

            $ gridCoordY += 1

screen GridHover():
    if HoveringGrid[0] >= 0 and HoveringGrid[1] >= 0:
        imagebutton:
            if (playerCoord[0] == HoveringGrid[0] and abs(playerCoord[1] - HoveringGrid[1]) == 1) or (playerCoord[1] == HoveringGrid[1] and abs(playerCoord[0] - HoveringGrid[0]) == 1):
                idle "GridMap/GridHover.png"
                hover "GridMap/GridHover.png"
                insensitive "GridMap/GridHover.png"
            else:
                idle "GridMap/GridHoverFar.png"
                hover "GridMap/GridHoverFar.png"
                insensitive "GridMap/GridHoverFar.png"
            xpos mapx + HoveringGrid[0]*GridMovement
            ypos mapy + HoveringGrid[1]*GridMovement

screen gridMoveKeys():
    if playerGridCanMove == True:
        key ["focus_left"] action [SensitiveIf(onGridMap==1),SensitiveIf(TheGrid!=[]), SetVariable("gridMoveable", 1), SetVariable("GridMovin", -1), Hide("gridMoveKeys"), Jump("GridXMovement")]
        key ["focus_right"]  action [SensitiveIf(onGridMap==1),SensitiveIf(TheGrid!=[]),SetVariable("gridMoveable", 1),SetVariable("GridMovin", 1), Hide("gridMoveKeys"), Jump("GridXMovement")]
        key ["focus_up"] action [SensitiveIf(onGridMap==1),SensitiveIf(TheGrid!=[]),SetVariable("gridMoveable", 1),SetVariable("GridMovin", -1), Hide("gridMoveKeys"), Jump("GridYMovement")]
        key ["focus_down"] action [SensitiveIf(onGridMap==1),SensitiveIf(TheGrid!=[]),SetVariable("gridMoveable", 1),SetVariable("GridMovin", 1),  Hide("gridMoveKeys"), Jump("GridYMovement")]

        key ["K_KP_ENTER", "K_RETURN", "pad_a_press", "pad_righttrigger_pos"] action [SensitiveIf(onGridMap==1), SensitiveIf(TheGrid!=[]),SetVariable("GridPXposPrior", GridPXpos),SetVariable("GridMovin", 0), SetVariable("GridPYposPrior", GridPYpos), SetVariable("GridInteracted", 2), Hide("gridMoveKeys"), Jump("GridInteract")]


screen GridmapPlayer():
    timer 0.2 action SetVariable("playerGridCanMove", True)
    if playerGridCanMove == False:
        key ["focus_left"] action NullAction()
        key ["focus_right"]  action NullAction()
        key ["focus_up"] action NullAction()
        key ["focus_down"] action NullAction()
    if playerGridCanMove == True:
        #key "button_select" action [SensitiveIf(onGridMap==1), SensitiveIf(TheGrid!=[]),SetVariable("GridPXposPrior", GridPXpos),SetVariable("GridPYposPrior", GridPYpos), SetVariable("GridInteracted", 1), Jump("GridInteract")]
        key "K_RETURN" action [SensitiveIf(onGridMap==1), SensitiveIf(TheGrid!=[]),SetVariable("GridPXposPrior", GridPXpos),SetVariable("GridMovin", 0), SetVariable("GridPYposPrior", GridPYpos), SetVariable("GridInteracted", 2), Jump("GridInteract")]
        key "K_KP_ENTER" action [SensitiveIf(onGridMap==1), SensitiveIf(TheGrid!=[]),SetVariable("GridPXposPrior", GridPXpos),SetVariable("GridMovin", 0), SetVariable("GridPYposPrior", GridPYpos), SetVariable("GridInteracted", 2), Jump("GridInteract")]
        key "pad_a_press" action [SensitiveIf(onGridMap==1), SensitiveIf(TheGrid!=[]),SetVariable("GridPXposPrior", GridPXpos),SetVariable("GridMovin", 0), SetVariable("GridPYposPrior", GridPYpos), SetVariable("GridInteracted", 2), Jump("GridInteract")]
        key "pad_righttrigger_pos" action [SensitiveIf(onGridMap==1), SensitiveIf(TheGrid!=[]),SetVariable("GridPXposPrior", GridPXpos),SetVariable("GridMovin", 0), SetVariable("GridPYposPrior", GridPYpos), SetVariable("GridInteracted", 2), Jump("GridInteract")]

    #player icon!
    fixed:
        #if CanInteractOnTile(TheGrid, playerCoord, tileset, ActiveGridNPCs)==1:
        imagebutton:
            idle playerGridIcon
            hover playerGridIcon
            insensitive playerGridIcon
            hovered SetVariable("HoveringGrid", [playerCoord[0], playerCoord[1]])
            unhovered SetVariable("HoveringGrid", [-1, -1])
            if playerGridCanMove == True:
                action [SensitiveIf(onGridMap==1), SensitiveIf(TheGrid!=[]),SetVariable("GridMovin", 0), SetVariable("GridPXposPrior", GridPXpos),SetVariable("GridPYposPrior", GridPYpos),SetVariable("GridInteracted", 1),Jump("GridInteract")]
            at playerGridmapPos
        #else:
        #    imagebutton:
        #        idle "GridMap/PlayerMapIcon.png"
        #        hover "GridMap/PlayerMapIcon.png"
        #        insensitive "GridMap/PlayerMapIcon.png"
        #        hovered SetVariable("HoveringGrid", [playerCoord[0], playerCoord[1]])
        #        unhovered SetVariable("HoveringGrid", [-1, -1])
        #        action NullAction()
        #        at playerGridmapPos


screen GridUI():
    #input_enter = [ 'K_RETURN', 'K_KP_ENTER' ],

    #player icon!
    fixed:
        xpos 1675
        ypos 324
        #if CanInteractOnTile(TheGrid, playerCoord, tileset, ActiveGridNPCs)==1:
        imagebutton:
            idle "gui/circlebuttonlarge.png"
            hover "gui/circlebuttonlarge_Hover.png"
            insensitive "gui/circlebuttonlarge_insensitive.png"
            xpos -6
            if playerGridCanMove == True:
                action [SensitiveIf(onGridMap==1), SensitiveIf(TheGrid!=[]),SetVariable("GridMovin", 0), SetVariable("GridPXposPrior", GridPXpos),SetVariable("GridPYposPrior", GridPYpos),SetVariable("GridInteracted", 1),Jump("GridInteract")]
        #else:
        #    imagebutton:
        #        idle "gui/circlebuttonlarge.png"
        #        hover "gui/circlebuttonlarge_Hover.png"
        #        insensitive "gui/circlebuttonlarge_insensitive.png"
        #        xpos -6


        imagebutton:
            idle "gui/PadButtonR_idle.png"
            hover "gui/PadButtonR_Hover.png"
            insensitive "gui/PadButtonR_idle.png"
            xpos 100
            ypos 5
            if playerGridCanMove == True:
                action [SensitiveIf(onGridMap==1),SensitiveIf(TheGrid!=[]),SetVariable("GridMovin", 1), Jump("GridXMovement")]
        imagebutton:
            idle "gui/PadButtonU_idle.png"
            hover "gui/PadButtonU_Hover.png"
            insensitive "gui/PadButtonU_idle.png"
            #xpos 100
            ypos -95
            if playerGridCanMove == True:
                action [SensitiveIf(onGridMap==1),SensitiveIf(TheGrid!=[]),SetVariable("GridMovin", -1), Jump("GridYMovement")]
        imagebutton:
            idle "gui/PadButtonL_idle.png"
            hover "gui/PadButtonL_Hover.png"
            insensitive "gui/PadButtonL_idle.png"
            xpos -100
            ypos 5
            if playerGridCanMove == True:
                action [SensitiveIf(onGridMap==1),SensitiveIf(TheGrid!=[]), SetVariable("GridMovin", -1), Jump("GridXMovement")]
        imagebutton:
            idle "gui/PadButtonD_idle.png"
            hover "gui/PadButtonD_Hover.png"
            insensitive "gui/PadButtonD_idle.png"
            #xpos 0
            ypos 105
            if playerGridCanMove == True:
                action [SensitiveIf(onGridMap==1),SensitiveIf(TheGrid!=[]),SetVariable("GridMovin", 1),  Jump("GridYMovement")]

screen GridInventory():
    if not DenyGridInventory:
        hbox:
            xalign 0.964 yalign 0.85
            textbutton _("Inventory") action ShowMenu("ON_CharacterDisplayScreen", UseTab="Inventory", UseInventoryMenuTab="Consumables")


screen GridmapNPCs():
    #input_enter = [ 'K_RETURN', 'K_KP_ENTER' ],

    #player icon!
    for each in ActiveGridNPCs:
        if each.pic != "Invisible" and each.Obstacle == 0:
            $ passSight = 1
            python:
                if PlayerGridSight > 0:
                    passSight = 0
                    for see in visibleGrid:
                        if each.coord[0] == see[0] and each.coord[1] == see[1]:
                            passSight = 1
                            break

            if passSight == 1:
                imagebutton:
                    #hovered SetVariable("ttCombat", monsterToolTip)
                    #unhovered SetVariable("ttCombat", "")
                    idle each.pic
                    hover each.pic
                    insensitive each.pic
                    #xpos mapx + each.GridposX
                    #ypos mapy + each.GridposY
                    hovered SetVariable("HoveringGrid", [each.coord[0], each.coord[1]])
                    unhovered SetVariable("HoveringGrid", [-1, -1])
                    at NPCGridmapPos(each.GridposX, each.GridposY, each.GridposXPrior, each.GridposYPrior)
                    #action NullAction()
                    #yalign 0.5
                    #xalign 0.5
                    #action SetVariable("ttCombat", ""), renpy.curry(renpy.end_interaction)(True)
                    #at characterPlacement(yMonpos, bodyY, bodyX, 0, xMonPos)
                    #xpos mapAnchor.xpos
                    #function NPCmove(mapx, mapy, each.GridposX, each.GridposY)

screen GridmapObstacles():
    #input_enter = [ 'K_RETURN', 'K_KP_ENTER' ],

    #player icon!
    for each in ActiveGridNPCs:
        if each.pic != "Invisible" and each.Obstacle == 1:
            $ passSight = 1
            python:
                if PlayerGridSight > 0:
                    passSight = 0
                    for see in visibleGrid:
                        if each.coord[0] == see[0] and each.coord[1] == see[1]:
                            passSight = 1
                            break

            if passSight == 1:
                imagebutton:
                    #hovered SetVariable("ttCombat", monsterToolTip)
                    #unhovered SetVariable("ttCombat", "")
                    idle each.pic
                    hover each.pic
                    insensitive each.pic
                    xpos mapx + each.GridposX
                    ypos mapy + each.GridposY
                    hovered SetVariable("HoveringGrid", [each.coord[0], each.coord[1]])
                    unhovered SetVariable("HoveringGrid", [-1, -1])
                    #action NullAction()
                    #yalign 0.5
                    #xalign 0.5
                    #action SetVariable("ttCombat", ""), renpy.curry(renpy.end_interaction)(True)
                    #at characterPlacement(yMonpos, bodyY, bodyX, 0, xMonPos)
                    #xpos mapAnchor.xpos
                    #function NPCmove(mapx, mapy, each.GridposX, each.GridposY)
