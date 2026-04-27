rpy python 3

label setDatabase:
    $ jsonList = []

    $ AdventureDatabase = []
    $ EventDatabase = []
    $ FetishList = []
    $ ItemDatabase = []
    $ LocationDatabase = []
    $ MonsterDatabase = []
    $ PerkDatabase = []
    $ SkillsDatabase = []

    # Bandaid lookup dictionaries for performance.
    $ EventDatabaseDict = {}
    $ MonsterDatabaseDict = {}
    $ SkillsDatabaseDict = {}
    $ ItemDatabaseDict = {}
    $ PerkDatabaseDict = {}
    $ LocationDatabaseDict = {}
    $ AdventureDatabaseDict = {}
    $ FetishDatabaseDict = {}

    $ LocationList = []

    $ LevelingPerkDatabase = []
    $ PerkDatabaseLVLDisplay = []
    $ AdditionalLevelPerks = []

    $ EndOfDayList = []
    $ TimePassedList = []
    $ StepTakenList = []
    $ EndOfTurnList = []
    $ EndOfCombatList = []
    $ StartOfTurnList = []
    $ StartOfCombatList = []
    $ OnPlayerClimaxList = []
    $ DreamList = []

    $ WaiterBrothel = []
    $ BarBrothel = []
    $ GloryHoleBrothel = []
    $ DayBrothel = []
