# Set funcs
label JsonFuncSetFlexibleSpeaker:
    $ lineOfScene += 1
    $ FlexibleSpeaker = int(displayingScene.theScene[lineOfScene])-1
    return
label JsonFuncSetProgress:
    $ lineOfScene += 1
    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
    $ ProgressEvent[DataLocation].eventProgress = int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncSetChoice:
    $ lineOfScene += 1
    $ HoldChoiceNumber = int(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1

    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)

    while HoldChoiceNumber-1 >= len(ProgressEvent[DataLocation].choices):
        $ ProgressEvent[DataLocation].choices.append("")
    $ ProgressEvent[DataLocation].choices[HoldChoiceNumber-1] = displayingScene.theScene[lineOfScene]
    return
label JsonFuncSetChoiceToPlayerName:
    $ lineOfScene += 1
    $ HoldChoiceNumber = int(displayingScene.theScene[lineOfScene])

    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)

    while HoldChoiceNumber-1 >= len(ProgressEvent[DataLocation].choices):
        $ ProgressEvent[DataLocation].choices.append("")

    $ ProgressEvent[DataLocation].choices[HoldChoiceNumber-1] = player.name
    return
label JsonFuncSetChoiceToPlayerNameFromOtherEvent:
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    $ choiceToCheck = int(displayingScene.theScene[lineOfScene])

    while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
        $ ProgressEvent[CheckEvent].choices.append("")

    $ ProgressEvent[CheckEvent].choices[choiceToCheck-1] = player.name
    return
label JsonFuncSetArousalToMax:
    $ player.stats.hp = player.stats.max_true_hp
    return
label JsonFuncSetArousalToXUnlessHigherThanX:
    $ lineOfScene += 1
    $ TheX = int(displayingScene.theScene[lineOfScene])

    if TheX <= player.stats.hp:
        $ player.stats.hp = TheX
    return
label JsonFuncSetArousalToXUnlessHigherThanXThenAddY:
    $ lineOfScene += 1
    $ TheX = int(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ TheY = int(displayingScene.theScene[lineOfScene])

    if TheX >= player.stats.hp:
        $ player.stats.hp = TheX
    else:
        $ player.stats.hp += TheY
    return
label JsonFuncSetSpirit:
    $ lineOfScene += 1
    $ player.stats.sp = int(displayingScene.theScene[lineOfScene])

    if player.stats.sp <= 0:
        $ player.stats.sp = 0
    if player.stats.sp > player.stats.max_true_sp:
        $ player.stats.sp = player.stats.max_true_sp
    return
label JsonFuncSetFetish:
    $ lineOfScene += 1
    $ resTarget = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ resAmount = int(displayingScene.theScene[lineOfScene])

    $ baseFetish = player.getFetish(resTarget)
    $ baseFetish = resAmount

    $ player.setFetish(resTarget, baseFetish)
    return
label JsonFuncSetPlayerGridPosition:
    $ lineOfScene += 1
    $ startplayerpos[0] = int(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ startplayerpos[1] = int(displayingScene.theScene[lineOfScene])
    $ playerCoord = startplayerpos
    $ GridPXpos = GridMovement*playerCoord[0]
    $ GridPYpos = GridMovement*playerCoord[1]
    $ GridPXposPrior = GridPXpos
    $ GridPYposPrior = GridPYpos
    return
label JsonFuncSetActiveGridNPC:
    $ lineOfScene += 1
    $ passcheck = 0
    $ count = 0
    python:
        for each in ActiveGridNPCs:
            if each.name == displayingScene.theScene[lineOfScene]:
                passcheck = 1
            if passcheck == 0:
                count += 1
    if passcheck == 1:
        $ currentGridNPC = count
    return
label JsonFuncSetPostName:
    $ lineOfScene += 1
    if displayingScene.theScene[lineOfScene] == "None":
        $ attackTitle = ""
    else:
        $ attackTitle = displayingScene.theScene[lineOfScene]
    return
label JsonFuncSetEros:
    $ lineOfScene += 1
    $ player.inventory.money = int(displayingScene.theScene[lineOfScene])

    if player.inventory.money <= 0:
        $ player.inventory.money = 0
    return
label JsonFuncSetStoredColor:
    $ jsonFuncLooping = 1
    $ lineOfScene += 1
    while jsonFuncLooping:
        if displayingScene.theScene[lineOfScene] == "1":
            $ lineOfScene += 1
            $ textColor = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "2":
            $ lineOfScene += 1
            $ textColor2 = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "3":
            $ lineOfScene += 1
            $ textColor3 = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "4":
            $ lineOfScene += 1
            $ textColor4 = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "5":
            $ lineOfScene += 1
            $ textColor5 = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "6":
            $ lineOfScene += 1
            $ textColor6 = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "7":
            $ lineOfScene += 1
            $ textColor7 = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "Reset":
            $ textColor = "#F6BADC"
            $ textColor2 = "#F6BADC"
            $ textColor3 = "#F6BADC"
            $ textColor4 = "#F6BADC"
            $ textColor5 = "#F6BADC"
            $ textColor6 = "#F6BADC"
            $ textColor7 = "#F6BADC"
            $ lineOfScene += 1
        else:
            $ jsonFuncLooping = 0
            $ lineOfScene -= 1
    return
# Get funcs
label JsonFuncGetEventAndSetProgress:
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    $ ProgressEvent[CheckEvent].eventProgress = int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncGetEventAndChangeProgress:
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    $ ProgressEvent[CheckEvent].eventProgress += int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncGetAnEventsProgressThenIfEquals:
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    if int(displayingScene.theScene[lineOfScene]) == ProgressEvent[CheckEvent].eventProgress:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_26
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncGetAnEventsProgressThenIfEqualsOrGreater:
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[CheckEvent].eventProgress:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_27
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncGetAnEventsProgressThenIfEqualsOrLess:
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    if int(displayingScene.theScene[lineOfScene]) >= ProgressEvent[CheckEvent].eventProgress:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_65
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncGetEventAndIfChoice:
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    $ choiceToCheck = int(displayingScene.theScene[lineOfScene])

    while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
        $ ProgressEvent[CheckEvent].choices.append("")


    $ lineOfScene += 1
    if displayingScene.theScene[lineOfScene] == ProgressEvent[CheckEvent].choices[choiceToCheck-1]:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_8
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncGetEventAndSetChoice:
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1

    while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
        $ ProgressEvent[CheckEvent].choices.append("")
    $ ProgressEvent[CheckEvent].choices[choiceToCheck-1] = displayingScene.theScene[lineOfScene]
    return
