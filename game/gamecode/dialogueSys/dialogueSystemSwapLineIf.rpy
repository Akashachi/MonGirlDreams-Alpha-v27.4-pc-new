init python:
    SwapLineIfRegistry = {
        "Stat": ["SwapLineIf_Stat"],
        "Level": ["SwapLineIf_Level"],
        "Arousal": ["SwapLineIf_Arousal"],
        "ArousalByPercent": ["SwapLineIf_ArousalByPercent"],
        "MaxArousal": ["SwapLineIf_MaxArousal"],
        "Energy": ["SwapLineIf_Energy"],
        "EnergyByPercent": ["SwapLineIf_EnergyByPercent"],
        "MaxEnergy": ["SwapLineIf_MaxEnergy"],
        "Virility": ["SwapLineIf_Virility"],
        "HasFetish": ["SwapLineIf_HasFetish"],
        "HasFetishLevelEqualOrGreater": ["SwapLineIf_HasFetishLevelEqualOrGreater"],
        "EncounterSize": ["SwapLineIf_EncounterSize"],
        "Progress": ["SwapLineIf_Progress"],
        "Choice": ["SwapLineIf_Choice"],
        "OtherEventsProgress": ["SwapLineIf_OtherEventsProgress"],
        "OtherEventsChoice": ["SwapLineIf_OtherEventsChoice"],
        "IfTimeIs": ["SwapLineIf_IfTimeIs"],
        "Eros": ["SwapLineIf_Eros"],
        "Item": ["SwapLineIf_Item"],
        "Perk": ["SwapLineIf_Perk"],
        "Random": ["SwapLineIf_Random"]
    }

label SwapLineIf_Stat:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            $ statToCheck = player.stats.getStat(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            if statToCheck >= int(displayingScene.theScene[lineOfScene]) and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_Level:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            if player.stats.lvl >= int(displayingScene.theScene[lineOfScene]) and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_Arousal:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            if player.stats.hp >= int(displayingScene.theScene[lineOfScene]) and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_ArousalByPercent:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            if player.stats.hp >= player.stats.max_true_hp*float(displayingScene.theScene[lineOfScene])*0.01 and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_MaxArousal:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            if player.stats.max_true_hp >= int(displayingScene.theScene[lineOfScene]) and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_Energy:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            if player.stats.ep >= int(displayingScene.theScene[lineOfScene]) and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_EnergyByPercent:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            if player.stats.ep >= player.stats.max_true_ep*float(displayingScene.theScene[lineOfScene])*0.01 and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_MaxEnergy:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            if player.stats.max_true_ep >= int(displayingScene.theScene[lineOfScene]) and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_Virility:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            if getVirility(player) >= int(displayingScene.theScene[lineOfScene]) and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_HasFetish:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            if player.getFetish(displayingScene.theScene[lineOfScene]) >= 25 and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_HasFetishLevelEqualOrGreater:
    $ lineOfScene += 1
    $ fetchFetish = displayingScene.theScene[lineOfScene]
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop" and linefound == 0:
            $ fetishLvl = int(displayingScene.theScene[lineOfScene])
            if player.getFetish(fetchFetish) >= fetishLvl:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_EncounterSize:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop" and linefound == 0:
            if len(monsterEncounter) >= int(displayingScene.theScene[lineOfScene]):
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_Progress:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[DataLocation].eventProgress and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_Choice:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            while choiceToCheck-1 >= len(ProgressEvent[DataLocation].choices):
                $ ProgressEvent[DataLocation].choices.append("")
            if displayingScene.theScene[lineOfScene] == ProgressEvent[DataLocation].choices[choiceToCheck-1] and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_OtherEventsProgress:
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            if int(displayingScene.theScene[lineOfScene]) <= ProgressEvent[CheckEvent].eventProgress and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_OtherEventsChoice:
    $ lineOfScene += 1
    $ CheckEvent = getFromName(displayingScene.theScene[lineOfScene], ProgressEvent)
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            $ choiceToCheck = int(displayingScene.theScene[lineOfScene])
            $ lineOfScene += 1
            $ CheckEvent = getFromName(ProgressEvent[CheckEvent].name, ProgressEvent)
            while choiceToCheck-1 >= len(ProgressEvent[CheckEvent].choices):
                $ ProgressEvent[CheckEvent].choices.append("")
            if displayingScene.theScene[lineOfScene] == ProgressEvent[CheckEvent].choices[choiceToCheck-1] and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_IfTimeIs:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            if 1 == IfTime(displayingScene.theScene[lineOfScene]) and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_Eros:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            if player.inventory.money >= int(displayingScene.theScene[lineOfScene]) and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_Item:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            $ hasThing = 0
            python:
                for item in player.inventory.items:
                    if item.name == displayingScene.theScene[lineOfScene]:
                        hasThing = 1
            if hasThing == 1 and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
    return

label SwapLineIf_Perk:
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ lineOfScene += 1
        if displayingScene.theScene[lineOfScene] != "EndLoop":
            $ hasThing = 0
            python:
                perk_name = displayingScene.theScene[lineOfScene]
                hasThing = int(any(perk.name == perk_name for perk in player.perks))
            if hasThing == 1 and linefound == 0:
                $ linefound = 1
                $ lineOfScene += 1
                $ display = displayingScene.theScene[lineOfScene]
            else:
                $ lineOfScene += 1
            $ hasThing = 0
    return

label SwapLineIf_Random:
    $ lineOfScene += 1
    $ linefound = 1
    $ randomSelection = []
    while displayingScene.theScene[lineOfScene] != "EndLoop":
        $ randomSelection.append(displayingScene.theScene[lineOfScene])
        $ lineOfScene += 1
    $ renpy.random.shuffle(randomSelection)
    $ display = randomSelection[0]
    return
