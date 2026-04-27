label SceneRequires_MinimumProgress:
    $ passLocalProgressChecks += 1
    $ lineOfScene += 1
    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
    if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[DataLocation].eventProgress:
        $ passLocalProgressCheck += 1
    $ lineOfScene += 1
    return

label SceneRequires_MinimumProgressFromEvent:
    $ passProgressChecks += 1
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[CheckEvent].eventProgress:
        $ passProgressCheck += 1
    $ lineOfScene += 1
    return

label SceneRequires_LessProgress:
    $ passLocalProgressChecks += 1
    $ lineOfScene += 1
    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
    if int(displayingScene.theScene[lineOfScene]) > ProgressEvent[DataLocation].eventProgress:
        $ passLocalProgressCheck += 1
    $ lineOfScene += 1
    return

label SceneRequires_LessProgressFromEvent:
    $ passProgressChecks += 1
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    if int(displayingScene.theScene[lineOfScene]) > ProgressEvent[CheckEvent].eventProgress:
        $ passProgressCheck += 1
    $ lineOfScene += 1
    return

label SceneRequires_Choice:
    $ passLocalChoiceChecks += 1
    $ lineOfScene += 1
    $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
    while choiceToCheck-1 >= len(ProgressEvent[DataLocation].choices):
        $ ProgressEvent[DataLocation].choices.append("")
    if displayingScene.theScene[lineOfScene] == ProgressEvent[DataLocation].choices[choiceToCheck-1]:
        $ passLocalChoiceCheck += 1
    $ lineOfScene += 1
    return

label SceneRequires_ChoiceFromEvent:
    $ passChoiceChecks += 1
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    $ lineOfScene += 1
    $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
    while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
        $ ProgressEvent[CheckEvent].choices.append("")
    $ lineOfScene += 1
    if displayingScene.theScene[lineOfScene] == ProgressEvent[CheckEvent].choices[choiceToCheck-1]:
        $ passChoiceCheck += 1
    $ lineOfScene += 1
    return

label SceneRequires_Time:
    $ passTimeChecks += 1
    $ lineOfScene += 1
    if IfTime(displayingScene.theScene[lineOfScene]) == 1:
        $ passTimeCheck += 1
    $ lineOfScene += 1
    return

label SceneRequires_Stat:
    $ passStatcheck = 0
    $ lineOfScene += 1
    $ whatStatisIt = displayingScene.theScene[lineOfScene]
    $ statToCheck = player.stats.getStat(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ needsStat = int(displayingScene.theScene[lineOfScene])
    if needsStat <= statToCheck:
        $ passStatcheck = 1
    $ lineOfScene += 1
    return

label SceneRequires_FetishLevelEqualOrGreater:
    $ passFetCheck += 1
    $ lineOfScene += 1
    $ fetchFetish = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ fetishLvl = int(displayingScene.theScene[lineOfScene])
    if player.getFetish(fetchFetish) >= fetishLvl:
        $ passFetChecks += 1
    $ lineOfScene += 1
    return

label SceneRequires_FetishLevelEqualOrLess:
    $ passFetCheck += 1
    $ lineOfScene += 1
    $ fetchFetish = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ fetishLvl = int(displayingScene.theScene[lineOfScene])
    if player.getFetish(fetchFetish) <= fetishLvl:
        $ passFetChecks += 1
    $ lineOfScene += 1
    return

label SceneRequires_Item:
    $ passItemCheck += 1
    $ lineOfScene += 1
    $ itemName = displayingScene.theScene[lineOfScene]
    if itemName in equippedItemsSet or itemName in inventoryItemsSet:
        $ passItemChecks += 1
    if passItemCheck != passItemChecks and failedItemChecked == 0:
        $ failedItemChecked = 1
        $ whatItemIsIt = itemName
    elif inverseRequirement == 1:
        $ whatItemIsIt = itemName
    $ lineOfScene += 1
    return

label SceneRequires_ItemEquipped:
    $ passEquipmentCheck += 1
    $ lineOfScene += 1
    $ itemName = displayingScene.theScene[lineOfScene]
    if itemName in equippedItemsSet:
        $ passEquipmentChecks += 1
    if passEquipmentCheck != passEquipmentChecks and failedEquipmentChecked == 0:
        $ failedEquipmentChecked = 1
        $ whatEquipmentIsIt = itemName
    elif inverseRequirement == 1:
        $ whatEquipmentIsIt = itemName
    $ lineOfScene += 1
    return

label SceneRequires_Skill:
    $ passSkillCheck += 1
    $ lineOfScene += 1
    $ skillName = displayingScene.theScene[lineOfScene]
    if skillName in skillNamesSet:
        $ passSkillChecks += 1
    if passSkillCheck != passSkillChecks and failedSkillChecked == 0:
        $ failedSkillChecked = 1
        $ whatSkillIsIt = skillName
    elif inverseRequirement == 1:
        $ whatSkillIsIt = skillName
    $ lineOfScene += 1
    return

label SceneRequires_Perk:
    $ passPerkCheck += 1
    $ lineOfScene += 1
    $ perk_name = displayingScene.theScene[lineOfScene]
    if perk_name in perkNamesSet:
        $ passPerkChecks += 1
    if passPerkCheck != passPerkChecks and failedPerkChecked == 0:
        $ failedPerkChecked = 1
        $ whatPerkIsIt = perk_name
    elif inverseRequirement == 1:
        $ whatPerkIsIt = perk_name
    $ lineOfScene += 1
    return

label SceneRequires_Energy:
    $ passEnergyCheck = 0
    $ hasEnergyCheck = 1
    $ lineOfScene += 1
    $ eAmount = displayingScene.theScene[lineOfScene]
    if player.stats.ep >= int(eAmount):
        $ passEnergyCheck = 1
    $ lineOfScene += 1
    return

label SceneRequires_Virility:
    $ passVirilityCheck = 0
    $ hasVirilityCheck = 1
    $ lineOfScene += 1
    $ vAmount = displayingScene.theScene[lineOfScene]
    if getVirility(player) >= int(vAmount):
        $ passVirilityCheck = 1
    $ lineOfScene += 1
    return

init python:
    requires_funcs = {
        "RequiresMinimumProgress": ["SceneRequires_MinimumProgress"],
        "RequiresMinimumProgressFromEvent": ["SceneRequires_MinimumProgressFromEvent"],
        "RequiresLessProgress": ["SceneRequires_LessProgress"],
        "RequiresLessProgressFromEvent": ["SceneRequires_LessProgressFromEvent"],
        "RequiresChoice": ["SceneRequires_Choice"],
        "RequiresChoiceFromEvent": ["SceneRequires_ChoiceFromEvent"],
        "RequiresTime": ["SceneRequires_Time"],
        "RequiresStat": ["SceneRequires_Stat"],
        "RequiresFetishLevelEqualOrGreater": ["SceneRequires_FetishLevelEqualOrGreater"],
        "RequiresFetishLevelEqualOrLess": ["SceneRequires_FetishLevelEqualOrLess"],
        "RequiresItem": ["SceneRequires_Item"],
        "RequiresItemEquipped": ["SceneRequires_ItemEquipped"],
        "RequiresSkill": ["SceneRequires_Skill"],
        "RequiresPerk": ["SceneRequires_Perk"],
        "RequiresEnergy": ["SceneRequires_Energy"],
        "RequiresVirility": ["SceneRequires_Virility"],
    }

label SceneRequiresCheck:
    $ equippedItemsSet = {
        player.inventory.RuneSlotOne.name,
        player.inventory.RuneSlotTwo.name,
        player.inventory.RuneSlotThree.name,
        player.inventory.AccessorySlot.name
    }
    $ inventoryItemsSet = {item.name for item in player.inventory.items}
    $ skillNamesSet = {skill.name for skill in player.skillList}
    $ perkNamesSet = {perk.name for perk in player.perks}

    $ whatStatisIt = ""
    $ whatItemIsIt = ""
    $ whatSkillIsIt = ""
    $ whatPerkIsIt = ""
    $ statToCheck = 0
    $ needsStat = 0
    $ eAmount = ""
    $ vAmount = ""
    $ hasVirilityCheck = 0
    $ hasEnergyCheck = 0
    $ hasStatCheck = 0

    $ passcheck = 0

    $ passStatcheck = 1

    $ passItemCheck = 0
    $ passItemChecks = 0
    $ passEquipmentCheck = 0
    $ passEquipmentChecks = 0
    $ passSkillCheck = 0
    $ passSkillChecks = 0
    $ passPerkCheck = 0
    $ passPerkChecks = 0
    $ passEnergyCheck = 1
    $ passVirilityCheck = 1
    $ passLocalProgressCheck = 0
    $ passLocalProgressChecks = 0
    $ passFetCheck = 0
    $ passFetChecks = 0
    $ passProgressCheck = 0
    $ passProgressChecks = 0
    $ passLocalChoiceCheck = 0
    $ passLocalChoiceChecks = 0
    $ passTimeCheck = 0
    $ passTimeChecks = 0
    $ passChoiceCheck = 0
    $ passChoiceChecks = 0
    $ hideFailedMenuChoice = 0
    $ isFinalOption = 0
    $ inverseRequirement = 0
    $ failedItemChecked = 0
    $ failedEquipmentChecked = 0
    $ failedSkillChecked = 0
    $ failedPerkChecked = 0
    $ Overriding = 0
    $ override = None

    $ checkPreFuncs = 0
    while checkPreFuncs == 0:
        if displayingScene.theScene[lineOfScene] == "HideOptionOnRequirementFail" and hideFailedMenuChoice == 0:
            $ hideFailedMenuChoice = 1
            $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "InverseRequirement":
            $ inverseRequirement = 1
            $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "ShuffleMenu":
            $ ShuffleMenuOptions = 1
            $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "OverrideOption":
            $ Overriding = 1
            $ lineOfScene += 1
        elif displayingScene.theScene[lineOfScene] == "FinalOption":
            $ lineOfScene += 1
            $ finalOption = displayingScene.theScene[lineOfScene]
            $ isFinalOption = 1
            $ finalOptionEvent = eventMenuJumps[-1]
            $ finalOptionEventScene = eventMenuSceneJumps[-1]
        elif displayingScene.theScene[lineOfScene] == "EventJump":
            $ lineOfScene += 1
            $ eventMenuJumps[-1] = displayingScene.theScene[lineOfScene]
            $ lineOfScene += 1
            if isFinalOption == 1:
                $ finalOptionEvent = eventMenuJumps[-1]
            if displayingScene.theScene[lineOfScene] == "ThenJumpToScene":
                $ lineOfScene += 1
                $ eventMenuSceneJumps[-1] = displayingScene.theScene[lineOfScene]
                $ lineOfScene += 1
                if isFinalOption == 1:
                    $ finalOptionEventScene = eventMenuSceneJumps[-1]

        elif displayingScene.theScene[lineOfScene] in requires_funcs:
            $ theLabelFunc = requires_funcs[displayingScene.theScene[lineOfScene]]
            $ renpy.call(*theLabelFunc)
        else:
            if Overriding == 1:
                $ override = displayingScene.theScene[lineOfScene]
            $ checkPreFuncs += 1

    if inverseRequirement == 0:
        if passStatcheck == 1 and passFetCheck == passFetChecks and passItemCheck == passItemChecks and passEquipmentCheck == passEquipmentChecks and passSkillCheck == passSkillChecks and passPerkCheck == passPerkChecks and passEnergyCheck == 1 and passVirilityCheck == 1 and passProgressCheck == passProgressChecks and passLocalProgressCheck == passLocalProgressChecks and passLocalChoiceCheck == passLocalChoiceChecks and passChoiceCheck == passChoiceChecks and passTimeCheck == passTimeChecks:
            $ passcheck = 1
        else:
            if hideFailedMenuChoice == 0:
                if passLocalChoiceCheck == passLocalChoiceChecks and passProgressCheck == passProgressChecks and passLocalProgressCheck == passLocalProgressChecks and passChoiceCheck == passChoiceChecks:
                    if passStatcheck == 0:
                        $ display = "Requires " + str(needsStat) + " " + whatStatisIt + "."
                    elif passItemCheck != passItemChecks:
                        $ display = "Requires a " + whatItemIsIt + " in your inventory."
                    elif passEquipmentCheck != passEquipmentChecks:
                        $ display = "Must not have " + whatEquipmentIsIt + " equipped."
                    elif passSkillCheck != passSkillChecks and failedSkillChecked == 1:
                        $ display = "Requires you to know the " + whatSkillIsIt + " skill."
                    elif passPerkCheck != passPerkChecks:
                        $ display = "Requires you to have the " + whatPerkIsIt + " perk."
                    elif passEnergyCheck == 0:
                        $ display = "Requires " + eAmount + " energy."
                    elif passVirilityCheck == 0:
                        $ display = "Requires " + vAmount + " virility."
    elif inverseRequirement == 1:
        if passStatcheck == 1 and passFetCheck == passFetChecks and passItemCheck == passItemChecks and passEquipmentCheck == passEquipmentChecks and passSkillCheck == passSkillChecks and passPerkCheck == passPerkChecks and passEnergyCheck == 1 and passVirilityCheck == 1 and passProgressCheck == passProgressChecks and passLocalProgressCheck == passLocalProgressChecks and passLocalChoiceCheck == passLocalChoiceChecks and passChoiceCheck == passChoiceChecks and passTimeCheck == passTimeChecks:
            if hideFailedMenuChoice == 0:
                if passLocalChoiceCheck == passLocalChoiceChecks and passProgressCheck == passProgressChecks and passLocalProgressCheck == passLocalProgressChecks and passChoiceCheck == passChoiceChecks:
                    if passVirilityCheck == 1 and hasVirilityCheck == 1:
                        $ display = "Must have less than " + vAmount + " virility."
                    if passEnergyCheck == 1 and hasEnergyCheck == 1:
                        $ display = "Must have less than " + eAmount + " energy."
                    if passPerkCheck == passPerkChecks and passPerkCheck == 1:
                        $ display = "Must not have the " + whatPerkIsIt + " perk."
                    if passSkillCheck == passSkillChecks and passSkillCheck == 1:
                        $ display = "Must not know the " + whatSkillIsIt + " skill."
                    if passItemCheck == passItemChecks and passItemCheck == 1:
                        $ display = "Must not have " + whatItemIsIt + " in your inventory."
                    if passEquipmentCheck == passEquipmentChecks and passEquipmentCheck == 1:
                        $ display = "Must not have " + whatEquipmentIsIt + " equipped."
                    if passStatcheck == 1 and hasStatCheck == 1:
                        $ display = "Must have less than " + str(needsStat) + " " + whatStatisIt + "."
        else:
            $ passcheck = 1
    return
