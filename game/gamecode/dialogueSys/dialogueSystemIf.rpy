label JsonFuncIfChoice:
    $ lineOfScene += 1
    $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)

    while choiceToCheck-1 >= len(ProgressEvent[DataLocation].choices):
        $ ProgressEvent[DataLocation].choices.append("")


    if displayingScene.theScene[lineOfScene] == ProgressEvent[DataLocation].choices[choiceToCheck-1]:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]

        call sortMenuD from _call_sortMenuD_4
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfProgressEqualsOrGreater:
    $ lineOfScene += 1
    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
    if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[DataLocation].eventProgress:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_2
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfProgressEquals:
    $ lineOfScene += 1
    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
    if int(displayingScene.theScene[lineOfScene]) == ProgressEvent[DataLocation].eventProgress:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_1
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfProgressEqualsOrLess:
    $ lineOfScene += 1
    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
    if int(displayingScene.theScene[lineOfScene]) >= ProgressEvent[DataLocation].eventProgress:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_58
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfEventExists:
    $ lineOfScene += 1
    if getFromName(displayingScene.theScene[lineOfScene], EventDatabase) != -1:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]

        call sortMenuD from _call_sortMenuD_101
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfRanAway:
    if RanAway == "True":
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]

        call sortMenuD from _call_sortMenuD_86
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1

    $ runAndStayInEvent = 0
    $ RanAway = "False"
    return
label JsonFuncIfHealingSickness:
    if HealingSickness > 0:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]

        call sortMenuD from _call_sortMenuD_54
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfDelayingNotifications:
    $ lineOfScene += 1
    if timeNotify == 1:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_72
    return
label JsonFuncIfPlayerOrgasm:
    $ lineOfScene += 1
    if player.stats.hp >= player.stats.max_true_hp:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_5
    return
label JsonFuncIfPlayerArousalOverPercentOfMax:
    $ lineOfScene += 1
    $ Percentage = float(displayingScene.theScene[lineOfScene])*0.01
    $ lineOfScene += 1
    if player.stats.hp >= player.stats.max_true_hp*Percentage:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_56
    return
label JsonFuncIfPlayerEnergyLessThanPercent:
    $ lineOfScene += 1
    $ percentCheck = (int(displayingScene.theScene[lineOfScene]))*0.01
    $ lineOfScene += 1
    if player.stats.ep <= player.stats.max_true_ep*percentCheck:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_59
    return
label JsonFuncIfPlayerEnergyGone:
    $ lineOfScene += 1
    if player.stats.ep <= 0:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_60
    return
label JsonFuncIfPlayerSpiritGone:
    $ lineOfScene += 1
    if player.stats.sp <= 0:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_6
    return
label JsonFuncIfHasItem(whichJsonFunc):
    $ funcBoolState = 1
    if whichJsonFunc in ["IfDoesntHaveItem", "IfDoesntHaveItemEquipped"]:
        $ funcBoolState = 0
    $ checkingOnlyEquipped = 0
    if whichJsonFunc in ["IfHasItemEquipped", "IfDoesntHaveItemEquipped"]:
        $ checkingOnlyEquipped = 1
    $ lineOfScene += 1
    $ hasThing = 0
    python:
        if displayingScene.theScene[lineOfScene] == "Tags":
            requiredTags = []
            while displayingScene.theScene[lineOfScene] != "EndLoop":
                lineOfScene += 1
                if displayingScene.theScene[lineOfScene] != "EndLoop":
                    requiredTags.append(displayingScene.theScene[lineOfScene])
            requiredTagSet = set(requiredTags)
            print(requiredTagSet)
            if requiredTagSet.issubset(set(player.inventory.RuneSlotOne.tags)):
                hasThing = 1
            elif requiredTagSet.issubset(set(player.inventory.RuneSlotTwo.tags)):
                hasThing = 1
            elif requiredTagSet.issubset(set(player.inventory.RuneSlotThree.tags)):
                hasThing = 1
            elif requiredTagSet.issubset(set(player.inventory.AccessorySlot.tags)):
                hasThing = 1
            else:
                if not checkingOnlyEquipped:
                    for each in player.inventory.items:
                        if requiredTagSet.issubset(set(each.tags)):
                            hasThing = 1
        else:
            if player.inventory.RuneSlotOne.name == displayingScene.theScene[lineOfScene]:
                hasThing = 1
            if player.inventory.RuneSlotTwo.name == displayingScene.theScene[lineOfScene]:
                hasThing = 1
            if player.inventory.RuneSlotThree.name == displayingScene.theScene[lineOfScene]:
                hasThing = 1
            if player.inventory.AccessorySlot.name == displayingScene.theScene[lineOfScene]:
                hasThing = 1
            if not checkingOnlyEquipped:
                for each in player.inventory.items:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        hasThing = 1
    if hasThing == funcBoolState:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_24
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfHasItems(whichJsonFunc):
    $ funcBoolState = 1
    if whichJsonFunc in ["IfDoesntHaveItems"]:
        $ funcBoolState = 0
    $ hasThing = 0
    python:
        ItemsToFind = []
        ItemsFound = []
        while displayingScene.theScene[lineOfScene] != "EndLoop":
            lineOfScene += 1
            if displayingScene.theScene[lineOfScene] != "EndLoop":
                ItemsToFind.append(displayingScene.theScene[lineOfScene])
        if player.inventory.RuneSlotOne.name == displayingScene.theScene[lineOfScene]:
            ItemsFound.append(player.inventory.RuneSlotOne.name)
        elif player.inventory.RuneSlotTwo.name == displayingScene.theScene[lineOfScene]:
            ItemsFound.append(player.inventory.RuneSlotTwo.name)
        elif player.inventory.RuneSlotThree.name == displayingScene.theScene[lineOfScene]:
            ItemsFound.append(player.inventory.RuneSlotThree.name)
        elif player.inventory.AccessorySlot.name == displayingScene.theScene[lineOfScene]:
            ItemsFound.append(player.inventory.AccessorySlot.name)
        else:
            for each in player.inventory.items:
                for item in ItemsToFind:
                    if each.name == item:
                        if each.name not in ItemsFound:
                            ItemsFound.append(each.name)
    if ItemsToFind == ItemsFound:
        $ hasThing = 1
    if hasThing == funcBoolState:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_93
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfHasItemInInventory(whichJsonFunc):
    $ funcBoolState = 1
    if whichJsonFunc in ["IfDoesntHaveItemInInventory"]:
        $ funcBoolState = 0
    $ lineOfScene += 1
    $ hasThing = 0
    python:
        if displayingScene.theScene[lineOfScene] == "Tags":
            requiredTags = []
            while displayingScene.theScene[lineOfScene] != "EndLoop":
                lineOfScene += 1
                if displayingScene.theScene[lineOfScene] != "EndLoop":
                    requiredTags.append(displayingScene.theScene[lineOfScene])
            requiredTagSet = set(requiredTags)
            lineOfScene += 1
            for each in player.inventory.items:
                if requiredTagSet.issubset(set(each.tags)):
                    if each.NumberHeld >= int(displayingScene.theScene[lineOfScene]):
                        hasThing = 1
        else:
            ItemName = displayingScene.theScene[lineOfScene]
            lineOfScene += 1
            for each in player.inventory.items:
                if each.name == ItemName:
                    if each.NumberHeld >= int(displayingScene.theScene[lineOfScene]):
                        hasThing = 1
    if hasThing == funcBoolState:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_23
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfHasRunesEquipped:
    $ lineOfScene += 1
    $ hasThing = 0
    python:
        NumberFullyHeld = 0
        if displayingScene.theScene[lineOfScene] == "Tags":
            requiredTags = []
            while displayingScene.theScene[lineOfScene] != "EndLoop":
                lineOfScene += 1
                if displayingScene.theScene[lineOfScene] != "EndLoop":
                    requiredTags.append(displayingScene.theScene[lineOfScene])
            requiredTagSet = set(requiredTags)
            if requiredTagSet.issubset(set(player.inventory.RuneSlotOne.tags)):
                NumberFullyHeld += 1
            elif requiredTagSet.issubset(set(player.inventory.RuneSlotTwo.tags)):
                NumberFullyHeld += 1
            elif requiredTagSet.issubset(set(player.inventory.RuneSlotThree.tags)):
                NumberFullyHeld += 1
            lineOfScene += 1
        else:
            ItemName = displayingScene.theScene[lineOfScene]
            lineOfScene += 1
            if player.inventory.RuneSlotOne.name == ItemName:
                NumberFullyHeld += 1
            if player.inventory.RuneSlotTwo.name == ItemName:
                NumberFullyHeld += 1
            if player.inventory.RuneSlotThree.name == ItemName:
                NumberFullyHeld += 1
        if NumberFullyHeld >= int(displayingScene.theScene[lineOfScene]):
            hasThing = 1
    if hasThing == 1:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_63
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfHasSkill:
    $ lineOfScene += 1
    $ passSkillCheck = 0
    python:
        skill_name = displayingScene.theScene[lineOfScene]
        passSkillCheck = int(any(skill.name == skill_name for skill in player.skillList))
    $ lineOfScene += 1

    if passSkillCheck == 1:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD
    return
label JsonFuncIfHasSkills:
    $ hasThing = 0
    $ ThingNeeded = 0
    python:
        while displayingScene.theScene[lineOfScene] != "EndLoop":
            lineOfScene += 1
            if displayingScene.theScene[lineOfScene] != "EndLoop":
                ThingNeeded += 1
                for each in  player.skillList:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        hasThing += 1

    if hasThing == ThingNeeded:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_94
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfHasPerk:
    $ lineOfScene += 1
    $ hasThing = 0
    python:
        perk_name = displayingScene.theScene[lineOfScene]
        hasThing = int(any(perk.name == perk_name for perk in player.perks))
    if hasThing == 1:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_25
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfSensitivityEqualOrGreater:
    $ lineOfScene += 1
    $ resTarget = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ resAmount = int(displayingScene.theScene[lineOfScene])

    if player.BodySensitivity.getRes(resTarget) >= resAmount:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_57
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfHasFetish:
    $ lineOfScene += 1
    if player.getFetish(displayingScene.theScene[lineOfScene]) >= 25:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_13
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfFetishLevelEqualOrGreater:
    $ lineOfScene += 1
    $ fetchFetish = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ fetishLvl = int(displayingScene.theScene[lineOfScene])

    if player.getFetish(fetchFetish) >= fetishLvl:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_28
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfInExploration:
    $ lineOfScene += 1
    if onAdventure == 0:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_61
    return
label JsonFuncIfGridPlayerStunned:
    $ lineOfScene += 1
    if stunnedGridPlayer >= 0:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_87
    return
label JsonFuncIfGridNPCSeesPlayer:
    $ lineOfScene += 1
    $ passcheck = 1
    $ NPCSeeRange = -1
    $ walls= 1
    if displayingScene.theScene[lineOfScene] == "IgnoreWalls":
        $ lineOfScene += 1
        $ walls= 0
    if displayingScene.theScene[lineOfScene] == "NPC":
        $ lineOfScene += 1
        python:
            for each in ActiveGridNPCs:
                if each.name == displayingScene.theScene[lineOfScene]:
                    Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]), (each.coord[0], each.coord[1]), tileset, ActiveGridNPCs, walls )
        $ lineOfScene += 1
    else:
        $ Path = astar(TheGrid, (ActiveGridNPCs[currentGridNPC].coord[0], ActiveGridNPCs[currentGridNPC].coord[1]), (playerCoord[0], playerCoord[1]), tileset, ActiveGridNPCs, walls )
    if displayingScene.theScene[lineOfScene] == "Range":
        $ lineOfScene += 1
        $ NPCSeeRange = int(displayingScene.theScene[lineOfScene])
        $ lineOfScene += 1

    if NPCSeeRange > 0:
        if len(Path) > NPCSeeRange + 1:
            $ passcheck = 0

    if walls == 1:
        python:
            for each in Path:
                if  tileset[FindTileType(TheGrid[each[1]][each[0]], tileset)][2] == "Wall":
                    passcheck = 0

    if passcheck == 1:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_88
    return
label JsonFuncIfGridNPCThere:
    $ lineOfScene += 1
    $ passcheck = 0
    python:
        for each in ActiveGridNPCs:
            if each.name == displayingScene.theScene[lineOfScene]:
                passcheck = 1
    $ lineOfScene += 1
    if passcheck == 1:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_89
    return
label JsonFuncIfGridVisonOn:
    $ lineOfScene += 1
    if PlayerGridSight != 0:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_90
    return
label JsonFuncIfPlayerHasStatusEffect(whichJsonFunc):
    $ functionInverse = True
    if whichJsonFunc == "IfPlayerDoesntHaveStatusEffect":
        $ functionInverse = False
    $ lineOfScene += 1
    $ hasThing = False
    $ check_has_status_effect = []
    if displayingScene.theScene[lineOfScene] == "RequireAll":
        $ hasThing = True
        $ lineOfScene += 1
    while isStatusEffect(displayingScene.theScene[lineOfScene]):
        $ check_has_status_effect.append(displayingScene.theScene[lineOfScene])
        $ lineOfScene += 1
    if functionInverse:
        if hasThing:
            if all(player.statusEffects.hasThisStatusEffect(statuseffect) for statuseffect in check_has_status_effect):
                $ print(displayingScene.theScene[lineOfScene])
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_12
                return
        else:
            if any(player.statusEffects.hasThisStatusEffect(statuseffect) for statuseffect in check_has_status_effect):
                $ print(displayingScene.theScene[lineOfScene])
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_40
                return
    else:
        if hasThing:
            if not all(player.statusEffects.hasThisStatusEffect(statuseffect) for statuseffect in check_has_status_effect):
                $ print(displayingScene.theScene[lineOfScene])
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_41
                return
        else:
            if not any(player.statusEffects.hasThisStatusEffect(statuseffect) for statuseffect in check_has_status_effect):
                $ print(displayingScene.theScene[lineOfScene])
                $ display = displayingScene.theScene[lineOfScene]
                call sortMenuD from _call_sortMenuD_42
                return
    return
label JsonFuncIfPlayerStunnedByParalysis:
    $ lineOfScene += 1
    if paralysisStunned == 1:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_62
    return
label JsonFuncIfPlayerLevelGreaterThan:
    $ lineOfScene += 1
    if player.stats.lvl >= int(displayingScene.theScene[lineOfScene]):
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_74
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfPlayerHasStatusEffectWithPotencyEqualOrGreater:
    $ lineOfScene += 1
    $ statusEffectChek = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ potencyChek = int(displayingScene.theScene[lineOfScene])

    $ TheCheck = player.statusEffects.hasThisStatusEffectPotency(statusEffectChek, potencyChek)

    if TheCheck == True:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_50
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfAttackCrits:
    $ lineOfScene += 1
    if Crit == 1:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_92
    return
label JsonFuncIfTimeIs:
    $ lineOfScene += 1
    $ passCheck = 0

    $ passCheck = IfTime(displayingScene.theScene[lineOfScene])
    if passCheck == 1:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_73
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfDifficultyIs:
    $ lineOfScene += 1
    if difficulty == displayingScene.theScene[lineOfScene]:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_104 
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfInputEquals:
    $ lineOfScene += 1
    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
    if int(displayingScene.theScene[lineOfScene]) == debt:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_7
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfInputEqualsOrLessThan:
    $ lineOfScene += 1
    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
    if int(displayingScene.theScene[lineOfScene]) >= debt:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_17
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfEventsProgressEqualsOrLessThanOtherEventsProgress:
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    $ CheckEvent2 = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)

    if ProgressEvent[CheckEvent].eventProgress <= ProgressEvent[CheckEvent2].eventProgress:
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_68
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncInputProgress:
    $ debt = 0
    call InputProgress from _call_InputProgress
    return
label JsonFuncIfPlayerIsUsingThisSkill:
    if monsterEncounter:
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] == combatChoice.name:
            $ lineOfScene += 1
            $ display = displayingScene.theScene[lineOfScene]
            call sortMenuD from _call_sortMenuD_64
            return
        else:
            $ lineOfScene += 1
    return
label JsonFuncIfPlayerHasStance:
    if monsterEncounter:
        $ lineOfScene += 1
        $ stancePass = 0
        python:
            for stance in player.combatStance:
                if displayingScene.theScene[lineOfScene] == "Penetration":
                    if stance.Stance == "Sex":
                        stancePass = 1
                    elif stance.Stance == "Anal":
                        stancePass = 1
                if stance.Stance == displayingScene.theScene[lineOfScene]:
                    stancePass = 1
                if stance.Stance != "" and stance.Stance != "None" and displayingScene.theScene[lineOfScene] == "Any":
                    stancePass = 1

        if stancePass == 1:
            $ lineOfScene += 1
            $ display = displayingScene.theScene[lineOfScene]
            call sortMenuD from _call_sortMenuD_31
            return
        else:
            $ lineOfScene += 1
    return
label JsonFuncIfPlayerHasStances:
    if monsterEncounter:
        $ stancePass = 0
        $ stanceNeeded = 0
        $ checked = []
        python:
            while displayingScene.theScene[lineOfScene] != "EndLoop":
                lineOfScene += 1
                if displayingScene.theScene[lineOfScene] != "EndLoop":
                    stanceNeeded += 1
                    s = 0
                    for stance in player.combatStance:
                        lookthrough = 0
                        for checkee in checked:
                            if checkee == s:
                                lookthrough = 1

                        if lookthrough == 0:
                            if displayingScene.theScene[lineOfScene] == "Penetration":
                                if stance.Stance == "Sex":
                                    stancePass += 1
                                    checked.append(s)
                                elif stance.Stance == "Anal":
                                    stancePass += 1
                                    checked.append(s)
                            if stance.Stance == displayingScene.theScene[lineOfScene]:
                                stancePass += 1
                                checked.append(s)
                            if stance.Stance != "" and stance.Stance != "None" and displayingScene.theScene[lineOfScene] == "Any":
                                stancePass += 1
                                checked.append(s)
                        s +=1

        if stancePass == stanceNeeded:
            $ lineOfScene += 1
            $ display = displayingScene.theScene[lineOfScene]
            call sortMenuD from _call_sortMenuD_70
            return
        else:
            $ lineOfScene += 1
    return
label JsonFuncIfPlayerDoesntHaveStance:
    if monsterEncounter:
        $ lineOfScene += 1
        $ stancePass = 0
        python:
            for stance in player.combatStance:
                if stance.Stance == displayingScene.theScene[lineOfScene]:
                    stancePass = 1

        if stancePass == 1:
            $ lineOfScene += 1
        else:
            $ lineOfScene += 1
            $ display = displayingScene.theScene[lineOfScene]
            call sortMenuD from _call_sortMenuD_32
    return
label JsonFuncIfMonsterHasStance:
    if monsterEncounter:
        $ lineOfScene += 1
        $ stancePass = 0
        python:
            for stance in monsterEncounter[CombatFunctionEnemytarget].combatStance:
                if stance.Stance == displayingScene.theScene[lineOfScene]:
                    stancePass = 1
                if stance.Stance != "" and stance.Stance != "None" and displayingScene.theScene[lineOfScene] == "Any":
                    stancePass = 1

        if stancePass == 1:
            $ lineOfScene += 1
            $ display = displayingScene.theScene[lineOfScene]
            call sortMenuD from _call_sortMenuD_33
            return
        else:
            $ lineOfScene += 1
    return
label JsonFuncIfMonsterDoesntHaveStance:
    if monsterEncounter:
        $ lineOfScene += 1
        $ stancePass = 0
        python:
            for stance in monsterEncounter[CombatFunctionEnemytarget].combatStance:
                if stance.Stance == displayingScene.theScene[lineOfScene]:
                    stancePass = 1

        if stancePass == 1:
            $ lineOfScene += 1
        else:
            $ lineOfScene += 1
            $ display = displayingScene.theScene[lineOfScene]
            call sortMenuD from _call_sortMenuD_34
    return
label JsonFuncIfOtherMonsterHasStance:
    if monsterEncounter:
        $ lineOfScene += 1
        $ stancePass = 0
        $ C = 0
        python:
            for each in trueMonsterEncounter:
                if C != CombatFunctionEnemytarget:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        stancePass = 1
                        found = copy.deepcopy(C)
                C += 1
        if stancePass == 1:
            $ lineOfScene += 1
            $ stancePass = 0
            python:
                for stance in monsterEncounter[found].combatStance:
                    if stance.Stance == displayingScene.theScene[lineOfScene]:
                        stancePass = 1
            if stancePass == 1:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                $ CombatFunctionEnemytarget = copy.deepcopy(found)
                call sortMenuD from _call_sortMenuD_35
                return
            else:
                $ lineOfScene += 1
        else:
            $ lineOfScene += 1
            $ lineOfScene += 1
    return
label JsonFuncIfOtherMonsterDoesntHaveStance:
    if monsterEncounter:
        $ lineOfScene += 1
        $ stancePass = 0
        $ C = 0
        python:
            for each in trueMonsterEncounter:
                if C != CombatFunctionEnemytarget:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        stancePass = 1
                        found = copy.deepcopy(C)
                C += 1
        if stancePass == 1:
            $ lineOfScene += 1
            $ stancePass = 0
            python:
                for stance in monsterEncounter[found].combatStance:
                    if stance.Stance == displayingScene.theScene[lineOfScene]:
                        stancePass = 1
            if stancePass == 1:
                $ lineOfScene += 1
            else:
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
                $ CombatFunctionEnemytarget = copy.deepcopy(found)
                call sortMenuD from _call_sortMenuD_36
                return
        else:
            $ lineOfScene += 1
            $ lineOfScene += 1
    return
label JsonFuncIfThisMonsterIsInEncounter:
    if monsterEncounter:
        $ lineOfScene += 1
        $ stancePass = 0
        $ C = 0
        python:
            for each in trueMonsterEncounter:
                if C != CombatFunctionEnemytarget:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        stancePass = 1
                        found = copy.deepcopy(C)
                C += 1
        if stancePass == 1:
            $ lineOfScene += 1
            $ display = displayingScene.theScene[lineOfScene]
            $ CombatFunctionEnemytarget = copy.deepcopy(found)
            call sortMenuD from _call_sortMenuD_39
            return
        else:
            $ lineOfScene += 1
    return
label JsonFuncIfMonsterHasStatusEffect(whichJsonFunc):
    if monsterEncounter:
        $ functionInverse = True
        if whichJsonFunc == "IfMonsterDoesntHaveStatusEffect":
            $ functionInverse = False
        $ lineOfScene += 1
        $ hasThing = False
        $ check_has_status_effect = []
        if displayingScene.theScene[lineOfScene] == "RequireAll":
            $ hasThing = True
            $ lineOfScene += 1
        while isStatusEffect(displayingScene.theScene[lineOfScene]):
            $ check_has_status_effect.append(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
        if functionInverse:
            if hasThing:
                if all(monsterEncounter[CombatFunctionEnemytarget].statusEffects.hasThisStatusEffect(statuseffect) for statuseffect in check_has_status_effect):
                    $ display = displayingScene.theScene[lineOfScene]
                    call sortMenuD from _call_sortMenuD_43
                    return
            else:
                if any(monsterEncounter[CombatFunctionEnemytarget].statusEffects.hasThisStatusEffect(statuseffect) for statuseffect in check_has_status_effect):
                    $ display = displayingScene.theScene[lineOfScene]
                    call sortMenuD from _call_sortMenuD_44
                    return
        else:
            if hasThing:
                if not all(monsterEncounter[CombatFunctionEnemytarget].statusEffects.hasThisStatusEffect(statuseffect) for statuseffect in check_has_status_effect):
                    $ display = displayingScene.theScene[lineOfScene]
                    call sortMenuD from _call_sortMenuD_45
                    return
            else:
                if not any(monsterEncounter[CombatFunctionEnemytarget].statusEffects.hasThisStatusEffect(statuseffect) for statuseffect in check_has_status_effect):
                    $ display = displayingScene.theScene[lineOfScene]
                    call sortMenuD from _call_sortMenuD_52
                    return
    return
label JsonFuncIfMonsterLevelGreaterThan:
    $ lineOfScene += 1
    if monsterEncounter[CombatFunctionEnemytarget].stats.lvl >= int(displayingScene.theScene[lineOfScene]):
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_75
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfMonsterHasStatusEffectWithPotencyEqualOrGreater:
    if monsterEncounter:
        $ lineOfScene += 1
        $ statusEffectChek = displayingScene.theScene[lineOfScene]
        $ lineOfScene += 1
        $ potencyChek = displayingScene.theScene[lineOfScene]

        if monsterEncounter[CombatFunctionEnemytarget].statusEffects.hasThisStatusEffectPotency(statusEffectChek, potencyChek) == True:
            $ lineOfScene += 1
            $ display = displayingScene.theScene[lineOfScene]
            call sortMenuD from _call_sortMenuD_51
            return
        else:
            $ lineOfScene += 1
    return
label JsonFuncIfOtherMonsterHasStatusEffect(whichJsonFunc):
    if monsterEncounter:
        $ functionInverse = True
        if whichJsonFunc == "IfOtherMonsterDoesntHaveStatusEffect":
            $ functionInverse = False
        $ lineOfScene += 1
        $ stancePass = 0
        $ C = 0
        python:
            for each in trueMonsterEncounter:
                if C != CombatFunctionEnemytarget:
                    if each.name == displayingScene.theScene[lineOfScene]:
                        stancePass = 1
                        found = copy.deepcopy(C)
                C += 1
        $ lineOfScene += 1
        $ hasThing = False
        $ check_has_status_effect = []
        if displayingScene.theScene[lineOfScene] == "RequireAll":
            $ hasThing = True
            $ lineOfScene += 1
        while isStatusEffect(displayingScene.theScene[lineOfScene]):
            $ check_has_status_effect.append(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
        if functionInverse:
            if hasThing:
                if all(monsterEncounter[found].statusEffects.hasThisStatusEffect(statuseffect) for statuseffect in check_has_status_effect):
                    if stancePass == 1:
                        $ display = displayingScene.theScene[lineOfScene]
                        $ CombatFunctionEnemytarget = copy.deepcopy(found)
                        call sortMenuD from _call_sortMenuD_53
                        return
            else:
                if any(monsterEncounter[found].statusEffects.hasThisStatusEffect(statuseffect) for statuseffect in check_has_status_effect):
                    if stancePass == 1:
                        $ display = displayingScene.theScene[lineOfScene]
                        $ CombatFunctionEnemytarget = copy.deepcopy(found)
                        call sortMenuD from _call_sortMenuD_85
                        return
        else:
            if hasThing:
                if not all(monsterEncounter[found].statusEffects.hasThisStatusEffect(statuseffect) for statuseffect in check_has_status_effect):
                    if stancePass == 1:
                        $ display = displayingScene.theScene[lineOfScene]
                        $ CombatFunctionEnemytarget = copy.deepcopy(found)
                        call sortMenuD from _call_sortMenuD_95
                        return
            else:
                if not any(monsterEncounter[found].statusEffects.hasThisStatusEffect(statuseffect) for statuseffect in check_has_status_effect):
                    if stancePass == 1:
                        $ display = displayingScene.theScene[lineOfScene]
                        $ CombatFunctionEnemytarget = copy.deepcopy(found)
                        call sortMenuD from _call_sortMenuD_96
                        return
    return
label JsonFuncIfMonsterArousalGreaterThan:
    $ lineOfScene += 1
    if monsterEncounter[CombatFunctionEnemytarget].stats.hp >= int(displayingScene.theScene[lineOfScene]):
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_46
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncIfMonsterOrgasm:
    $ lineOfScene += 1
    if monsterEncounter[CombatFunctionEnemytarget].stats.hp >= monsterEncounter[CombatFunctionEnemytarget].stats.max_true_hp:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_47
    return
label JsonFuncIfMonsterEnergyGone:
    $ lineOfScene += 1
    if monsterEncounter[CombatFunctionEnemytarget].stats.ep <= 0:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_91
    return
label JsonFuncIfMonsterSpiritGone:
    $ lineOfScene += 1
    if monsterEncounter[CombatFunctionEnemytarget].stats.sp <= 0:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_55
    return
label JsonFuncIfMonsterHasSkill:
    $ lineOfScene += 1
    $ passSkillCheck = 0
    python:
        for each in monsterEncounter[CombatFunctionEnemytarget].skillList:
            if each.name == displayingScene.theScene[lineOfScene]:
                passSkillCheck = 1
    $ lineOfScene += 1
    if passSkillCheck == 1:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_48
    return
label JsonFuncIfMonsterHasPerk:
    $ lineOfScene += 1
    $ passSkillCheck = 0
    python:
        for each in  monsterEncounter[CombatFunctionEnemytarget].perks:
            if each.name == displayingScene.theScene[lineOfScene]:
                passSkillCheck = 1
    $ lineOfScene += 1
    if passSkillCheck == 1:
        $ display = displayingScene.theScene[lineOfScene]
        call sortMenuD from _call_sortMenuD_49
    return
