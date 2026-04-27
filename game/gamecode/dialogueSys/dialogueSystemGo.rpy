# GoTo funcs
label JsonFuncGoToTown:
    $ monsterEncounter = []
    $ monsterEncounterCG = []
    $ trueMonsterEncounter = []
    $ DefeatedEncounterMonsters = []
    $ SceneCharacters = []
    $ displayingScene = Dialogue()
    $ player = player.statusEffects.refresh(player)
    #$ player.stats.refresh()
    $ player.clearStance()
    $ player.restraintStruggle = [""]
    $ player.restraintStruggleCharmed = [""]
    $ player.restraintEscaped = [""]
    $ player.restraintEscapedFail = [""]
    $ explorationDeck = []
    $ deckProgress = 0
    $ InventoryAvailable = True
    $ canRun = True

    jump returnToTown
    return
label JsonFuncGoToChurch:
    $ monsterEncounter = []
    $ monsterEncounterCG = []
    $ trueMonsterEncounter = []
    $ DefeatedEncounterMonsters = []
    $ SceneCharacters = []
    $ displayingScene = Dialogue()
    $ player = player.statusEffects.refresh(player)
    #$ player.stats.refresh()
    $ player.clearStance()
    $ player.restraintStruggle = [""]
    $ player.restraintStruggleCharmed = [""]
    $ player.restraintEscaped = [""]
    $ player.restraintEscapedFail = [""]
    $ explorationDeck = []
    $ deckProgress = 0
    $ InventoryAvailable = True
    $ canRun = True

    jump Church
    return
label JsonFuncGoToRandomBrothelWaiterScene:
    $ DialogueIsFrom = "NPC"
    $ isEventNow = 1
    $ currentChoice = 0

    $ LocationCurrentList = []
    python:
        for each in WaiterBrothel:

            if each.CardType == "WaiterShift" or each.description == "WaiterShift":
                hasReq = 0
                hasReq = requiresCheck(each.requires, each.requiresEvent, player, ProgressEvent)

                if hasReq >= len(each.requires) + len(each.requiresEvent):
                    LocationCurrentList.append(copy.deepcopy(each))

    $ renpy.random.shuffle(LocationCurrentList)

    $ DataLocation = getFromName(LocationCurrentList[0].name, EventDatabase)
    jump sortMenuD
    return
label JsonFuncGoToRandomBrothelBarScene:
    $ DialogueIsFrom = "NPC"
    $ isEventNow = 1
    $ currentChoice = 0

    $ LocationCurrentList = []
    python:
        for each in BarBrothel:
            if each.CardType == "BarShift" or each.description == "BarShift":
                hasReq = 0
                hasReq = requiresCheck(each.requires, each.requiresEvent, player, ProgressEvent)

                if hasReq >= len(each.requires) + len(each.requiresEvent):
                    LocationCurrentList.append(copy.deepcopy(each))

    $ renpy.random.shuffle(LocationCurrentList)

    $ DataLocation = getFromName(LocationCurrentList[0].name, EventDatabase)
    jump sortMenuD
    return
label JsonFuncGoToRandomBrothelHoleScene:
    $ DialogueIsFrom = "NPC"
    $ isEventNow = 1
    $ currentChoice = 0

    $ LocationCurrentList = []
    python:
        for each in GloryHoleBrothel:
            if each.CardType == "GloryHoleShift" or each.description == "GloryHoleShift":
                hasReq = 0
                hasReq = requiresCheck(each.requires, each.requiresEvent, player, ProgressEvent)

                if hasReq >= len(each.requires) + len(each.requiresEvent):
                    LocationCurrentList.append(copy.deepcopy(each))

    $ renpy.random.shuffle(LocationCurrentList)

    $ DataLocation = getFromName(LocationCurrentList[0].name, EventDatabase)
    jump sortMenuD
    return
label JsonFuncGoToRandomBrothelDayScene:
    $ DialogueIsFrom = "NPC"
    $ isEventNow = 1
    $ currentChoice = 0

    $ LocationCurrentList = []
    python:
        for each in DayBrothel:
            if each.CardType == "DayShift" or each.description == "DayShift":
                hasReq = 0
                hasReq = requiresCheck(each.requires, each.requiresEvent, player, ProgressEvent)

                if hasReq >= len(each.requires) + len(each.requiresEvent):
                    LocationCurrentList.append(copy.deepcopy(each))

    $ renpy.random.shuffle(LocationCurrentList)

    $ DataLocation = getFromName(LocationCurrentList[0].name, EventDatabase)
    jump sortMenuD
    return
label JsonFuncGoBackToStoredEvent:
    $ displayingScene = StoredScene
    $ lineOfScene = StoredLine
    $ DataLocation = StoredDataLoc
    $ StoredScene = ""
    $ StoredLine = ""
    $ StoredDataLoc = ""
    return
label JsonFuncGoToMap:
    $ startplayerpos = [0,0]
    $ onGridMap = 1
    $ tileset = []
    $ TheGrid = []
    $ TheGridNPCs = []
    $ ActiveGridNPCs = []
    $ gridStepLine = ""
    $ PlayerGridSight = 0
    $ stunnedGridPlayer = -1
    $ playerGridIcon = "GridMap/PlayerMapIcon.png"

    $ display = ""
    $ toggledGridEvent = 0
    $ gridYAdjust = 0
    while displayingScene.theScene[lineOfScene] != "StartMap":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "StartMap":
            if displayingScene.theScene[lineOfScene] == "Tileset":
                while displayingScene.theScene[lineOfScene] != "EndLoop":
                    $ Tile = []
                    $ lineOfScene += 1
                    if displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ Tile.append(displayingScene.theScene[lineOfScene])
                        $ lineOfScene += 1
                        $ Tile.append(displayingScene.theScene[lineOfScene])
                        $ lineOfScene += 1
                        $ Tile.append(displayingScene.theScene[lineOfScene])
                        $ lineOfScene += 1
                        $ Tile.append(displayingScene.theScene[lineOfScene])
                        $ lineOfScene += 1
                        $ Tile.append(displayingScene.theScene[lineOfScene])
                        $ lineOfScene += 1
                        $ Tile.append(displayingScene.theScene[lineOfScene])
                        $ tileset.append(copy.deepcopy(Tile))
            elif displayingScene.theScene[lineOfScene] == "YAdjust":
                $ lineOfScene += 1
                $ gridYAdjust = int(displayingScene.theScene[lineOfScene])

            elif displayingScene.theScene[lineOfScene] == "PlayerIcon":
                $ lineOfScene += 1
                $ playerGridIcon = displayingScene.theScene[lineOfScene]

            elif displayingScene.theScene[lineOfScene] == "PlayerCoord":
                $ lineOfScene += 1
                $ startplayerpos[0] = int(displayingScene.theScene[lineOfScene])
                $ lineOfScene += 1
                $ startplayerpos[1] = int(displayingScene.theScene[lineOfScene])
                $ playerCoord = startplayerpos
                $ GridPXpos = GridMovement*playerCoord[0]
                $ GridPYpos = GridMovement*playerCoord[1]
                $ GridPXposPrior = GridPXpos
                $ GridPYposPrior = GridPYpos
            elif displayingScene.theScene[lineOfScene] == "Sight":
                $ lineOfScene += 1
                $ PlayerGridSight = int(displayingScene.theScene[lineOfScene])
            elif displayingScene.theScene[lineOfScene] == "DenyGridInventory":
                $ DenyGridInventory = True
            elif displayingScene.theScene[lineOfScene] == "NPC":
                $ newNPC = GridNPC()
                while displayingScene.theScene[lineOfScene] != "EndLoop":
                    $ lineOfScene += 1
                    if displayingScene.theScene[lineOfScene] != "EndLoop":
                        if displayingScene.theScene[lineOfScene] == "Name":
                            $ lineOfScene += 1
                            $ newNPC.name = displayingScene.theScene[lineOfScene]
                        elif displayingScene.theScene[lineOfScene] == "Img":
                            $ lineOfScene += 1
                            $ newNPC.pic = displayingScene.theScene[lineOfScene]
                        elif displayingScene.theScene[lineOfScene] == "Event":
                            $ lineOfScene += 1
                            $ newNPC.NPCevent = [displayingScene.theScene[lineOfScene], displayingScene.theScene[lineOfScene+1], displayingScene.theScene[lineOfScene+2]]
                            $ lineOfScene += 2
                        elif displayingScene.theScene[lineOfScene] == "TurnEvent":
                            $ lineOfScene += 1
                            $ newNPC.NPCMoveEvent = [displayingScene.theScene[lineOfScene], displayingScene.theScene[lineOfScene+1]]
                            $ lineOfScene += 1
                        elif displayingScene.theScene[lineOfScene] == "Movement":
                            $ lineOfScene += 1
                            $ newNPC.Movement = displayingScene.theScene[lineOfScene]
                            $ lineOfScene += 1
                            $ newNPC.MovementTarget = displayingScene.theScene[lineOfScene]

                            if newNPC.Movement == "Whimsical":
                                $ lineOfScene += 1
                                $ newNPC.WhimsyRange = int(displayingScene.theScene[lineOfScene])
                        elif displayingScene.theScene[lineOfScene] == "Obstacle":
                            $ newNPC.Obstacle = 1
                        elif displayingScene.theScene[lineOfScene] == "Wall":
                            $ newNPC.Wall = "Wall"
                        elif displayingScene.theScene[lineOfScene] == "Timer":
                            $ lineOfScene += 1
                            $ newNPC.Timer = int(displayingScene.theScene[lineOfScene])
                            $ newNPC.TimerReset = int(displayingScene.theScene[lineOfScene])
                            $ lineOfScene += 1
                            $ newNPC.TimerEvent = [displayingScene.theScene[lineOfScene], displayingScene.theScene[lineOfScene+1]]
                        elif displayingScene.theScene[lineOfScene] == "TimerMax":
                            $ lineOfScene += 1
                            $ newNPC.TimerReset = int(displayingScene.theScene[lineOfScene])
                        elif displayingScene.theScene[lineOfScene] == "Description":
                            $ lineOfScene += 1
                            $ newNPC.Description = displayingScene.theScene[lineOfScene]
                        elif displayingScene.theScene[lineOfScene] == "CanShareTile":
                            $ lineOfScene += 1
                            if displayingScene.theScene[lineOfScene] == "False":
                                $ newNPC.CanShareTile = False
                            else:
                                $ newNPC.CanShareTile = True
                $ TheGridNPCs.append(copy.deepcopy(newNPC))

            elif displayingScene.theScene[lineOfScene] == "SpawnNPC":
                $ lineOfScene += 1
                $ newNPC = copy.deepcopy(TheGridNPCs[getFromName(displayingScene.theScene[lineOfScene], TheGridNPCs)] )
                $ lineOfScene += 1
                if displayingScene.theScene[lineOfScene] == "Timer":
                    $ lineOfScene += 1
                    $ newNPC.Timer = int(displayingScene.theScene[lineOfScene])
                    $ newNPC.TimerReset = int(displayingScene.theScene[lineOfScene])
                    $ lineOfScene += 1
                if displayingScene.theScene[lineOfScene] == "TimerMax":
                    $ lineOfScene += 1
                    $ newNPC.TimerReset = int(displayingScene.theScene[lineOfScene])
                    $ lineOfScene += 1
                $ newNPC.coord[0] = int(displayingScene.theScene[lineOfScene])
                $ lineOfScene += 1
                $ newNPC.coord[1] = int(displayingScene.theScene[lineOfScene])

                $ newNPC.GridposX = GridMovement*newNPC.coord[0]
                $ newNPC.GridposY = GridMovement*newNPC.coord[1]
                $ newNPC.GridposXPrior = newNPC.GridposX
                $ newNPC.GridposYPrior = newNPC.GridposY

                $ ActiveGridNPCs.append(copy.deepcopy(newNPC))


            elif displayingScene.theScene[lineOfScene] == "Row":
                $ Row = []
                while displayingScene.theScene[lineOfScene] != "EndLoop":
                    $ lineOfScene += 1
                    if displayingScene.theScene[lineOfScene] != "EndLoop":
                        $ Row.append(displayingScene.theScene[lineOfScene])
                $ TheGrid.append(copy.deepcopy(Row))

    call displayTileMap from _call_displayTileMap

    label postGridMap:
        # Empty labels is an ancient Thresh hack to get the old dialogue system to jump properly.
        # The new registry based dialogue system can experience bugs with it if there is logic after these empty jumps.
        # This might not even be needed anymore, but we can leave that for future adjustments.
    return