init -1 python:
    class Alias:
        def __init__(self, fn):
            self.fn = fn
        def __str__(self):
            return str(self.fn())

    def PinkTag(tag, argument, contents):
        return [(renpy.TEXT_TAG, "color=#F6BADC")] + contents + [(renpy.TEXT_TAG, "/color")]
    config.custom_text_tags["Pink"] = PinkTag

    # General Interpolation
    def getHeOrShe(target): #getGenderPronoun
        if target.gender == "male":
            return "he"
        else:
            return "she"

    def getHimOrHer(target): #getGenderPronounPossesive
        if target.gender == "male":
            return "him"
        else:
            return "her"

    def getHisOrHer(target): #getGenderPossesive
        if target.gender == "male":
            return "his"
        else:
            return "her"

    def getYouOrMonsterName(target):
        # if target.species == "Player":
        #     return "you"
        # else:
        return target.name

    def getPenetration(player):
        global sexBank, assBank
        theSexWord = ""
        for each in player.combatStance:
            if each.Stance == "Sex":
                theSexWord = renpy.random.choice(sexBank)
            elif each.Stance == "Anal":
                theSexWord = renpy.random.choice(assBank)
        return theSexWord

    def getPenetrationAjectives(player):
        global sexAdjectiveBank, assAdjectiveBank
        theSexAjective = ""
        for each in player.combatStance:
            if each.Stance == "Sex":
                theSexAjective = renpy.random.choice(sexAdjectiveBank)
            elif each.Stance == "Anal":
                theSexAjective = renpy.random.choice(assAdjectiveBank)
        return theSexAjective

    def theForGeneric(target):
        the = ""
        if target.species != "Player":
            if target.generic == "True":
                the = "The "
        return the

    # Item Interpolation
    def ItemEnergy(itemEnergy, player):
        tooltipBonus = 1
        if itemEnergy > 0:
            for perk in player.perks:
                for i, perk_type in enumerate(perk.PerkType):
                    if perk_type == "ItemBonus":
                        tooltipBonus += (perk.EffectPower[i])*0.01
        return abs(int(math.floor(itemEnergy*tooltipBonus)))
    def ItemArousal(itemArousal, player):
        tooltipBonus = 1
        if itemArousal > 0:
            for perk in player.perks:
                for i, perk_type in enumerate(perk.PerkType):
                    if perk_type == "ItemBonus":
                        tooltipBonus += (perk.EffectPower[i])*0.01

        return abs(int(math.floor(itemArousal*tooltipBonus)))
    def ItemSpirit(itemSpirit, player):
        tooltipBonus = 1
        if itemSpirit > 0:
            for perk in player.perks:
                for i, perk_type in enumerate(perk.PerkType):
                    if perk_type == "ItemBonus":
                        tooltipBonus += (perk.EffectPower[i])*0.01

        return abs(int(math.floor(itemSpirit*tooltipBonus)))

    # Combat Interpolation
    def DamageToPlayerInterp():
        global damageToPlayer, monsterEncounter, CombatFunctionEnemytarget, recoil, effectiveText, critText
        damageToPlayer = " You gain " + str(finalDamage) + " arousal."
        if len(monsterEncounter) > 0 and CombatFunctionEnemytarget < len(monsterEncounter):
            if recoil > 0:
                damageToPlayer += " " + monsterEncounter[CombatFunctionEnemytarget].name + " is also aroused by " + str(recoil) +"!"
        return ""#critText + effectiveText + damageToPlayer

    def DamageToEnemyInterp():
        global damageToEnemy, monsterEncounter, CombatFunctionEnemytarget, recoil, effectiveText, critText, player
        return ""
        if len(monsterEncounter) > 0 and CombatFunctionEnemytarget < len(monsterEncounter):
            damageToEnemy = critText +  effectiveText + monsterEncounter[CombatFunctionEnemytarget].name + " gains " + str(finalDamage) + " arousal."
            if recoil > 0:
                damageToEnemy += " " + player.name +" is also aroused by " + str(recoil) +"!"
                return damageToEnemy
            else:
                return damageToEnemy
        else:
            return ""

    def PlayerOrgasmLineInterp():
        global playerOrgasmLine, player, spiritLost
        playerOrgasmLine = " " + player.name + " loses " + str(spiritLost) + " spirit."
        return playerOrgasmLine

    def PostOrgasmInterp():
        global postOrgasmLine, player, attacker
        holder = PostOrgasmCheck(player, attacker)
        player = holder[0]
        attacker = holder[1]
        postOrgasmLine = holder[2]
        if postOrgasmLine != "":
            disLineOne = " As " + attacker.name + " takes in your semen, "
            postOrgasmLine = disLineOne + postOrgasmLine
        return postOrgasmLine
       
    def MonsterOrgasmLineInterp():
        global monsterOrgasmLine, monsterEncounter, CombatFunctionEnemytarget, spiritLost
        if len(monsterEncounter) > 0 and CombatFunctionEnemytarget < len(monsterEncounter):
            monsterOrgasmLine = " " +  monsterEncounter[CombatFunctionEnemytarget].name + " loses " + str(spiritLost) + " spirit."
            return monsterOrgasmLine
        else:
            monsterOrgasmLine = ""
            return monsterOrgasmLine

    # Monster Interpolation
    def FocusedMonsterNameInterp():
        global monsterEncounter, CombatFunctionEnemytarget
        if len(monsterEncounter) > 1:
            if len(monsterEncounter) > CombatFunctionEnemytarget:
                focusedName = monsterEncounter[CombatFunctionEnemytarget].name
            else:
                focusedName = ""
        else:
            focusedName = ""
        return focusedName

    # Progress Interpolation
    def ProgressDisplayInterp():
        global progressDisplay, ProgressEvent, DataLocation
        DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
        progressDisplay = ProgressEvent[DataLocation].eventProgress
        return progressDisplay

    # Color Interpolation
    def ColorEndInterp():
        return "{/color}"

    def StoredColorInterp():
        global textColor
        return "{" + "color={}".format(textColor) + "}"

    def StoredColor2Interp():
        global textColor2
        return "{" + "color={}".format(textColor2) + "}"

    def StoredColor3Interp():
        global textColor3
        return "{" + "color={}".format(textColor3) + "}"

    def StoredColor4Interp():
        global textColor4
        return "{" + "color={}".format(textColor4) + "}"

    def StoredColor5Interp():
        global textColor5
        return "{" + "color={}".format(textColor5) + "}"

    def StoredColor6Interp():
        global textColor6
        return "{" + "color={}".format(textColor6) + "}"

    def StoredColor7Interp():
        global textColor7
        return "{" + "color={}".format(textColor7) + "}"
    
    # Input interpolation
    def getPlayersInput(isUpper):
        if persistent.lastInput == "Mouse":
            if isUpper:
                return "Click"
            else:
                return "click"
        elif persistent.lastInput == "Touch":
            if isUpper:
                return "Tap"
            else:
                return "tap"
        elif persistent.lastInput == "Keyboard":
            if isUpper:
                return "Press"
            else:
                return "press"
        elif persistent.lastInput == "Pad":
            if isUpper:
                return "Press"
            else:
                return "press"
        else:
            if renpy.variant("touch"):
                if isUpper:
                    return "Tap"
                else:
                    return "tap"
            else:
                if isUpper:
                    return "Click"
                else:
                    return "click"

    def BigStruggleDisplay(player):
        if player.statusEffects.paralysis.duration > 0:
            return "{color=#F8FF6A}Costs " + str(math.floor(20*GetParalEnergyChange(player)+GetParalFlatEnergyChange(player))) + " Energy.{/color} "
        else:
            return "Costs 20 Energy. "


init -1:
    # Player Name
    define interpolate.ThePlayerName = Alias(lambda: player.name)
    define interpolate.TPN = Alias(lambda: player.name[0])
    define interpolate.THEPLAYERNAME = Alias(lambda: player.name.upper())

    # Player Stats
    define interpolate.PlayerMoney = Alias(lambda: player.inventory.money)
    define interpolate.PlayerLevel = Alias(lambda: player.stats.lvl)
    define interpolate.PlayerVirility = Alias(lambda: getVirility(player))
    define interpolate.PlayerFavor = Alias(lambda: CalcGoddessFavor(player))
    define interpolate.favorPool = Alias(lambda: favorPool)
    define interpolate.favorStrain = Alias(lambda: favorStrain)
    
    # Item
    $ itemEnergyAmount = 0
    $ itemArousalAmount = 0
    $ itemSpiritAmount = 0
    define interpolate.ItemEnergy = Alias(lambda: ItemEnergy(itemEnergyAmount, player))
    define interpolate.ItemArousal = Alias(lambda: ItemArousal(itemArousalAmount, player))
    define interpolate.ItemSpirit = Alias(lambda: ItemSpirit(itemSpiritAmount, player))


    # Combat
    define interpolate.FinalDamage = Alias(lambda: str(finalDamage))
    define interpolate.FinalSleepy = Alias(lambda: str(finalSleepy))
    define interpolate.SpiritLost = Alias(lambda: str(spiritLost))
    define interpolate.CritText = Alias(lambda: critText)
    define interpolate.EffectiveText = Alias(lambda: effectiveText)
    define interpolate.StatusEffectiveText = Alias(lambda: statusEffectiveText)
    define interpolate.RecoverAmount = Alias(lambda: str(recoverAmount))

    define interpolate.DamageToPlayer = Alias(lambda: DamageToPlayerInterp())
    define interpolate.DamageToEnemy = Alias(lambda: DamageToEnemyInterp())
    define interpolate.PlayerOrgasmLine = Alias(lambda: PlayerOrgasmLineInterp())
    define interpolate.MonsterOrgasmLine = Alias(lambda: MonsterOrgasmLineInterp())
    define interpolate.PostOrgasmLine= Alias(lambda: PostOrgasmInterp())
    
    define interpolate.HistoryDisplay = Alias(lambda: historyDisplay)

    # Monster Name
    define interpolate.FocusedMonsterName = Alias(lambda: FocusedMonsterNameInterp())

    # Attacker
    define interpolate.AttackerYouOrMonsterName = Alias(lambda: theAttacker + attackerName)
    define interpolate.AttackerName = Alias(lambda: theAttacker + attackerYouOrMonsterName)
    define interpolate.AttackerName2 = Alias(lambda: attackerNameStance2)
    define interpolate.AttackerName3 = Alias(lambda: attackerNameStance3)
    define interpolate.AttackerName4 = Alias(lambda: attackerNameStance4)
    define interpolate.AttackerName5 = Alias(lambda: attackerNameStance5)

    define interpolate.AttackerHeOrShe = Alias(lambda: attackerHeOrShe)
    define interpolate.AttackerHisOrHer = Alias(lambda: attackerHisOrHer)
    define interpolate.AttackerHimOrHer = Alias(lambda: attackerHimOrHer)

    # Target
    define interpolate.TargetName = Alias(lambda: theTarget + targetName)
    define interpolate.TargetYouOrMonsterName = Alias(lambda: theTarget + targetYouOrMonsterName)

    define interpolate.TargetHeOrShe = Alias(lambda: targetHeOrShe)
    define interpolate.TargetHisOrHer = Alias(lambda: targetHisOrHer)
    define interpolate.TargetHimOrHer = Alias(lambda: targetHimOrHer)

    # Random Words
    define interpolate.SexWord = Alias(lambda: getPenetration(player))
    define interpolate.SexAdjective = Alias(lambda: getPenetrationAjectives(player))

    # Display Choice/Progress
    define interpolate.DisplayPlayerChoice = Alias(lambda: PlayerChoiceToDisplay)
    define interpolate.DisplayMonsterChoice = Alias(lambda: MonsterChoiceToDisplay)

    define interpolate.ProgressDisplay = Alias(lambda: ProgressDisplayInterp())

    # ParalEnergyCost/statcheckthing
    define interpolate.StatCheckPost = Alias(lambda: GetParalFlatEnergyCostDisplay(player))
    define interpolate.BigStruggleDisplay = Alias(lambda: BigStruggleDisplay(player))


    # Color "Tags"
    define interpolate.ColorEnd = Alias(lambda: ColorEndInterp())
    define interpolate.StoredColor = Alias(lambda: StoredColorInterp())
    define interpolate.StoredColor2 = Alias(lambda: StoredColor2Interp())
    define interpolate.StoredColor3 = Alias(lambda: StoredColor3Interp())
    define interpolate.StoredColor4 = Alias(lambda: StoredColor4Interp())
    define interpolate.StoredColor5 = Alias(lambda: StoredColor5Interp())
    define interpolate.StoredColor6 = Alias(lambda: StoredColor6Interp())
    define interpolate.StoredColor7 = Alias(lambda: StoredColor7Interp())

    # Player Temp Sensitivity

    define interpolate.PlayerTempSensSex = Alias(lambda: TempSensitivity.getRes("Sex"))
    define interpolate.PlayerTempSensAss = Alias(lambda: TempSensitivity.getRes("Ass"))
    define interpolate.PlayerTempSensNipples = Alias(lambda: TempSensitivity.getRes("Nipples"))
    define interpolate.PlayerTempSensMouth = Alias(lambda: TempSensitivity.getRes("Mouth"))
    define interpolate.PlayerTempSensSeduction = Alias(lambda: TempSensitivity.getRes("Seduction"))
    define interpolate.PlayerTempSensMagic = Alias(lambda: TempSensitivity.getRes("Magic"))
    define interpolate.PlayerTempSensPain = Alias(lambda: TempSensitivity.getRes("Pain"))

    # Player Temp Fetish

    # Internal Misc
    define interpolate.PlayersInput = Alias(lambda: getPlayersInput(True))

    define interpolate.playersinput = Alias(lambda: getPlayersInput(False))

label read(): #did you set display to something before calling this?
    #check for line breaks.
    $ parseL = display.partition("|c|")[0]
    $ displayOrder = parseL.split("|n|") if parseL else []

    if RoledCGOn == 1:
        $ monsterEncounterCG = UpdateCGRoles(monsterEncounterCG, monsterEncounter)

    $ par = 0
    while par < len(displayOrder):
        $ display = ""
        $ splittingDisplay = displayOrder[par].partition("|f|")
        $ showBeforeFunction = splittingDisplay[0]


        $ display = showBeforeFunction
        if display != "" and display != " " and display != "\n" :

            if preFunctionLine == 1:
                $ preFunctionLine = 0
                $ display += "\n" + monsterEncounter[monLossCheck].name + " reaches climax and loses " + str(spiritLost) +" spirit!\n"


            if persistent.showVFX == True:
                call playSpecialEffects(VisualEffect, 1) from _call_playSpecialEffects_3
                call playSpecialEffects(VisualEffect2, 2) from _call_playSpecialEffects_4
                call playSpecialEffects(VisualEffect3, 3) from _call_playSpecialEffects_5

            if persistent.showVFX == True:
                if MotionEffect == "Explosion":
                    Speaker "[display!i]" with Explosion
                elif MotionEffect == "LongExplosion":
                    Speaker "[display!i]" with LongExplosion
                elif MotionEffect == "Crash":
                    Speaker "[display!i]" with Crash
                elif MotionEffect == "CrashSmol":
                    Speaker "[display!i]" with CrashSmol
                elif MotionEffect == "Quake":
                    Speaker "[display!i]" with Quake
                elif MotionEffect == "SlowScreenBounce":
                    Speaker "[display!i]" with slowBounceScreen
                elif MotionEffect == "ScreenBounce":
                    Speaker "[display!i]" with bounceScreen
                elif MotionEffect == "ScreenSway":
                    Speaker "[display!i]" with swayScreen
                else:
                    Speaker "[display!i]"
            else:
                Speaker "[display!i]"


            call postSpecialEffectsCall(VisualEffect, 1) from _call_postSpecialEffectsCall_3
            call postSpecialEffectsCall(VisualEffect2, 2) from _call_postSpecialEffectsCall_4
            call postSpecialEffectsCall(VisualEffect3, 3) from _call_postSpecialEffectsCall_5

            if MotionEffectLoop == 0:
                $ MotionEffect = ""
                $ GlobalMotion = ""

            hide kiss onlayer visualEffects
            if kissBarOnce == 1:
                $ kissBarOnce = 0
                hide kissingBarrage onlayer visualEffects
                hide kissingBarrageFade onlayer visualEffects
            hide lvlDown onlayer visualEffects
            hide lvlDownPulse onlayer visualEffects


        if splittingDisplay[2] != "":
            if HoldingForFuntion == 0 and not monsterEncounter and displayingScene.NameOfScene != "" and itemEvent == 0 and onGridMap <= 1:
                $ HoldingSceneF = copy.deepcopy(displayingScene)
                $ HoldingLineF = copy.copy(lineOfScene) + 1
                $ HoldingDataLocF = copy.copy(DataLocation)
                $ HoldingForFuntion = 1

            $ parseL = splittingDisplay[2].split("|/|")
            $ displayingScene = Dialogue()
            $ displayingScene.theScene = [f for f in parseL if f and f != " "]
            $ HoldSpeaker = Speaker

            $ lastDisplay = copy.copy(display)
            $ LastDisplayOrder = copy.copy(displayOrder)
            $ lastPar = copy.copy(par)
            call displayScene from _call_displayScene_6
            $ LastLine = lastDisplay
            #if display != lastDisplay:
            #    $ LastDisplayOrder = []
            #    $ LastDisplayOrder.append(Dialogue())
            $ displayOrder = copy.copy(LastDisplayOrder)
            $ Speaker = HoldSpeaker
            $ par = copy.copy(lastPar)
            $ LastDisplayOrder = []


        $ par += 1

    if par >= 0 and not monsterEncounter and HoldingForFuntion == 1 and HoldingSceneF != Dialogue() and onGridMap <= 1:
        $ displayingScene = copy.deepcopy(HoldingSceneF)
        $ lineOfScene = copy.copy(HoldingLineF)
        $ DataLocation = copy.copy(HoldingDataLocF)
        $ HoldingSceneF = Dialogue()
        $ HoldingLineF = 0
        $ HoldingDataLocF = 0
        $ HoldingForFuntion = 0
        $ LastDisplayOrder = []
        if itemEvent == 1:
            return
        jump resumeSceneAfterCombat

    return
