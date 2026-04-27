# Change funcs
label JsonFuncChangeImageFor:
    if DialogueIsFrom == "Monster":
        $ lineOfScene += 1
        python:
            try:
                settingCharcter = int(displayingScene.theScene[lineOfScene]) - 1
                lineOfScene += 1
                settingToImage = displayingScene.theScene[lineOfScene]
            except:
                settingToImage = displayingScene.theScene[lineOfScene]
                settingCharcter = CombatFunctionEnemytarget
        $ imgI = 0
        python:
            for each in monsterEncounter:
                if imgI == settingCharcter:
                    each.ImageSets[each.currentSet].ImageSet[0].currentImage = getFromName(settingToImage, each.ImageSets[each.currentSet].ImageSet[0].Images)
                    if each.ImageSets[each.currentSet].ImageSet[0].AlwaysOn == 1 and each.ImageSets[each.currentSet].ImageSet[0].currentImage <= 0:
                        each.ImageSets[each.currentSet].ImageSet[0].currentImage = 1
                imgI += 1
            imgI = 0
            for each in DefeatedEncounterMonsters:
                if imgI == settingCharcter:
                    each.ImageSets[each.currentSet].ImageSet[0].currentImage = getFromName(settingToImage, each.ImageSets[each.currentSet].ImageSet[0].Images)
                    if each.ImageSets[each.currentSet].ImageSet[0].AlwaysOn == 1 and each.ImageSets[each.currentSet].ImageSet[0].currentImage <= 0:
                        each.ImageSets[each.currentSet].ImageSet[0].currentImage = 1
                imgI += 1
    else:
        if len(monsterEncounter) == 0 or hidingCombatEncounter == 1:
            $ lineOfScene += 1
            $ settingCharcter = int(displayingScene.theScene[lineOfScene]) - 1
        $ lineOfScene += 1
        $ settingToImage = displayingScene.theScene[lineOfScene]
        $ imgI = 0
        python:
            if len(monsterEncounter) > 0 and hidingCombatEncounter == 0:
                for each in monsterEncounter:
                    if imgI == CombatFunctionEnemytarget:
                        each.ImageSets[each.currentSet].ImageSet[0].currentImage = getFromName(settingToImage, each.ImageSets[each.currentSet].ImageSet[0].Images)
                        if each.ImageSets[each.currentSet].ImageSet[0].AlwaysOn == 1 and each.ImageSets[each.currentSet].ImageSet[0].currentImage <= 0:
                            each.ImageSets[each.currentSet].ImageSet[0].currentImage = 1
                    imgI += 1
            else:
                imgI = 0
                for each in SceneCharacters:
                    if imgI == settingCharcter:
                        each.ImageSets[each.currentSet].ImageSet[0].currentImage = getFromName(settingToImage, each.ImageSets[each.currentSet].ImageSet[0].Images)
                        if each.ImageSets[each.currentSet].ImageSet[0].AlwaysOn == 1 and each.ImageSets[each.currentSet].ImageSet[0].currentImage <= 0:
                            each.ImageSets[each.currentSet].ImageSet[0].currentImage = 1
                    imgI += 1
    hide screen ON_CharacterDialogueScreen
    return
label JsonFuncChangeImageLayer(forEvery=False, forSpecific=False):
    $ everyLayerRandom = []
    $ everyLayerSpecific = {}
    $ settingToImage = ""
    if RoledCGOn == 1:
        $ monsterEncounterCG = UpdateCGRoles(monsterEncounterCG, monsterEncounter)
    $ lineOfScene += 1
    $ layerToChange = displayingScene.theScene[lineOfScene]
    if "ForEvery" == displayingScene.theScene[lineOfScene+1]:
        $ forEvery = True
        $ lineOfScene += 2
        $ settingCharacter = displayingScene.theScene[lineOfScene]
        $ lineOfScene += 1
        if "Random" == displayingScene.theScene[lineOfScene]:
            $ lineOfScene += 1
            while displayingScene.theScene[lineOfScene] != "EndLoop":
                $ everyLayerRandom.append(displayingScene.theScene[lineOfScene])
                $ lineOfScene += 1
            $ lineOfScene += 1
        else:
            $ settingToImage = displayingScene.theScene[lineOfScene]
        $ imgI = 0
        $ ifIsInScene = 0
    elif "ForSpecific" == displayingScene.theScene[lineOfScene+1]:
        $ forSpecific = True
        $ lineOfScene += 2
        $ settingCharacter = displayingScene.theScene[lineOfScene]
        $ lineOfScene += 1
        while displayingScene.theScene[lineOfScene] != "EndLoop":
            $ everyLayerSpecificIndex = int(displayingScene.theScene[lineOfScene]) - 1
            $ lineOfScene += 1
            $ everyLayerSpecific[settingCharacter + str(everyLayerSpecificIndex)] = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
        $ imgI = 0
        $ ifIsInScene = 0
    else:
        if DialogueIsFrom == "Monster":
            $ lineOfScene += 1
            python:
                try:
                    settingCharcter = int(displayingScene.theScene[lineOfScene]) - 1
                    lineOfScene += 1
                    settingToImage = displayingScene.theScene[lineOfScene]
                except:
                    ifIsInScene = 0

                    if len(monsterEncounter) > 0 and hidingCombatEncounter == 0:
                        #during combat layer change
                        if getFromName(displayingScene.theScene[lineOfScene], trueMonsterEncounter)!= -1:
                            ifIsInScene = 1
                            settingCharcter = getFromName(displayingScene.theScene[lineOfScene], trueMonsterEncounter)
                            lineOfScene += 1
                            settingToImage = displayingScene.theScene[lineOfScene]
                    if ifIsInScene == 0:
                        settingToImage = displayingScene.theScene[lineOfScene]
                        settingCharcter = CombatFunctionEnemytarget

            if RoledCGOn == 1:
                $ settingCharcter = getFromName("RoleTrackedCG", monsterEncounter)

            #change the image layers for monsters post combat, I need to really condense all the image card stuff into one single thing, but condensing the change image layer crap into one is a start.
            if layerToChange == "ImageSet" or  layerToChange == "ImageSetDontCarryOver" or layerToChange == "ImageSetPersist":
                $ monsterEncounter = changeImgSet(monsterEncounter, settingCharcter, layerToChange, settingToImage)
                $ DefeatedEncounterMonsters = changeImgSet(DefeatedEncounterMonsters, settingCharcter, layerToChange, settingToImage)
                #$ monsterEncounter[settingCharcter] = initiateOverlays(monsterEncounter[settingCharcter])
                #$ DefeatedEncounterMonsters[settingCharcter] = initiateOverlays(DefeatedEncounterMonsters[settingCharcter])
            elif layerToChange == "ImageSetRoleStart":
                if RoledCGOn == 0:
                    $ RoledCGOn = 1
                    $ monsterEncounter.append(copy.deepcopy(monsterEncounter[CombatFunctionEnemytarget]))
                    $ monsterEncounter[-1].name = "RoleTrackedCG"
                    $ layerToChange = "ImageSetDontCarryOver"
                    $ settingCharcter = len(monsterEncounter) - 1
                    $ monsterEncounter = changeImgSet(monsterEncounter, settingCharcter, layerToChange, settingToImage)
            else:
                $ monsterEncounter = changeImgLayer(monsterEncounter, settingCharcter, layerToChange, settingToImage)
                $ DefeatedEncounterMonsters = changeImgLayer(DefeatedEncounterMonsters, settingCharcter, layerToChange, settingToImage)
        else:
            if len(monsterEncounter) == 0 or hidingCombatEncounter == 1 and not forEvery:
                python:
                    try:
                        lineOfScene += 1
                        settingCharcter = int(displayingScene.theScene[lineOfScene]) - 1
                    except:
                        ifIsInScene = 0
                        if len(monsterEncounter) > 0 and hidingCombatEncounter == 0:
                            #during combat layer change
                            if getFromName(displayingScene.theScene[lineOfScene], trueMonsterEncounter)!= -1:
                                ifIsInScene = 1#CombatFunctionEnemytarget
                                settingCharcter = getFromName(displayingScene.theScene[lineOfScene], trueMonsterEncounter)
                        else:
                            #out of combat layer change
                            if getFromName(displayingScene.theScene[lineOfScene], SceneCharacters)!= -1:
                                ifIsInScene = 1
                                settingCharcter = getFromName(displayingScene.theScene[lineOfScene], SceneCharacters)
                        if ifIsInScene == 0:
                            lineOfScene -= 1
                            settingCharcter = 0
            else:
                $ settingCharcter = CombatFunctionEnemytarget
            $ lineOfScene += 1
            $ settingToImage = displayingScene.theScene[lineOfScene]
            $ imgI = 0
    if len(monsterEncounter) > 0 and hidingCombatEncounter == 0:
        #during combat layer change
        if RoledCGOn == 1:
            $ settingCharcter = 0
            python:
                for each in CgRoleKeeper:
                    stancePass = 0
                    imgI = 0
                    for mon in monsterEncounter:
                        if imgI == CombatFunctionEnemytarget:
                            for stance in mon.combatStance:
                                if stance.Stance == each.StanceReq:
                                    stancePass = 1
                                if each.StanceReq == "" or each.StanceReq == "None" or each.StanceReq == "Any":
                                    stancePass = 1
                        imgI += 1
                    if stancePass == 1:
                        for relay in each.Translators:
                            if relay.In == layerToChange:
                                layerToChange = relay.Out
        elif settingCharcter == -1:
            $ settingCharcter = len(monsterEncounter) - 1
        if layerToChange == "ImageSet" or layerToChange == "ImageSetPersist"  or  layerToChange == "ImageSetDontCarryOver":            
            if RoledCGOn == 1:
                $ monsterEncounterCG = changeImgSet(monsterEncounterCG, settingCharcter, layerToChange, settingToImage)
            elif forEvery:
                python:
                    for i, everyifiedMonster in enumerate(monsterEncounter):
                        if settingCharacter == everyifiedMonster.IDname:
                            if everyLayerRandom:
                                settingToImage = renpy.random.choice(everyLayerRandom)
                            monsterEncounter = changeImgSet(monsterEncounter, settingCharcter, layerToChange, settingToImage)
            elif forSpecific:
                python:
                    for i, everyifiedMonster in enumerate(monsterEncounter):
                        everyLayerSpecificKey = settingCharacter + str(i)
                        if everyLayerSpecificKey in everyLayerSpecific:
                            settingToImage = everyLayerSpecific[everyLayerSpecificKey]
                            monsterEncounter = changeImgSet(monsterEncounter, settingCharcter, layerToChange, settingToImage)
            else:
                $ monsterEncounter = changeImgSet(monsterEncounter, settingCharcter, layerToChange, settingToImage)
            #$ monsterEncounter[settingCharcter] = initiateOverlays(monsterEncounter[settingCharcter])
        elif layerToChange == "ImageSetRoleStart":
            if RoledCGOn == 0:
                $ RoledCGOn = 1
                $ CgRoleKeeper = []
                $ monsterEncounterCG = []
                $ CGRoleBuffer = 5
                $ monsterEncounterCG.append(copy.deepcopy(monsterEncounter[CombatFunctionEnemytarget]))
                $ layerToChange = "ImageSetDontCarryOver"
                $ settingCharcter = 0
                $ monsterEncounterCG = changeImgSet(monsterEncounterCG, settingCharcter, layerToChange, settingToImage)
                $ CgRoleKeeper = copy.deepcopy(monsterEncounterCG[0].ImageSets[monsterEncounterCG[0].currentSet].Roles)
                #$ CgRoleKeeper = [
                #                    CGRole("FaceRider", "Face Sit", "Imp", [CGTranslator("Expression", "FaceImpExpressionRide")], ["FaceImpExpressionRide", "FaceImp"], "Yes"),
                #                    CGRole("Sex", "Sex", "Imp", [CGTranslator("Expression", "DickImpExpression")], ["DickImpExpression", "DickImp"], "Yes"),
                #                    CGRole("Silhouette4", "", "Imp", [], ["ImpSilhouette4"]),
                #                    CGRole("Silhouette1", "", "Imp", [], ["ImpSilhouette1"]),
                #                    CGRole("Silhouette3", "", "Imp", [], ["ImpSilhouette3"]),
                #                    CGRole("Silhouette2", "", "Imp", [], ["ImpSilhouette2"])
                #                    ]
                $ monsterEncounterCG = UpdateCGRoles(monsterEncounterCG, monsterEncounter)
        else:
            if RoledCGOn == 1:
                $ monsterEncounterCG = changeImgLayer(monsterEncounterCG, settingCharcter, layerToChange, settingToImage)
            else:
                if forEvery:
                    python:
                        for i, everyifiedMonster in enumerate(monsterEncounter):
                            if settingCharacter == everyifiedMonster.IDname:
                                if everyLayerRandom:
                                    settingToImage = renpy.random.choice(everyLayerRandom)
                                monsterEncounter = changeImgLayer(monsterEncounter, settingCharcter, layerToChange, settingToImage)
                elif forSpecific:
                    python:
                        for i, everyifiedMonster in enumerate(monsterEncounter):
                            everyLayerSpecificKey = settingCharacter + str(i)
                            if everyLayerSpecificKey in everyLayerSpecific:
                                settingToImage = everyLayerSpecific[everyLayerSpecificKey]
                                monsterEncounter = changeImgLayer(monsterEncounter, settingCharcter, layerToChange, settingToImage)
                else:
                    $ monsterEncounter = changeImgLayer(monsterEncounter, settingCharcter, layerToChange, settingToImage)
    else:
        #out of combat layer change
        if layerToChange == "ImageSet" or layerToChange == "ImageSetPersist"  or  layerToChange == "ImageSetDontCarryOver":
            if forEvery:
                python:
                    for i, everyifiedMonster in enumerate(SceneCharacters):
                        if settingCharacter == everyifiedMonster.IDname:
                            if everyLayerRandom:
                                settingToImage = renpy.random.choice(everyLayerRandom)
                            SceneCharacters = changeImgSet(SceneCharacters, settingCharcter, layerToChange, settingToImage)
            elif forSpecific:
                python:
                    for i, everyifiedMonster in enumerate(SceneCharacters):
                        everyLayerSpecificKey = settingCharacter + str(i)
                        if everyLayerSpecificKey in everyLayerSpecific:
                            settingToImage = everyLayerSpecific[everyLayerSpecificKey]
                            SceneCharacters = changeImgSet(SceneCharacters, settingCharcter, layerToChange, settingToImage)
            else:
                $ SceneCharacters = changeImgSet(SceneCharacters, settingCharcter, layerToChange, settingToImage)
            # $ SceneCharacters[settingCharcter] = initiateOverlays(SceneCharacters[settingCharcter])
        else:
            if forEvery:
                python:
                    for i, everyifiedMonster in enumerate(SceneCharacters):
                        if settingCharacter == everyifiedMonster.IDname:
                            if everyLayerRandom:
                                settingToImage = renpy.random.choice(everyLayerRandom)
                            SceneCharacters = changeImgLayer(SceneCharacters, i, layerToChange, settingToImage)
            elif forSpecific:
                python:
                    for i, everyifiedMonster in enumerate(SceneCharacters):
                        everyLayerSpecificKey = settingCharacter + str(i)
                        if everyLayerSpecificKey in everyLayerSpecific:
                            settingToImage = everyLayerSpecific[everyLayerSpecificKey]
                            SceneCharacters = changeImgLayer(SceneCharacters, i, layerToChange, settingToImage)
            else:
                $ SceneCharacters = changeImgLayer(SceneCharacters, settingCharcter, layerToChange, settingToImage)
    hide screen ON_CharacterDialogueScreen
    return
label JsonFuncChangeProgress:
    $ lineOfScene += 1
    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
    $ ProgressEvent[DataLocation].eventProgress += int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncChangeProgressBasedOnVirility:
    $ lineOfScene += 1
    $ multiplier = float(displayingScene.theScene[lineOfScene])

    $ virilityProg = getVirility(player)*0.1
    #if getVirility(player) < 350:
    #    $ virilityProg = 0.5 + ( getVirility(player)/(50-( getVirility(player)*0.1259)))
    #else:
    #    $ virilityProg = getVirility(player)-290.5
    $ virilityProg *= multiplier

    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
    $ ProgressEvent[DataLocation].eventProgress += virilityProg
    return
label JsonFuncChangeArousal(whichJsonFunc):
    $ functionQuiet = 0 
    if whichJsonFunc == "ChangeArousalQuietly":
        $ functionQuiet = 1
    $ lineOfScene += 1
    $ player.stats.hp += int(displayingScene.theScene[lineOfScene])
    if not functionQuiet:
        if (int(displayingScene.theScene[lineOfScene]) > 0):
            $ display = "You were aroused by " + displayingScene.theScene[lineOfScene] + "!" 
        else:
            $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
            $ display = "You calmed down by " + str(amountLost) + "!"
    if player.stats.hp <= 0:
        $ player.stats.hp = 0
    if (int(displayingScene.theScene[lineOfScene]) != 0) and (functionQuiet == 0):
        call read from _call_read_57
    return
label JsonFuncChangeArousalByPercent:
    $ lineOfScene += 1
    $ check = ( float(displayingScene.theScene[lineOfScene]) / 100) * player.stats.max_true_hp
    $ check = math.floor(check)
    $ check = int(check)
    $ player.stats.hp += check

    if player.stats.hp <= 0:
        $ player.stats.hp = 0
    return
label JsonFuncChangeEnergy(whichJsonFunc):
    $ functionQuiet = 0
    if whichJsonFunc == "ChangeEnergyQuietly":
        $ functionQuiet = 1
    $ lineOfScene += 1
    $ player.stats.ep += int(displayingScene.theScene[lineOfScene]) 
    if not functionQuiet:
        if (int(displayingScene.theScene[lineOfScene]) < 0):
            $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
            $ display = "You lost " + str(amountLost) + " energy!"
        else:
            $ display = "You gain " + displayingScene.theScene[lineOfScene] + " energy!"
    if player.stats.ep <= 0:
        $ player.stats.ep = 0
    if player.stats.ep > player.stats.max_true_ep:
        $ player.stats.ep = player.stats.max_true_ep
    if (int(displayingScene.theScene[lineOfScene]) != 0) and (functionQuiet == 0):
        "[display!i]"
    return
label JsonFuncChangeEnergyByPercent:
    $ lineOfScene += 1
    $ check = ( float(displayingScene.theScene[lineOfScene]) / 100) * player.stats.max_true_ep
    $ check = math.floor(check)
    $ check = int(check)
    $ player.stats.ep += check

    if player.stats.ep <= 0:
        $ player.stats.ep = 0
    if player.stats.ep > player.stats.max_true_ep:
        $ player.stats.ep = player.stats.max_true_ep
    return
label JsonFuncChangeSpirit(whichJsonFunc):
    $ functionQuiet = 0
    if whichJsonFunc == "ChangeSpiritQuietly":
        $ functionQuiet = 1
    $ lineOfScene += 1
    $ player.stats.sp += int(displayingScene.theScene[lineOfScene])
    if not functionQuiet:
        if (int(displayingScene.theScene[lineOfScene]) < 0):
            $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
            $ display = "You lost " + str(amountLost) + " spirit!"
        else:
            $ display = "You gain " + displayingScene.theScene[lineOfScene] + " spirit!"
    if player.stats.sp <= 0:
        $ player.stats.sp = 0
    if player.stats.sp > player.stats.max_true_sp:
        $ player.stats.sp = player.stats.max_true_sp
    if (int(displayingScene.theScene[lineOfScene]) != 0) and functionQuiet == 0:
        "[display!i]"
    return
label JsonFuncChangeMaxArousal:
    $ lineOfScene += 1

    $ player.stats.max_hp += int(displayingScene.theScene[lineOfScene])
    $ player.CalculateStatBoost()

    if (int(displayingScene.theScene[lineOfScene]) > 0):
        $ display = "You gained " + displayingScene.theScene[lineOfScene] + " maximum arousal!"
    else:
        $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
        $ display = "You lost " + str(amountLost) + " maximum arousal!"

    if player.stats.hp <= 0:
        $ player.stats.hp = 0
    if (int(displayingScene.theScene[lineOfScene]) != 0):
        "[display!i]"
    return
label JsonFuncChangeMaxEnergy:
    $ lineOfScene += 1

    $ player.stats.max_ep += int(displayingScene.theScene[lineOfScene])
    $ player.CalculateStatBoost()

    if (int(displayingScene.theScene[lineOfScene]) < 0):
        $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
        $ display = "You lost " + str(amountLost) + " maximum energy!"
    else:
        $ display = "You gain " + displayingScene.theScene[lineOfScene] + " maximum energy!"
    if player.stats.ep <= 0:
        $ player.stats.ep = 0
    if player.stats.ep > player.stats.max_true_ep:
        $ player.stats.ep = player.stats.max_true_ep
    if (int(displayingScene.theScene[lineOfScene]) != 0):
        "[display!i]"
    return
label JsonFuncChangeMaxSpirit:
    $ lineOfScene += 1
    $ player.stats.max_sp += int(displayingScene.theScene[lineOfScene])
    if (int(displayingScene.theScene[lineOfScene]) < 0):
        $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
        $ display = "You lost " + str(amountLost) + " maximum spirit!"
    else:
        $ display = "You gain " + displayingScene.theScene[lineOfScene] + " maximum spirit!"
    if player.stats.sp <= 0:
        $ player.stats.sp = 0
    if player.stats.sp > player.stats.max_true_sp:
        $ player.stats.sp = player.stats.max_true_sp
    if (int(displayingScene.theScene[lineOfScene]) != 0):
        "[display!i]"
    return
label JsonFuncChangePower:
    $ lineOfScene += 1
    $ player.stats.Power += int(displayingScene.theScene[lineOfScene])
    if (int(displayingScene.theScene[lineOfScene]) < 0):
        $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
        $ display = "You permanently lost " + str(amountLost) + " power!"
    else:
        $ display = "You permanently gain " + displayingScene.theScene[lineOfScene] + " power!"
    $ player.CalculateStatBoost()
    if (int(displayingScene.theScene[lineOfScene]) != 0):
        "[display!i]"
    return
label JsonFuncChangeWill:
    $ lineOfScene += 1
    $ player.stats.Willpower += int(displayingScene.theScene[lineOfScene])
    if (int(displayingScene.theScene[lineOfScene]) < 0):
        $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
        $ display = "You permanently lost " + str(amountLost) + " willpower!"
    else:
        $ display = "You permanently gain " + displayingScene.theScene[lineOfScene] + " willpower!"
    $ player.CalculateStatBoost()
    if (int(displayingScene.theScene[lineOfScene]) != 0):
        "[display!i]"
    return
label JsonFuncChangeInt:
    $ lineOfScene += 1
    $ player.stats.Int += int(displayingScene.theScene[lineOfScene])
    if (int(displayingScene.theScene[lineOfScene]) < 0):
        $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
        $ display = "You permanently lost " + str(amountLost) + " intelligence!"
    else:
        $ display = "You permanently gain " + displayingScene.theScene[lineOfScene] + " intelligence!"
    $ player.CalculateStatBoost()
    if (int(displayingScene.theScene[lineOfScene]) != 0):
        "[display!i]"
    return
label JsonFuncChangeTech:
    $ lineOfScene += 1
    $ player.stats.Tech += int(displayingScene.theScene[lineOfScene])
    if (int(displayingScene.theScene[lineOfScene]) < 0):
        $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
        $ display = "You permanently lost " + str(amountLost) + " technique!"
    else:
        $ display = "You permanently gain " + displayingScene.theScene[lineOfScene] + " technique!"
    if (int(displayingScene.theScene[lineOfScene]) != 0):
        "[display!i]"
    return
label JsonFuncChangeAllure:
    $ lineOfScene += 1
    $ player.stats.Allure += int(displayingScene.theScene[lineOfScene])
    if (int(displayingScene.theScene[lineOfScene]) < 0):
        $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
        $ display = "You permanently lost " + str(amountLost) + " allure!"
    else:
        $ display = "You permanently gain " + displayingScene.theScene[lineOfScene] + " allure!"
    if (int(displayingScene.theScene[lineOfScene]) != 0):
        "[display!i]"
    return
label JsonFuncChangeLuck:
    $ lineOfScene += 1
    $ player.stats.Luck += int(displayingScene.theScene[lineOfScene])
    if (int(displayingScene.theScene[lineOfScene]) < 0):
        $ amountLost = int(displayingScene.theScene[lineOfScene])*-1
        $ display = "You permanently lost " + str(amountLost) + " luck!"
    else:
        $ display = "You permanently gain " + displayingScene.theScene[lineOfScene] + " luck!"
    if (int(displayingScene.theScene[lineOfScene]) != 0):
        "[display!i]"
    return
label JsonFuncChangeSensitivity:
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
        $ display = "You lost " + str(amountLost) + " " + resTarget +  " sensitivity!"
    else:
        $ TempSensitivity.changeRes (resTarget, resAmount)
        if resTarget == "Breasts":
            $ resTarget = "Nipple"
        if resTarget == "Sex":
            $ resTarget = "Cock"
        $ display = "You gained " + displayingScene.theScene[lineOfScene] + " " + resTarget +  " sensitivity!"
    if (int(displayingScene.theScene[lineOfScene]) != 0):
        "[display!i]"
    return
label JsonFuncChangeFetish:
    $ lineOfScene += 1
    $ resTarget = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ resAmount = int(displayingScene.theScene[lineOfScene])
    $ baseFetish = player.getFetish(resTarget)
    $ fetchFetish = getFromName(resTarget, player.FetishList)
    if player.FetishList[fetchFetish].Type == "Fetish":
        while resAmount + baseFetish > 100 and resAmount > 0:
            $ resAmount-=1
            if resAmount < 0:
                $ resAmount = 0
    $ baseFetish += resAmount
    $ player.setFetish(resTarget, baseFetish)
    if (resAmount > 0):
        $ L = 0
        python:
            for fet in TempFetishes:
                if fet.name == resTarget and player.FetishList[L].Type == "Fetish":
                    TempFetishes[L].Level += resAmount
                    if TempFetishes[L].Level > 100 - baseFetish + TempFetishes[L].Level and baseFetish <100:
                        TempFetishes[L].Level = 100 - baseFetish + TempFetishes[L].Level
                L += 1
    if player.FetishList[fetchFetish].Type == "Fetish":
        if baseFetish < 100:
            if (resAmount > 0):
                if baseFetish - resAmount == 0:
                    $ display = "You have started getting a fetish for " + resTarget +  "..."
                elif baseFetish - resAmount < 25 and baseFetish >= 25:
                    $ display = "You have acquired a fetish for " + resTarget +  "."
                else:
                    $ display = "Your fetish for " + resTarget +  " has intensified!"
            elif (resAmount < 0):
                if baseFetish <= 0:
                    $ display = "You have lost your fetish for " + resTarget +  "."
                else:
                    $ display = "Your fetish for " + resTarget +  " has receded."
        if baseFetish >= 100:
            if baseFetish >= 100:
                $ display = "Your fetish for " + resTarget +  " has become a complete and total obsession, but it can't get any worse than it is now...."
            #elif baseFetish > 10:
                #$ display = "Fantasies of " + resTarget +  " swirl through your mind as your heart pounds in your chest... You have {i}permanently{/i} gained a fetish level for " + resTarget + ", temporarily bringing your obsessive fetish of " + resTarget +  " to level " + str(fetchFetish) + "..."
        if (int(displayingScene.theScene[lineOfScene]) != 0):
            "[display!i]"
    return
label JsonFuncChangeGridNPCMovement:
    $ lineOfScene += 1
    $ ActiveGridNPCs[currentGridNPC].Movement = displayingScene.theScene[lineOfScene]
    if ActiveGridNPCs[currentGridNPC].Movement != "Wander":
        $ lineOfScene += 1
        if  displayingScene.theScene[lineOfScene] == "Coord":
            $ ActiveGridNPCs[currentGridNPC].MovementTarget = "TargetSet"
            $ lineOfScene += 1
            $ ActiveGridNPCs[currentGridNPC].TargetCoords[0]
            $ lineOfScene += 1
            $ ActiveGridNPCs[currentGridNPC].TargetCoords[1]
        else:
            $ ActiveGridNPCs[currentGridNPC].MovementTarget = displayingScene.theScene[lineOfScene]

            if ActiveGridNPCs[currentGridNPC].Movement == "Whimsical":
                $ lineOfScene += 1
                $ ActiveGridNPCs[currentGridNPC].WhimsyRange = int(displayingScene.theScene[lineOfScene])
                $ ActiveGridNPCs[currentGridNPC].MovementVector=[-1,-1]
    return
label JsonFuncChangeGridVision:
    $ lineOfScene += 1
    $ PlayerGridSight = int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncChangeMapTile:
    $ lineOfScene += 1
    $ coordX = int(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ coordY = int(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ newTile = displayingScene.theScene[lineOfScene]
    $ TheGrid[coordY][coordX] = newTile
    return
label JsonFuncChangeNextStatCheckDifficulty:
    $ lineOfScene += 1
    $ increaseStatCheck += int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncChangeBG:
    $ lineOfScene += 1
    $ bg = changeBG(displayingScene.theScene[lineOfScene])
    return
label JsonFuncChangeBGM:
    $ lineOfScene += 1
    $ bgm = displayingScene.theScene[lineOfScene]
    $ BGMlist = []
    $ BGMlist.append(bgm)
    $ renpy.random.shuffle(BGMlist)
    $ overrideCombatMusic = 0
    if renpy.music.get_playing(channel='music') != bgm:
        play music BGMlist fadeout 1.0 fadein 1.0
    $ musicLastPlayed = BGMlist
    return
label JsonFuncChangeBGMOverrideCombatMusic:
    $ lineOfScene += 1
    $ bgm = displayingScene.theScene[lineOfScene]
    $ BGMlist = []
    $ BGMlist.append(bgm)
    $ renpy.random.shuffle(BGMlist)
    if renpy.music.get_playing(channel='music') != bgm:
        play music BGMlist fadeout 1.0 fadein 1.0
    $ musicLastPlayed = BGMlist
    $ overrideCombatMusic = 1
    return
label JsonFuncChangeBGMNoFade:
    $ lineOfScene += 1
    $ bgm = displayingScene.theScene[lineOfScene]
    $ BGMlist = []
    $ BGMlist.append(bgm)
    $ renpy.random.shuffle(BGMlist)
    if renpy.music.get_playing(channel='music') != bgm:
        play music BGMlist
    $ musicLastPlayed = BGMlist
    return
label JsonFuncChangeBGMList:
    $ BGMlist = []
    $ musicLastPlayed = BGMlist
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1

        $ bgm = displayingScene.theScene[lineOfScene]
        $ BGMlist.append(bgm)

    $ renpy.random.shuffle(BGMlist)
    play music BGMlist fadeout 1.0 fadein 1.0
    return
label JsonFuncChangeEros:
    $ lineOfScene += 1
    $ moneyEarned = int(displayingScene.theScene[lineOfScene])
    $ player.inventory.money += moneyEarned
    if int(displayingScene.theScene[lineOfScene]) > 0:
        $ display = "Gained " + str(moneyEarned) + " eros!"
    else:
        $ amountLost = moneyEarned*-1
        $ display = "Lost " + str(amountLost) + " eros!"
    "[display!i]"
    return
label JsonFuncChangeErosByPercent:
    $ lineOfScene += 1
    $ preChange = copy.copy(player.inventory.money)
    $ check = ( float(displayingScene.theScene[lineOfScene]) / 100) * player.inventory.money
    $ check = math.floor(check)
    $ check = int(check)
    $ player.inventory.money += check

    if player.inventory.money <= 0:
        $ player.inventory.money = 0

    if float(displayingScene.theScene[lineOfScene]) >= 100:
        $ display = "Gained " + str(check - preChange) + " eros!"
    else:
        $ display = "Lost " + str(preChange - check) + " eros!"
    "[display!i]"
    return
label JsonFuncChangePerkDuration:
    $ lineOfScene += 1
    $ perkToChange = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ amountToChange = int(displayingScene.theScene[lineOfScene])
    $ displayList = []

    $ holda = changePerkDuration(player, perkToChange, amountToChange)
    $ player = holda[0]
    $ displayList = holda[1]

    $ p = 0
    while p < len(displayList):
        $ display = displayList[p]
        "[display!i]"
        $ p += 1
    return
# Change monster funcs
label JsonFuncChangeMonsterArousal:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].stats.hp += int(displayingScene.theScene[lineOfScene])
    if monsterEncounter[CombatFunctionEnemytarget].stats.hp <= 0:
        $ monsterEncounter[CombatFunctionEnemytarget].stats.hp = 0
    return
label JsonFuncChangeMonsterEnergy:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].stats.ep += int(displayingScene.theScene[lineOfScene])
    if monsterEncounter[CombatFunctionEnemytarget].stats.ep <= 0:
        $ monsterEncounter[CombatFunctionEnemytarget].stats.ep = 0
    if monsterEncounter[CombatFunctionEnemytarget].stats.ep > monsterEncounter[CombatFunctionEnemytarget].stats.max_true_ep:
        $ monsterEncounter[CombatFunctionEnemytarget].stats.ep = monsterEncounter[CombatFunctionEnemytarget].stats.max_true_ep
    return
label JsonFuncChangeMonsterLevel:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].stats.lvl += int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncChangeMonsterSpirit:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].stats.sp += int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncChangeMonsterMaxArousal:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].stats.max_hp += int(displayingScene.theScene[lineOfScene])
    $ monsterEncounter[CombatFunctionEnemytarget].stats.max_true_hp =  monsterEncounter[CombatFunctionEnemytarget].stats.max_hp
    return
label JsonFuncChangeMonsterMaxEnergy:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].stats.max_ep += int(displayingScene.theScene[lineOfScene])
    $ monsterEncounter[CombatFunctionEnemytarget].stats.max_true_ep =  monsterEncounter[CombatFunctionEnemytarget].stats.max_ep
    $ monsterEncounter[CombatFunctionEnemytarget].stats.ep += int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncChangeMonsterMaxSpirit:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].stats.max_sp += int(displayingScene.theScene[lineOfScene])
    $ monsterEncounter[CombatFunctionEnemytarget].stats.sp += int(displayingScene.theScene[lineOfScene])
    $ monsterEncounter[CombatFunctionEnemytarget].stats.max_true_sp =  monsterEncounter[CombatFunctionEnemytarget].stats.max_sp
    return
label JsonFuncChangeMonsterPower:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].stats.Power += int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncChangeMonsterWill:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].stats.Willpower += int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncChangeMonsterInt:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].stats.Int += int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncChangeMonsterTech:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].stats.Tech += int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncChangeMonsterAllure:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].stats.Allure += int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncChangeMonsterLuck:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].stats.Luck += int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncChangeMonsterSensitivity:
    $ lineOfScene += 1
    $ resTarget = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ resAmount = int(displayingScene.theScene[lineOfScene])
    $ monsterEncounter[CombatFunctionEnemytarget].BodySensitivity.changeRes(resTarget, resAmount)
    return
label JsonFuncChangeMonsterStatusEffectResistances:
    $ lineOfScene += 1
    $ resTarget = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ resAmount = int(displayingScene.theScene[lineOfScene])
    $ monsterEncounter[CombatFunctionEnemytarget].resistancesStatusEffects.changeRes(resTarget, resAmount)
    return
label JsonFuncChangeMonsterFetish:
    $ lineOfScene += 1
    $ resTarget = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ resAmount = int(displayingScene.theScene[lineOfScene])
    $ baseFetish = monsterEncounter[CombatFunctionEnemytarget].getFetish(resTarget)
    $ baseFetish += resAmount
    $ monsterEncounter[CombatFunctionEnemytarget].setFetish(resTarget, baseFetish)
    return
label JsonFuncChangeMonsterErosDrop:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].moneyDropped += int(displayingScene.theScene[lineOfScene])
    return
label JsonFuncChangeMonsterExpDrop:
    $ lineOfScene += 1
    $ monsterEncounter[CombatFunctionEnemytarget].stats.Exp += int(displayingScene.theScene[lineOfScene])
    return
