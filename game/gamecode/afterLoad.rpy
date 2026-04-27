label after_load:
    
    if _version.startswith("Renpy-8") or _version.startswith("Alpha-v20") or _version.startswith("Alpha-v19") or _version.startswith("Alpha-v25") or _version.startswith("Alpha-v24") or _version.startswith("Alpha-v23") or _version.startswith("Alpha-v22") or _version.startswith("Alpha-v21"):
        $ save_name = copy.copy(player.name)
        $ _version = "Alpha-v26"
        #$ print("Updated") #Do prints to verify behavior.
        #You can console insert '_version' in the in-game console to see if it applied.
        #Make sure to first interact with the game before saving again to see if it remembered,
        #Ren'Py does not overwite a save that only had changes made via autoload,
        #the actual game itself needs its state changed first.

    # if _version in ["Alpha-v26", "Alpha-v26a", "Alpha-v26b", "Alpha-v26.1", "Alpha-v26.1b"]:
    #Do this to update saves that were on the last set of versions that were on an afflicted save.
    #Then, once done, update it to the current game version to be shipped.
    #     $ _version = "Alpha-v26.2"
    #Now during the after_load it is considered a v26.2 save.
    #Let's say the actual current version of the game is v27.
    #You then run the next conditional that will catch it:
    # if _version in ["Alpha-v26.2", "Alpha-v26.2a", "Alpha-v26.3", "Alpha-v26.3a"]:
    #Now any save being loaded marked the above, including those that just did the previous if will
    #apply these changes to the save next.
    #     _version = "Alpha-v27"
    #Now any save between 26 in the first if condition to v26.3a in the second are up to date as v27.
    #You don't have to worry about it applying to a v27 save again as v27 isn't checked for in any conditional.
    #Thus, it is impossible to apply to an already up to date save by mistake for as long as your if condition
    #never contains the current game version you are intending to ship.

    if (_version in ["Alpha-v26", "Alpha-v26a", "Alpha-v26b",  "Alpha-v26.a", "Alpha-v26.b", "Alpha-v26.3"]) or _version.startswith("Alpha-v26.1") or _version.startswith("Alpha-v26.2"):
        $ recoilHit = 0
        "The wind blows in a sudden gust and a small silver ticket flies into your face. It seems like you happened across a Guild-Approved respec ticket!"
        $ player.inventory.give("Respec Ticket", 1)
        $ _version = "Alpha-v26.3a"

    if (_version in ["Alpha-v26.3a", "Alpha-v26.4", "Alpha-v26.4a", "Alpha-v26.4b"]):
        hide screen ON_MapMenu onlayer master
        $ _version = "Alpha-v26.5"

    if (_version in ["Alpha-v26.5b", "Alpha-v26.5a", "Alpha-v26.5"]) or _version.startswith("Alpha-v26.6") or _version.startswith("Alpha-v26.7") or _version.startswith("Alpha-v26.8") or _version.startswith("Alpha-v26.9"):
        $ i = 0
        python:
            for each in player.perks: 
                if each.name == "Mara's Boytoy":
                    player.giveOrTakePerk(each.name, -1)
                    player.giveOrTakePerk("Mara's Boy Toy", 1)
                player.perks[i].Update()
                i +=1
        $ _version = "Alpha-v27"

    if  _version in ["27b-Alpha", "27a-Alpha", "Alpha-v27b", "Alpha-v27a", "Alpha-v27"] or _version.startswith("Alpha-v27.1") or _version.startswith("Alpha-v27.2"):        
        $ transfering = copy.deepcopy(player.pastLevelUps)
        $ player.pastLevelUps = []
        $ ExpTotal = 0
        python:
            for each in transfering:
                if isinstance(each, str):
                    player.pastLevelUps.append(each)
                    continue

                for extra in each:
                    player.pastLevelUps.append(extra)
        $ _version = "Alpha-v27.3"

    if  _version in ["Alpha-v27.3"]: 
        python: #the anti silliness update wall to make sure the change gets through in the situation where it didnt update before but their save got marked as v27.3
            try:
                ExpTotal
            except NameError:
                transfering = copy.deepcopy(player.pastLevelUps)
                player.pastLevelUps = []
                ExpTotal = 0 
                for each in transfering:
                    if isinstance(each, str):
                        player.pastLevelUps.append(each)
                        continue

                    for extra in each:
                        player.pastLevelUps.append(extra)
            else:
                ExpTotal = ExpTotal
        $ _version = "Alpha-v27.3a"



    if onGridMap == 0:
        hide screen gridMoveKeys

    if favorPool == -1:
        $ favorPool = CalcGoddessFavor(player)
    $ previousHP = player.stats.hp
    $ previousEP = player.stats.ep
    $ previousSP = player.stats.sp
    $ needToUpdate = 0
    hide screen FishingHitEffect
    show screen input_detection
    python:
        UpdatedGameCheck = len(SkillsDatabase) + len(ItemDatabase) + len(MonsterDatabase) + len(PerkDatabase) + len(LocationDatabase) + len(EventDatabase) + len(AdventureDatabase)

        try:
            CurrentIteration
        except NameError:
            needToUpdate = 1
            CurrentIteration = copy.deepcopy(UpdatedGameCheck)

    if CurrentIteration != UpdatedGameCheck:
        $ needToUpdate = 1
        $ CurrentIteration = copy.deepcopy(UpdatedGameCheck)

    if needToUpdate == 1 or CurrentVersion != config.version:

        if historyUpdate == 0:
            # For the markup change in v25.6
            $ _history_list = []
            define SexAdjective = Alias(lambda: getPenetrationAjectives(player))
            #define SexWord = Alias(lambda: getPenetration(player))
            $ historyUpdate = 1

        $ CurrentVersion = config.version
        call AutoReloadDatabase from _call_AutoReloadDatabase_1

    jump exitCombatFunction



    # if persistent.genModData == True:
    #     call setDatabase
    #     $ set_lists()
    #     $ loadingDatabaseType = 0
    #     call loadDatabase
    #     $ loadingDatabaseType = 1
    #     $ persistent.genModData = False
    #     if persistent.modCount == None:
    #         $ persistent.modCount = 0
    #     if persistent.modCount != 0:
    #         $ renpy.notify("[persistent.modCount] Mods loaded.")
