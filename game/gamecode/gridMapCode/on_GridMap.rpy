init python:
    def FindTileType(Tile, Tileset):
        TileType = 0
        targetFound = 0
        for each in Tileset:
            if each[0] == Tile:
                targetFound = 1
            elif targetFound == 0:
                TileType += 1
        return TileType


    def NPCmove(trans, st, at, mapx, mapy, GridposX, GridposY):
        trans.xpos = mapx + GridposX
        trans.ypos = mapy + GridposY

    def CanInteractOnTile(TheGrid, playerCoord, tileset, ActiveGridNPCs):
        Interactable = 0
        tileTarget = TheGrid[playerCoord[1]][playerCoord[0]]

        if tileset[FindTileType(tileTarget, tileset)][2] == "Interactable":
            Interactable = 1

        currentGridNPC = 0
        for each in ActiveGridNPCs:
            if each.coord == playerCoord:
                if each.NPCevent[0] == "Interactable":
                    Interactable = 1

        return Interactable

    class GridNPC(renpy.store.object):
        def __init__(self, name = "", pic = "", coord=[0,0], NPCevent = ["", "", ""], NPCMoveEvent = ["", ""], GridposX=0, GridposY=0, Movement="", MovementTarget="", MovementVector=[-1,-1], TargetCoords=[-1,-1], Obstacle=0, Wall="", Timer=-1, TimerReset=-1, TimerEvent=["", ""], JustSpawned=0, Description="", CanShareTile=True):
            self.name = name
            self.pic = pic
            self.coord = coord
            self.GridposX = GridposX
            self.GridposY = GridposY
            self.GridposXPrior = GridposX
            self.GridposYPrior = GridposY
            self.NPCevent = NPCevent
            self.NPCMoveEvent = NPCMoveEvent
            self.Movement = Movement
            self.MovementTarget = MovementTarget
            self.MovementVector = MovementVector
            self.TargetCoords = TargetCoords
            self.Obstacle = Obstacle
            self.Wall = Wall
            self.Timer = Timer
            self.TimerReset = TimerReset
            self.TimerEvent = TimerEvent
            self.JustSpawned = JustSpawned
            self.Description = Description
            self.CanShareTile = CanShareTile

init:
    $ DenyGridInventory = False
    $ tileset = []
    $ TheGrid = []
    $ TheGridNPCs = []
    $ ActiveGridNPCs = []

    $ NPCMove = 0
    $ mapTest = [
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,1,1,1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0],
[0,0,1,1,1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0],
[0,1,1,1,1,1,1,1,1,1,2,1,1,1,1,0,0,0,0,0,0],
[0,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,0,0,0,0],
[1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,0,0,0,0],
[1,1,1,1,1,2,2,2,2,2,2,2,1,1,1,1,1,0,0,0,0],
[1,1,1,1,1,2,2,2,2,2,2,2,1,1,1,1,1,1,0,0,0],
[1,1,1,1,1,2,2,2,2,2,2,2,1,1,1,1,1,1,0,0,0],
[1,1,1,1,1,2,2,2,2,2,2,2,1,1,1,1,1,1,0,0,0],
[1,1,1,1,1,1,1,2,2,2,1,1,1,1,1,1,1,0,0,0,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0]
]
    $ HoveringGrid = [-1,-1]
    $ lastPlayerMove = [0,0]
    $ GridPYpos = 0
    $ GridPXpos = 0
    $ GridPYposPrior = 0
    $ GridPXposPrior = 0
    $ startplayerpos = [0,0] #(x,y)
    $ playerCoord = startplayerpos
    $ mapx = 0
    $ mapy = 0
    $ gridYAdjust = 0
    $ GridMovement = 50
    $ GridMovin = 0
    $ tileTarget = 0
    $ onGridMap = 0
    $ gridEvent = "Interactable"
    $ gridStepLine = ""
    $ GridInteracted = 0
    $ PlayerGridSight = 0
    $ visibleGrid = []
    $ StunGridPlayer = 0
    $ stunnedGridPlayer = -1
    $ playerGridCanMove = True
    $ gridMapDethAdjuster = 0

    $ playerGridIcon = "GridMap/PlayerMapIcon.png"

    $ TileEventArray = []

    #$ config.keymap['screenshot'].remove('s')
    $ config.keymap['screenshot'].remove('noshift_K_s')
    $ config.keymap['screenshot'].append('shift_K_s')
    #$ config.keymap['accessibility'].remove('K_a')
    $ config.keymap['accessibility'].append('shift_K_a')

    #$ config.keymap['screenshot'].remove('noshift_K_s')

    transform playerGridmapPos:
        subpixel True
        xpos mapx + GridPXposPrior ypos mapy + GridPYposPrior
        ease 0.125 xpos mapx + GridPXpos ypos mapy + GridPYpos

    transform NPCGridmapPos(GridXpos, GridYpos, GridXposPrior, GridYposPrior):
        subpixel True
        xpos mapx + GridXposPrior ypos mapy + GridYposPrior
        ease 0.125 xpos mapx + GridXpos ypos mapy + GridYpos

    transform MapPos:
        subpixel True
        yalign 0.10
        xalign 0.5



label displayTileMap:
    if GridInteracted == 1:
        $ setNPCPos = 0
        while setNPCPos < len(ActiveGridNPCs):
            $ ActiveGridNPCs[setNPCPos].GridposXPrior = ActiveGridNPCs[setNPCPos].GridposX
            $ ActiveGridNPCs[setNPCPos].GridposYPrior = ActiveGridNPCs[setNPCPos].GridposY
            $ setNPCPos += 1


    $ TileEventArray = []
    $ GridInteracted = 0
    $ TileMoveComplete = 0
    $ onGridMap = 1
    $ NPCMove = 0
    #show tilemap1 at MapPos
    if TheGrid == []:
        jump postGridMap

    $ mapx = int(960 - ((len(TheGrid[0]))*50)*0.5)
    $ mapy = int((0.5*1080) - (len(TheGrid)*50)*0.76) - gridYAdjust
    $ gridEvent = "Interactable"
    #$ GridPXpos += 50
    if DenyGridInventory == True:
        $ InventoryAvailable = False
    else:
        $ InventoryAvailable = True
    $ visibleGridList = []
    $ visibleGrid = []
    if PlayerGridSight > 0:
        $ visibleGridList = gridVision(TheGrid, playerCoord, PlayerGridSight, tileset, ActiveGridNPCs)
        $ [visibleGrid.append(x) for x in visibleGridList if x not in visibleGrid]

    $ player = ClearNonPersistentEffects(player)


    show screen Gridmap
    show screen GridmapObstacles
    show screen GridmapPlayer
    show screen GridmapNPCs
    show screen GridUI
    show screen GridInventory
    show screen GridHover



    $ tileTarget = TheGrid[playerCoord[1]][playerCoord[0]]

    $ display = ""
    $ currentGridNPC = 0
    while currentGridNPC < len(ActiveGridNPCs):
        if ActiveGridNPCs[currentGridNPC].Description != "":
            if ActiveGridNPCs[currentGridNPC].Obstacle == 1:
                if ActiveGridNPCs[currentGridNPC].coord == playerCoord:
                    $ display = ActiveGridNPCs[currentGridNPC].Description
        $ currentGridNPC += 1

    if display == "":
        $ display = tileset[FindTileType(tileTarget, tileset)][5]



    #if player.statusEffects.paralysis.potency >= 1 and player.statusEffects.paralysis.duration >= 1 and paralysisIgnored == 0:

    #    if getParalysisBoost(player) >= renpy.random.randint(0, 100):
    #       $ stunnedGridPlayer = 1
    #        $ turnsStunnedByParalysis += 1
    #        $ player.statusEffects.paralysis.potency - 1
    #        "You're too paralyzed to move properly!"
    #    else:
    #        $ turnsStunnedByParalysis = 0
    #        $ paralysisIgnored = 1

    #else:
    #    $ turnsStunnedByParalysis = 0

    if stunnedGridPlayer > 0:
        $ stunnedGridPlayer -= 1
        $ GridPXposPrior = copy.copy(GridPXpos)
        $ GridPYposPrior = copy.copy(GridPYpos)
        jump GridMovement

    show screen gridMoveKeys

    $ Speaker = Character(_(''))
    if display == "":
        if gridStepLine != "":

            $ display = gridStepLine
            call read from _call_read_29
        else:
            ""
    else:
        if toggledGridEvent == 0:
            #$ onGridMap = 2
            $ LastLine = copy.copy(display)
            if gridStepLine != "" and display != "" and display != " ":
                $ gridStepLine =  gridStepLine
            $ display += " " + gridStepLine
            call read from _call_read_37
        else:
            if gridStepLine != "" and LastLine != "" and LastLine != " ":
                $ gridStepLine = gridStepLine
            $ display = copy.copy(LastLine) + " " + gridStepLine
            call read from _call_read_38

    jump displayTileMap

label postGridTextEvent:
    $ onGridMap = 1
    $ toggledGridEvent = 1
    $ GridPXposPrior = copy.copy(GridPXpos)
    $ GridPYposPrior = copy.copy(GridPYpos)
    hide screen GridmapPlayer
    #call screen track_coordinate(tilemap1)
    #"[_return]"
    $ paralysisIgnored = 0
    jump displayTileMap


label GridMovement:
    $ onGridMap = 1
    hide screen GridmapPlayer
    hide screen GridmapObstacles
    hide screen GridmapNPCs
    hide screen GridmapNPCs
    hide screen GridUI
    hide screen GridInventory
    hide screen GridHover
    hide screen gridMoveKeys
    $ NPCMove = 1

    $ EventConsister = ""
    $ EventConsisterTarget = 0


    $ specifyCurrentChoice = 0

    #SET NPC CALLS HERE FOR AI MOVEMENT
    $ currentGridNPC = 0
    $ intendedMoves = []
    while currentGridNPC < len(ActiveGridNPCs):
        if ActiveGridNPCs[currentGridNPC].Obstacle != 1:
            $ gridEvent = "Auto"
            $ AIMove = [0,0]
            $ Path = []
            $ moveTo = [ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]]
            $ ActiveGridNPCs[currentGridNPC].GridposXPrior = ActiveGridNPCs[currentGridNPC].GridposX
            $ ActiveGridNPCs[currentGridNPC].GridposYPrior = ActiveGridNPCs[currentGridNPC].GridposY
            $ delProjectile = 0
            if ActiveGridNPCs[currentGridNPC].Movement != "":
                if ActiveGridNPCs[currentGridNPC].MovementTarget == "Player":
                    $ ActiveGridNPCs[currentGridNPC].TargetCoords = (playerCoord[0], playerCoord[1])
                elif ActiveGridNPCs[currentGridNPC].MovementTarget == "TargetSet":
                    $ ActiveGridNPCs[currentGridNPC].TargetCoords = ActiveGridNPCs[currentGridNPC].TargetCoords
                elif ActiveGridNPCs[currentGridNPC].MovementTarget != "":
                    python:
                        checkingGridNPC = 0
                        locationChoiceArray = []
                        for each in ActiveGridNPCs:
                            if checkingGridNPC != currentGridNPC and each.name == ActiveGridNPCs[currentGridNPC].MovementTarget:
                                locationChoiceArray.append(each)
                            checkingGridNPC += 1
                        if len(locationChoiceArray) > 0:
                            targcoord = locationChoiceArray[renpy.random.randint(-1, len(locationChoiceArray)-1)].coord
                            ActiveGridNPCs[currentGridNPC].TargetCoords = (targcoord[0], targcoord[1])
                            ActiveGridNPCs[currentGridNPC].MovementTarget = "TargetSet"
                        else:
                            ActiveGridNPCs[currentGridNPC].TargetCoords = (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1])


                if ActiveGridNPCs[currentGridNPC].Movement == "Chase":
                    $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]), ActiveGridNPCs[currentGridNPC].TargetCoords, tileset, ActiveGridNPCs, NPCCanShareTile=ActiveGridNPCs[currentGridNPC].CanShareTile)
                elif ActiveGridNPCs[currentGridNPC].Movement == "Ambush":
                    $ positionAcceptable = 1
                    $ distanceFromPlayer = 4
                    $ AmbushX = ActiveGridNPCs[currentGridNPC].TargetCoords[0]
                    $ AmbushY = ActiveGridNPCs[currentGridNPC].TargetCoords[1]
                    while positionAcceptable != 0:
                        if positionAcceptable == 1 and distanceFromPlayer != 0:
                            if AmbushX + lastPlayerMove[0]*distanceFromPlayer < 0 or AmbushX + lastPlayerMove[0]*distanceFromPlayer > len(TheGrid[0])-1  or AmbushY + lastPlayerMove[1]*distanceFromPlayer < 0 or AmbushY + lastPlayerMove[1]*distanceFromPlayer > len(TheGrid)-1:
                                $ distanceFromPlayer -= 1
                            else:
                                $ tileTarget = TheGrid[AmbushY + lastPlayerMove[1]*distanceFromPlayer][AmbushX + lastPlayerMove[0]*distanceFromPlayer]
                                if tileset[FindTileType(tileTarget, tileset)][2] == "Wall":
                                    $ distanceFromPlayer -= 1
                                else:
                                    $ positionAcceptable = 0
                        else:
                            $ positionAcceptable = 0

                    $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]), (ActiveGridNPCs[currentGridNPC].TargetCoords[0] + lastPlayerMove[0]*distanceFromPlayer, ActiveGridNPCs[currentGridNPC].TargetCoords[1] + lastPlayerMove[1]*distanceFromPlayer), tileset, ActiveGridNPCs, NPCCanShareTile=ActiveGridNPCs[currentGridNPC].CanShareTile)
                elif ActiveGridNPCs[currentGridNPC].Movement == "Whimsical":
                    $ positionAcceptable = 1
                    $ distanceFromPlayer = 2
                    $ AmbushX = ActiveGridNPCs[currentGridNPC].TargetCoords[0]
                    $ AmbushY = ActiveGridNPCs[currentGridNPC].TargetCoords[1]

                    if ActiveGridNPCs[currentGridNPC].MovementVector[0] == -1:
                        $ ActiveGridNPCs[currentGridNPC].MovementVector=[renpy.random.randint(-ActiveGridNPCs[currentGridNPC].WhimsyRange, ActiveGridNPCs[currentGridNPC].WhimsyRange), renpy.random.randint(-ActiveGridNPCs[currentGridNPC].WhimsyRange, ActiveGridNPCs[currentGridNPC].WhimsyRange)]
                    $ WhimsyX = copy.copy(ActiveGridNPCs[currentGridNPC].MovementVector[0])
                    $ WhimsyY = copy.copy(ActiveGridNPCs[currentGridNPC].MovementVector[1])

                    while positionAcceptable != 0:
                        if positionAcceptable == 1:
                            if AmbushX + WhimsyX < 0:
                                $ WhimsyX += 1
                            elif AmbushX + WhimsyX > len(TheGrid[0])-1:
                                $ WhimsyX -= 1
                            else:
                                if AmbushY + WhimsyY < 0:
                                    $ WhimsyY += 1
                                elif AmbushY + WhimsyY > len(TheGrid)-1:
                                    $ WhimsyY -= 1
                                else:
                                    $ tileTarget = TheGrid[AmbushY + WhimsyY][AmbushX + WhimsyX]
                                    if tileset[FindTileType(tileTarget, tileset)][2] == "Wall":
                                        if WhimsyX > 0:
                                            $ WhimsyX -= 1
                                        elif WhimsyX < 0:
                                            $ WhimsyX += 1
                                        $ tileTarget = TheGrid[AmbushY + WhimsyY][AmbushX + WhimsyX]
                                        if tileset[FindTileType(tileTarget, tileset)][2] == "Wall":
                                            if WhimsyY > 0:
                                                $ WhimsyY -= 1
                                            elif WhimsyY < 0:
                                                $ WhimsyY += 1
                                        else:
                                            $ positionAcceptable = 0
                                    else:
                                        $ positionAcceptable = 0
                        else:
                            $ positionAcceptable = 0
                    $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]), (ActiveGridNPCs[currentGridNPC].TargetCoords[0] +  WhimsyX, ActiveGridNPCs[currentGridNPC].TargetCoords[1] +  WhimsyY), tileset, ActiveGridNPCs, NPCCanShareTile=ActiveGridNPCs[currentGridNPC].CanShareTile)
                elif ActiveGridNPCs[currentGridNPC].Movement == "Wander":
                    #right, left, up, down

                    $ BumpChance = 0
                    $ ranDirection = ["R", "L", "U", "D"]

                    if tileset[FindTileType(TheGrid[ActiveGridNPCs[currentGridNPC].coord[1]][ActiveGridNPCs[currentGridNPC].coord[0]+1], tileset)][2] == "Wall":
                        $ BumpChance = renpy.random.randint(1, 100)
                        if BumpChance > 20:
                            $ del ranDirection[0]

                    if tileset[FindTileType(TheGrid[ActiveGridNPCs[currentGridNPC].coord[1]][ActiveGridNPCs[currentGridNPC].coord[0]-1], tileset)][2] == "Wall":
                        $ BumpChance = renpy.random.randint(1, 100)
                        if BumpChance > 20:
                            $ del ranDirection[ranDirection.index("L")]

                    if tileset[FindTileType(TheGrid[ActiveGridNPCs[currentGridNPC].coord[1]-1][ActiveGridNPCs[currentGridNPC].coord[0]], tileset)][2] == "Wall":
                        $ BumpChance = renpy.random.randint(1, 100)
                        if BumpChance > 20:
                            $ del ranDirection[ranDirection.index("U")]

                    if tileset[FindTileType(TheGrid[ActiveGridNPCs[currentGridNPC].coord[1]+1][ActiveGridNPCs[currentGridNPC].coord[0]], tileset)][2] == "Wall":
                        $ BumpChance = renpy.random.randint(1, 100)
                        if BumpChance > 20:
                            $ del ranDirection[ranDirection.index("D")]

                    $ renpy.random.shuffle(ranDirection)

                    if ranDirection[0] == "R":
                        $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]),(ActiveGridNPCs[currentGridNPC].coord[0]+1, ActiveGridNPCs[currentGridNPC].coord[1]), tileset, ActiveGridNPCs, NPCCanShareTile=ActiveGridNPCs[currentGridNPC].CanShareTile)
                    elif ranDirection[0] == "L":
                        $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]),(ActiveGridNPCs[currentGridNPC].coord[0]-1, ActiveGridNPCs[currentGridNPC].coord[1]), tileset, ActiveGridNPCs, NPCCanShareTile=ActiveGridNPCs[currentGridNPC].CanShareTile)
                    elif ranDirection[0] == "U":
                        $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]),(ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]+1), tileset, ActiveGridNPCs, NPCCanShareTile=ActiveGridNPCs[currentGridNPC].CanShareTile)
                    elif ranDirection[0] == "D":
                        $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]),(ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]-1), tileset, ActiveGridNPCs, NPCCanShareTile=ActiveGridNPCs[currentGridNPC].CanShareTile)

                elif ActiveGridNPCs[currentGridNPC].Movement == "ProjectileRight":
                    $ tileTarget = TheGrid[ActiveGridNPCs[currentGridNPC].coord[1]][ActiveGridNPCs[currentGridNPC].coord[0]+1]

                    if lastPlayerCoord[0] == ActiveGridNPCs[currentGridNPC].coord[0]+1 and lastPlayerCoord[1] == ActiveGridNPCs[currentGridNPC].coord[1] and playerCoord[0] == ActiveGridNPCs[currentGridNPC].coord[0] and playerCoord[1] == ActiveGridNPCs[currentGridNPC].coord[1]:
                        $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]),(ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]), tileset, ActiveGridNPCs, NPCCanShareTile=ActiveGridNPCs[currentGridNPC].CanShareTile)
                    elif tileset[FindTileType(tileTarget, tileset)][2] == "Wall":
                        $ delProjectile = 1
                    else:
                        $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]),(ActiveGridNPCs[currentGridNPC].coord[0]+1, ActiveGridNPCs[currentGridNPC].coord[1]), tileset, ActiveGridNPCs, NPCCanShareTile=ActiveGridNPCs[currentGridNPC].CanShareTile)
                elif ActiveGridNPCs[currentGridNPC].Movement == "ProjectileLeft":
                    $ tileTarget = TheGrid[ActiveGridNPCs[currentGridNPC].coord[1]][ActiveGridNPCs[currentGridNPC].coord[0]-1]
                    if lastPlayerCoord[0] == ActiveGridNPCs[currentGridNPC].coord[0]-1 and lastPlayerCoord[1] == ActiveGridNPCs[currentGridNPC].coord[1] and playerCoord[0] == ActiveGridNPCs[currentGridNPC].coord[0] and playerCoord[1] == ActiveGridNPCs[currentGridNPC].coord[1]:
                        $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]),(ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]), tileset, ActiveGridNPCs, NPCCanShareTile=ActiveGridNPCs[currentGridNPC].CanShareTile)
                    elif tileset[FindTileType(tileTarget, tileset)][2] == "Wall":
                        $ delProjectile = 1
                    else:
                        $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]),(ActiveGridNPCs[currentGridNPC].coord[0]-1, ActiveGridNPCs[currentGridNPC].coord[1]), tileset, ActiveGridNPCs, NPCCanShareTile=ActiveGridNPCs[currentGridNPC].CanShareTile)
                elif ActiveGridNPCs[currentGridNPC].Movement == "ProjectileUp":
                    $ tileTarget = TheGrid[ActiveGridNPCs[currentGridNPC].coord[1]-1][ActiveGridNPCs[currentGridNPC].coord[0]]
                    if lastPlayerCoord[0] == ActiveGridNPCs[currentGridNPC].coord[0] and lastPlayerCoord[1] == ActiveGridNPCs[currentGridNPC].coord[1]-1 and playerCoord[0] == ActiveGridNPCs[currentGridNPC].coord[0] and playerCoord[1] == ActiveGridNPCs[currentGridNPC].coord[1]:
                        $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]),(ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]), tileset, ActiveGridNPCs, NPCCanShareTile=ActiveGridNPCs[currentGridNPC].CanShareTile)
                    elif tileset[FindTileType(tileTarget, tileset)][2] == "Wall":
                        $ delProjectile = 1
                    else:
                        $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]),(ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]-1), tileset, ActiveGridNPCs, NPCCanShareTile=ActiveGridNPCs[currentGridNPC].CanShareTile)
                elif ActiveGridNPCs[currentGridNPC].Movement == "ProjectileDown":
                    $ tileTarget = TheGrid[ActiveGridNPCs[currentGridNPC].coord[1]+1][ActiveGridNPCs[currentGridNPC].coord[0]]
                    if lastPlayerCoord[0] == ActiveGridNPCs[currentGridNPC].coord[0] and lastPlayerCoord[1] == ActiveGridNPCs[currentGridNPC].coord[1]+1 and playerCoord[0] == ActiveGridNPCs[currentGridNPC].coord[0] and playerCoord[1] == ActiveGridNPCs[currentGridNPC].coord[1]:
                        $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]),(ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]), tileset, ActiveGridNPCs, NPCCanShareTile=ActiveGridNPCs[currentGridNPC].CanShareTile)
                    elif tileset[FindTileType(tileTarget, tileset)][2] == "Wall":
                        $ delProjectile = 1
                    else:
                        $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]),(ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]+1), tileset, ActiveGridNPCs, NPCCanShareTile=ActiveGridNPCs[currentGridNPC].CanShareTile)

                if delProjectile == 0:
                    if len(Path) > 1:
                        $ moveTo = Path[1]
                    elif len(Path) == 1:
                        $ moveTo = Path[0]
                    else:
                        # No path found, stay in place
                        $ moveTo = [ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]]
                    $ intendedMoves.append((currentGridNPC, moveTo))

                else:
                    $ delProjectile = 0
                    $ del ActiveGridNPCs[currentGridNPC]
                    $ currentGridNPC -= 1

        $ currentGridNPC += 1

    # Process intended moves with collision detection (only if there are intended moves)
    if len(intendedMoves) > 0:
        python:
            for i, (npc_index, move_to) in enumerate(intendedMoves):
                collision = False
                for j, (other_index, other_move_to) in enumerate(intendedMoves):
                    if i != j:
                        if ActiveGridNPCs[other_index].coord == move_to:
                            mover_can_share = ActiveGridNPCs[npc_index].CanShareTile
                            target_can_share = ActiveGridNPCs[other_index].CanShareTile

                            if not mover_can_share and not target_can_share:
                                if other_move_to != ActiveGridNPCs[npc_index].coord:
                                    collision = True
                                    break
                if not collision:
                    npc = ActiveGridNPCs[npc_index]
                    if npc.coord[0]+1 == move_to[0] and npc.coord[1] == move_to[1]:
                        AIMove = [1,0]
                    elif npc.coord[0]-1 == move_to[0] and npc.coord[1] == move_to[1]:
                        AIMove = [-1,0]
                    elif npc.coord[0] == move_to[0] and npc.coord[1]+1 == move_to[1]:
                        AIMove = [0,1]
                    elif npc.coord[0] == move_to[0] and npc.coord[1]-1 == move_to[1]:
                        AIMove = [0,-1]
                    else:
                        AIMove = [0,0]  # No movement if not adjacent
                    npc.GridposX += AIMove[0]*GridMovement
                    npc.coord[0] += AIMove[0]
                    npc.GridposY += AIMove[1]*GridMovement
                    npc.coord[1] += AIMove[1]

    $ currentGridNPC = 0

    while currentGridNPC < len(ActiveGridNPCs):
        if ActiveGridNPCs[currentGridNPC].TimerReset != -1:
            if ActiveGridNPCs[currentGridNPC].JustSpawned == 0:
                $ ActiveGridNPCs[currentGridNPC].Timer -= 1
                if ActiveGridNPCs[currentGridNPC].Timer == 0:
                    $ ActiveGridNPCs[currentGridNPC].Timer = ActiveGridNPCs[currentGridNPC].TimerReset

                    $ specifyDataLocation = getFromName(ActiveGridNPCs[currentGridNPC].TimerEvent[0], EventDatabase)

                    $ specifyCurrentChoice = 0
                    $ specifyCurrentChoice = getFromNameOfScene(ActiveGridNPCs[currentGridNPC].TimerEvent[1], EventDatabase[specifyDataLocation].theEvents)

                    $ showingDream = []
                    $ showingDream.append(copy.deepcopy(EventDatabase[specifyDataLocation]))
                    call TimeEvent(CardType="Any", LoopedList=showingDream) from _call_TimeEvent_18

        $ currentGridNPC += 1

    $ currentGridNPC = 0
    while currentGridNPC < len(ActiveGridNPCs):
        $ ActiveGridNPCs[currentGridNPC].JustSpawned = 0
        if ActiveGridNPCs[currentGridNPC].NPCMoveEvent[0] != "": # TurnEvent
            $ specifyDataLocation = getFromName(ActiveGridNPCs[currentGridNPC].NPCMoveEvent[0], EventDatabase)

            $ specifyCurrentChoice = 0
            $ specifyCurrentChoice = getFromNameOfScene(ActiveGridNPCs[currentGridNPC].NPCMoveEvent[1], EventDatabase[specifyDataLocation].theEvents)

            $ showingDream = []
            $ showingDream.append(copy.deepcopy(EventDatabase[specifyDataLocation]))
            call TimeEvent(CardType="Any", LoopedList=showingDream) from _call_TimeEvent_16
        $ currentGridNPC += 1

    jump GridInteract

label PostGridMovement:
    if stunnedGridPlayer == 0:
        $ stunnedGridPlayer -= 1
    $ NPCMove = 0
    $ display = ""
    
    $ tileTarget = TheGrid[playerCoord[1]][playerCoord[0]]
    $ display = tileset[FindTileType(tileTarget, tileset)][5]

    $ toggledGridEvent = 0
    $ lastPlayerMove = [0,0]
    $ paralysisIgnored = 0

    jump displayTileMap



label GridXMovement:
    if playerGridCanMove:
        $ gridStepLine = ""
        call statusStep from _call_statusStep_2
        $ playerGridCanMove = False
        if stunnedGridPlayer > 0:
            $ stunnedGridPlayer -= 1
            $ GridPXposPrior = copy.copy(GridPXpos)
            $ GridPYposPrior = copy.copy(GridPYpos)
            jump GridMovement
        if onGridMap == 3:
            jump GridEvent
        $ gridEvent = "Auto"
        $ canMove = 1
        $ GridPXposPrior = copy.copy(GridPXpos)
        $ GridPYposPrior = copy.copy(GridPYpos)
        $ lastPlayerCoord = copy.copy(playerCoord)
        if GridPXpos + GridMovin*GridMovement >= 0 and GridPXpos+ GridMovin*GridMovement < len(TheGrid[0])*50:
            $ tileTarget = TheGrid[playerCoord[1]][playerCoord[0] + GridMovin]

            python:
                for each in ActiveGridNPCs:
                    if each.Wall == "Wall":
                        if each.coord == [playerCoord[0] + GridMovin, playerCoord[1]]:
                            canMove = 0

            if tileset[FindTileType(tileTarget, tileset)][2] == "Wall":
                $ canMove = 0

            if canMove == 1:
                $ GridPXpos += GridMovin*GridMovement
                $ playerCoord[0] += GridMovin

                $ lastPlayerMove = [GridMovin,0]

        jump GridMovement

label GridYMovement:
    if playerGridCanMove:
        $ gridStepLine = ""
        call statusStep from _call_statusStep_3
        $ playerGridCanMove = False
        if stunnedGridPlayer > 0:
            $ stunnedGridPlayer -= 1
            $ GridPXposPrior = copy.copy(GridPXpos)
            $ GridPYposPrior = copy.copy(GridPYpos)
            jump GridMovement
        if onGridMap == 3:
            jump GridEvent
        $ gridEvent = "Auto"
        $ canMove = 1
        $ GridPXposPrior = copy.copy(GridPXpos)
        $ GridPYposPrior = copy.copy(GridPYpos)
        $ lastPlayerCoord = copy.copy(playerCoord)
        if GridPYpos + GridMovin*GridMovement >= 0 and GridPYpos+ GridMovin*GridMovement < len(TheGrid)*50:
            $ tileTarget = TheGrid[playerCoord[1] + GridMovin][playerCoord[0]]

            python:
                for each in ActiveGridNPCs:
                    if each.Wall == "Wall":
                        if each.coord == [playerCoord[0], playerCoord[1] + GridMovin]:
                            canMove = 0

            if tileset[FindTileType(tileTarget, tileset)][2] == "Wall":
                $ canMove = 0

            if canMove == 1:
                $ GridPYpos += GridMovin*GridMovement
                $ playerCoord[1] += GridMovin
                $ lastPlayerMove = [0,GridMovin]
        jump GridMovement


label GridInteract:
    if playerGridCanMove:
        $ gridStepLine = ""
        call statusStep from _call_statusStep_4
    $ playerGridCanMove = False
    $ TileMoveComplete = 0

    if stunnedGridPlayer > 0:
        $ stunnedGridPlayer -= 1
        $ GridPXposPrior = copy.copy(GridPXpos)
        $ GridPYposPrior = copy.copy(GridPYpos)
        jump GridMovement
    $ eventTriggered = 0

    python:
        currentGridNPC = 0
        for each in ActiveGridNPCs:
            if each.coord == playerCoord:
                if each.NPCevent[0] == gridEvent:
                    eventTriggered = 1
                    DataLocation = getFromName(each.NPCevent[1], EventDatabase)
                    currentChoice = 0
                    if each.NPCevent[2] != "":
                        currentChoice = getFromNameOfScene(each.NPCevent[2], EventDatabase[DataLocation].theEvents)
                    TileEventArray.append([DataLocation, currentChoice, currentGridNPC])
            currentGridNPC += 1

    if GridMovin == 0:
        $ playerGridCanMove = True

    if eventTriggered == 1:
        jump GridEvent

label TileHitinteract:
    $ eventTriggered = 0
    $ TileMoveComplete = 1
    $ tileTarget = TheGrid[playerCoord[1]][playerCoord[0]]
    if eventTriggered == 0:
        if tileset[FindTileType(tileTarget, tileset)][2] == gridEvent:

            $ eventTriggered = 1

            $ DataLocation = getFromName(tileset[FindTileType(tileTarget, tileset)][3], EventDatabase)
            $ currentChoice = 0
            if tileset[FindTileType(tileTarget, tileset)][4] != "":
                $ currentChoice = getFromNameOfScene(tileset[FindTileType(tileTarget, tileset)][4], EventDatabase[DataLocation].theEvents)
            $ TileEventArray.append([DataLocation, currentChoice, 0])
            jump GridEvent

    if eventTriggered == 0 and GridInteracted == 2:
        $ GridInteracted = 0
        jump displayTileMap
    jump PostGridMovement

label NPCinteract: #not currently used
    $ onGridMap = 1
    $ eventTriggered = 0
    python:
        currentGridNPC = 0
        for each in ActiveGridNPCs:
            if each.coord == playerCoord and each.Obstacle != 1:
                if each.NPCevent[0] == gridEvent and eventTriggered == 0:
                    eventTriggered = 1
                    DataLocation = getFromName(each.NPCevent[1], EventDatabase)
                    currentChoice = 0
                    if each.NPCevent[2] != "":
                        currentChoice = getFromNameOfScene(each.NPCevent[2], EventDatabase[DataLocation].theEvents)
            if eventTriggered == 0:
                currentGridNPC += 1

    if eventTriggered == 1:
        jump GridEvent

    if GridInteracted == 2:
        $ GridInteracted = 1

    jump GridMovement

label GridEvent:
    $ InventoryAvailable = False
    $ DialogueIsFrom = "Event"
    $ isEventNow = 1
    $ onGridMap = 3
    $ gridMapDethAdjuster = 0

    $ setNPCPos = 0

    $ HoveringGrid = [-1,-1]

    if GridInteracted == 0:
        hide screen Gridmap
        hide screen GridmapPlayer
        hide screen GridmapObstacles
        hide screen GridmapNPCs
        hide screen GridUI
        hide screen GridInventory
        hide screen GridHover
        hide screen gridMoveKeys
        show screen Gridmap
        show screen GridmapObstacles
        show screen GridmapPlayer
        show screen GridmapNPCs
        show screen GridUI
        show screen GridInventory
        show screen GridHover
        #$ renpy.free_memory()
        pause 0.195
    hide screen Gridmap
    hide screen GridmapPlayer
    hide screen GridmapObstacles
    hide screen GridmapNPCs
    hide screen GridUI
    hide screen GridInventory
    hide screen GridHover
    hide screen gridMoveKeys


    $ GridPXposPrior = copy.copy(GridPXpos)
    $ GridPYposPrior = copy.copy(GridPYpos)


    while len(TileEventArray) != 0:
        if len(TileEventArray) > 0:
            $ DataLocation = copy.deepcopy(TileEventArray[0][0]) #is this part of the crash problem? eg datalocation being set to a str not an int?
            $ currentChoice = copy.deepcopy(TileEventArray[0][1])
            $ currentGridNPC = copy.deepcopy(TileEventArray[0][2]) - gridMapDethAdjuster
            $ lineOfScene = 0
            $ isEventNow = 1

            $ del TileEventArray[0]
            jump sortMenuD

            label postGridEvent:

    if TheGrid == []:
        return
    if NPCMove == 0:
        if GridInteracted == 2:
            $ GridInteracted = 0
        jump GridMovement
    if TileMoveComplete == 0:
        $ GridInteracted = 1
        jump TileHitinteract
    $ setNPCPos = 0
    while setNPCPos < len(ActiveGridNPCs):
        $ ActiveGridNPCs[setNPCPos].GridposXPrior = ActiveGridNPCs[setNPCPos].GridposX
        $ ActiveGridNPCs[setNPCPos].GridposYPrior = ActiveGridNPCs[setNPCPos].GridposY
        $ setNPCPos += 1
    $ onGridMap = 1
    jump PostGridMovement
