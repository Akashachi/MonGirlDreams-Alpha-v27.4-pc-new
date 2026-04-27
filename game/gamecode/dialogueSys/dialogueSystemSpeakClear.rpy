# 'S' funcs
label JsonFuncSpeak:
    $ lineOfScene += 1
    if displayingScene.theScene[lineOfScene] != "":
        $ Speaker = Character(_(displayingScene.theScene[lineOfScene]),
                                what_prefix='"',
                                what_suffix='"')
    else:
        $ Speaker = Character(_(''))
    $ lineOfScene += 1
    $ readLine = 1
    return
label JsonFuncSpeakSkill:
    $ lineOfScene += 1
    if displayingScene.theScene[lineOfScene] != "":
        $ Speaker = Character(_(displayingScene.theScene[lineOfScene]))
    else:
        $ Speaker = Character(_(''))
    $ lineOfScene += 1
    $ readLine = 1
    return
label JsonFuncSpeaks:
    if len(monsterEncounter) >= 1:
        $ actorNames[0] = monsterEncounter[0].name
    $ Speaker = Character(_(actorNames[0])+attackTitle,
                            what_prefix='"',
                            what_suffix='"')
    $ lineOfScene += 1
    $ readLine = 1
    return
label JsonFuncSpeaks2(theFuncyNumber):
    $ theFuncyNumber -= 1
    if len(monsterEncounter) >= theFuncyNumber + 1:
        $ Speaker = monsterEncounter[theFuncyNumber].name+attackTitle
    else:
        $ Speaker = getSpeaker(theFuncyNumber, EventDatabase, MonsterDatabase)
    $ lineOfScene += 1
    $ readLine = 1
    return
label JsonFuncSpawnGridNPC:
    if TheGrid != []:
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
        if displayingScene.theScene[lineOfScene] == "Here":
            $ newNPC.coord[0] = ActiveGridNPCs[currentGridNPC].coord[0]
            $ newNPC.coord[1] = ActiveGridNPCs[currentGridNPC].coord[1]
        else:
            $ newNPC.coord[0] = int(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ newNPC.coord[1] = int(displayingScene.theScene[lineOfScene])

        $ newNPC.GridposX = GridMovement*newNPC.coord[0]
        $ newNPC.GridposY = GridMovement*newNPC.coord[1]
        $ newNPC.GridposXPrior = newNPC.GridposX
        $ newNPC.GridposYPrior = newNPC.GridposY

        $ newNPC.JustSpawned = 1

        $ ActiveGridNPCs.append(copy.deepcopy(newNPC))
    else:
        $ lineOfScene += 2
    return
label JsonFuncSleepPlayer:
    $ lineOfScene += 1
    $ delayCheck = displayingScene.theScene[lineOfScene]
    $ player = player.statusEffects.refresh(player)
    $ player.stats.refresh()
    $ favorPool = CalcGoddessFavor(player)
    $ favorStrain = 0
    $ dreaming = 1
    if delayCheck == "DelayNotifications":
        $ timeNotify = 1
    else:
        $ lineOfScene -= 1

    call advanceTime(TimeIncrease=1) from _call_advanceTime_2
    if delayCheck == "DelayNotifications":
        $ timeNotify = 1
    if timeNotify == 0:
        $ shuffledDream = copy.deepcopy(DreamList)
        $ renpy.random.shuffle(shuffledDream)
        $ showingDream = []
        $ showingDream.append(copy.deepcopy(shuffledDream[0]))
        call TimeEvent(CardType="Dream", LoopedList=showingDream) from _call_TimeEvent_3
        $ timeNotify = 0

    if TimeOfDay != Morning:
        while TimeOfDay != Morning:
            if TimeOfDay != Morning:
                if delayCheck == "DelayNotifications":
                    $ timeNotify = 1
                call advanceTime(TimeIncrease=1) from _call_advanceTime_3
    $ notFunction = 0
    $ noCombatFunction = 0
    $ noDFunction = 0
    return
label JsonFuncStatCheck(whichJsonFunc):
    $ functionInverse = True
    if whichJsonFunc == "StatCheckRollUnder":
        $ functionInverse = False
    $ checkStat = 0
    $ lineOfScene += 1
    $ increaseStatCheck = 0 

    $ checkPreFuncs = 0
    while checkPreFuncs == 0:
        if displayingScene.theScene[lineOfScene] == "ChangeStatCheckDifficulty":
            $ lineOfScene += 1
            if displayingScene.theScene[lineOfScene] == "IfEncounterSizeGreaterOrEqualTo":
                if monsterEncounter:
                    $ lineOfScene += 1
                    if len(monsterEncounter) >= int(displayingScene.theScene[lineOfScene]):
                        $ lineOfScene += 1
                        $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                    else:
                        $ lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "IfEncounterSizeLessOrEqualTo":
                if monsterEncounter:
                    $ lineOfScene += 1
                    if len(monsterEncounter) <= int(displayingScene.theScene[lineOfScene]):
                        $ lineOfScene += 1
                        $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                    else:
                        $ lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "IfPlayerHasStatusEffect": 
                $ lineOfScene += 1
                if player.statusEffects.hasThisStatusEffect(displayingScene.theScene[lineOfScene]) == True:
                    $ lineOfScene += 1
                    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                else:
                    $ lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "IfPlayerHasStatusEffectWithPotencyEqualOrGreater": 
                $ lineOfScene += 1
                $ statusEffectChek = displayingScene.theScene[lineOfScene]
                $ lineOfScene += 1
                $ potencyChek = int(displayingScene.theScene[lineOfScene])

                $ TheCheck = player.statusEffects.hasThisStatusEffectPotency(statusEffectChek, potencyChek)

                if TheCheck == True:
                    $ lineOfScene += 1
                    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                else:
                    $ lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "IfHasFetish":
                $ lineOfScene += 1
                if player.getFetish(displayingScene.theScene[lineOfScene]) >= 25:
                    $ lineOfScene += 1
                    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                else:
                    $ lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "IfFetishLevelEqualOrGreater":
                $ lineOfScene += 1
                $ fetchFetish = displayingScene.theScene[lineOfScene]
                $ lineOfScene += 1
                $ fetishLvl = int(displayingScene.theScene[lineOfScene])

                if player.getFetish(fetchFetish) >= fetishLvl:
                    $ lineOfScene += 1
                    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                else:
                    $ lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "IfVirilityEqualsOrGreater":
                $ lineOfScene += 1

                if int(displayingScene.theScene[lineOfScene]) <= getVirility(player) :
                    $ lineOfScene += 1
                    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                else:
                    $ lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "IfMonsterLevelGreaterThan":
                $ lineOfScene += 1
                if monsterEncounter[CombatFunctionEnemytarget].stats.lvl >= int(displayingScene.theScene[lineOfScene]):
                    $ lineOfScene += 1
                    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                else:
                    $ lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "IfProgressEqualsOrGreater":
                $ lineOfScene += 1
                $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
                if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[DataLocation].eventProgress:
                    $ lineOfScene += 1
                    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                else:
                    $ lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "IfHasPerk":
                $ lineOfScene += 1
                $ hasThing = 0
                python:
                    perk_name = displayingScene.theScene[lineOfScene]
                    hasThing = int(any(perk.name == perk_name for perk in player.perks))
                if hasThing == 1:
                    $ lineOfScene += 1
                    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                else:
                    $ lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "GetAnEventsProgressThenIfEqualsOrGreater":
                $ lineOfScene += 1
                $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
                $ lineOfScene += 1
                if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[CheckEvent].eventProgress:
                    $ lineOfScene += 1
                    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                else:
                    $ lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "IfChoice":
                $ lineOfScene += 1
                $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
                $ lineOfScene += 1
                $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)

                while choiceToCheck-1 >= len(ProgressEvent[DataLocation].choices):
                    $ ProgressEvent[DataLocation].choices.append("")

                if displayingScene.theScene[lineOfScene] == ProgressEvent[DataLocation].choices[choiceToCheck-1]:
                    $ lineOfScene += 1
                    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                else:
                    $ lineOfScene += 1
            elif displayingScene.theScene[lineOfScene] == "GetEventAndIfChoice":
                $ lineOfScene += 1
                $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
                $ lineOfScene += 1
                $ choiceToCheck = int(displayingScene.theScene[lineOfScene])

                while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
                    $ ProgressEvent[CheckEvent].choices.append("")

                $ lineOfScene += 1
                if displayingScene.theScene[lineOfScene] == ProgressEvent[CheckEvent].choices[choiceToCheck-1]:
                    $ lineOfScene += 1
                    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
                else:
                    $ lineOfScene += 1
            else:
                $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
        else:
            $ checkPreFuncs += 1

    $ statType = displayingScene.theScene[lineOfScene]
    $ maxStatDisplay = ""
    if statType == "Temptation":
        $ statToCheck = int(math.floor(  (player.stats.Int-5)*0.05 + (player.stats.Willpower-5)*0.2 + (player.stats.Allure-5)*0.05  ))
        if statToCheck >= 15:
            $ statToCheck = 15
            $ maxStatDisplay = "(Max)"
    else:
        $ statToCheck = int(math.floor((player.stats.getStat(displayingScene.theScene[lineOfScene])-5)*0.15))

    $ lineOfScene += 1
    if nightmare == 1:
        #$ increaseStatCheck += int(math.floor(player.stats.lvl*0.1))
        $ playerWeaker = 0
        if monsterEncounter:
            if monsterEncounter[0].stats.lvl >= player.stats.lvl:
                $ playerWeaker = 1
        if playerWeaker == 0:
            if float(displayingScene.theScene[lineOfScene]) <= player.stats.lvl*0.2:
                $ increaseStatCheck += 5
            if float(displayingScene.theScene[lineOfScene]) <= player.stats.lvl*0.3:
                $ increaseStatCheck += 5
            if float(displayingScene.theScene[lineOfScene]) <= player.stats.lvl*0.4:
                $ increaseStatCheck += 5

    $ opposedCheck = int(displayingScene.theScene[lineOfScene]) + increaseStatCheck

    #luck part
    $ luckDie = int(math.floor(player.stats.getStat("Luck")*0.20))

    if luckDie < 1 and luckDie > -1 :
        $ luckDie = 0

    if luckDie == 0:
        $ luckAddition = 0
    elif luckDie < 1:
        $ luckAddition = renpy.random.randint(luckDie, -1)
    else:
        $ luckAddition = renpy.random.randint(1,luckDie)

    #perk application
    $ perkLine = ""
    $ perkBonus = 0   
    $ minDie = 1
    python:
        for perk in player.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "MinStatCheckDie":
                    minDie += perk.EffectPower[p]
                if perk.PerkType[p] == "TemptationCheckBonus":
                    if statType == "Temptation":
                        perkBonus += perk.EffectPower[p]
                p += 1
    if perkBonus != 0:
        $ perkLine = " + Perk Bonus: +" + str(perkBonus)

    #roll!
    $ randomRoll = renpy.random.randint(minDie,20)

    $ defenceBonus = 0
    #defence bonus for stat check!
    if statType == "Technique" or statType == "Power" or statType == "Willpower" or statType == "Intelligence" or statType == "Temptation":
        if (player.statusEffects.defend.duration > 0):
            if player.statusEffects.defend.potency == 3:
                $ defenceBonus = 5
            elif player.statusEffects.defend.potency == 2:
                $ defenceBonus = 3
            elif player.statusEffects.defend.potency == 1:
                $ defenceBonus = 1
    $ defLine = ""
    if defenceBonus != 0:
        $ defLine = " + Defend Bonus: +" + str(defenceBonus)

    #charm penalty for temptation checks.
    if statType == "Temptation":
        if (player.statusEffects.charmed.duration > 0):
            $ opposedCheck += 1
            if difficulty == "Hard":
                $ opposedCheck += 4

    #add it all together then make the display line
    $ combinedCheck = statToCheck + randomRoll + luckAddition + defenceBonus + perkBonus
    if statType == "Temptation":
        if functionInverse == True:
            $ showing = "Temptation Check" + GetParalFlatEnergyCostDisplayCheck(player) + "!\nRoll d20: " + str(randomRoll) + " + (Will-5)*0.2 + (Int-5)*0.05 + (Allure-5)*0.05: " + str(statToCheck) + maxStatDisplay + " + Luck*0.20 = d" + str(luckDie) +": "  + str(luckAddition) + defLine + perkLine + ".\nTotal: " + str(combinedCheck) + " vs Check: " + str(opposedCheck) + "."
        elif functionInverse == False:
            $ showing = "{b}Roll Under{/b} " + "Temptation Check! Roll under the value!" + GetParalFlatEnergyCostDisplayCheck(player) + "\nRoll d20: " + str(randomRoll) + " + (Will-5)*0.2 + (Int-5)*0.05 + (Allure-5)*0.05: " + str(statToCheck) + maxStatDisplay + " + Luck*0.20 = d" + str(luckDie) +": "  + str(luckAddition) + defLine + perkLine +  ".\nTotal: " + str(combinedCheck) + " vs Check: " + str(opposedCheck) + "."
    else:
        if functionInverse == True:
            $ showing = statType + " Stat Check!" + GetParalFlatEnergyCostDisplayCheck(player) + "\nRoll d20: " + str(randomRoll) + " + (" + statType + "-5)*0.15: " + str(statToCheck) + " + Luck*0.20 = d" + str(luckDie) +": "  + str(luckAddition) + defLine + perkLine +  ".\nTotal: " + str(combinedCheck) + " vs Check: " + str(opposedCheck) + "."
        elif functionInverse == False:
            $ showing = "{b}Roll Under{/b} " + statType + " Stat Check! Roll under the value!" + GetParalFlatEnergyCostDisplayCheck(player) + "\nRoll d20: " + str(randomRoll) + " + (" + statType + "-5)*0.15: " + str(statToCheck) + " + Luck*0.20 = d" + str(luckDie) +": "  + str(luckAddition) + defLine + perkLine +  ".\nTotal: " + str(combinedCheck) + " vs Check: " + str(opposedCheck) + "."

    $ lineOfScene += 1
    $ display = displayingScene.theScene[lineOfScene]

    if int(GetParalFlatEnergyChange(player)) <= player.stats.ep:
        $ player.stats.ep -= int(math.floor(GetParalFlatEnergyChange(player)))
    else:
        $ lineOfScene += 2
        $ display = displayingScene.theScene[lineOfScene]
        $ checkStat = 1
        $ showing = "With paralysis afflicting you, you lack the " + str(int(math.floor(GetParalFlatEnergyChange(player)))) + " energy to resist!"
        "[showing]"
        $ increaseStatCheck = 0
        call sortMenuD from _call_sortMenuD_69
        if monsterEncounter:
            return

    if combinedCheck >= opposedCheck and player.statusEffects.hasThisStatusEffect("Surrender") == False and functionInverse == True:
        $ checkStat = 1
        $ showing += "  PASS!"
        "[showing]"
        $ increaseStatCheck = 0
        call sortMenuD from _call_sortMenuD_97
        if monsterEncounter:
            return
    elif combinedCheck < opposedCheck and functionInverse == False:
        $ checkStat = 1
        $ showing += " PASS!"
        "[showing]"
        $ increaseStatCheck = 0
        call sortMenuD from _call_sortMenuD_98
        if monsterEncounter:
            return
    elif combinedCheck >= opposedCheck and functionInverse == False:
        $ lineOfScene += 2
        $ display = displayingScene.theScene[lineOfScene]
        $ checkStat = 1
        $ showing += " FAILED!"
        "[showing]"
        $ increaseStatCheck = 0
        call sortMenuD from _call_sortMenuD_99
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
        $ showing += "  FAILED!"
        #"[showing]"
        
        if player.statusEffects.hasThisStatusEffect("Surrender") == True:
            $ lineOfScene += 1
            $ display = displayingScene.theScene[lineOfScene]
            $ checkStat = 1
            $ increaseStatCheck = 0
            call sortMenuD from _call_sortMenuD_100
            if monsterEncounter:
                return
        else:
            $ OpposingCost = ((int(math.floor(opposedCheck / 5)))*30)
            $ DefendingCost = ((int(math.floor(statToCheck)))*5)
            $ surpassEnergyCost =  ((int(math.floor(opposedCheck / 5)))*30)  - ((int(math.floor(statToCheck)))*5)

            if difficulty == "Hard":
                $ surpassEnergyCost = int(math.floor(surpassEnergyCost*1.25))
            elif difficulty == "Easy":
                $ surpassEnergyCost = int(math.floor(surpassEnergyCost*0.75))
                
            if difficulty == "Hard":
                $ minimum = "EP Cost. (Min 25)"
                if surpassEnergyCost < 25:
                    $ surpassEnergyCost = 25
            else:
                $ minimum = "EP Cost. (Min 10)"
                if surpassEnergyCost < 10:
                    $ surpassEnergyCost = 10
            $ surpassEnergyCost = int(math.floor(surpassEnergyCost*GetParalEnergyChange(player)*(1+favorStrain*0.01)))
            $ LastLine =  showing + " Surpass your failure for " + str(surpassEnergyCost) + " Energy?"

            if statType == "Temptation":
                $ LastLine += "\n\n"  + "Check(" + str(opposedCheck) + "): " + str(OpposingCost) + "EP x Strain: " + str(favorStrain) + "% - Temptation Res" + "(" + str(statToCheck) + "): " + str(DefendingCost) + " EP = " + str(surpassEnergyCost) + minimum + "\nStrain resets on rest."
            else:
                $ LastLine += "\n\n"  + "Check(" + str(opposedCheck) + "): " + str(OpposingCost) + "EP x Strain: " + str(favorStrain) + "% - " + statType + "(" + str(statToCheck) + "): " + str(DefendingCost) + " EP = " + str(surpassEnergyCost) + minimum + "\nStrain resets on rest."


            show screen fakeTextBox
            window hide
            label surpassMenuBlip:
            menu surpassMenu:
                "Spend a Goddess' Favor to pass? [favorPool] Remaining." if favorPool > 0:
                    $ favorPool -= 1
                    $ increaseStatCheck = 0
                    hide screen fakeTextBox
                    call sortMenuD from _call_sortMenuD_105
                    if monsterEncounter:
                        return 

                "Goddess' Favor has run out..." if favorPool == 0 and player.stats.ep >= surpassEnergyCost: 
                    jump surpassMenuBlip
                    if monsterEncounter:
                        return 
                
                "Goddess' Favor has run out..." if favorPool == 0 and player.stats.ep < surpassEnergyCost:
                    hide screen fakeTextBox
                    hide screen fakeTextBox
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]
                    $ checkStat = 1
                    $ increaseStatCheck = 0
                    call sortMenuD from _call_sortMenuD_106
                    if monsterEncounter:
                        return 

                "Surpass Failure for [surpassEnergyCost] Energy. +25 Strain." if player.stats.ep >= surpassEnergyCost:
                    $ player.stats.ep -= surpassEnergyCost
                    $ increaseStatCheck = 0
                    $ favorStrain += 25
                    hide screen fakeTextBox
                    call sortMenuD from _call_sortMenuD_29
                    if monsterEncounter:
                        return
                
                "You don't have the Energy to resist." if favorPool > 0 and player.stats.ep < surpassEnergyCost: 
                    jump surpassMenuBlip
                    if monsterEncounter:
                        return 

                "You don't have the Energy to resist." if player.stats.ep < surpassEnergyCost and favorPool == 0:
                    #jump surpassMenuBlip
                    hide screen fakeTextBox
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]
                    $ checkStat = 1
                    $ increaseStatCheck = 0
                    call sortMenuD from _call_sortMenuD_84
                    if monsterEncounter:
                        return

                "Give up." if player.stats.ep >= surpassEnergyCost or favorPool > 0:

                    hide screen fakeTextBox
                    $ lineOfScene += 1
                    $ display = displayingScene.theScene[lineOfScene]
                    $ checkStat = 1
                    $ increaseStatCheck = 0
                    call sortMenuD from _call_sortMenuD_11
                    if monsterEncounter:
                        return

    $ lineOfScene += 1
    return
label JsonFuncStatEqualsOrMore:
    $ lineOfScene += 1
    $ statToCheck = player.stats.getStat(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    if statToCheck >= int(displayingScene.theScene[lineOfScene]):
        $ lineOfScene += 1
        $ display = displayingScene.theScene[lineOfScene]
        $ checkStat = 1
        call sortMenuD from _call_sortMenuD_21
        if monsterEncounter:
            return
    else:
        $ lineOfScene += 1
    return
label JsonFuncStunGridPlayer:
    $ lineOfScene += 1
    $ stunnedGridPlayer = int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncStoreCurrentEventSpotSkippingLines:
    $ lineOfScene += 1
    $ StoredScene = copy.deepcopy(displayingScene)
    $ StoredLine = copy.copy(lineOfScene) + int(displayingScene.theScene[lineOfScene])
    $ StoredDataLoc = copy.deepcopy(DataLocation)
    return
label JsonFuncSaveNextLine:
    $ savedLine = displayingScene.theScene[lineOfScene+1]
    $ savedLineInMenu = 0
    return
label JsonFuncStoreCurrentBG:
    $ heldBG = copy.copy(bg)
    return
label JsonFuncStopBGM:
    $ overrideCombatMusic = 0
    stop music fadeout 1.0
    $ musicChanged = [""]
    return
label JsonFuncStopBGMHard:
    $ overrideCombatMusic = 0
    stop music
    $ musicChanged = [""]
    return
label JsonFuncStoreCurrentBGM:
    $ storedBGM = copy.deepcopy(BGMlist)
    return
label JsonFuncStopSoundEffect:
    stop sound fadeout 1.0
    return
label JsonFuncStopSoundEffect2:
    stop soundChannel2 fadeout 1.0
    return
label JsonFuncStopSoundEffectLoop:
    stop loopingSound fadeout 1.0
    return
label JsonFuncStopSoundEffectLoop2:
    stop loopingSound2 fadeout 1.0
    return
label JsonFuncShowTreasureChest:
    show chest:
        yalign 0
        xalign 0.35
    return
label JsonFuncSkillShoppingMenu:
    if renpy.variant("touch") or persistent.lastInput == "Touch":
        $ shopSticky = "Tap skill to view information, hold tap to purchase."
    $ ShoppingSkillList = []
    $ showOnSide = 1
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] == "PurchasesToProgress":
            $ PurchasesToProgress = 1
        elif displayingScene.theScene[lineOfScene] != "EndLoop":
            $ dataTarget = getFromName(displayingScene.theScene[lineOfScene], SkillsDatabase)
            $ blankItem = SkillsDatabase[dataTarget]
            $ ShoppingSkillList.append(blankItem)

    $ buying = 1
    $ SkillShopping = 1
    call Shopping from _call_Shopping
    $ purchasing = 0
    $ amountToBuy = 1
    $ on_shoppingtooltip = ""
    show screen ON_CharacterDialogueScreen onlayer master
    hide screen ON_ShoppingScreen
    $ showOnSide = 0
    $ ShoppingSkillList = []
    return
label JsonFuncShoppingMenu:
    if renpy.variant("touch") or persistent.lastInput == "Touch":
        $ shopSticky = "Tap item to view information, hold tap to purchase."
    $ ShoppingItemList = []
    $ showOnSide = 1
    $ NoSelling = 0
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1

        if displayingScene.theScene[lineOfScene] == "PurchasesToProgress":
            $ PurchasesToProgress = 1
        elif displayingScene.theScene[lineOfScene] == "NoSelling":
            $ NoSelling = 1
        elif displayingScene.theScene[lineOfScene] != "EndLoop":
            $ dataTarget = getFromName(displayingScene.theScene[lineOfScene], ItemDatabase)
            $ blankItem = ItemDatabase[dataTarget]
            $ ShoppingItemList.append(blankItem)

    $ buying = 1
    $ SkillShopping = 0
    call Shopping from _call_Shopping_1
    $ purchasing = 0
    $ amountToBuy = 1
    $ on_shoppingtooltip = ""
    show screen ON_CharacterDialogueScreen onlayer master
    hide screen ON_ShoppingScreen
    $ showOnSide = 0
    $ ShoppingSkillList = []
    $ PurchasesToProgress = 0
    return
label JsonFuncSensitivityRestore:
    call RestoreSensitivity from _call_RestoreSensitivity
    return
label JsonFuncSemenHeal:
    $ healText = 0
    $ lineOfScene += 1
    $ recoverAmount = int(displayingScene.theScene[lineOfScene]) * (1+getVirility(player)*0.01)
    $ recoverAmount *= renpy.random.randint(75, 125)*0.01
    $ recoverAmount = math.floor(recoverAmount)
    $ recoverAmount= int(recoverAmount)
    $ monsterEncounter[CombatFunctionEnemytarget].stats.hp -= recoverAmount
    #$ finalDamage = recoverAmount
    return
label JsonFuncShuffleMonsterEncounter:
    python:
        c = 0
        for each in monsterEncounter:
            monsterEncounter[c].name = copy.deepcopy(trueMonsterEncounter[c].name)
            c += 1
    $ renpy.random.shuffle(monsterEncounter)
    $ trueMonsterEncounter = copy.deepcopy(monsterEncounter)
    $ monsterEncounter = NumberMonsters(monsterEncounter)
    return
label JsonFuncSkipPlayerAttack:
    $ skipAttack = 1
    return
label JsonFuncSkipMonsterAttack:
    $ monsterEncounter[CombatFunctionEnemytarget].skippingAttack = 1
    return
label JsonFuncSkipAllMonsterAttacks:
    python:
        for each in monsterEncounter:
            each.skippingAttack = 1
    return
label JsonFuncShowMonsterEncounter:
    if len(monsterEncounter) >= 1:
        hide screen ON_CharacterDialogueScreen
        show screen ON_EnemyCardScreen onlayer master
        $ SceneCharacters = []
    $ hidingCombatEncounter = 0
    return
# Clear funcs
label JsonFuncClearPlayerStatusEffects:
    $ player = player.statusEffects.refresh(player)
    return
label JsonFuncClearNonPersistentStatusEffects:
    $ player = ClearNonPersistentEffects(player)
    return
label JsonFuncClearMonsterSkillList:
    $ monsterEncounter[CombatFunctionEnemytarget].skillList = []
    return
label JsonFuncClearMonsterPerks:
    $ monsterEncounter[CombatFunctionEnemytarget].perks = []
    return
label JsonFuncClearStances:
    $ player.clearStance()
    python:
        for each in monsterEncounter:
            each.clearStance()
    return
label JsonFuncClearStanceFromMonsterAndPlayer:
    $ lineOfScene += 1
    $ removeThisStance = ""
    $ stanceDurabilityHoldOverTarget = 0
    $ stanceDurabilityHoldOverAttacker = 0
    if displayingScene.theScene[lineOfScene] == "All":
        python:
            copyStances = copy.deepcopy(monsterEncounter[CombatFunctionEnemytarget].combatStance)
            for each in copyStances:
                stanceDurabilityHoldOverTarget += player.getStanceDurability(displayingScene.theScene[lineOfScene])
                player.removeStanceByName(each.Stance)
                monsterEncounter[CombatFunctionEnemytarget].removeStanceByName(each.Stance)
    else:
        $ stanceDurabilityHoldOverTarget += player.getStanceDurability(displayingScene.theScene[lineOfScene])
        $ player.removeStanceByName(displayingScene.theScene[lineOfScene])
        $ monsterEncounter[CombatFunctionEnemytarget].removeStanceByName(displayingScene.theScene[lineOfScene])

    $ stanceDurabilityHoldOverAttacker += monsterEncounter[CombatFunctionEnemytarget].getStanceDurability(displayingScene.theScene[lineOfScene])
    return
label JsonFuncClearMonsterEncounter:
    $ monsterEncounter = []
    $ monsterEncounterCG = []
    $ trueMonsterEncounter = []
    $ DefeatedEncounterMonsters = []
    $ player.clearStance()
    $ player.restraintStruggle = [""]
    $ player.restraintStruggleCharmed = [""]
    $ player.restraintEscaped = [""]
    $ player.restraintEscapedFail = [""]
    $ canRun = True
    return
label JsonFuncClearMonsterEncounterBossFight:
    $ monsterEncounter = []
    $ monsterEncounterCG = []
    $ trueMonsterEncounter = []
    $ DefeatedEncounterMonsters = []
    $ player.clearStance()
    $ player.restraintStruggle = [""]
    $ player.restraintStruggleCharmed = [""]
    $ player.restraintEscaped = [""]
    $ player.restraintEscapedFail = [""]
    return

label JsonFuncClearFightForVictory:
    $ monsterEncounter = []
    $ monsterEncounterCG = []
    $ trueMonsterEncounter = []
    $ player.clearStance()
    $ player.restraintStruggle = [""]
    $ player.restraintStruggleCharmed = [""]
    $ player.restraintEscaped = [""]
    $ player.restraintEscapedFail = [""]
    $ canRun = True
    return

