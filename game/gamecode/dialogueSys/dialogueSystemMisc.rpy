# The rest just dumped out of Core for now.
label JsonFuncFlexibleSpeaks:
    if len(monsterEncounter) >= 2:
        $ Speaker = monsterEncounter[FlexibleSpeaker].name+attackTitle
    else:
        $ Speaker = getSpeaker(FlexibleSpeaker, EventDatabase, MonsterDatabase)

    $ lineOfScene += 1
    $ readLine = 1
    return
label JsonFuncDisplayCharacters:
    $ showSpeakers = 1
    $ lineOfScene += 1
    $ SceneCharacters = []
    $ RoledCGOn = 0
    $ textboxCGXAdjust = 0
    $ CgRoleKeeper = []
    if len(monsterEncounter) == 0:
        $ hidingCombatEncounter = 0

    if hidingCombatEncounter == 0:
        $ monsterEncounter = []
        $ monsterEncounterCG = []  
        
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ strCheck = 0
        python:
            try:
                targetChar = int(displayingScene.theScene[lineOfScene]) - 1
            except:
                characterDataLocation = getFromName(displayingScene.theScene[lineOfScene], MonsterDatabase)
                strCheck = 1

        if strCheck == 0:
            $ characterDataLocation = getFromName(EventDatabase[DataLocation].Speakers[targetChar].name, MonsterDatabase)
        if characterDataLocation != -1:
            $ SceneCharacters.append(copy.deepcopy(MonsterDatabase[characterDataLocation]))
        if strCheck == 0:
            if EventDatabase[DataLocation].Speakers[targetChar].SpeakerType == "?":
                $ SceneCharacters.append(copy.deepcopy(Monster(Stats(),0,  "?", "?")))

        $ lineOfScene += 1
    python:
        for each in SceneCharacters:
            each = initiateImageLayers(each)

            for SetData in persistantMonSetData:
                if SetData.name == each.IDname:
                    each.currentSet = getFromName(SetData.startingSet, each.ImageSets)

    #if hidingCombatEncounter == 0:
    #    hide screen ON_HealthDisplayBacking
    #    hide screen ON_HealthDisplay
    show screen ON_CharacterDialogueScreen onlayer master
    #if hidingCombatEncounter == 0:
    #    if displayHealthInEvent == 1:
    #        hide screen ON_HealthDisplayBacking
    #        hide screen ON_HealthDisplay
    #    else:
    #        hide screen ON_HealthDisplayBacking
    #        hide screen ON_HealthDisplay
    return
label JsonFuncAnimateImageLayer:
    $ lineOfScene += 1
    $ settingToImage = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ layerToChange = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    python:
        try:
            settingCharcter = int(displayingScene.theScene[lineOfScene]) - 1
        except:
            ifIsInScene = 0
            if len(monsterEncounter) > 0 and hidingCombatEncounter == 0:
                searchingCharacters = monsterEncounter
            else:
                searchingCharacters = SceneCharacters
            if len(searchingCharacters) > 0 and hidingCombatEncounter == 0:
                #during combat layer change
                if getFromName(displayingScene.theScene[lineOfScene], searchingCharacters)!= -1:
                    ifIsInScene = 1
                    settingCharcter = getFromName(displayingScene.theScene[lineOfScene], searchingCharacters)
            if ifIsInScene == 0:
                settingCharcter = CombatFunctionEnemytarget
    if settingToImage == "Animation":
        $ animationList = []
        $ animationChoice = ""
        $ currentAnimationImg = 0
    elif settingToImage == "Animation2":
        $ animationList2 = []
        $ animationChoice2 = ""
        $ currentAnimationImg2 = 0
    elif settingToImage == "Animation3":
        $ animationList3 = []
        $ animationChoice3 = ""
        $ currentAnimationImg3 = 0
    $ lineOfScene += 1
    if settingToImage == "Animation":
        $ animationSpeed = float(displayingScene.theScene[lineOfScene])
        $ animationTime = float(displayingScene.theScene[lineOfScene])
    elif settingToImage == "Animation2":
        $ animationSpeed2 = float(displayingScene.theScene[lineOfScene])
        $ animationTime2 = float(displayingScene.theScene[lineOfScene])
    elif settingToImage == "Animation3":
        $ animationSpeed3 = float(displayingScene.theScene[lineOfScene])
        $ animationTime3 = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    if settingToImage == "Animation":
        $ animationList = []
    elif settingToImage == "Animation2":
        $ animationList2 = []
    elif settingToImage == "Animation3":
        $ animationList3 = []
    if displayingScene.theScene[lineOfScene] != "EndLoop":
        while displayingScene.theScene[lineOfScene] != "EndLoop":
            if displayingScene.theScene[lineOfScene] != "EndLoop":
                if settingToImage == "Animation":
                    $ animationList.append(displayingScene.theScene[lineOfScene])
                elif settingToImage == "Animation2":
                    $ animationList2.append(displayingScene.theScene[lineOfScene])
                elif settingToImage == "Animation3":
                    $ animationList3.append(displayingScene.theScene[lineOfScene])
                $ lineOfScene += 1
    if settingToImage == "Animation":
        if len(animationList) > 0:
            $ animationChoice = animationList[0]
    elif settingToImage == "Animation2":
        if len(animationList2) > 0:
            $ animationChoice2 = animationList2[0]
    elif settingToImage == "Animation3":
        if len(animationList3) > 0:
            $ animationChoice3 = animationList3[0]
    $ searchingCharacters = AnimateImgLayer(searchingCharacters, settingCharcter, layerToChange, settingToImage)
    return
label JsonFuncHideHealth:
    $ displayHealthInEvent = 0
    return
label JsonFuncHoldCurrentVirility:
    $ heldVirility = copy.copy(getVirility(player))
    return
label JsonFuncHoldCurrentVirilityEnd:
    $ heldVirility = 0
    return
label JsonFuncEventsProgressEqualsOtherEventsProgress:
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    $ CheckEvent2 = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)

    if ProgressEvent[CheckEvent].eventProgress == ProgressEvent[CheckEvent2].eventProgress:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_66
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncEventsProgressEqualsOrGreaterThanOtherEventsProgress:
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    $ CheckEvent2 = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)

    if ProgressEvent[CheckEvent].eventProgress >= ProgressEvent[CheckEvent2].eventProgress:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_67
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncVirilityEqualsOrGreater:
    $ lineOfScene += 1
    if int(displayingScene.theScene[lineOfScene]) <= getVirility(player) :
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_71
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncChoiceToDisplayPlayer:
    $ lineOfScene += 1
    $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)

    while choiceToCheck-1 >= len(ProgressEvent[DataLocation].choices):
        $ ProgressEvent[DataLocation].choices.append("")

    $ PlayerChoiceToDisplay = ProgressEvent[DataLocation].choices[choiceToCheck-1]
    return
label JsonFuncChoiceToDisplayMonster:
    $ lineOfScene += 1
    $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)

    while choiceToCheck-1 >= len(ProgressEvent[DataLocation].choices):
        $ ProgressEvent[DataLocation].choices.append("")

    $ MonsterChoiceToDisplay = ProgressEvent[DataLocation].choices[choiceToCheck-1]
    return
label JsonFuncChoiceToDisplayPlayerFromOtherEvent:
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    $ choiceToCheck = int(displayingScene.theScene[lineOfScene])

    while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
        $ ProgressEvent[CheckEvent].choices.append("")

    $ PlayerChoiceToDisplay = ProgressEvent[DataLocation].choices[choiceToCheck-1]
    return
label JsonFuncChoiceToDisplayMonsterFromOtherEvent:
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    $ choiceToCheck = int(displayingScene.theScene[lineOfScene])

    while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
        $ ProgressEvent[CheckEvent].choices.append("")

    $ MonsterChoiceToDisplay = ProgressEvent[DataLocation].choices[choiceToCheck-1]
    return
label JsonFuncHealingSickness:
    $ HealingSickness = 6
    return
label JsonFuncAdvanceTime:
    $ lineOfScene += 1
    if int(displayingScene.theScene[lineOfScene]) > 0:
        $ number = int(displayingScene.theScene[lineOfScene])
        $ lineOfScene += 1
        python:
            try:
                if displayingScene.theScene[lineOfScene] == "DelayNotifications":
                    timeNotify = 1
                else:
                    lineOfScene -= 1
            except:
                lineOfScene -= 1
        call advanceTime(number) from _call_advanceTime_4
    return
label JsonFuncRestPlayer:
    $ lineOfScene += 1
    if lineOfScene < len(displayingScene.theScene):
        if displayingScene.theScene[lineOfScene] == "DelayNotifications":
            $ timeNotify = 1
        else:
            $ lineOfScene -= 1
    else:
        $ lineOfScene -= 1
    call advanceTime(TimeIncrease=1) from _call_advanceTime_1 
    $ player = Resting(player)
    $ notFunction = 0
    return
label JsonFuncRefreshPlayer:
    $ player = player.statusEffects.refresh(player)
    $ player.stats.refresh()
    $ favorPool = CalcGoddessFavor(player)
    $ favorStrain = 0
    return
label JsonFuncPermanentlyChangeSensitivity:
    $ lineOfScene += 1
    $ resTarget = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ resAmount = int(displayingScene.theScene[lineOfScene])
    $ player.BodySensitivity.changeRes (resTarget, resAmount)

    if (int(displayingScene.theScene[lineOfScene]) < 0):
        $ amountLost = resAmount*-1
        if resTarget == "Breasts":
            $ resTarget = "Nipple"
        if resTarget == "Sex":
            $ resTarget = "Cock"
        $ display = "You {i}permanently{/i} lost " + str(amountLost) + " " + resTarget +  " sensitivity!"
    else:
        if resTarget == "Breasts":
            $ resTarget = "Nipple"
        if resTarget == "Sex":
            $ resTarget = "Cock"
        $ display = "You {i}permanently{/i} gained " + displayingScene.theScene[lineOfScene] + " " + resTarget +  " sensitivity!"
    if (int(displayingScene.theScene[lineOfScene]) != 0):
        "[display!i]"
    return
label JsonFuncPermanentChangeStatusEffectResistances:
    $ lineOfScene += 1
    $ resTarget = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ resAmount = int(displayingScene.theScene[lineOfScene])

    $ player.resistancesStatusEffects.changeRes (resTarget, resAmount)

    if (int(displayingScene.theScene[lineOfScene]) < 0):
        $ amountLost = resAmount*-1

        $ display = "You lost " + str(amountLost) + " " + resTarget +  " resistance!"
    else:
        $ display = "You gained " + displayingScene.theScene[lineOfScene] + " " + resTarget +  " resistance!"
    if (int(displayingScene.theScene[lineOfScene]) != 0):
        "[display!i]"
    return
label JsonFuncPermanentlyChangeFetish:
    $ lineOfScene += 1
    $ resTarget = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ resAmount = int(displayingScene.theScene[lineOfScene])

    $ baseFetish = player.getFetish(resTarget)
    $ baseFetish += resAmount

    $ player.setFetish(resTarget, baseFetish)

    $ fetchFetish = getFromName(resTarget, player.FetishList)
    if player.FetishList[fetchFetish].Type == "Fetish":

        if baseFetish < 100:
            if (int(displayingScene.theScene[lineOfScene]) >= 1):
                if resAmount > 1:
                    $ display = "You {i}permanently{/i} gained " + str(resAmount) + " fetish levels for " + resTarget +  "..."
                else:
                    $ display = "You have {i}permanently{/i} gained a fetish level for " + resTarget +  "."

            elif (int(displayingScene.theScene[lineOfScene]) < 0):
                $ resAmount *= -1
                if resAmount > 1:
                    $ display = "You have {i}permanently{/i} lost " + str(resAmount) +" fetish levels for " + resTarget +  "."
                else:
                    $ display = "You have {i}permanently{/i} lost a fetish level for " + resTarget +  "."
        if baseFetish > 100 and resAmount >= 1:
            $ display = "Fantasies of " + resTarget +  " swirl through your mind, and your heart beats faster, you have {i}permanently{/i} gained a fetish level for " + resTarget + ", exceeding your normal obsession..."

        if (resAmount != 0):
            "[display!i]"
    return
label JsonFuncEmptySpiritCounter:
    $ spiritLost = 0
    return
label JsonFuncRoledCGEnd:
    $ monsterEncounterCG = []
    $ RoledCGOn = 0
    $ CgRoleKeeper = []
    return
label JsonFuncMenu:
    $ index = 0
    $ lineOfScene += 1
    $ MenuLineSceneCheckMark = copy.copy(lineOfScene)

    #$ check = ProgressEvent[DataLocation].choices[1]
    #"[check]"

    label recheckMenu:
        $ ind = index
        $ lineOfScene = copy.copy(MenuLineSceneCheckMark)
        $ menuArray = []
        $ passedArray = []


    $ MaxMenuSlots = 6
    if displayingScene.theScene[lineOfScene] == "MaxMenuSlots":
        $ lineOfScene += 1
        $ MaxMenuSlots = int(displayingScene.theScene[lineOfScene])
        $ lineOfScene += 1

    $ eventMenuJumps = []
    $ eventMenuSceneJumps = []
    $ clear1 = 0
    $ clear2 = 0
    $ clear3 = 0
    $ clear4 = 0
    $ clear5 = 0
    $ clear6 = 0

    $ display1 = ""
    $ display2 = ""
    $ display3 = ""
    $ display4 = ""
    $ display5 = ""
    $ display6 = ""

    $ finalOption = ""
    $ finalOptionEvent = ""
    $ finalOptionEventScene = ""
    $ finalSet = 0

    $ ShuffleMenuOptions = 0
    #$ showOnSide = 1
    while displayingScene.theScene[lineOfScene] != "EndLoop":

        $ passcheck = 0
        $ override = ""
        $ display = ""
        $ eventMenuJumps.append("")
        $ eventMenuSceneJumps.append("")
        call SceneRequiresCheck from _call_SceneRequiresCheck

        #"[override]"

        if override != "":
            python:
                ova = 0
                for each in menuArray:
                    if each == override:
                        del menuArray[ova]
                        del passedArray[ova]
                        del eventMenuJumps[ova]
                        del eventMenuSceneJumps[ova]
                        ova -= 1
                    ova +=1

        if displayingScene.theScene[lineOfScene] != "EndLoop":

            if passcheck == 1 :
                $ display = ""
                $ display = displayingScene.theScene[lineOfScene]
                $ passedArray.append(1)

            else:
                if display != "":
                    $ passedArray.append(0)
        if display != "":
            $ menuArray.append(copy.copy(display))
        else:
            $ del eventMenuJumps[-1]
            $ del eventMenuSceneJumps[-1]


        if displayingScene.theScene[lineOfScene] != "EndLoop":
            $ lineOfScene += 1

    if ShuffleMenuOptions == 1:
        $ menuArrays = list(zip(menuArray, passedArray, eventMenuJumps, eventMenuSceneJumps))
        $ renpy.random.shuffle(menuArrays)
        $ menuArray, passedArray, eventMenuJumps, eventMenuSceneJumps = zip(*menuArrays)


    $ choiceName = ""

    $ exist1 = 0
    $ exist2 = 0
    $ exist3 = 0
    $ exist4 = 0
    $ exist5 = 0
    $ exist6 = 0

    $ setEventJump1 = ""
    $ setEventJump2 = ""
    $ setEventJump3 = ""
    $ setEventJump4 = ""
    $ setEventJump5 = ""
    $ setEventJump6 = ""

    $ setEventSceneJump1 = ""
    $ setEventSceneJump2 = ""
    $ setEventSceneJump3 = ""
    $ setEventSceneJump4 = ""
    $ setEventSceneJump5 = ""
    $ setEventSceneJump6 = ""



    if finalOption != "" and finalSet == 0:
        python:
            ova = 0
            for each in menuArray:
                if each == finalOption:
                    del menuArray[ova]
                    del passedArray[ova]
                    del eventMenuJumps[ova]
                    del eventMenuSceneJumps[ova]
                    ova -= 1
                ova +=1

        if MaxMenuSlots == 6:
            $ MaxMenuSlots = 5

    if len(menuArray) > MaxMenuSlots:
        show screen MenuPageButtons
    else:
        hide screen MenuPageButtons

    while ind < len(menuArray):
        if display1 == ""and MaxMenuSlots >= 1:
            $ display1 = menuArray[ind]
            $ clear1 = passedArray[ind]
            $ setEventJump1 = eventMenuJumps[ind]
            $ setEventSceneJump1 = eventMenuSceneJumps[ind]
        elif display2 == "" and MaxMenuSlots >= 2:
            $ display2 = menuArray[ind]
            $ clear2 = passedArray[ind]
            $ setEventJump2 = eventMenuJumps[ind]
            $ setEventSceneJump2 = eventMenuSceneJumps[ind]
        elif display3 == "" and MaxMenuSlots >= 3:
            $ display3 = menuArray[ind]
            $ clear3 = passedArray[ind]
            $ setEventJump3 = eventMenuJumps[ind]
            $ setEventSceneJump3 = eventMenuSceneJumps[ind]
        elif display4 == "" and MaxMenuSlots >= 4:
            $ display4 = menuArray[ind]
            $ clear4 = passedArray[ind]
            $ setEventJump4 = eventMenuJumps[ind]
            $ setEventSceneJump4 = eventMenuSceneJumps[ind]
        elif display5 == "" and MaxMenuSlots >= 5:
            $ display5 = menuArray[ind]
            $ clear5 = passedArray[ind]
            $ setEventJump5 = eventMenuJumps[ind]
            $ setEventSceneJump5 = eventMenuSceneJumps[ind]
        elif display6 == "" and finalOption == "" and MaxMenuSlots >= 6:
            $ display6 = menuArray[ind]
            $ clear6 = passedArray[ind]
            $ setEventJump6 = eventMenuJumps[ind]
            $ setEventSceneJump6 = eventMenuSceneJumps[ind]
        $ ind +=1


    if display1 != "":
        $ exist1 = 1
    if display2 != "":
        $ exist2 = 1
    if display3 != "":
        $ exist3 = 1
    if display4 != "":
        $ exist4 = 1
    if display5 != "":
        $ exist5 = 1
    if finalOption != "" and finalSet == 0:
        $ finalSet =1
    elif display6 != "":
        $ exist6 = 1


    #$ damageToPlayer = " [CritText] [EffectiveText]" + "You gain " + str(finalDamage) + " arousal."
    #if len(monsterEncounter) > 0 and CombatFunctionEnemytarget < len(monsterEncounter):
    #    $ damageToEnemy = " [CritText] [EffectiveText]" + monsterEncounter[CombatFunctionEnemytarget].name + " gains " + str(finalDamage) + " arousal."
    #else:
    #    $ damageToEnemy = ""

    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
    $ progressDisplay = copy.copy(ProgressEvent[DataLocation].eventProgress)

    if savedLine != "" and savedLineInMenu == 1:
        $ LastLine = copy.copy(savedLine)
        $ savedLine = ""
        $ savedLineInMenu = 0
    elif LastLine != "StartCombat" and LastLine != "EndLoop" and LastLine != "end":
        pass
    else:
        $ LastLine = ""


    call playSpecialEffects(VisualEffect, 1) from _call_playSpecialEffects
    call playSpecialEffects(VisualEffect2, 2) from _call_playSpecialEffects_1
    call playSpecialEffects(VisualEffect3, 3) from _call_playSpecialEffects_2

    show screen fakeTextBox
    window hide

    if mgdAutosaveCount <= 0:
        $ renpy.force_autosave()
        #$ renpy.pause(1, True)
        $ mgdAutosaveCount = copy.copy(mgdAutosaveFrequency)
    else:
        if len(monsterEncounter) == 0:
            $ mgdAutosaveCount -= 2
        else:
            $ mgdAutosaveCount -= 1

    menu menuList:
        "[display1!i]" if exist1 == 1:
            if clear1 == 1:
                hide screen MenuPageButtons
                hide screen fakeTextBox
                if setEventJump1 == "":
                    $ display = display1
                    $ choiceName = display1
                    $ MenuLineSceneCheckMark = -1
                    call sortMenuD from _call_sortMenuD_9
                    if monsterEncounter:
                        return
                else:
                    $ isEventNow = 1
                    $ currentChoice = 0
                    $ DataLocation = getFromName(setEventJump1, EventDatabase)
                    if setEventSceneJump1 != "":
                        $ currentChoice = getFromNameOfScene(setEventSceneJump1, EventDatabase[DataLocation].theEvents)
                    jump sortMenuD
            else:
                call recheckMenu from _call_recheckMenu
                if monsterEncounter:
                    return
        "[display2!i]" if exist2 == 1 :
            if clear2 == 1:
                hide screen MenuPageButtons
                hide screen fakeTextBox
                if setEventJump2 == "":
                    $ display = display2
                    $ choiceName = display2
                    $ MenuLineSceneCheckMark = -1
                    call sortMenuD from _call_sortMenuD_10
                    if monsterEncounter:
                        return
                else:
                    $ isEventNow = 1
                    $ currentChoice = 0
                    $ DataLocation = getFromName(setEventJump2, EventDatabase)
                    if setEventSceneJump2 != "":
                        $ currentChoice = getFromNameOfScene(setEventSceneJump2, EventDatabase[DataLocation].theEvents)
                    jump sortMenuD
            else:
                call recheckMenu from _call_recheckMenu_1
                if monsterEncounter:
                    return
        "[display3!i]" if exist3 == 1:
            if clear3 == 1:
                hide screen MenuPageButtons
                hide screen fakeTextBox
                if setEventJump3 == "":
                    $ display = display3
                    $ choiceName = display3
                    $ MenuLineSceneCheckMark = -1
                    call sortMenuD from _call_sortMenuD_14
                    if monsterEncounter:
                        return
                else:
                    $ isEventNow = 1
                    $ currentChoice = 0
                    $ DataLocation = getFromName(setEventJump3, EventDatabase)
                    if setEventSceneJump3 != "":
                        $ currentChoice = getFromNameOfScene(setEventSceneJump3, EventDatabase[DataLocation].theEvents)
                    jump sortMenuD
            else:
                call recheckMenu from _call_recheckMenu_2
                if monsterEncounter:
                    return
        "[display4!i]" if exist4 == 1:
            if clear4 == 1:
                hide screen MenuPageButtons
                hide screen fakeTextBox
                if setEventJump4 == "":
                    $ display = display4
                    $ choiceName = display4
                    $ MenuLineSceneCheckMark = -1
                    call sortMenuD from _call_sortMenuD_16
                    if monsterEncounter:
                        return
                else:
                    $ isEventNow = 1
                    $ currentChoice = 0
                    $ DataLocation = getFromName(setEventJump4, EventDatabase)
                    if setEventSceneJump4 != "":
                        $ currentChoice = getFromNameOfScene(setEventSceneJump4, EventDatabase[DataLocation].theEvents)
                    jump sortMenuD
            else:
                call recheckMenu from _call_recheckMenu_3
                if monsterEncounter:
                    return
        "[display5!i]" if exist5 == 1:
            if clear5 == 1:
                hide screen MenuPageButtons
                hide screen fakeTextBox
                if setEventJump5 == "":
                    $ display = display5
                    $ choiceName = display5
                    $ MenuLineSceneCheckMark = -1
                    call sortMenuD from _call_sortMenuD_18
                    if monsterEncounter:
                        return
                else:
                    $ isEventNow = 1
                    $ currentChoice = 0
                    $ DataLocation = getFromName(setEventJump5, EventDatabase)
                    if setEventSceneJump5 != "":
                        $ currentChoice = getFromNameOfScene(setEventSceneJump5, EventDatabase[DataLocation].theEvents)
                    jump sortMenuD
            else:
                call recheckMenu from _call_recheckMenu_4
                if monsterEncounter:
                    return
        "[display6!i]" if exist6 == 1 :
            if clear6 == 1:
                hide screen MenuPageButtons
                hide screen fakeTextBox
                if setEventJump6 == "":
                    $ display = display6
                    $ choiceName = display6
                    $ MenuLineSceneCheckMark = -1
                    call sortMenuD from _call_sortMenuD_19
                    if monsterEncounter:
                        return
                else:
                    $ isEventNow = 1
                    $ currentChoice = 0
                    $ DataLocation = getFromName(setEventJump6, EventDatabase)
                    if setEventSceneJump6 != "":
                        $ currentChoice = getFromNameOfScene(setEventSceneJump6, EventDatabase[DataLocation].theEvents)
                    jump sortMenuD
            else:
                call recheckMenu from _call_recheckMenu_5
                if monsterEncounter:
                    return
        "[finalOption!i]" if hasattr(store, "finalSet") and finalSet == 1:
            hide screen MenuPageButtons
            hide screen fakeTextBox
            if finalOptionEvent == "":
                $ display = finalOption
                $ choiceName = finalOption
                $ MenuLineSceneCheckMark = -1
                call sortMenuD from _call_sortMenuD_82
                if monsterEncounter:
                    return
            else:
                $ isEventNow = 1
                $ currentChoice = 0
                $ DataLocation = getFromName(finalOptionEvent, EventDatabase)
                if finalOptionEventScene != "":
                    $ currentChoice = getFromNameOfScene(finalOptionEventScene, EventDatabase[DataLocation].theEvents)
                jump sortMenuD
    return
label JsonFuncApplyStatusEffect:
    $ lineOfScene += 1
    $ skillAt = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
    $ statusSkill = SkillsDatabase[skillAt]

    if statusSkill.statusEffect != "Damage" and statusSkill.statusEffect != "Defence" and statusSkill.statusEffect != "Power" and statusSkill.statusEffect != "Technique" and statusSkill.statusEffect != "Willpower" and statusSkill.statusEffect != "Intelligence" and statusSkill.statusEffect != "Allure" and statusSkill.statusEffect != "Luck" and skillChoice.statusEffect != "%Power" and skillChoice.statusEffect != "%Technique" and skillChoice.statusEffect != "%Intelligence" and skillChoice.statusEffect != "%Willpower" and skillChoice.statusEffect != "%Allure" and skillChoice.statusEffect != "%Luck" and statusSkill.statusEffect != "Escape" and statusSkill.statusEffect != "Crit" and skillChoice.statusEffect != "TargetStances":
        if monsterEncounter:
            $ player = statusAfflict(player, statusSkill, monsterEncounter[CombatFunctionEnemytarget])
        else:
            $ player = statusAfflict(player, statusSkill)
    else:
        if monsterEncounter:
            $ holder = statusBuff(player, monsterEncounter[CombatFunctionEnemytarget], statusSkill, 1)
        else:
            $ holder = statusBuff(player, player, statusSkill, 1)

        $ player = holder[0]

    if statusSkill.statusEffect == "Restrain":
        $ player.restraintStruggle = copy.copy(statusSkill.restraintStruggle)
        $ player.restraintStruggleCharmed = copy.copy(statusSkill.restraintStruggleCharmed)
        $ player.restraintEscaped = copy.copy(statusSkill.restraintEscaped)
        $ player.restraintEscapedFail = copy.copy(statusSkill.restraintEscapedFail)
        if len(monsterEncounter) >= 1:
            $ player.restrainer = monsterEncounter[CombatFunctionEnemytarget]
    return
label JsonFuncAllowRunning:
    $ canRun = True
    return
label JsonFuncCombatEncounter:
    $ lineOfScene += 1
    $ monsterEncounter = []
    $ monsterEncounterCG = []
    $ trueMonsterEncounter = []
    $ monNum = 0
    $ runBG = ""
    $ runAndStayInEvent = 0
    $ checkPreFuncs = 0
    $ combatItems = 0

    while checkPreFuncs == 0:
        if displayingScene.theScene[lineOfScene] == "NoRunning":
            $ canRun = False
            $ lineOfScene += 1

        elif displayingScene.theScene[lineOfScene] == "SetBGOnRun":
            $ lineOfScene += 1
            $ runBG = changeBG(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "DenyInventory":
            $ combatItems = 1
            $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "RunningWontSkipEvent":
            $ runAndStayInEvent = 1
            $ lineOfScene += 1
        else:
            $ checkPreFuncs += 1

    while displayingScene.theScene[lineOfScene] != "StartCombat":
        $ insertToLocation = len(monsterEncounter)
        $ addMonsterTo(displayingScene.theScene[lineOfScene], monsterEncounter, insertToLocation)
        #$ monsterEncounter[monNum] = monsterEncounter[monNum].statusEffects.refresh( monsterEncounter[monNum])
        $ addMonsterTo(displayingScene.theScene[lineOfScene], trueMonsterEncounter, insertToLocation)
        #$ trueMonsterEncounter[monNum] = trueMonsterEncounter[monNum].statusEffects.refresh(trueMonsterEncounter[monNum])
        $ lineOfScene += 1
        $ checkPreFuncs = 0
        while checkPreFuncs == 0:
            if displayingScene.theScene[lineOfScene] == "ApplyStance":
                $ lastAttack = Skill()
                $ lineOfScene += 1
                $ givingStance = displayingScene.theScene[lineOfScene]
                $ lineOfScene += 1
                python:
                    try:
                        if displayingScene.theScene[lineOfScene] == "SetAttack":
                            lineOfScene += 1
                            lastAttack = SkillsDatabase[getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)]
                        else:
                            lineOfScene -= 1
                    except:
                        lineOfScene -= 1
                $ monsterEncounter[monNum].giveStance(givingStance, player, lastAttack)
                $ player.giveStance(givingStance, monsterEncounter[monNum], lastAttack)
                $ lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "Restrainer":
                $ player.restrainer = monsterEncounter[monNum]
                $ lineOfScene += 1
            else:
                $ checkPreFuncs += 1
        $ monNum += 1
    $ monsterEncounter = NumberMonsters(monsterEncounter)
    $ SceneCharacters = []
    if monsterEncounter:
        $ HoldingSceneForCombat = copy.deepcopy(displayingScene)
        $ HoldingLineForCombat = copy.copy(lineOfScene)
        $ HoldingDataLocForCombat = copy.deepcopy(DataLocation)
        call combat from _call_combat_1
        if HoldingSceneForCombat != Dialogue():
            $ displayingScene = copy.deepcopy(HoldingSceneForCombat)
            $ lineOfScene = copy.copy(HoldingLineForCombat)
            $ DataLocation = copy.deepcopy(HoldingDataLocForCombat)
            $ HoldingSceneForCombat = Dialogue()
            $ HoldingLineForCombat = 0
            $ HoldingDataLocForCombat = 0

    $ stunnedGridPlayer = -1
    return
label JsonFuncMiniGameSnake:
    call ParadeGameInit from _call_ParadeGameInit
    hide screen SnakeGameScreen
    return
label JsonFuncFishingMiniGame:
    $ AppearTimerMin = 100
    $ AppearTimerMax = 500
    $ DifficultyTimerMin = 175
    $ DifficultyTimerMax = 250
    $ ReelsNeeded = 1
    $ FishingPassJump = ""
    $ FishingFailJump = ""
    $ FishingJump = ""

    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] == "AppearTimerRange":
            $ lineOfScene += 1
            $ AppearTimerMin = int(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ AppearTimerMax = int(displayingScene.theScene[lineOfScene])
        elif displayingScene.theScene[lineOfScene] == "FailTimerRange":
            $ lineOfScene += 1
            $ DifficultyTimerMin = int(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ DifficultyTimerMax = int(displayingScene.theScene[lineOfScene])
        elif displayingScene.theScene[lineOfScene] == "ReelsNeeded":
            $ lineOfScene += 1
            $ ReelsNeeded = int(displayingScene.theScene[lineOfScene])
        elif displayingScene.theScene[lineOfScene] == "FishingPassJump":
            $ lineOfScene += 1
            $ FishingPassJump = displayingScene.theScene[lineOfScene]
        elif displayingScene.theScene[lineOfScene] == "FishingFailJump":
            $ lineOfScene += 1
            $ FishingFailJump = displayingScene.theScene[lineOfScene]

    call fishingMiniGame from _call_fishingMiniGame

    $ display = FishingJump

    call sortMenuD from _call_sortMenuD_102
    return
label JsonFuncJumpToScene:
    $ lineOfScene += 1
    $ display = displayingScene.theScene[lineOfScene]

    call sortMenuD from _call_sortMenuD_20
    return
label JsonFuncJumpToRandomScene:
    $ lineOfScene += 1

    $ randomSelection = []

    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ passcheck = 0
        $ display = ""
        call SceneRequiresCheck from _call_SceneRequiresCheck_1

        if passcheck == 1:
            $ randomSelection.append(displayingScene.theScene[lineOfScene])
        $ lineOfScene += 1

    $ renpy.random.shuffle(randomSelection)
    $ display = randomSelection[0]
    $ randomSelection = []
    call sortMenuD from _call_sortMenuD_22
    return
label JsonFuncJumpToEvent:
    $ lineOfScene += 1
    $ DialogueIsFrom = "Event"
    $ isEventNow = 1
    $ currentChoice = 0
    $ Speaker = Character(_(''))
    $ DataLocation = getFromName(displayingScene.theScene[lineOfScene], EventDatabase)

    jump sortMenuD
    return
label JsonFuncJumpToEventThenScene:
    $ lineOfScene += 1
    $ DialogueIsFrom = "Event"
    $ isEventNow = 1
    $ currentChoice = 0
    $ Speaker = Character(_(''))
    $ DataLocation = getFromName(displayingScene.theScene[lineOfScene], EventDatabase)
    $ lineOfScene += 1
    $ currentChoice = getFromNameOfScene(displayingScene.theScene[lineOfScene], EventDatabase[DataLocation].theEvents)

    jump sortMenuD
    return
label JsonFuncCallNextSceneJumpThenReturn:
    $ callNextJump = 2
    $ inCalledSceneJump = 2

    $ specifyCurrentChoice = 0
    $ showingDream = []

    label playSceneJump:
        if callNextJump == 1:
            $ specifyCurrentChoice = getFromNameOfScene(display, EventDatabase[DataLocation].theEvents)
            $ showingDream.append(copy.deepcopy(EventDatabase[DataLocation]))
            $ callNextJump = 0
            $ inCalledSceneJump = 0
            call TimeEvent(CardType="Any", LoopedList=showingDream) from _call_TimeEvent_17
            return
    return
label JsonFuncCallSceneThenReturn:
    $ lineOfScene += 1
    $ specifyCurrentChoice = 0
    $ specifyCurrentChoice = getFromNameOfScene(displayingScene.theScene[lineOfScene], EventDatabase[DataLocation].theEvents)

    $ showingDream = []
    $ showingDream.append(copy.deepcopy(EventDatabase[DataLocation]))
    call TimeEvent(CardType="Any", LoopedList=showingDream) from _call_TimeEvent_8
    return
label JsonFuncCallEventAndSceneThenReturn:
    $ lineOfScene += 1

    $ specifyDataLocation = getFromName(displayingScene.theScene[lineOfScene], EventDatabase)

    $ lineOfScene += 1
    $ specifyCurrentChoice = 0
    $ specifyCurrentChoice = getFromNameOfScene(displayingScene.theScene[lineOfScene], EventDatabase[specifyDataLocation].theEvents)

    $ showingDream = []
    $ showingDream.append(copy.deepcopy(EventDatabase[specifyDataLocation]))

    call TimeEvent(CardType="Any", LoopedList=showingDream) from _call_TimeEvent_9
    return
label JsonFuncCallCombatEventAndScene:
    $ lineOfScene += 1
    $ DialogueIsFrom = "Event"
    $ isEventNow = 1
    $ currentChoice = 0
    $ HideOrgasmLine = 1

    $ DataLocation = getFromName(displayingScene.theScene[lineOfScene], EventDatabase)
    $ lineOfScene += 1
    $ currentChoice = getFromNameOfScene(displayingScene.theScene[lineOfScene], EventDatabase[DataLocation].theEvents)

    call sortMenuD from _call_sortMenuD_30
    return
label JsonFuncJumpToNPCEvent:
    $ lineOfScene += 1
    $ DialogueIsFrom = "NPC"
    $ isEventNow = 1
    $ currentChoice = 0
    $ EnteringLocationCheck = 0
    $ DataLocation = getFromName(displayingScene.theScene[lineOfScene], EventDatabase)
    jump sortMenuD
    return
label JsonFuncJumpToNPCEventThenScene:
    $ lineOfScene += 1
    $ DialogueIsFrom = "NPC"
    $ isEventNow = 1
    $ currentChoice = 0

    $ DataLocation = getFromName(displayingScene.theScene[lineOfScene], EventDatabase)
    $ lineOfScene += 1
    $ currentChoice = getFromNameOfScene(displayingScene.theScene[lineOfScene], EventDatabase[DataLocation].theEvents)
    $ EnteringLocationCheck = 0
    jump sortMenuD
    return
label JsonFuncJumpToLossEvent:
    hide screen ON_EnemyCardScreen
    $ lineOfScene += 1
    $ DialogueIsFrom = "LossEvent"
    $ isEventNow = 1
    $ currentChoice = 0

    $ DataLocation = getFromName(displayingScene.theScene[lineOfScene], EventDatabase)
    jump sortMenuD
    return
label JsonFuncForceAutoSave:
    $ renpy.force_autosave(block=True)
    return
label JsonFuncExitGridmap:
    $ onGridMap = 0
    $ runAndStayInEvent = 0
    $ RanAway = "False"
    $ InventoryAvailable = True
    $ DenyGridInventory = False
    hide screen Gridmap
    hide screen GridmapPlayer
    hide screen GridmapNPCs
    hide screen GridmapObstacles
    hide screen gridMoveKeys
    $ TheGrid = []
    return
# Combat funcs
label JsonFuncResetStatCheckDifficultyModifer:
    $ increaseStatCheck = 0
    return
label JsonFuncAddMonsterToEncounter:
    $ lineOfScene += 1
    $ replacingMonster = 0
    $ insertToLocation = len(monsterEncounter)
    if displayingScene.theScene[lineOfScene] == "ChangeForm":
        $ lineOfScene += 1
        $ replacingMonster = 1
        $ insertToLocation = copy.deepcopy(CombatFunctionEnemytarget)
        $ KeepingHP = copy.copy(monsterEncounter[CombatFunctionEnemytarget].stats.hp)
        $ KeepingSP = copy.copy(monsterEncounter[CombatFunctionEnemytarget].stats.sp)
        $ KeepingStatusEffects = copy.deepcopy(monsterEncounter[CombatFunctionEnemytarget].statusEffects)
        $ KeepingStances = copy.deepcopy(monsterEncounter[CombatFunctionEnemytarget].combatStance)

        python:
            del monsterEncounter[CombatFunctionEnemytarget]
            del trueMonsterEncounter[CombatFunctionEnemytarget]

    $ addMonsterTo(displayingScene.theScene[lineOfScene], monsterEncounter, insertToLocation)
    $ monsterEncounter[insertToLocation] = monsterEncounter[insertToLocation].statusEffects.refresh(monsterEncounter[insertToLocation])
    $ addMonsterTo(displayingScene.theScene[lineOfScene], trueMonsterEncounter,insertToLocation)
    $ trueMonsterEncounter[insertToLocation] = trueMonsterEncounter[insertToLocation].statusEffects.refresh(trueMonsterEncounter[insertToLocation])

    if replacingMonster == 0:
        $ monInititive.append(-999)
        $ monSkillChoice.append( getSkill(" ", SkillsDatabase))

    else:
        $ monsterEncounter[insertToLocation].stats.hp = copy.copy(KeepingHP)
        $ monsterEncounter[insertToLocation].stats.sp = copy.copy(KeepingSP)
        $ monsterEncounter[insertToLocation].statusEffects = copy.deepcopy(KeepingStatusEffects)
        $ monsterEncounter[insertToLocation].combatStance = copy.deepcopy(KeepingStances)

        python:
            del KeepingHP, KeepingStatusEffects, KeepingStances
            try:
                del KeepingStatusEffects
            except:
                pass

    if nightmare == 1:
        $ goToLevel = player.stats.lvl
        python:
            if goToLevel > monsterEncounter[insertToLocation].stats.lvl:
                monsterEncounter[insertToLocation].levelUp(goToLevel)

                eroMod = 0.5
                lvlchek = monsterEncounter[insertToLocation].stats.lvl
                monsterEncounter[insertToLocation].moneyDropped = int(((lvlchek)^2+(lvlchek*10)+48)*eroMod)

                expMod = 0.35
                lvlchek = monsterEncounter[insertToLocation].stats.lvl
                monsterEncounter[insertToLocation].stats.Exp = int(((0.4*(lvlchek*lvlchek))+(2*lvlchek)+(15*math.sqrt(lvlchek)-8))*expMod)

    $ monsterEncounter[insertToLocation] = initiateImageLayers(monsterEncounter[insertToLocation])
    python:
        for SetData in persistantMonSetData:
            if SetData.name == monsterEncounter[insertToLocation].IDname:
                monsterEncounter[insertToLocation].currentSet = getFromName(SetData.startingSet, monsterEncounter[insertToLocation].ImageSets)

        c = 0
        for each in monsterEncounter:
            monsterEncounter[c].name = copy.copy(trueMonsterEncounter[c].name)

            c += 1
    $ monsterEncounter = NumberMonsters(monsterEncounter)

    $ m = -1
    $ ar = 0
    while ar < len(monsterEncounter[m].combatDialogue):
        $ specifyStance = 0
        if ar < len(monsterEncounter[m].combatDialogue):
            if monsterEncounter[m].combatDialogue[ar].lineTrigger == "MonsterArrived":
                $ CombatFunctionEnemytarget = m
                $ Speaker = Character(_(monsterEncounter[m].name))
                $ display = monsterEncounter[m].combatDialogue[ar].theText[renpy.random.randint(-1, len(monsterEncounter[m].combatDialogue[ar].theText)-1)]
                call read from _call_read_55
        $ ar += 1
    return
label JsonFuncDamagePlayerFromMonster:
    $ recoil = 0
    $ critText = ""
    $ effectiveText = ""
    $ lineOfScene += 1
    $ MonAt = getFromName(displayingScene.theScene[lineOfScene], MonsterDatabase)
    $ holder = MonsterDatabase[MonAt]
    $ lineOfScene += 1
    $ skillAt = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
    $ holder = AttackCalc(holder, player,  SkillsDatabase[skillAt], 1)
    $ finalDamage = holder[0]
    $ critText = holder[2]
    $ effectiveText = holder[5]
    if len(monsterEncounter) >= 1:
        $ recoil = holder[4]
        $ recoil =  int(math.floor(recoil))
        $ monsterEncounter[CombatFunctionEnemytarget].stats.hp += recoil

    $ player.stats.hp += holder[0]
    $ holder = []
    return
# Assorted funcs
label JsonFuncTimeBecomesNight:
    if TimeOfDay == Morning:
        $ TimeOfDay = MorningNight
    elif TimeOfDay == Noon:
        $ TimeOfDay = NoonNight
    elif TimeOfDay == Afternoon:
        $ TimeOfDay = AfternoonNight
    elif TimeOfDay == DuskDay:
        $ TimeOfDay = Dusk
    elif TimeOfDay == EveningDay:
        $ TimeOfDay = Evening
    elif TimeOfDay == MidnightDay:
        $ TimeOfDay = Midnight
    $ bg = bgToNightDay(bg, ".png", "Night.png")
    return
label JsonFuncTimeBecomesDay:
    if TimeOfDay == MorningNight:
        $ TimeOfDay = Morning
    elif TimeOfDay == NoonNight:
        $ TimeOfDay = Noon
    elif TimeOfDay == AfternoonNight:
        $ TimeOfDay = Afternoon
    elif TimeOfDay == Dusk:
        $ TimeOfDay = DuskDay
    elif TimeOfDay == Evening:
        $ TimeOfDay = EveningDay
    elif TimeOfDay == Midnight:
        $ TimeOfDay = MidnightDay
    $ bg = bgToNightDay(bg, "Night.png", ".png")
    return
label JsonFuncTimeBecomesNormal:
    if TimeOfDay == MorningNight:
        $ TimeOfDay = Morning
        $ bg = bgToNightDay(bg, "Night.png", ".png")
    elif TimeOfDay == NoonNight:
        $ TimeOfDay = Noon
        $ bg = bgToNightDay(bg, "Night.png", ".png")
    elif TimeOfDay == AfternoonNight:
        $ TimeOfDay = Afternoon
        $ bg = bgToNightDay(bg, "Night.png", ".png")

    if TimeOfDay == DuskDay:
        $ TimeOfDay = Dusk
        $ bg =  bgToNightDay(bg, ".png", "Night.png")
    elif TimeOfDay == EveningDay:
        $ TimeOfDay = Evening
        $ bg =  bgToNightDay(bg, ".png", "Night.png")
    elif TimeOfDay == MidnightDay:
        $ TimeOfDay = Midnight
        $ bg =  bgToNightDay(bg, ".png", "Night.png")
    return
label JsonFuncDisplaySavedLine:
    $ display = savedLine
    call read from _call_read_52
    return
label JsonFuncUseSavedLineInMenu:
    $ savedLineInMenu = 1
    return
label JsonFuncCallLossLevelUp:
    $ NoGameOver = 1
    call lostExpCheck from _call_lostExpCheck
    return
label JsonFuncUseHeldBG:
    if heldBG != "":
        $ heldBG =  bgToNightDay(heldBG, "Night.png", ".png")
        $ bg  = changeBG(copy.copy(heldBG))
    $ heldBG = ""
    return
label JsonFuncHideTreasureChest:
    hide chest
    return
label JsonFuncHasErosLessThan:
    $ lineOfScene += 1
    if int(displayingScene.theScene[lineOfScene]) > player.inventory.money:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_15
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncAllowInventory:
    $ InventoryAvailable = True
    return
label JsonFuncDenyInventory:
    $ InventoryAvailable = False
    return
label JsonFuncBumpToTown:
    jump Town
    return
label JsonFuncGameOver:
    $ LostGameOver = 1
    $ NoGameOver = 0
    jump lostExpCheck
    return
label JsonFuncTrueGameOver:
    $ renpy.full_restart()
    return
label JsonFuncQuestComplete:
    if DialogueIsFrom == "Event":
        $ ProgressEvent[DataLocation].questComplete = 1
    return
label JsonFuncAdventureComplete:
    $ lineOfScene += 1
    $ AdvLocation = getFromName(displayingScene.theScene[lineOfScene], ProgressAdventure)
    $ ProgressAdventure[AdvLocation].questComplete = 1
    return
label JsonFuncHasErosLessThanInput:
    if debt > player.inventory.money:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_3
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncAddInputToProgress:
    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
    $ ProgressEvent[DataLocation].eventProgress += int(math.floor(debt))
    return
label JsonFuncRespecPlayer:
    $ player.respec()
    $ sexResCap = 150
    $ assResCap = 150
    $ nipResCap = 200
    $ chuResCap = 150
    $ seducResCap = 150
    $ magResCap = 150
    $ painResCap = 150
    $ hpFloor = 50
    $ epFloor = 20
    $ spFloor = 1
    $ powFloor = 1
    $ spdFloor = 1
    $ intFloor = 1
    $ allFloor = 1
    $ wilFloor = 1
    $ lukFloor = 1
    $ respeccing = 1
    $ hasResPoints = 1
    hide screen ON_HealthDisplay
    hide screen ON_HealthDisplayBacking

    $ tentativeStats = copy.deepcopy(player)
    call characterCreation from _call_characterCreation_2
    call setStatFloors from _call_setStatFloors_5
    $ favorPool = CalcGoddessFavor(player)
    show screen ON_HealthDisplayBacking #(_layer="hplayer")
    show screen ON_HealthDisplay #(_layer="sayScreen")
    $ respeccing = 0
    return
label JsonFuncDonateToGoddess:
    call DonateToGoddess from _call_DonateToGoddess
    return
label JsonFuncPurgeFetishes:
    call PurgeFetishes from _call_PurgeFetishes
    return
label JsonFuncAddTributeToProgress:
    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
    $ ProgressEvent[DataLocation].eventProgress += int(math.floor(tribute))
    $ tribute = 0
    return
label JsonFuncLevelUpMonster:
    $ lineOfScene += 1
    $ goToLevel = monsterEncounter[CombatFunctionEnemytarget].stats.lvl
    if displayingScene.theScene[lineOfScene] == "MatchPlayer":
        $ goToLevel = player.stats.lvl
    elif displayingScene.theScene[lineOfScene] == "GoUpByProgress":
        $ goToLevel += ProgressEvent[DataLocation].eventProgress
    elif displayingScene.theScene[lineOfScene] == "GoUpByProgressFromOtherEvent":
        $ lineOfScene += 1
        $ locOfProg = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
        $ goToLevel += ProgressEvent[locOfProg].eventProgress
    else:
        $ goToLevel += int(displayingScene.theScene[lineOfScene])

    if goToLevel > monsterEncounter[CombatFunctionEnemytarget].stats.lvl:
        $ monsterEncounter[CombatFunctionEnemytarget].levelUp(goToLevel)
    return
label JsonFuncEnergyDrain:
    $ lineOfScene += 1
    $ energyLost = int(displayingScene.theScene[lineOfScene])
    $ Drain = energyLost * (1+getVirility(player)*0.01)
    $ Drain *= (renpy.random.randint(75, 125)*0.01)
    $ Drain = math.floor(Drain)
    $ Drain = int(Drain)
    $ player.stats.ep -= Drain
    $ recoverAmount = Drain
    return
label JsonFuncApplyStance:
    if monsterEncounter:
        $ lineOfScene += 1
        $ givingStance = displayingScene.theScene[lineOfScene]

        $ lineOfScene += 1
        python:
            try:
                if displayingScene.theScene[lineOfScene] == "SetAttack":
                    lineOfScene += 1
                    lastAttack = SkillsDatabase[getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)]
                else:
                    lineOfScene -= 1
            except:
                lineOfScene -= 1

        $ monsterEncounter[CombatFunctionEnemytarget].giveStance(givingStance, player, lastAttack, holdoverDura=stanceDurabilityHoldOverAttacker)
        $ player.giveStance(givingStance, monsterEncounter[CombatFunctionEnemytarget], lastAttack, holdoverDura=stanceDurabilityHoldOverTarget)
    return
label JsonFuncApplyStanceToOtherMonster:
    if monsterEncounter:
        $ lineOfScene += 1
        $ monName = displayingScene.theScene[lineOfScene]
        $ lineOfScene += 1
        $ givingStance = displayingScene.theScene[lineOfScene]

        $ stancePass = 0
        $ found = -1
        $ C = 0
        python:
            for each in trueMonsterEncounter:
                stancePass = 0
                if C != CombatFunctionEnemytarget:
                    if each.name == monName:
                        for stance in monsterEncounter[C].combatStance:
                            if stance.Stance == givingStance:
                                stancePass = 2
                        if stancePass != 2:
                            stancePass = 1
                            found = copy.deepcopy(C)
                C += 1
        if found != -1:
            $ lineOfScene += 1
            python:
                try:
                    if displayingScene.theScene[lineOfScene] == "SetAttack":
                        lineOfScene += 1
                        lastAttack = SkillsDatabase[getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)]
                    else:
                        lineOfScene -= 1
                except:
                    lineOfScene -= 1

            $ monsterEncounter[found].giveStance(givingStance, player, lastAttack, holdoverDura=stanceDurabilityHoldOverAttacker)
            $ player.giveStance(givingStance, monsterEncounter[found], lastAttack, holdoverDura=stanceDurabilityHoldOverTarget)
            $ CombatFunctionEnemytarget = copy.deepcopy(found)
    return
label JsonFuncEncounterSizeGreaterOrEqualTo:
    if monsterEncounter:
        $ lineOfScene += 1
        if len(monsterEncounter) >= int(displayingScene.theScene[lineOfScene]):
            $ lineOfScene += 1
            $ display = displayingScene.theScene[lineOfScene]
            call sortMenuD from _call_sortMenuD_37
            return
        else:
            $ lineOfScene += 1
    return
label JsonFuncEncounterSizeLessOrEqualTo:
    if monsterEncounter:
        $ lineOfScene += 1
        if len(monsterEncounter) <= int(displayingScene.theScene[lineOfScene]):
            $ lineOfScene += 1
            $ display = displayingScene.theScene[lineOfScene]
            call sortMenuD from _call_sortMenuD_38
            return
        else:
            $ lineOfScene += 1
    return
label JsonFuncRecalculateMonsterErosDrop:
    $ lineOfScene += 1
    $ eroMod = 1
    if lineOfScene < len(displayingScene.theScene):
        if displayingScene.theScene[lineOfScene] == "AlterByPercent":
            $ lineOfScene += 1
            $ eroMod = int(displayingScene.theScene[lineOfScene])*0.01
        else:
            $ lineOfScene -= 1
    else:
        $ lineOfScene -= 1
    $ lvlchek = monsterEncounter[CombatFunctionEnemytarget].stats.lvl
    $ monsterEncounter[CombatFunctionEnemytarget].moneyDropped = int(((lvlchek)^2+(lvlchek*10)+48)*eroMod)
    return
label JsonFuncRecalculateMonsterExpDrop:
    $ lineOfScene += 1
    $ expMod = 1
    if lineOfScene < len(displayingScene.theScene):
        if displayingScene.theScene[lineOfScene] == "AlterByPercent":
            $ lineOfScene += 1
            $ expMod = int(displayingScene.theScene[lineOfScene])*0.01
        else:
            $ lineOfScene -= 1
    else:
        $ lineOfScene -= 1
    $ lvlchek = monsterEncounter[CombatFunctionEnemytarget].stats.lvl
    $ monsterEncounter[CombatFunctionEnemytarget].stats.Exp = int(((0.4*(lvlchek*lvlchek))+(2*lvlchek)+(15*math.sqrt(lvlchek)-8))*expMod)
    return
label JsonFuncRefreshMonster:
    $ monsterEncounter[CombatFunctionEnemytarget] = monsterEncounter[CombatFunctionEnemytarget].statusEffects.refresh(monsterEncounter[CombatFunctionEnemytarget])
    $ monsterEncounter[CombatFunctionEnemytarget].stats.refresh()
    return
label JsonFuncCallMonsterEncounterOrgasmCheck:
    $ orgasmTarget = monsterEncounter[CombatFunctionEnemytarget]
    $ orgasmCauser = player
    call setDefender(monsterEncounter[CombatFunctionEnemytarget]) from _call_setDefender_2

    call theOrgasmCheck from _call_theOrgasmCheck_1
    call MonsterLossCheck from _call_MonsterLossCheck_2

    if len(monsterEncounter) <= 0:
        jump combatWin
    return
label JsonFuncMonsterOrgasm:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].stats.hp = 0
    $ spiritLost = SpiritCalulation(monsterEncounter[CombatFunctionEnemytarget], int(displayingScene.theScene[lineOfScene]))
    $ monsterEncounter[CombatFunctionEnemytarget].stats.sp -= spiritLost
    if monsterEncounter[CombatFunctionEnemytarget].stats.sp <= 0:
        $ monsterEncounter[CombatFunctionEnemytarget].stats.sp = 0
    if monsterEncounter[CombatFunctionEnemytarget].stats.sp > monsterEncounter[CombatFunctionEnemytarget].stats.max_true_sp:
        $ monsterEncounter[CombatFunctionEnemytarget].stats.sp = monsterEncounter[CombatFunctionEnemytarget].stats.max_true_sp
    return
label JsonFuncApplyStatusEffectToMonster:
    $ lineOfScene += 1
    $ skillAt = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
    $ statusSkill = SkillsDatabase[skillAt]

    if statusSkill.statusEffect != "Damage" and statusSkill.statusEffect != "Defence" and statusSkill.statusEffect != "Power" and statusSkill.statusEffect != "Technique" and statusSkill.statusEffect != "Intelligence" and statusSkill.statusEffect != "Willpower" and statusSkill.statusEffect != "Allure" and statusSkill.statusEffect != "Luck" and skillChoice.statusEffect != "%Power" and skillChoice.statusEffect != "%Technique" and skillChoice.statusEffect != "%Intelligence" and skillChoice.statusEffect != "%Willpower" and skillChoice.statusEffect != "%Allure" and skillChoice.statusEffect != "%Luck" and statusSkill.statusEffect != "Escape" and statusSkill.statusEffect != "Crit" and skillChoice.statusEffect != "TargetStances":
        $ monsterEncounter[CombatFunctionEnemytarget] = statusAfflict(monsterEncounter[CombatFunctionEnemytarget], statusSkill)
    else:
        $ holder = statusBuff(monsterEncounter[CombatFunctionEnemytarget], monsterEncounter[CombatFunctionEnemytarget], statusSkill, 1)
        $ monsterEncounter[CombatFunctionEnemytarget] = holder[0]
    if statusSkill.statusEffect == "Restrain":
        $ monsterEncounter[CombatFunctionEnemytarget].restraintStruggle = copy.copy(statusSkill.restraintStruggle)
        $ monsterEncounter[CombatFunctionEnemytarget].restraintStruggleCharmed = copy.copy(statusSkill.restraintStruggleCharmed)
        $ monsterEncounter[CombatFunctionEnemytarget].restraintEscaped = copy.copy(statusSkill.restraintEscaped)
        $ monsterEncounter[CombatFunctionEnemytarget].restraintEscapedFail = copy.copy(statusSkill.restraintEscapedFail)
        $ monsterEncounter[CombatFunctionEnemytarget].restrainer = player
    return
label JsonFuncRefocusOnInitialMonster:
    $ CombatFunctionEnemytarget = copy.deepcopy(CombatFunctionEnemyInitial)
    return
label JsonFuncFocusOnMonster:
    $ lineOfScene += 1
    if int(displayingScene.theScene[lineOfScene]) <= len(monsterEncounter):
        $ CombatFunctionEnemytarget = int(displayingScene.theScene[lineOfScene])-1
    else:
        $ CombatFunctionEnemytarget = len(monsterEncounter)-1
    return
label JsonFuncFocusOnRandomMonster:
    if len(monsterEncounter) >= 1:
        $ CombatFunctionEnemytarget = renpy.random.randint(0, len(monsterEncounter)-1)
    return
label JsonFuncFocusedSpeaks:
    if len(monsterEncounter) >= 1:
        #$ Speaker = monsterEncounter[CombatFunctionEnemytarget].name + attackTitle

        $ Speaker = Character(_(monsterEncounter[CombatFunctionEnemytarget].name) + attackTitle,
                                what_prefix='"',
                                what_suffix='"')
        $ lineOfScene += 1
        $ readLine = 1
    return
label JsonFuncFocusedSpeaksSkill:
    if len(monsterEncounter) >= 1:
        #$ Speaker = monsterEncounter[CombatFunctionEnemytarget].name + attackTitle

        $ Speaker = Character(_(monsterEncounter[CombatFunctionEnemytarget].name) + attackTitle )
        $ lineOfScene += 1
        $ readLine = 1
    return
label JsonFuncCallMonsterAttack:
    if monsterEncounter:
        $ specified = 0
        $ lineOfScene += 1
        $ m = CombatFunctionEnemytarget
        python:
            try:
                if displayingScene.theScene[lineOfScene] == "SpecificAttack":
                    lineOfScene += 1
                    specified = 1
                    monSkillChoice[CombatFunctionEnemytarget] = SkillsDatabase[getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)]
                else:
                    lineOfScene -= 1
            except:
                lineOfScene -= 1

        $ HoldingSceneCA = copy.deepcopy(displayingScene)
        $ HoldingLineCA = copy.copy(lineOfScene+1)
        $ HoldingDataLocCA = copy.deepcopy(DataLocation)

        if(monsterEncounter[CombatFunctionEnemytarget].statusEffects.stunned.duration > 0):
            $ display = monsterEncounter[CombatFunctionEnemytarget].name + " is stunned and cannot act!"
            "[display!i]"
        else:
            if specified == 0:
                $ pickNewSkill = 1
                call enemySkillChoice(mSC=CombatFunctionEnemytarget) from _call_enemySkillChoice_1

            $ skillcheck = monSkillChoice[CombatFunctionEnemytarget]
            if player.statusEffects.sleep.potency < 5:
                $ Speaker = Character(_(monsterEncounter[CombatFunctionEnemytarget].name + " - " + monSkillChoice[CombatFunctionEnemytarget].name))
            else:
                $ Speaker = Character(_(monsterEncounter[CombatFunctionEnemytarget].name))
            $ attacker = monsterEncounter[CombatFunctionEnemytarget]
            $ defender = player
            $ skillChoice = monSkillChoice[CombatFunctionEnemytarget]
            call combatActionTurn from _call_combatActionTurn_2
            #call EnemyTurn from _call_EnemyTurn

        #$ display = ""
        $ LastDisplayOrder = []
        if HoldingSceneCA != Dialogue():
            $ displayingScene = copy.deepcopy(HoldingSceneCA)
            $ lineOfScene = copy.copy(HoldingLineCA)
            $ DataLocation = copy.deepcopy(HoldingDataLocCA)
        $ HoldingSceneCA = Dialogue()
        $ HoldingLineCA = 0
        $ HoldingDataLocCA = 0

        if len(monsterEncounter) == 0: #combat is over due to recoil
            jump combatWin

        jump resumeSceneAfterCombat
    return
label JsonFuncHitPlayerWith:
    $ recoil = 0
    $ lineOfScene += 1
    $ attacker = monsterEncounter[CombatFunctionEnemytarget]
    $ defender = player
    $ skillAt = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
    $ holder = AttackCalc(monsterEncounter[CombatFunctionEnemytarget], player,  SkillsDatabase[skillAt], 1)
    $ finalDamage = holder[0]
    $ critText = holder[2]
    $ effectiveText = holder[5]
    $ recoil = holder[4]
    $ recoil =  int(math.floor(recoil))
    $ monsterEncounter[CombatFunctionEnemytarget].stats.hp += recoil
    $ recoilHit = recoil
    $ player.stats.hp += holder[0]
    return
label JsonFuncHitMonsterWith:
    $ lineOfScene += 1
    $ attacker = player
    $ defender = monsterEncounter[CombatFunctionEnemytarget]
    $ skillAt = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
    $ holder = AttackCalc(player, monsterEncounter[CombatFunctionEnemytarget],  SkillsDatabase[skillAt], 1)
    $ finalDamage = holder[0]
    $ critText = holder[2]
    $ effectiveText = holder[5]
    $ recoil = holder[4]
    $ recoil =  int(math.floor(recoil))
    $ player.stats.hp += recoil
    $ recoilHit = recoil
    $ monsterEncounter[CombatFunctionEnemytarget].stats.hp += holder[0]
    return
label JsonFuncDamageMonsterFromMonster:
    $ recoil = 0
    $ lineOfScene += 1
    $ MonAt = getFromName(displayingScene.theScene[lineOfScene], MonsterDatabase)
    $ holder = MonsterDatabase[MonAt]
    $ lineOfScene += 1
    $ skillAt = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
    $ holder = AttackCalc(holder, monsterEncounter[CombatFunctionEnemytarget],  SkillsDatabase[skillAt], 1)
    $ finalDamage = holder[0]
    if len(monsterEncounter) >= 1:
        $ critText = holder[2]
        $ effectiveText = holder[5]
    #    $ recoil = holder[4]
    #    $ recoil =  int(math.floor(recoil))
        #$ monsterEncounter[CombatFunctionEnemytarget].stats.hp += recoil
    $ monsterEncounter[CombatFunctionEnemytarget].stats.hp += holder[0]
    $ holder = []
    return
label JsonFuncDenyPlayerOrgasm:
    $ skipPlayerOrgasm = 1
    return
label JsonFuncDenyMonsterOrgasm:
    $ skipMonsterOrgasm = 1
    return
label JsonFuncDenyTargetOrgasm:
    $ skipTargetOrgasm = 1
    return
label JsonFuncDenyAttackerOrgasm:
    $ skipAttackOrgasm = 1
    return
label JsonFuncResumeMonsterAttack:
    $ monsterEncounter[CombatFunctionEnemytarget].skippingAttack = 0
    return
label JsonFuncResumeAllMonsterAttacks:
    python:
        for each in monsterEncounter:
            each.skippingAttack = 0
    return
label JsonFuncHideMonsterEncounter:
    if len(monsterEncounter) >= 1:
        hide screen ON_EnemyCardScreen onlayer master
        $ hidingCombatEncounter = 1
    return
label JsonFuncDefeatMonster:
    if monsterEncounter[CombatFunctionEnemytarget].restraintOnLoss[0] != "":
        $ restrainholdyLine = copy.copy(lineOfScene)
        $ restrainholdyScene= copy.deepcopy(displayingScene)
        $ restrainholdyData = copy.deepcopy(DataLocation)

        $ display = monsterEncounter[CombatFunctionEnemytarget].restraintOnLoss[renpy.random.randint(-1, len(monsterEncounter[CombatFunctionEnemytarget].restraintOnLoss)-1)]
        call read from _call_read_41

        $ lineOfScene = copy.copy(restrainholdyLine)
        $ displayingScene = copy.deepcopy(restrainholdyScene)
        $ DataLocation = copy.deepcopy(restrainholdyData)

    $ DefeatMonster(CombatFunctionEnemytarget)

    if len(monsterEncounter) <=0:
        call combatWin from _call_combatWin
    return

