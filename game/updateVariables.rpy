label UpdateGameVersionVariables:
    python:
        try:
            attackerHeOrShe
        except NameError:
            attackerHeOrShe = ""
        else:
            attackerHeOrShe = attackerHeOrShe

        try:
            targetHeOrShe
        except NameError:
            targetHeOrShe = ""
        else:
            targetHeOrShe = targetHeOrShe

        try:
            attackerHisOrHer
        except NameError:
            attackerHisOrHer = ""
        else:
            attackerHisOrHer = attackerHisOrHer

        try:
            targetHisOrHer
        except NameError:
            targetHisOrHer = ""
        else:
            targetHisOrHer = targetHisOrHer

        try:
            targetYouOrMonsterName
        except NameError:
            targetYouOrMonsterName = ""
        else:
            targetYouOrMonsterName = targetYouOrMonsterName

        try:
            attackerYouOrMonsterName
        except NameError:
            attackerYouOrMonsterName = ""
        else:
            attackerYouOrMonsterName = attackerYouOrMonsterName

        try:
            targetHimOrHer
        except NameError:
            targetHimOrHer = ""
        else:
            targetHimOrHer = targetHimOrHer

        try:
            attackerHimOrHer
        except NameError:
            attackerHimOrHer = ""
        else:
            attackerHimOrHer = attackerHimOrHer

        try:
            PerkDatabase
        except NameError:
            PerkDatabase = []
        else:
            PerkDatabase = PerkDatabase

        try:
            DefeatedEncounterMonsters
        except NameError:
            DefeatedEncounterMonsters = []
        else:
            DefeatedEncounterMonsters = DefeatedEncounterMonsters

        try:
            displayOrder
        except NameError:
            displayOrder = []
        else:
            displayOrder = displayOrder


        try:
            SceneBookMarkRead
        except NameError:
            SceneBookMarkRead = 0
        else:
            SceneBookMarkRead = SceneBookMarkRead

        try:
            HoldingDataLoc
        except NameError:
            HoldingDataLoc = []
        else:
            HoldingDataLoc = HoldingDataLoc

        try:
            HoldingScene
        except NameError:
            HoldingScene = []
        else:
            HoldingScene = HoldingScene

        try:
            HoldingLine
        except NameError:
            HoldingLine = -1
        else:
            HoldingLine = HoldingLine

        try:
            CombatFunctionEnemytarget
        except NameError:
            CombatFunctionEnemytarget = 0
        else:
            CombatFunctionEnemytarget = CombatFunctionEnemytarget

        try:
            CombatFunctionEnemyInitial
        except NameError:
            CombatFunctionEnemyInitial = 0
        else:
            CombatFunctionEnemyInitial = CombatFunctionEnemyInitial

        try:
            actorNames
        except NameError:
            actorNames = ["", "", "", "", ""]
        else:
            actorNames = actorNames

        try:
            attackTitle
        except NameError:
            attackTitle = ""
        else:
            attackTitle = attackTitle

        try:
            runAndStayInEvent = 0
        except NameError:
            runAndStayInEvent = 0
        else:
            runAndStayInEvent = runAndStayInEvent

        try:
            pushAwayAttempt = 0
        except NameError:
            pushAwayAttempt = 0
        else:
            pushAwayAttempt = pushAwayAttempt

        try:
            desperateStruggle = 0
        except NameError:
            desperateStruggle = 0
        else:
            desperateStruggle = desperateStruggle

        try:
            savedLine = ""
        except NameError:
            savedLine = ""
        else:
            savedLine = savedLine

        try:
            PlayerChoiceToDisplay = ""
        except NameError:
            PlayerChoiceToDisplay = ""
        else:
            PlayerChoiceToDisplay = PlayerChoiceToDisplay

        try:
            MonsterChoiceToDisplay = ""
        except NameError:
            MonsterChoiceToDisplay = ""
        else:
            MonsterChoiceToDisplay = MonsterChoiceToDisplay

        try:
            FlexibleSpeaker = 0
        except NameError:
            FlexibleSpeaker = 0
        else:
            FlexibleSpeaker = FlexibleSpeaker

        try:
            preFunctionLine = 0
        except NameError:
            preFunctionLine = 0
        else:
            preFunctionLine = preFunctionLine

        try:
            NoGameOver = 0
        except NameError:
            NoGameOver = 0
        else:
            NoGameOver = NoGameOver

        try:
            savedLineInMenu = 0
        except NameError:
            savedLineInMenu = 0
        else:
            savedLineInMenu = savedLineInMenu

        try:
            HoldingForFuntion = 0
        except NameError:
            HoldingForFuntion = 0
        else:
            HoldingForFuntion = HoldingForFuntion

        try:
            SetSongAfterCombat = ""
        except NameError:
            SetSongAfterCombat = ""
        else:
            SetSongAfterCombat = SetSongAfterCombat

        try:
            vfx = ""
        except NameError:
            vfx = ""
        else:
            vfx = vfx

        try:
            vfx2 = ""
        except NameError:
            vfx2 = ""
        else:
            vfx2 = vfx2

        try:
            vfx3 = ""
        except NameError:
            vfx3 = ""
        else:
            vfx3 = vfx3

        try:
            VisualEffect = ""
        except NameError:
            VisualEffect = ""
        else:
            VisualEffect = VisualEffect

        try:
            VisualEffect2 = ""
        except NameError:
            VisualEffect2 = ""
        else:
            VisualEffect2 = VisualEffect2

        try:
            VisualEffect3 = ""
        except NameError:
            VisualEffect3 = ""
        else:
            VisualEffect3 = VisualEffect3

        try:
            MotionEffect = ""
        except NameError:
            MotionEffect = ""
        else:
            MotionEffect = MotionEffect

        try:
            hpDeficit = 0
        except NameError:
            hpDeficit = 0
        else:
            hpDeficit = hpDeficit

        try:
            epDeficit = 0
        except NameError:
            epDeficit = 0
        else:
            epDeficit = epDeficit

        try:
            hidingCombatEncounter = 0
        except NameError:
            hidingCombatEncounter = 0
        else:
            hidingCombatEncounter = hidingCombatEncounter


        try:
            storedBGM = []
        except NameError:
            storedBGM = []
        else:
            storedBGM = storedBGM

        try:
            LossExp = 0
        except NameError:
            LossExp = 0
        else:
            LossExp = LossExp

        try:
            increaseStatCheck = 0
        except NameError:
            increaseStatCheck = 0
        else:
            increaseStatCheck = increaseStatCheck

        try:
            DayNumber = 1
        except NameError:
            DayNumber = 1
        else:
            DayNumber = DayNumber

        try:
            TimeOfDay = Morning
        except NameError:
            TimeOfDay = Morning
        else:
            TimeOfDay = TimeOfDay

        try:
            EnteringLocationCheck = 0
        except NameError:
            EnteringLocationCheck = 0
        else:
            EnteringLocationCheck = EnteringLocationCheck

        try:
            TimeAdvancedCheck = 0
        except NameError:
            TimeAdvancedCheck = 0
        else:
            TimeAdvancedCheck = TimeAdvancedCheck

        try:
            HealingSickness = 0
        except NameError:
            HealingSickness = 0
        else:
            HealingSickness = HealingSickness

        try:
            HoldingDataLocForTime
        except NameError:
            HoldingDataLocForTime = []
        else:
            HoldingDataLocForTime = HoldingDataLocForTime

        try:
            HoldingSceneForTime
        except NameError:
            HoldingSceneForTime = []
        else:
            HoldingSceneForTime = HoldingSceneForTime

        try:
            HoldingLineForTime
        except NameError:
            HoldingLineForTime = -1
        else:
            HoldingLineForTime = HoldingLineForTime

        try:
            HoldingDataLocForTimeArray
        except NameError:
            HoldingDataLocForTimeArray = []
        else:
            HoldingDataLocForTimeArray = HoldingDataLocForTimeArray

        try:
            HoldingSceneForTimeArray
        except NameError:
            HoldingSceneForTimeArray = []
        else:
            HoldingSceneForTimeArray = HoldingSceneForTimeArray

        try:
            HoldingLineForTimeArray
        except NameError:
            HoldingLineForTimeArray = []
        else:
            HoldingLineForTimeArray = HoldingLineForTimeArray

        try:
            holdActorsArray
        except NameError:
            holdActorsArray = []
        else:
            holdActorsArray = holdActorsArray

        try:
            DialogueTypeHolderArray
        except NameError:
            DialogueTypeHolderArray = []
        else:
            DialogueTypeHolderArray = DialogueTypeHolderArray

        try:
            lastTimeReturnArray
        except NameError:
            lastTimeReturnArray = []
        else:
            lastTimeReturnArray = lastTimeReturnArray

        try:
            TimeAdvancedCheckArray
        except NameError:
            TimeAdvancedCheckArray = [0]
        else:
            TimeAdvancedCheckArray = TimeAdvancedCheckArray

        try:
            callNextJump
        except NameError:
            callNextJump = 0
        else:
            callNextJump = callNextJump

        try:
            LoopedList
        except NameError:
            LoopedList = []
        else:
            LoopedList = LoopedList

        try:
            Rut
        except NameError:
            Rut = False
        else:
            Rut = Rut

        try:
            heldVirility
        except NameError:
            heldVirility = 0
        else:
            heldVirility = heldVirility

        try:
            DialogueIsFrom
        except NameError:
            DialogueIsFrom = "Event"
        else:
            DialogueIsFrom = DialogueIsFrom

        try:
            displayTown1
        except NameError:
            displayTown1 = ""
            displayTown2 = ""
            displayTown3 = ""
            displayTown4 = ""
            displayTown5 = ""
        else:
            displayTown1 = displayTown1


        try:
            exist1 = 0
            exist2 = 0
            exist3 = 0
            exist4 = 0
            exist5 = 0
            exist6 = 0
        except NameError:
            exist1 = 0
            exist2 = 0
            exist3 = 0
            exist4 = 0
            exist5 = 0
            exist6 = 0
        else:
            exist1 = exist1
            exist2 = exist2
            exist3 = exist3
            exist4 = exist4
            exist5 = exist5
            exist6 = exist6
