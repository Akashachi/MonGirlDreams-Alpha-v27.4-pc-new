# Play funcs
label JsonFuncPlayerSpeaks:
    $ Speaker = Character(_(player.name+attackTitle),
                            what_prefix='"',
                            what_suffix='"')
    $ lineOfScene += 1
    $ readLine = 1
    return
label JsonFuncPlayerSpeaksSkill:
    if len(monsterEncounter) >= 1:
        $ Speaker = Character(_(player.name+attackTitle) )
        $ lineOfScene += 1
        $ readLine = 1
    return
label JsonFuncPlayerCurrentEnergyCost:
    $ player.stats.ep -= combatChoice.cost
    return
label JsonFuncPlayerOrgasm:
    $ lineOfScene += 1
    $ player.stats.hp = 0
    $ spiritLostO = SpiritCalulation(player, int(displayingScene.theScene[lineOfScene]))
    $ player.stats.sp -= spiritLostO
    $ spiritLost += spiritLostO
    call TimeEvent(CardType="PlayerOrgasm", LoopedList=OnPlayerClimaxList) from _call_TimeEvent_4
    #$ spiritLost += int(displayingScene.theScene[lineOfScene])
    #"[spiritLost]"

    if player.stats.sp <= 0:
        $ player.stats.sp = 0
    if player.stats.sp > player.stats.max_true_sp:
        $ player.stats.sp = player.stats.max_true_sp
    return
label JsonFuncPlayerOrgasmNoSpiritLoss:
    $ player.stats.hp = 0
    $ spiritLost0 = SpiritCalulation(player, 0)
    call TimeEvent(CardType="PlayerOrgasm", LoopedList=OnPlayerClimaxList) from _call_TimeEvent_5
    return
label JsonFuncPlayerStep:
    call statusStep from _call_statusStep
    return
label JsonFuncPlayStoredBGM:
    $ BGMlist = []
    $ bgm = storedBGM[0]
    $ BGMlist = copy.deepcopy(storedBGM)
    $ renpy.random.shuffle(BGMlist)
    if renpy.music.get_playing(channel='music') != bgm:
        play music BGMlist fadeout 1.0 fadein 1.0
    $ musicLastPlayed = BGMlist
    return
label JsonFuncPlayThisSongAfterCombat:
    $ lineOfScene += 1
    $ SetSongAfterCombat = displayingScene.theScene[lineOfScene]
    return
label JsonFuncPlaySoundEffect:
    $ lineOfScene += 1
    $ sfx = ""
    $ usingBank = 0

    $ sfxHolder = CheckSoundBank(displayingScene.theScene[lineOfScene])
    $ usingBank = sfxHolder[0]
    $ soundList = sfxHolder [1]

    if usingBank == 0:
        $ sfx = copy.copy(displayingScene.theScene[lineOfScene])
    else:
        $ renpy.random.shuffle(soundList)
        $ sfx = soundList[0]
    play sound sfx #fadeout 0.25 fadein 0.25
    return
label JsonFuncPlaySoundEffect2:
    $ lineOfScene += 1
    $ sfx = ""
    $ usingBank = 0

    $ sfxHolder = CheckSoundBank(displayingScene.theScene[lineOfScene])
    $ usingBank = sfxHolder[0]
    $ soundList = sfxHolder [1]

    if usingBank == 0:
        $ sfx = copy.copy(displayingScene.theScene[lineOfScene])
    else:
        $ renpy.random.shuffle(soundList)
        $ sfx = soundList[0]
    play soundChannel2 sfx #fadeout 0.25 fadein 0.25
    return
label JsonFuncPlaySoundBankOnce:
    $ lineOfScene += 1
    $ trueSoundList = []
    $ usingBank = 0

    $ sfxHolder = CheckSoundBank(displayingScene.theScene[lineOfScene])
    $ usingBank = sfxHolder[0]
    $ soundList = sfxHolder [1]

    if usingBank == 0:
        $ trueSoundList.append(copy.copy(displayingScene.theScene[lineOfScene]))
    else:
        $ renpy.random.shuffle(soundList)
        python:
            for each in soundList:
                trueSoundList.append(each)
                trueSoundList.append("<silence .25>")
    play sound trueSoundList #fadeout 0.25 fadein 0.25
    return
label JsonFuncPlayLoopingSoundEffect:
    $ lineOfScene += 1
    $ trueSoundList = []
    $ usingBank = 0

    $ sfxHolder = CheckSoundBank(displayingScene.theScene[lineOfScene])
    $ usingBank = sfxHolder[0]
    $ soundList = sfxHolder [1]

    if usingBank == 0:
        $ trueSoundList.append(copy.copy(displayingScene.theScene[lineOfScene]))
    else:
        $ renpy.random.shuffle(soundList)
        python:
            for each in soundList:
                trueSoundList.append(each)
                trueSoundList.append("<silence .25>")
    play loopingSound trueSoundList fadeout 0.05 fadein 0.05 loop
    return
label JsonFuncPlayLoopingSoundEffect2:
    $ lineOfScene += 1
    $ trueSoundList = []
    $ usingBank = 0

    $ sfxHolder = CheckSoundBank(displayingScene.theScene[lineOfScene])
    $ usingBank = sfxHolder[0]
    $ soundList = sfxHolder [1]

    if usingBank == 0:
        $ trueSoundList.append(copy.deepcopy(displayingScene.theScene[lineOfScene]))
    else:
        $ renpy.random.shuffle(soundList)
        python:
            for each in soundList:
                trueSoundList.append(each)
                trueSoundList.append("<silence .25>")
    play loopingSound2 trueSoundList fadeout 0.05 fadein 0.05 loop
    return
label JsonFuncPlayVisualEffect:
    hide displayVFX onlayer visualEffects
    $ lineOfScene += 1
    $ VisualEffect = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ vfx = displayingScene.theScene[lineOfScene]
    return
label JsonFuncPlayVisualEffect2:
    hide displayVFX2 onlayer visualEffects
    $ lineOfScene += 1
    $ VisualEffect2 = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ vfx2 = displayingScene.theScene[lineOfScene]
    return
label JsonFuncPlayVisualEffect3:
    hide displayVFX3 onlayer visualEffects
    $ lineOfScene += 1
    $ VisualEffect3 = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ vfx3 = displayingScene.theScene[lineOfScene]
    return
label JsonFuncPlayImagePulseLoopingList:
    hide ImagePulseLoopingList onlayer visualEffects
    $ currentPulsingImg = 0

    $ lineOfScene += 1
    $ pulsingSpeed = float(displayingScene.theScene[lineOfScene])
    $ pulsingTime = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ pulseZoom = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ pulsingOpacity = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    if displayingScene.theScene[lineOfScene] != "EndLoop":
        $ pulsingList = []
        while displayingScene.theScene[lineOfScene] != "EndLoop":
            if displayingScene.theScene[lineOfScene] != "EndLoop":
                $ pulsingList.append(displayingScene.theScene[lineOfScene])
                $ lineOfScene += 1

    $ pulsingChoice = pulsingList[0]
    if persistent.showVFX == True:
        show ImagePulseLoopingList onlayer visualEffects at truecenter, ImagePulseLoopingList
    return
label JsonFuncPlayImagePulseLoopingList2:
    hide ImagePulseLoopingList2 onlayer visualEffects
    $ currentPulsingImg2 = 0
    $ lineOfScene += 1
    $ pulsingSpeed2 = float(displayingScene.theScene[lineOfScene])
    $ pulsingTime2 = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ pulseZoom2 = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ pulsingOpacity2 = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    if displayingScene.theScene[lineOfScene] != "EndLoop":
        $ pulsingList2 = []
        while displayingScene.theScene[lineOfScene] != "EndLoop":
            if displayingScene.theScene[lineOfScene] != "EndLoop":
                $ pulsingList2.append(displayingScene.theScene[lineOfScene])
                $ lineOfScene += 1

    $ pulsingChoice2 = pulsingList2[0]
    if persistent.showVFX == True:
        show ImagePulseLoopingList2 onlayer visualEffects at truecenter, ImagePulseLoopingList2
    return
label JsonFuncPlayImagePulseLoopingRandom:
    hide ImagePulseLoopingListRandom onlayer visualEffects

    $ currentPulsingImg = 0

    $ lineOfScene += 1
    $ pulsingSpeedRand = float(displayingScene.theScene[lineOfScene])
    $ pulsingTimeRand = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ pulseZoomRand = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ pulsingOpacityRand = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    if displayingScene.theScene[lineOfScene] != "EndLoop":
        $ pulsingListRand = []
        while displayingScene.theScene[lineOfScene] != "EndLoop":
            if displayingScene.theScene[lineOfScene] != "EndLoop":
                $ pulsingListRand.append(displayingScene.theScene[lineOfScene])
                $ lineOfScene += 1

    $ pulsingChoiceRand = pulsingListRand[0]

    if persistent.showVFX == True:
        show ImagePulseLoopingListRandom onlayer visualEffects at truecenter, ImagePulseLoopingListRandom
    return
label JsonFuncPlayHypnoSpiral:
    hide hypnosisSpiral onlayer visualEffects
    hide hypnosisSpiral behind EnemyCard
    hide hypnosisSpiral behind ON_CharacterDialogueScreen
    $ lineOfScene += 1
    $ sprialSpeed = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ spiralOpacity = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ spiralVFX = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ playBehind = int(displayingScene.theScene[lineOfScene])
    if persistent.showVFX == True:
        if playBehind == 0:
            show hypnosisSpiral onlayer visualEffects at HypnoSpiral
        else:
            if len(monsterEncounter) >= 1:
                show hypnosisSpiral behind EnemyCard at HypnoSpiral
            else:
                show hypnosisSpiral behind ON_CharacterDialogueScreen at HypnoSpiral
    return
label JsonFuncPlayPendulum:
    hide pendulum onlayer visualEffects
    $ lineOfScene += 1
    $ pendulumSpeed = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ pendulumSway = float(displayingScene.theScene[lineOfScene])

    $ lineOfScene += 1
    $ pendulumVFX = displayingScene.theScene[lineOfScene]

    show pendulum onlayer visualEffects at PendulumSwing
    return
label JsonFuncPlayKiss:
    if persistent.showVFX == True:
        show kiss onlayer visualEffects at kiss
    return
label JsonFuncPlayKissingBarrage:
    hide kissingBarrage onlayer visualEffects
    hide kissingBarrageFade onlayer visualEffects
    if persistent.showVFX == True:
        show kissingBarrage onlayer visualEffects at kissingBarrage
        show kissingBarrageFade onlayer visualEffects at kissingBarrageFade
    return
label JsonFuncPlayKissingBarrageOnce:
    if persistent.showVFX == True:
        show kissingBarrage onlayer visualEffects at kissingBarrageOnce
        show kissingBarrageFade onlayer visualEffects at kissingBarrageFadeOnce
        $ kissBarOnce = 1
    return
label JsonFuncPlayCustomBarrage:
    hide kissingBarrageCustom onlayer visualEffects
    hide kissingBarrageFadeCustom onlayer visualEffects

    $ barragefadeSkip = 0
    $ lineOfScene += 1
    $ currentBarrageImg = 0
    $ currentBarrageFadeImg = 0
    $ BarrageTime = float(displayingScene.theScene[lineOfScene])
    $ BarrageSpeed = float(displayingScene.theScene[lineOfScene])
    $ BarrageFadeSpeed = float(displayingScene.theScene[lineOfScene])
    $ BarrageFadeTime = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ BarrageOpacity = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    if displayingScene.theScene[lineOfScene] != "EndLoop":
        $ barrageList = []
        $ barrageFadeList = []
        while displayingScene.theScene[lineOfScene] != "EndLoop":
            if displayingScene.theScene[lineOfScene] != "EndLoop":
                $ barrageList.append(displayingScene.theScene[lineOfScene])
                $ barrageFadeList.append(displayingScene.theScene[lineOfScene])
                $ lineOfScene += 1

    $ barrageChoice = barrageList[0]
    $ barrageFadeChoice = barrageFadeList[0]
    if persistent.showVFX == True:
        show kissingBarrageCustom onlayer visualEffects at kissingBarrageCustom
        show kissingBarrageFadeCustom onlayer visualEffects at kissingBarrageFadeCustom
    return
label JsonFuncPlayCustomBarrage2:
    hide kissingBarrageCustom2 onlayer visualEffects
    hide kissingBarrageFadeCustom2 onlayer visualEffects

    $ barragefadeSkip = 0
    $ lineOfScene += 1
    $ currentBarrageImg2 = 0
    $ currentBarrageFadeImg2 = 0
    $ BarrageTime2 = float(displayingScene.theScene[lineOfScene])
    $ BarrageSpeed2 = float(displayingScene.theScene[lineOfScene])
    $ BarrageFadeSpeed2 = float(displayingScene.theScene[lineOfScene])
    $ BarrageFadeTime2 = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ BarrageOpacity2 = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    if displayingScene.theScene[lineOfScene] != "EndLoop":
        $ barrageList = []
        $ barrageFadeList = []
        while displayingScene.theScene[lineOfScene] != "EndLoop":
            if displayingScene.theScene[lineOfScene] != "EndLoop":
                $ barrageList2.append(displayingScene.theScene[lineOfScene])
                $ barrageFadeList2.append(displayingScene.theScene[lineOfScene])
                $ lineOfScene += 1

    $ barrageChoice2 = barrageList2[0]
    $ barrageFadeChoice2 = barrageFadeList2[0]
    if persistent.showVFX == True:
        show kissingBarrageCustom2 onlayer visualEffects at kissingBarrageCustom2
        show kissingBarrageFadeCustom2 onlayer visualEffects at kissingBarrageFadeCustom2
    return
label JsonFuncPlayBlackOut:
    hide dark onlayer visualEffects
    if persistent.showVFX == True:
        show dark onlayer visualEffects at BlackOut
    return
label JsonFuncPlayMotionEffect:
    #"MotionEffect", "EffectName", "Target", "Speed", "Distance"
    #Effects: Bounce, SwayPump, Vibrate, Ride,
        #screen only effects: ScreenSway, ScreenBounce, SlowScreenBounce, Explosion, LongExplosion, Crash, Quake
    $ MotionEffectLoop = 0
    #$ GlobalMotion = ""
    $ lineOfScene += 1
    $ MotionEffect = displayingScene.theScene[lineOfScene]

    if MotionEffect != "Explosion" and MotionEffect != "LongExplosion" and MotionEffect != "Crash" and MotionEffect != "CrashSmol" and MotionEffect != "Quake" and MotionEffect != "SlowScreenBounce" and MotionEffect != "ScreenBounce" and MotionEffect != "ScreenSway":
        $ GlobalMotion = copy.copy(MotionEffect)
        $ MotionEffect = ""
    return
label JsonFuncPlayMotionEffectLoop:
    #$ GlobalMotion = ""
    $ lineOfScene += 1
    $ MotionEffect = displayingScene.theScene[lineOfScene]
    if MotionEffect != "Explosion" and MotionEffect != "LongExplosion" and MotionEffect != "Crash" and MotionEffect != "CrashSmol" and MotionEffect != "Quake" and MotionEffect != "SlowScreenBounce" and MotionEffect != "ScreenBounce" and MotionEffect != "ScreenSway":
        $ GlobalMotion = copy.copy(MotionEffect)
        $ MotionEffect = ""
    $ MotionEffectLoop = 1
    return
label JsonFuncPlayMotionEffectCustom:
    #"MotionEffect", "EffectName", "Target", "Speed", "Distance"
    #Effects: Bounce, Sway
        #screen only effects: SlowBounce, Explosion, LongExplosion, Crash, Quake
        #non-screen only effects: Pump, Vibrate, Ride,
    #Targets: Screen, Characters, Character, Bodypart
    $ MotionEffectLoop = 1
    #$ GlobalMotion = ""
    $ lineOfScene += 1
    $ MotionEffect = displayingScene.theScene[lineOfScene]
    $ lineOfScene += 1
    $ MotionTarget = displayingScene.theScene[lineOfScene]

    if MotionEffect != "":
        $ MotionEffect+= "Custom"
    else:
        $ MotionEffect = "Realign"

    if MotionTarget == "Characters":
        $ GlobalMotion = copy.deepcopy(MotionEffect)
    elif MotionTarget == "Character" or MotionTarget == "Bodypart":
        $ lineOfScene += 1
        python:
            try:
                settingCharcter = int(displayingScene.theScene[lineOfScene]) - 1
            except:
                ifIsInScene = 0
                if len(monsterEncounter) > 0 and hidingCombatEncounter == 0:
                    searchingCharacters = trueMonsterEncounter
                else:
                    searchingCharacters = SceneCharacters
                if len(searchingCharacters) > 0 and hidingCombatEncounter == 0:
                    #during combat layer change
                    if getFromName(displayingScene.theScene[lineOfScene], searchingCharacters)!= -1:
                        ifIsInScene = 1
                        settingCharcter = getFromName(displayingScene.theScene[lineOfScene], searchingCharacters)

                if ifIsInScene == 0:
                    settingCharcter = CombatFunctionEnemytarget

            bodypartTarget = ""
            if MotionTarget == "Bodypart":
                lineOfScene += 1
                bodypartTarget = displayingScene.theScene[lineOfScene]

            for each in searchingCharacters:
                if searchingCharacters[settingCharcter].name == each.name:
                    for layers in each.ImageSets[each.currentSet].ImageSet:
                        if MotionTarget == "Bodypart":
                            if bodypartTarget == layers.name:
                                layers.motion = MotionEffect
                        else:
                            layers.motion = MotionEffect

    $ lineOfScene += 1
    $ motionSpeed = float(displayingScene.theScene[lineOfScene])
    $ lineOfScene += 1
    $ motionDistance = float(displayingScene.theScene[lineOfScene])
    $ MotionEffect = ""
    return
label JsonFuncPlayerLosesCombat:
    if len(monsterEncounter) >= 1:
        $ theLastAttacker = monsterEncounter[CombatFunctionEnemytarget]
        jump combatLoss
    return
# End funcs
label JsonFuncEndVisualEffect:
    $ VisualEffect = ""
    hide displayVFX onlayer visualEffects
    return
label JsonFuncEndVisualEffect2:
    $ VisualEffect2 = ""
    hide displayVFX2 onlayer visualEffects
    return
label JsonFuncEndVisualEffect3:
    $ VisualEffect3 = ""
    hide displayVFX3 onlayer visualEffects
    return
label JsonFuncEndImagePulseLoopingList:
    hide ImagePulseLoopingList onlayer visualEffects
    return
label JsonFuncEndImagePulseLoopingList2:
    hide ImagePulseLoopingList2 onlayer visualEffects
    return
label JsonFuncEndImagePulseLoopingRandom:
    hide ImagePulseLoopingListRandom onlayer visualEffects
    return
label JsonFuncEndHypnoSpiral:
    hide hypnosisSpiral onlayer visualEffects
    hide hypnosisSpiral behind EnemyCard
    hide hypnosisSpiral behind ON_CharacterDialogueScreen
    return
label JsonFuncEndPendulum:
    hide pendulum onlayer visualEffects
    return
label JsonFuncEndKissingBarrage:
    hide kissingBarrage onlayer visualEffects
    hide kissingBarrageFade onlayer visualEffects
    return
label JsonFuncEndCustomBarrage:
    hide kissingBarrageCustom onlayer visualEffects
    hide kissingBarrageFadeCustom onlayer visualEffects
    return
label JsonFuncEndCustomBarrage2:
    hide kissingBarrageCustom2 onlayer visualEffects
    hide kissingBarrageFadeCustom2 onlayer visualEffects
    return
label JsonFuncEndBlackOut:
    hide dark onlayer visualEffects
    return
label JsonFuncEndAllVisualEffects:
    call EndAllEffects from _call_EndAllEffects_5
    return
label JsonFuncEndMotionEffect:
    $ MotionEffect = ""
    $ MotionEffectLoop = 0
    $ GlobalMotion = ""
    return
label JsonFuncEndCounterChecks:
    $ canGo = 0
    return
label JsonFuncEndCombat:
    jump combatWin
    return

