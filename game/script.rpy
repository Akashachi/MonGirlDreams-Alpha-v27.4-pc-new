init -1 python:
    import math
    import copy
    import random
    import itertools

init python:

    lastReturn = []

    dontJumpOutOfGridEvents = 0
    postCombatEventGridFailsafe = 0
    NoSelling = 0
    finalDamage = 0
    finalSleepy = 0
    recoverAmount = 0

    slimeSnakeHighScore = 0
    minigameQuickMenuHide = 0

    favorPool = -1
    favorStrain = 0

    textboxCGXAdjust = 0

    historyDisplay = ""

    perkLenCheck = 0

    lastMonDamage = 0
    lastMonDamageCrit = ""
    lastMonDamageWeak = ""
    lastMonStatusRes = ""
    lastMonRecoil = 0
    recoilHit = 0

    lastPlayerDamage = 0
    lastPlayerDamageCrit = ""
    lastPlayerDamageWeak = ""
    lastPlayerStatusRes = ""
    lastPlayerRecoil = 0

    #config.rollback_length = 10
    config.longpress_vibrate = 0.1
    config.quicksave_slots = 12
    config.pause_after_rollback = True

    config.autosave_frequency = 0
    mgdAutosaveFrequency = 100
    mgdAutosaveCount = copy.deepcopy(mgdAutosaveFrequency)
    config.autosave_on_choice = False
    config.autosave_on_quit = True
    config.autosave_slots = 10
    #config.autosave_callback = Notify("Autosaved.")

    config.cache_surfaces = True
    config.image_cache_size_mb = 500

    cachecheck = 0

    RoledCGOn = 0
    CgRoleKeeper = []
    monsterEncounterCG = []
    combatMonUIoveride = []

    historyUpdate = 0

    lineOfScene = 0

    showTimeofDay = 1

    restraintMaxHP = 0


    # NWB change 4: attrs_arrDR and stats_arrDR turned into dictionaries with only the required info
    attrs_arrDR = {
        "Arousal": (hpFloor, hpCap),
        "Energy": (epFloor, epCap),
        "Spirit": (spFloor, spCap)
    }
    stats_arrDR = {
        "Power": (powFloor, powCap),
        "Technique": (spdFloor, spdCap),
        "Intelligence": (intFloor, intCap),
        "Allure": (allFloor, allCap),
        "Willpower": (wilFloor, wilCap),
        "Luck": (lukFloor, lukCap)
    }
    # NWB change 4 continued: sens_arrDR also gets turned into a dictionary, makes searching a lot more efficient :EllyGlasses:
    sens_arrDR = {
        "Sex": [-5, sexResFloor, sexResCap],
        "Ass": [-10, assResFloor, assResCap],
        "Breasts": [-25, nipResFloor, nipResCap],
        "Mouth": [-10, chuResFloor, chuResCap],
        "Seduction": [-10, seducResFloor, seducResCap],
        "Magic": [-10, magResFloor, magResCap],
        "Pain": [-10, painResFloor, painResCap]
    }


    #config.predict_screen_statements = False
    #config.predict_screens = False

    if persistent.showCharacterImages is None:
        persistent.showCharacterImages = True

    if persistent.showCardBubbles is None:
        persistent.showCardBubbles = True

    if persistent.showVFX is None:
        persistent.showVFX = True
    #showCharacterImages = False

    if persistent.setBaseVolume is None:
        _preferences.set_volume('music', 0.5)
        persistent.setBaseVolume = True
        renpy.restart_interaction()

    if renpy.android and persistent.validatorAtStartup:
        persistent.validatorAtStartup = False

    renpy.music.register_channel("soundChannel2","sfx",loop=False,tight=False)
    renpy.music.register_channel("loopingSound","sfx",loop=True,tight=True)
    renpy.music.register_channel("loopingSound2","sfx",loop=True,tight=True)

    kissQuickSoundBank = ["sfx/Erotic/KissQuick/Kiss sound 01.wav", "sfx/Erotic/KissQuick/Kiss sound 04.wav", "sfx/Erotic/KissQuick/Kiss sound 11.wav", "sfx/Erotic/KissQuick/Kiss sound 14.wav", "sfx/Erotic/KissQuick/kiss1.wav"]
    kissLongSoundBank = ["sfx/Erotic/KissLong/Kiss sound 07.wav", "sfx/Erotic/KissLong/Kiss sound 09.wav", "sfx/Erotic/KissLong/Kiss sound 10.wav", "sfx/Erotic/KissLong/Kiss sound 16.wav"]
    kissMakeOutSoundBank = ["sfx/Erotic/KissMakeout/Kiss sound 03.wav", "sfx/Erotic/KissMakeout/Kiss sound 05.wav", "sfx/Erotic/KissMakeout/Kiss sound 18.wav", "sfx/Erotic/KissMakeout/Kiss sound 19.wav", "sfx/Erotic/KissMakeout/Kiss sound 20.wav", "sfx/Erotic/KissMakeout/Kiss sound 21.wav",  "sfx/Erotic/KissMakeout/Kiss sound 23.wav", "sfx/Erotic/KissMakeout/Kiss sound 24.wav", "sfx/Erotic/KissMakeout/kiss2.mp3"]

    blowjobLickingSoundBank = ["sfx/Erotic/Sucking/Fast tongue movement.mp3", "sfx/Erotic/Sucking/licking010.wav", "sfx/Erotic/Sucking/licking015.wav", "sfx/Erotic/Sucking/licking031.wav", "sfx/Erotic/Sucking/licking040.wav", "sfx/Erotic/Sucking/lickingAndSucking.mp3"]
    blowjobSuckingSoundBank = ["sfx/Erotic/Sucking/sucking004.wav", "sfx/Erotic/Sucking/sucking012.wav", "sfx/Erotic/Sucking/sucking014.wav", "sfx/Erotic/Sucking/sucking028.wav", "sfx/Erotic/Sucking/sucking035.wav", "sfx/Erotic/Sucking/sucking037.wav",  "sfx/Erotic/Sucking/sucking041.wav", "sfx/Erotic/Sucking/sucking043.wav","sfx/Erotic/Sucking/sucking047.wav"]
    blowjobDeepSuckingSoundBank = ["sfx/Erotic/Sucking/slurp005.wav", "sfx/Erotic/Sucking/slurp006.wav", "sfx/Erotic/Sucking/suckingLong.mp3"]
    blowjobVigorousSoundBank = ["sfx/Erotic/Sucking/vigorous.mp3", "sfx/Erotic/Sucking/vigorous044.wav"]

    ejaculationSoundBank =  ["sfx/Erotic/Ejaculation/Ejaculation sound go out (short) 1.wav", "sfx/Erotic/Ejaculation/Ejaculation sound go out (short) 5.wav", "sfx/Erotic/Ejaculation/Ejaculation sound go out (short) 10.wav", "sfx/Erotic/Ejaculation/Ejaculation sound go out (long) 1.wav"]
    messyEjaculationSoundBank = ["sfx/Erotic/Ejaculation/Ejaculation sound go out (long) 3.wav", "sfx/Erotic/Ejaculation/Ejaculation sound go out (long) 4.wav","sfx/Erotic/Ejaculation/Ejaculation sound go out (long) 8.wav"]

    checkCapitalProgress = 0

    MenuLineSceneCheckMark = -1

    viewportID2 = ""

    recoil = 0
    theTimeType = ""
    perkDurationTip = 0
    LostGameOver = 0
    Crit = 0
    itemEvent = 0

    nightmare = 0

    inCalledSceneJump = 0

    specifyCurrentChoice = 0
    specifyDataLocation = 0

    MotionEffectLoop = 0

    PurchasesToProgress = 0

    spaceNext = 0

    inTownMenu = 0

    combatItems = 0
    currentEnemy = 0
    e = 0

    flatCore = 0
    percentCore = 0
    powerDisplay =0
    techDisplay = 0
    intDisplay = 0
    allureDisplay = 0
    willDisplay = 0
    luckDisplay = 0
    powerBoost = 0
    powerPerBoost = 0
    intBoost = 0
    intPerBoost = 0
    techBoost = 0
    techPerBoost = 0
    allureBoost = 0
    allurePerBoost = 0
    willBoost = 0
    willPerBoost = 0
    luckBoost = 0
    luckPerBoost = 0
    statDamMod = 0

    override = ""

    EventConsister = ""
    EventConsisterTarget = 0

    TogglePerkFilter = False
    PerkOrder = "None"
    PerkFilter = "None"

    # TODO May be useful to reset these to default values between events/scenes/adventures/??? to ease management of them? Breaking behavior if so.
    textColor = "#F6BADC"
    textColor2 = "#F6BADC"
    textColor3 = "#F6BADC"
    textColor4 = "#F6BADC"
    textColor5 = "#F6BADC"
    textColor6 = "#F6BADC"
    textColor7 = "#F6BADC"

    rehauled = 0
    progressionBoost = 0

    npcCount = 0
    senCount = 0
    fetCount = 0

    notFunction = 0
    timeNotify = 0

    damageToPlayer = 0
    damageToEnemy = 0
    progressDisplay = 0
    playerOrgasmLine = ""
    monsterOrgasmLine = ""
    PostOrgasmLine = ""

    lineBank = ["Do your best!", "Can't we just hold hands?", "Or maybe, it's a nightmare?", "Free adventuring school!", "Why would you resist love?", "The goddess will protect you.", "Hot succubi are in your area.♥", "Don't stay up {i}too{/i} late.♥", "Ten out of ten mimics say you should open every treasure chest.", "Relax and enjoy.♥", "Awaken a new kink, today!", "Not guaranteed to give you lewd dreams.", "Cozy, sexy, and more!", "No imps were harmed in the making of this production.", "Surrendering is a fun option.♥", "A manticore is rapidly approaching your location.", "There is no secret slime society.", "Harpy Delivery is not responsible for any damage to your mail.", "Don't forget to stop and smell the sweet alraunes.♥", "Being a hero never felt so good.♥"]

    sexBank = ["pussy", "pussy", "slit", "honeypot"]
    assBank = ["ass", "ass", "rear", "behind", "derriere"]

    sexAdjectiveBank = ["", "wet ", "tight ", "wet ", "tight ", "receptive ", "warm "]
    assAdjectiveBank = ["", "tight ", "tight ", "curved ", "rounded ", "receptive "]


    Morning = "{color=#ffe9b5}Morning{/color}"
    Noon = "{color=#ffe9b5}Noon{/color}"
    Afternoon = "{color=#ffe9b5}Afternoon{/color}"

    MorningNight = "{color=#cfb8df}Morning{/color}"
    NoonNight = "{color=#cfb8df}Noon{/color}"
    AfternoonNight = "{color=#cfb8df}Afternoon{/color}"

    Dusk = "{color=#cfb8df}Dusk{/color}"
    Evening = "{color=#cfb8df}Evening{/color}"
    Midnight = "{color=#cfb8df}Midnight{/color}"

    DuskDay = "{color=#ffe9b5}Dusk{/color}"
    EveningDay = "{color=#ffe9b5}Evening{/color}"
    MidnightDay = "{color=#ffe9b5}Midnight{/color}"

    UseFancyScrollBar = False

    #config.use_cpickle = False
    config.history_length = 150
    if renpy.variant("touch") or renpy.variant("small"):
        config.history_length = 50

    npcProgHolder = []
    eventProgHolder = []
    advenProgHolder = []
    purchasing = 0
    amountToBuy = 1

    LoopedList = []
    LoopedListHolder = []
    teiHold = -1
    callLoopTei= []
    holdChoiceForLoop = []

    removedSkillPosition = []
    removedSkill = []

    manualSort = ""
    swappingSkill = -1
    swappingItem = -1

    overrideCombatMusic = 0
    musicLastPlayed = [""]

    buff = ""
    postNote = ""
    vfx = "white.png"
    vfx2 = "white.png"
    vfx3 = "white.png"
    spiralVFX = "white.png"

    spiritLost = 0

    expGiven = 1

    shifting = 1


    playBehind = 0
    sprialSpeed = 5
    spiralOpacity = 0.8

    pendulumSpeed = 5
    pendulumSway = 45
    pendulumVFX = "white.png"

    bounceAmount = 10
    bounceSpeed = 0.6

    #currently frame animation stuff
    animationList = [ ]
    animationChoice = ""
    currentAnimationImg = 1
    animationSpeed = 0.5
    animationTime = 0

    #currently frame animation stuff
    animationList2 = [ ]
    animationChoice2 = ""
    currentAnimationImg2 = 1
    animationSpeed2 = 0.5
    animationTime2 = 0

    #currently frame animation stuff
    animationList3 = [ ]
    animationChoice3 = ""
    currentAnimationImg3 = 1
    animationSpeed3 = 0.5
    animationTime3 = 0

    pulsingList = []
    pulsingChoice = ""
    currentPulsingImg = 0
    pulseZoom = 1.0
    pulsingSpeed = 1.0
    pulsingOpacity = 1.0
    pulsingTime = 0

    pulsingList2 = []
    pulsingChoice2 = ""
    currentPulsingImg2 = 0
    pulseZoom2 = 1.0
    pulsingSpeed2 = 1.0
    pulsingOpacity2 = 1.0
    pulsingTime2 = 0

    pulsingListRand = []
    pulsingChoiceRand = ""
    currentPulsingImgRand = 0
    pulseZoomRand = 1.0
    pulsingSpeedRand = 1.0
    pulsingOpacityRand = 1.0
    pulsingTimeRand = 0

    CurrentIteration = 0


    BarrageOpacity = 0
    barrageList = []
    barrageChoice = ""
    currentBarrageImg = 0
    BarrageTime = 0
    BarrageSpeed = 0

    barrageFadeList = []
    barrageFadeChoice = ""
    currentBarrageFadeImg = 0
    BarrageFadeTime = 0
    BarrageFadeSpeed = 0
    barragefadeSkip = 0

    BarrageOpacity2 = 0
    barrageList2 = []
    barrageChoice2 = ""
    currentBarrageImg2 = 0
    BarrageTime2 = 0
    BarrageSpeed2 = 0

    barrageFadeList2 = []
    barrageFadeChoice2 = ""
    currentBarrageFadeImg2 = 0
    BarrageFadeTime2 = 0
    BarrageFadeSpeed2 = 0
    barragefadeSkip2 = 0

    lastCombatSongPosition = ""
    lastCombatSong = ""

    selectingCircleBar = 0

    needToUpdate = 0
    critChance = 0
    critDamage = 0
    fontsize = 35
    HPfontsize = 25
    theXpadding = 12
    theYpadding = 10
    InStanceEvade = 0
    OutOfStanceEvade = 0
    AccuracyBonus = 0
    InStanceAccuracyBonus = 0

    effectiveText = ""
    statusEffectiveText = ""

    LastLine = ""
    LastSpeaker = ""

    whatStatisIt = ""
    whatItemIsIt = ""
    whatSkillIsIt = ""
    whatPerkIsIt = ""
    refinedSkillList = []

    theTarget = ""
    theAttacker = ""

    triggerItemUse = 0

    kissBarOnce = 0

    randomMenuLine = renpy.random.choice(lineBank)

    config.rollback_enabled = False
    config.save_dump = True


    showMoreFetish = 0
    getFetish = 0
    setThisFetish = 0
    tryRemoveThisStance = 0

    creating = 1
    hasResPoints = 0
    loadingDatabaseType = 0
    respeccing = 0



    perkChosen = ""
    perkBuyUse = False

    InIntro = 0

init:
    define config.history_current_dialogue = False
    $ config.save_dump = False
    # $ config.console = True
    # $ config.developer = True
    default _game_menu_screen = None


    transform invisible:
        alpha 0.0

    default persistent.modsArePresent = False
    default persistent.modCount = 0
    default persistent.validatorAtStartup = False
    default persistent.validatorAtReload = False
    default persistent.genModData = False
    default persistent.animatedUI = True

    call setDatabase from _call_setDatabase_1

    $ monSkillChoice = []

    define config.layers = ['master', 'transient', 'visualEffects', 'screens',  'overlay' ]
    #$ config.say_layer = "sayScreen"

    define config.gl2 = True

    call UpdateGameVersionVariables from _call_UpdateGameVersionVariables
    call InitInventory from _call_InitInventory
    call specialEffects from _call_specialEffects
    call playerClass from _call_playerClass
    call monsterClass from _call_monsterClass
    call AdventuringDeckClass from _call_AdventuringDeckClass
    call combatFunctions from _call_combatFunctions

    $ set_lists()
    call loadDatabase from _call_loadDatabase_2


    $ player_display = "Body"
    $ PlayerPicker = True

    $ body_tint = ColorPicker(340, 340, "#FFFFFF")
    $ hair_color_l = ColorPicker(340, 340, "#f5d6c9")
    $ hair_color_d = ColorPicker(340, 340, "#150600")

    $ player_satur = 1.0
    $ player_opac = 1.0
    $ player_hue_bar = 1.0

    transform CharacterPicker:
        matrixcolor TintMatrix(body_tint.color)
    transform CharacterOpacity:
        matrixcolor OpacityMatrix(player_opac)
    transform CharacterSaturation:
        matrixcolor SaturationMatrix(player_satur, (0.2126, 0.7152, 0.0722))
    transform CharacterHairPicker:
        matrixcolor ColorizeMatrix(hair_color_d.color, hair_color_l.color)
    transform CharacterHue:
        matrixcolor TintMatrix(body_tint.color)

    $ silhouette_color = ColorPicker(340, 340, "#993577")
    $ player_sil_satur = 1.0
    $ player_sil_opac = 0.9

    transform CharacterSilPicker:
        matrixcolor ColorizeMatrix(silhouette_color.color, silhouette_color.color)
    transform CharacterSilOpacity:
        matrixcolor OpacityMatrix(player_sil_opac)
    transform CharacterSilSaturation:
        matrixcolor SaturationMatrix(player_sil_satur, (0.2126, 0.7152, 0.0722))


    $ Quake = Shake((0, 0, 0, 0), 6000.0, dist=5)
    $ Crash = Shake((0, 0, 0, 0), 0.5, dist=20)
    $ CrashSmol = Shake((0, 0, 0, 0), 0.25, dist=10)
    $ Explosion = Shake((0, 0, 0, 0), 0.75, dist=35)
    $ LongExplosion = Shake((0, 0, 0, 0), 3.0, dist=35)

    $ motionSpeed = 0.3
    $ motionDistance = 10

    $ GlobalMotion = ""

    python:
        style.smallerTextButton = Style(style.button_text)
        style.smallerTextButton.size = 20
        style.smallerTextButton.color = "#E470B2"
        style.smallerTextButton.hover_color = "#F6BADC"


    image bg = "#3f3f3f"
    image bg heaven = "heaven.png"
    image bg combat = "combat.png"
    image bg forest = "forest.png"
    image bg town = "standIn.png"

    image splashScreen = "SplashPage.png"

    image chest = "Monsters/Mimic/mimic_closed.png"
    image bag = "Monsters/Stella/BagPlain.png"

    transform CharacterZoom:
        zoom 0.75

    transform combatOpacity:
        alpha 0.80

    transform statusOpacity:
        alpha 0.7

    transform combatStanceOpacity:
        alpha 0.70

    transform statusIconZoom:
        zoom 0.25

    transform LossSceneZoom:
        zoom 1.0


    $ God = Character(_('???'),
                            what_prefix='"',
                            what_suffix='"')

    $ Goddess = Character(_('Goddess Venereae'),
                            what_prefix='"',
                            what_suffix='"')


    $ Lily = Character(_('Lillian'),
                            what_prefix='"',
                            what_suffix='"')

    $ shopKeeper = Character(_('Amber'),
                            what_prefix='"',
                            what_suffix='"')

    $ innKeeper = Character(_('Vivian Von Kaar'),
                            what_prefix='"',
                            what_suffix='"')

    $ guildDesk = Character(_('Elena'), #Farshaw
                            what_prefix='"',
                            what_suffix='"')

    $ Librarian = Character(_('Elly'), #Farshaw
                            what_prefix='"',
                            what_suffix='"')



    $ Perpetua = Character(_('Perpetua'), #Slime Girl
                            what_prefix='"',
                            what_suffix='"')

    $ srsly = Character(_('Allura'),
                            what_prefix='"',
                            what_suffix='"')

    $ Aife = Character(_('Aife'), #elf
                            what_prefix='"',
                            what_suffix='"')

    $ Nihltu = Character(_('Nihltu'), #Demon Commander 4
                            what_prefix='"',
                            what_suffix='"')

    #places
    #Lucidia - Monster Continent
    #Fertilia - Human continent
    #Adventum - Adventuring School!



label splashscreen:
    if persistent.shownSplash is True:
        return

    play music "music/Forest/Starry sky.mp3" fadeout 1.0 fadein 1.0
    show splashScreen
    $ persistent.shownSplash = True
    pause

    return

# The game starts here.
label start:
    $ cmenu_columns = []
    $ cmenu_breadcrumb = []
    $ persistantMonSetData = []
    $ renpy.block_rollback()
    $ config.rollback_enabled = False
    $ renpy.retain_after_load()
    $ TempSensitivity = BodySensitivity()
    $ CurrentVersion = config.version

    show screen input_detection

    python:
        playerGone = 0
        playerCloseMark = 0
        monsterEncounter = []
        trueMonsterEncounter = []
        DefeatedEncounterMonsters = []
        lastAttack = ""
        theLastAttacker = ""
        critText = ""
        display = ""
        displayOrder = []
        attackerName = ""
        attackerNameStance2 = ""
        attackerNameStance3 = ""
        attackerNameStance4 = ""
        attackerNameStance5 = ""
        targetName = ""

        SPLossLow = 35
        SPLossHigh = 65
        stanceGo = "False"
        AIStruggle = 0
        ExpPool = 0
        LootDrops = []
        MoneyDrops = 0
        canRun = True
        RanAway = "False"
        Run = "True"
        canbreakFree = False
        combatChoice = ""
        justEscapedStance = 0
        SkillNumber = 0
        ItemNumber = 0
        index = 0
        moveFilter = ""
        runBG = ""

        DataLocation = 0
        isEventNow = 0

        DayNumber = 1
        TimeOfDay = copy.deepcopy(Morning)


    $ orgasmCount = 0
    $ lossCount = 0

    $ difficulty = "Normal"

    $ ExpTotal = 0

    $ bg = ""

    $ VisualEffect = ""
    $ VisualEffect2 = ""
    $ VisualEffect3 = ""

    $ MotionEffect = ""
    $ MotionEffectLoop = 0

    $ CurrentIteration = len(SkillsDatabase) + len(ItemDatabase) + len(MonsterDatabase) + len(PerkDatabase) + len(LocationDatabase) + len(EventDatabase) + len(AdventureDatabase)

    $ Speaker = Character(_(''))
    $ extension = ""
    $ currentLocation = ""
    $ currentNPC = 0
    $ currentChoice = 0
    $ introduced = 1
    $ choiceName = ""
    $ HoldChoice = 0
    $ HoldChoiceNumber = 0

    $ rehauled = 1
    $ progressionBoost = 1

    $ attacker = Monster(Stats())
    $ defender = Monster(Stats())
    $ skillChoice = Skill()

    $ DisplayInventory = 1
    $ ItemToolTip = 0
    $ InventoryAvailable = False
    $ InvTopRowAlignmentY = 0.265
    $ morePages = False
    $ blankHoverValue = 0

    $ DisplaySkills = 1
    $ skillTarget = 0
    $ skillToolTip = 0

    $ SkillTopRowAlignmentY = InvTopRowAlignmentY + 0.15

    $ targetLocation = 0
    $ adventureDeck = []
    $ explorationDeck = []
    $ monsterDeck = []
    $ eventDeck = []
    $ QuestSlot = Event()
    $ tabToggle = 1
    $ currentCardName = ""
    $ currentEvent = 0
    $ deckProgress = 0
    $ questTaken = 0
    $ onAdventure = 0
    $ AdventureHolder = AdventuringDeck()

    $ displayHealthInEvent = 1

    $ Rut = False

    $ debt = 1000000
    $ debtPayed = "False"

    $ tribute = 0
    $ tributeStep = 0


    $ lossCount = 0
    $ winCount = 0


    $ TempFetishes = copy.deepcopy(FetishList)
    $ player = Player()
    $ player._resetPlayerAtStart(copy.deepcopy(FetishList))

    $ tentativeStats = copy.deepcopy(player)


    #make base player
    $ povname = ""
    $ pov = DynamicCharacter("povname", color=(192, 64, 64, 255))

    $ displayingScene = Dialogue()
    $ actorNames = ["", "", "", "", "", "", "", "", "", "", "", ""]


    $ DialogueIsFrom = ""
    $ SceneCharacters = ""
    $ showOnSide = 0

    python:
        player.stats.isPlayer = "True"
        addSkillTo("Kiss", player)
        addSkillTo("Breast Caress", player)
        addSkillTo("Grope Ass", player)
        addSkillTo("Penetrate", player)
        addSkillTo("Thrust", player)

        player.inventory.give("Calming Potion", 5)
        player.inventory.give("Energy Potion", 3)
        player.inventory.give("Anaph Herb", 3)

        player.inventory.money = 1000
        player.CalculateStatBoost()
        #player.perks.append(PerkDatabase[getFromName("Alluring", PerkDatabase)])


    $ _game_menu_screen="save"
    $ skippedIntro = 0


    $ ProgressNPC = []
    $ ProgressEvent = []
    $ ProgressAdventure = []


    $ loadingDatabaseType = 1

    $ historyUpdate = 0
    
    $ favorPool = CalcGoddessFavor(player)

    call loadDatabase from _call_loadDatabase_5


    $ player.name = "Adventurer"

    scene bg town

    menu watchIntro:
        "Watch Intro":
            jump Intro
        "Skip Intro":
            jump SkipIntro


    label SkipIntro:
        scene bg heaven
    label namingNoIntro:
        $ player.name = renpy.input(_("What's your name?"), exclude='{}[]', length=13) or _("Hero")
        $ player.name.strip()
        $ save_name = copy.copy(player.name)
        $ tentativeStats = copy.deepcopy(player)
        $ skippedIntro = 1
        "(Any unspent points will be lost after character creation.)"
        jump characterCreation
        #jump to char creator
        ##Goto Town

    label Intro:
        $ InIntro = 1
        $ currentEvent = 0
        $ DataLocation = 0

        $ DialogueIsFrom= "Event"
        $ displayingScene =  EventDatabase[getFromName("Intro Part 1", EventDatabase)].theEvents[0]

        $ characterDataLocation = getFromName(EventDatabase[DataLocation].Speakers[0].name, MonsterDatabase)
        $ actorNames[0] = MonsterDatabase[characterDataLocation].name + EventDatabase[DataLocation].Speakers[0].postName
        if EventDatabase[DataLocation].Speakers[0].SpeakerType == "?":
            $ actorNames[0] = EventDatabase[DataLocation].Speakers[0].name

        call displayScene from _call_displayScene_4

        scene bg heaven
        window show dissolve
        "A serene female voice is heard from all around you."

        $ God = Character(_('Goddess Venereae'),
                                what_prefix='"',
                                what_suffix='"')
        God "I am the Goddess Venereae, and I have chosen you. You are destined to defeat the Demon Queen."
        "She seems to mutter to herself for a moment."
        God "Now let's see... Male... Graduated Adventum... Ooo top of your class..."
        "She coughs before asking you something important."

    label namingIntro:
        $ player.name = renpy.input(_("Oh brave hero. What is your name?"), exclude='{}[]', length=13) or _("Hero")
        $ player.name.strip()

        if player.name[0] == "[" or  player.name[0] == "{":
            God "Hmm... It appears that is not a name?"
            jump namingIntro


        $ save_name = copy.copy(player.name)
        God "[player.name!t]... a fitting name for a hero..."
        God "Now... let's see your heroic qualifications..."
        "(Any unspent points will be lost after character creation.)"
        $ tentativeStats = copy.deepcopy(player)
        jump characterCreation
    label creatorEnd:
        hide screen  CreatorDisplay
        call uncapStats from _call_uncapStats
        $ player.statPoints = 0
        $ player.SensitivityPoints = 0
        $ creating = 0
    if skippedIntro == 0:
        God "Ah, that should probably do."
        God "Now awaken chosen hero. Your adventure awaits..."

        $ bg = "town.png"
        show screen ON_HealthDisplayBacking #(_layer="hplayer")
        show screen ON_HealthDisplay #(_layer="sayScreen")
        show screen DisplayBG onlayer master
        $ InIntro = 1
        $ currentEvent = 0
        $ explorationDeck = []
        $ DataLocation = getFromName("Intro Part 2", EventDatabase)
        $ DialogueIsFrom= "Event"
        $ displayingScene =  EventDatabase[DataLocation].theEvents[0]

        $ characterDataLocation = getFromName(EventDatabase[DataLocation].Speakers[0].name, MonsterDatabase)
        $ actorNames[0] = MonsterDatabase[characterDataLocation].name + EventDatabase[DataLocation].Speakers[0].postName
        if EventDatabase[DataLocation].Speakers[0].SpeakerType == "?":
            $ actorNames[0] = EventDatabase[DataLocation].Speakers[0].name
        call displayScene from _call_displayScene_5


    $ explorationDeck = []
    $ SceneCharacters = []
    $ InIntro = 0

    if len(FetishList) > len(TempFetishes):
        $ holdFetish = copy.deepcopy(TempFetishes)
        $ TempFetishes = copy.deepcopy(FetishList)

        $ i = 0
        while i < len(holdFetish):
            $ TempFetishes[i].Level = holdFetish[i].Level

            $ i += 1
    $ player.stats.refresh()
    $ favorPool = CalcGoddessFavor(player)
    jump Town

    # This ends the game.

    return
