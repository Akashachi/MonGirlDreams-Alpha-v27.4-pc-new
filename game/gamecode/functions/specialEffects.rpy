
default VisualEffects = ""

init python:
    def IncrementImgSelect(st, at):
        global pulsingChoice, pulsingList, currentPulsingImg, pulsingSpeed, pulsingTime
        if st >= pulsingTime:
            currentPulsingImg += 1
            if currentPulsingImg >= len(pulsingList):
                currentPulsingImg = 0
            pulsingChoice = pulsingList[currentPulsingImg]
            pulsingTime +=  pulsingSpeed
        d = pulsingChoice
        return d, 0.01
    def RandomImgSelect(st, at):
        global pulsingChoiceRand, pulsingListRand, currentPulsingImgRand, pulsingSpeedRand, pulsingTimeRand
        if st >= pulsingTimeRand:
            global pulsingChoiceRand, pulsingListRand
            renpy.random.shuffle(pulsingListRand)
            pulsingChoiceRand = pulsingListRand[0]
            pulsingTimeRand +=  pulsingSpeedRand
        d = pulsingChoiceRand
        return d, 0.01

    def IncrementImgSelect2(st, at):
        global pulsingChoice2, pulsingList2, currentPulsingImg2, pulsingSpeed2, pulsingTime2
        if st >= pulsingTime2:
            currentPulsingImg2 += 1
            if currentPulsingImg2 >= len(pulsingList2):
                currentPulsingImg2 = 0
            pulsingChoice2 = pulsingList2[currentPulsingImg2]
            pulsingTime2 +=  pulsingSpeed2
        d = pulsingChoice2
        return d, 0.01


    def IncrementAnimation(st, at):
        global animationChoice, animationList, currentAnimationImg, animationSpeed, animationTime
        if st >= animationTime:
            currentAnimationImg += 1
            if currentAnimationImg >= len(animationList):
                currentAnimationImg = 0
            animationChoice = animationList[currentAnimationImg]
            animationTime +=  animationSpeed
        d = animationChoice
        return d, animationSpeed

    def IncrementAnimation2(st, at):
        global animationChoice2, animationList2, currentAnimationImg2, animationSpeed2, animationTime2
        if st >= animationTime2:
            currentAnimationImg2 += 1
            if currentAnimationImg2 >= len(animationList2):
                currentAnimationImg2 = 0
            animationChoice2 = animationList2[currentAnimationImg2]
            animationTime2 +=  animationSpeed2
        d = animationChoice2
        return d, animationSpeed2

    def IncrementAnimation3(st, at):
        global animationChoice3, animationList3, currentAnimationImg3, animationSpeed3, animationTime3
        if st >= animationTime3:
            currentAnimationImg3 += 1
            if currentAnimationImg3 >= len(animationList3):
                currentAnimationImg3 = 0
            animationChoice3 = animationList3[currentAnimationImg3]
            animationTime3 +=  animationSpeed3
        d = animationChoice3
        return d, animationSpeed3




    def nextBarrageImgSelect(st, at):
        global barrageChoice, barrageList, currentBarrageImg, BarrageTime, BarrageSpeed
        if st >= BarrageTime:
            currentBarrageImg += 1
            if currentBarrageImg >= len(barrageList):
                currentBarrageImg = 0
            barrageChoice = barrageList[currentBarrageImg]
            BarrageTime += BarrageSpeed

        d = barrageChoice
        return d, 0.01
    def nextBarrageFadeImgSelect(st, at):
        global barrageFadeChoice, barrageFadeList, currentBarrageFadeImg, BarrageFadeTime, BarrageFadeSpeed, barragefadeSkip
        if st >= BarrageFadeTime:
            if barragefadeSkip == 1:
                currentBarrageFadeImg += 1
                if currentBarrageFadeImg >= len(barrageFadeList):
                    currentBarrageFadeImg = 0
                barrageFadeChoice = barrageFadeList[currentBarrageFadeImg]
            else:
                barragefadeSkip = 1
            BarrageFadeTime += BarrageFadeSpeed

        d = barrageFadeChoice
        return d, 0.01

    def nextBarrageImgSelect2(st, at):
        global barrageChoice2, barrageList2, currentBarrageImg2, BarrageTime2, BarrageSpeed2
        if st >= BarrageTime2:
            currentBarrageImg2 += 1
            if currentBarrageImg2 >= len(barrageList2):
                currentBarrageImg2 = 0
            barrageChoice2 = barrageList2[currentBarrageImg2]
            BarrageTime2 += BarrageSpeed2

        d = barrageChoice2
        return d, 0.01
    def nextBarrageFadeImgSelect2(st, at):
        global barrageFadeChoice2, barrageFadeList2, currentBarrageFadeImg2, BarrageFadeTime2, BarrageFadeSpeed2, barragefadeSkip2
        if st >= BarrageFadeTime2:
            if barragefadeSkip2 == 1:
                currentBarrageFadeImg2 += 1
                if currentBarrageFadeImg2 >= len(barrageFadeList2):
                    currentBarrageFadeImg2 = 0
                barrageFadeChoice2 = barrageFadeList2[currentBarrageFadeImg2]
            else:
                barragefadeSkip2 = 1
            BarrageFadeTime2 += BarrageFadeSpeed2

        d = barrageFadeChoice2
        return d, 0.01

    def CheckSoundBank(sfx): #actual sound funtion!
        soundList = []
        usingBank = 0
        if sfx == "QuickKiss":
            soundList = copy.deepcopy(kissQuickSoundBank)
            usingBank = 1
        elif sfx == "LongKiss":
            soundList = copy.deepcopy(kissLongSoundBank)
            usingBank = 1
        elif sfx == "MakeOut":
            soundList = copy.deepcopy(kissMakeOutSoundBank)
            usingBank = 1
        elif sfx == "BlowjobLicking":
            soundList = copy.deepcopy(blowjobLickingSoundBank)
            usingBank = 1
        elif sfx == "BlowjobSucking":
            soundList = copy.deepcopy(blowjobSuckingSoundBank)
            usingBank = 1
        elif sfx == "BlowjobDeepSuction":
            soundList = copy.deepcopy(blowjobDeepSuckingSoundBank)
            usingBank = 1
        elif sfx == "BlowjobVigorous":
            soundList = copy.deepcopy(blowjobVigorousSoundBank)
            usingBank = 1
        elif sfx == "Ejaculation":
            soundList = copy.deepcopy(ejaculationSoundBank)
            usingBank = 1
        elif sfx == "EjaculationLong":
            soundList = copy.deepcopy(messyEjaculationSoundBank)
            usingBank = 1

        return [usingBank, soundList]




label specialEffects:

    transform Vibrate:
        on show, replace:
            linear 0.01 xoffset -5 yoffset 5
            linear 0.01 xoffset 5 yoffset -5
            linear 0.01 xoffset 0 yoffset 5
            linear 0.01 xoffset -5 yoffset 0
            linear 0.01 xoffset 5 yoffset -5
            linear 0.01 xoffset -5 yoffset -5
            linear 0.01 xoffset 0 yoffset 0
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0
    transform VibrateCustom:
        on show, replace:
            linear motionSpeed xoffset -motionDistance yoffset motionDistance
            linear motionSpeed xoffset motionDistance yoffset -motionDistance
            linear motionSpeed xoffset 0 yoffset motionDistance
            linear motionSpeed xoffset -motionDistance yoffset 0
            linear motionSpeed xoffset motionDistance yoffset -motionDistance
            linear motionSpeed xoffset -motionDistance yoffset -motionDistance
            linear motionSpeed xoffset 0 yoffset 0
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0

    transform Realign:
        xoffset 0 yoffset 0

    transform PumpCustom: #looks smoother, in a pump pump pump kinda way
        on show, replace:
            easein motionSpeed yoffset motionDistance
            easeout motionSpeed yoffset -motionDistance
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0
    transform Pump: #looks smoother, in a pump pump pump kinda way
        on show, replace:
            easein .3 yoffset 10
            easeout .3 yoffset -10
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0
    transform PumpSlow: #looks smoother, in a pump pump pump kinda way
        on show, replace:
            easein .5 yoffset 10
            easeout .5 yoffset -10
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0
    transform PumpFast: #looks smoother, in a pump pump pump kinda way
        on show, replace:
            easein .15 yoffset 10
            easeout .15 yoffset -10
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0

    transform BounceCustom: #looks floaty as fuck, but smooth, works best for sway!
        on show, replace:
            ease motionSpeed yoffset motionDistance
            ease motionSpeed yoffset -motionDistance
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0
    transform BounceOnce: #looks floaty as fuck, but smooth, works best for sway!
        on show, replace:
            ease .3 yoffset 10
            ease .3 yoffset -10
            ease .3 yoffset 10
            ease .3 yoffset 0
        on hide, replaced:
            xoffset 0 yoffset 0
    transform Bounce: #looks floaty as fuck, but smooth, works best for sway!
        on show, replace:
            ease .3 yoffset 10
            ease .3 yoffset -10
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0
    transform BounceSlow: #looks floaty as fuck, but smooth, works best for sway!
        on show, replace:
            ease .5 yoffset 10
            ease .5 yoffset -10
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0
    transform BounceFast: #looks floaty as fuck, but smooth, works best for sway!
        on show, replace:
            ease .15 yoffset 10
            ease .15 yoffset -10
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0

    transform SwayCustom: #looks floaty as fuck, but smooth, works best for sway!
        on show, replace:
            ease motionSpeed xoffset motionDistance
            ease motionSpeed xoffset -motionDistance
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0
    transform Sway: #looks floaty as fuck, but smooth, works best for sway!
        on show, replace:
            ease .3 xoffset 13
            ease .3 xoffset -13
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0
    transform SwayOnce: #looks floaty as fuck, but smooth, works best for sway!
        on show, replace:
            ease .3 xoffset 13
            ease .3 xoffset -13
            ease .3 xoffset 13
            ease .3 xoffset 0
        on hide, replaced:
            xoffset 0 yoffset 0
    transform SwaySlow: #looks floaty as fuck, but smooth, works best for sway!
        on show, replace:
            ease .6 xoffset 13
            ease .6 xoffset -13
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0
    transform SwayFast: #looks floaty as fuck, but smooth, works best for sway!
        on show, replace:
            ease .15 xoffset 15
            ease .15 xoffset -15
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0

    transform RideCustom:
        on show, replace:
            pause .15
            yoffset 0
            easein motionSpeed yoffset -motionDistance
            easeout motionSpeed yoffset 0
            easein motionSpeed yoffset -motionDistance/2
            easeout motionSpeed yoffset 0
            yoffset 0
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0
    transform Ride:
        on show, replace:
            pause .15
            yoffset 0
            easein .275 yoffset -20
            easeout .275 yoffset 0
            easein .275 yoffset -10
            easeout .275 yoffset 0
            yoffset 0
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0
    transform RideFast:
        on show, replace:
            pause .10
            yoffset 0
            easein .15 yoffset -20
            easeout .15 yoffset 0
            easein .15 yoffset -10
            easeout .15 yoffset 0
            yoffset 0
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0
    transform RideSlow:
        on show, replace:
            pause .2
            yoffset 0
            easein .5 yoffset -20
            easeout .5 yoffset 0
            easein .5 yoffset -10
            easeout .5 yoffset 0
            yoffset 0
            repeat
        on hide, replaced:
            xoffset 0 yoffset 0

    transform characterPlacement(yMonpos, bodyY, bodyX, ShuntOver, xMonPos):
        #yalign yMonpos
        ypos bodyY + yMonpos
        xpos bodyX + ShuntOver + xMonPos + 0.5




    #some unused motion effects from testing.
    transform BounceOGStyle: #likely better for the one off bounces
        on show, replace:
            linear .3 yoffset 10
            linear .3 yoffset -10
            repeat
        on hide, replaced:
            yoffset 0

    #compared to bounce/sway effects with move, ATL transforms are about half the time for setting speed.
    #so base bounce and sway are .3 speed and 10 move, fast bounce would be about 0.2 speed
    transform shakeTest:
        on show, replace:
            ease .8 xoffset 15
            pause 0.01
            ease .8 xoffset -15
            pause 0.01
            repeat
        on hide, replaced:
            xoffset 0

    transform shakeRide:
        on show, replace:
            ease .3 yoffset 18
            ease .3 yoffset -18
            ease .4 yoffset 16
            ease .4 yoffset -16
            ease .5 yoffset 12
            ease .5 yoffset -12
            ease .4 yoffset 8
            ease .4 yoffset -8
            ease .5 yoffset 12
            ease .5 yoffset -12
            ease .4 yoffset 16
            ease .4 yoffset -16
            repeat
        on hide, replaced:
            yoffset 0

    transform shakeNyaa:
        ease .6 yoffset 24
        ease .6 yoffset -24
        ease .5 yoffset 20
        ease .5 yoffset -20
        ease .4 yoffset 16
        ease .4 yoffset -16
        ease .3 yoffset 12
        ease .3 yoffset -12
        ease .2 yoffset 8
        ease .2 yoffset -8
        ease .1 yoffset 4
        ease .1 yoffset -4
        ease .1 yoffset 0
        repeat


    transform screenFlash:
        alpha 0.0
        linear 0.25 alpha 0.75
        linear 0.25 alpha 0.0
        on hide:
            linear 0.25 alpha 0.0

    transform fishAppear:
        alpha 0.0
        linear 0.25 alpha 1.0
        on hide:
            linear 0.05 alpha 0.0

    transform SplashRipple:
        alpha 0.0
        xysize (100, 100)
        linear 0.3 alpha 0.75 xysize (250, 250)
        linear 0.3 alpha 0.0 xysize (600, 600)
        on hide:
            linear 0.05 alpha 0.0

    transform SplashRippleHit:
        alpha 0.1
        xysize (25, 25)
        ease 0.2 alpha 0.5 xysize (250, 250)
        linear 0.2 alpha 0.0 xysize (600, 600)
        on hide:
            linear 0.05 alpha 0.0

    transform SplashBubbleHit:
        alpha 0.1
        xysize (50, 100)
        linear 0.3 alpha 0.95 ypos -80 xysize (200, 320)
        linear 0.2 alpha 0.0 ypos 20 xysize (350, 250)
        on hide:
            linear 0.05 alpha 0.0

    transform SplashRipple2:
        alpha 0.0
        xysize (100, 100)
        0.25
        linear 0.3 alpha 0.75 xysize (250, 250)
        linear 0.3 alpha 0.0 xysize (600, 600)
        on hide:
            linear 0.05 alpha 0.0

    transform SplashRipple3:
        alpha 0.0
        xysize (100, 100)
        0.5
        linear 0.3 alpha 0.75 xysize (250, 250)
        linear 0.3 alpha 0.0 xysize (600, 600)
        on hide:
            linear 0.05 alpha 0.0

    transform screenBlindingFlash:
        alpha 0.0
        linear 0.15 alpha 1.0
        0.15
        linear 3.5 alpha 0.0
        on hide:
            linear 2.0 alpha 0.0

    transform screenPulse:
        alpha 0.0
        linear 0.2 alpha 0.2
        linear 0.2 alpha 0.0
        on hide:
            linear 0.2 alpha 0.0
    transform repeatingPulse:
        alpha 0.0
        linear 0.35 alpha 0.2
        linear 0.35 alpha 0.0
        repeat
    transform OrgasmPulse:
        alpha 0.0
        linear 0.1 alpha 0.5
        linear 0.15 alpha 0.1
        linear 0.1 alpha 0.5
        linear 0.15 alpha 0.1
        linear 0.2 alpha 0.7
        0.05
        linear 1.5 alpha 0.0
        on hide:
            linear 0.2 alpha 0.0
    transform DoublePulse:
        alpha 0.0
        linear 0.3 alpha 0.35
        0.05
        linear 0.15 alpha 0.0
        linear 0.3 alpha 0.35
        0.05
        linear 0.15 alpha 0.0
        on hide:
            linear 0.2 alpha 0.0
    transform TriplePulse:
        alpha 0.0
        linear 0.2 alpha 0.25
        0.05
        linear 0.1 alpha 0.0
        linear 0.2 alpha 0.25
        0.05
        linear 0.1 alpha 0.0
        linear 0.2 alpha 0.25
        0.05
        linear 0.1 alpha 0.0
        on hide:
            linear 0.2 alpha 0.0

    transform startHaze:
        alpha 0.0
        linear 1.5 alpha 0.15
        on hide:
            linear 0.5 alpha 0.0
    transform minorHaze:
        alpha 0.15
        on hide:
            linear 0.5 alpha 0.0
    transform growingHaze:
        alpha 0.15
        linear 1.5 alpha 0.3
        on hide:
            linear 0.5 alpha 0.0
    transform fadingHaze:
        alpha 0.3
        linear 1.5 alpha 0.15
        on hide:
            linear 0.5 alpha 0.0
    transform midHaze:
        alpha 0.3
        on hide:
            linear 0.5 alpha 0.0
    transform decreasingHaze:
        alpha 0.6
        linear 1.5 alpha 0.3
        on hide:
            linear 0.5 alpha 0.0
    transform increasingHaze:
        alpha 0.3
        linear 1.5 alpha 0.6
        on hide:
            linear 0.5 alpha 0.0
    transform MajorHazeToBlackOut:
        alpha 0.6
        linear 1.5 alpha 1.0
        on hide:
            linear 0.5 alpha 0.0

    transform majorHaze:
        alpha 0.6
        on hide:
            linear 0.5 alpha 0.0
    transform suddenHaze:
        alpha 0.0
        linear 1.0 alpha 0.6
        on hide:
            linear 0.5 alpha 0.0
    transform BlackOut:
        alpha 0.0
        linear 1.5 alpha 1.0
        on hide:
            linear 1.5 alpha 0.0
    transform BlackedOut:
        alpha 1.0
        on hide:
            linear 1.5 alpha 0.0


    transform SlowImagePulse:
        #on show:
        parallel:
            zoom 1
            linear 3 zoom 1.3
        parallel:
            alpha 0.0
            ease 1.5 alpha 0.6
            ease 1.5 alpha 0.0
        on hide, replaced:
            linear 0.5 alpha 0.0
    transform ImagePulse:
        #on show:
        parallel:
            zoom 1
            linear 1.6 zoom 1.3
        parallel:
            alpha 0.0
            ease 0.8 alpha 0.6
            ease 0.8 alpha 0.0
        on hide, replaced:
            linear 0.5 alpha 0.0
    transform FastImagePulse:
        #on show:
        parallel:
            zoom 1
            linear 0.6 zoom 1.3
        parallel:
            alpha 0.0
            ease 0.3 alpha 0.6
            ease 0.3 alpha 0.0
        on hide, replaced:
            linear 0.5 alpha 0.0
    transform SlowImagePulseLooping:
        #on show:
        parallel:
            zoom 1
            linear 3 zoom 1.3
            repeat
        parallel:
            alpha 0.0
            ease 1.5 alpha 0.6
            ease 1.5 alpha 0.0
            repeat
        on hide, replaced:
            linear 0.5 alpha 0.0
    transform ImagePulseLooping:
        #on show:
        parallel:
            zoom 1
            linear 1.6 zoom 1.3
            repeat
        parallel:
            alpha 0.0
            ease 0.8 alpha 0.6
            ease 0.8 alpha 0.0
            repeat
        on hide, replaced:
            linear 0.5 alpha 0.0
    transform FastImagePulseLooping:
        #on show:
        parallel:
            zoom 1
            linear 0.6 zoom 1.3
            repeat
        parallel:
            alpha 0.0
            ease 0.3 alpha 0.6
            ease 0.3 alpha 0.0
            repeat
        on hide, replaced:
            linear 0.5 alpha 0.0
    transform HypnoSpiral:
        #on show:
        parallel:
            alpha 0.0
            linear 2 alpha spiralOpacity
        parallel:
            xcenter 0.5
            ycenter 0.5
            rotate 0.0
            linear sprialSpeed rotate 360
            repeat

        on hide, replaced:
            linear 0.5 alpha 0.0

    transform PendulumSwing: #Requires a specific image to do this, one that's large enough so it's center point is the top of the screen, you can't reposistion the rotation center in renpy.
        #on show:
        parallel:
            xcenter 0.5
            ycenter 0.0
        parallel:
            ease pendulumSpeed rotate -pendulumSway
            pause 0.1
            ease pendulumSpeed rotate pendulumSway
            pause 0.1
            repeat
        on hide:
            rotate 0


    #frameAnimation Test is here for stuff - aiko
    image animatingLayer = DynamicDisplayable(IncrementAnimation)
    image animatingLayer2 = DynamicDisplayable(IncrementAnimation2)
    image animatingLayer3 = DynamicDisplayable(IncrementAnimation3)

    image ImagePulseLoopingList = DynamicDisplayable(IncrementImgSelect)
    transform ImagePulseLoopingList:
        #on show:
        parallel:
            zoom 1
            linear pulsingSpeed zoom pulseZoom
            repeat
        parallel:
            alpha 0.0
            ease pulsingSpeed/2 alpha pulsingOpacity
            ease pulsingSpeed/2 alpha 0.0
            repeat

        on hide, replaced:
            linear 0.5 alpha 0.0
    image ImagePulseLoopingList2 = DynamicDisplayable(IncrementImgSelect2)
    transform ImagePulseLoopingList2:
        #on show:
        parallel:
            zoom 1
            linear pulsingSpeed2 zoom pulseZoom2
            repeat
        parallel:
            alpha 0.0
            ease pulsingSpeed2/2 alpha pulsingOpacity2
            ease pulsingSpeed2/2 alpha 0.0
            repeat

        on hide, replaced:
            linear 0.5 alpha 0.0


    image ImagePulseLoopingListRandom = DynamicDisplayable(RandomImgSelect)
    transform ImagePulseLoopingListRandom:
        #on show:
        parallel:
            zoom 1
            linear pulsingSpeedRand zoom pulseZoomRand
            repeat
        parallel:
            alpha 0.0
            ease pulsingSpeedRand/2 alpha pulsingOpacityRand
            ease pulsingSpeedRand/2 alpha 0.0
            repeat

        on hide, replaced:
            linear 0.5 alpha 0.0


    transform kiss:
        alpha 0.0
        linear 0.1 alpha 1
        0.2
        linear 0.2 alpha 0.0
        on hide:
            linear 0.2 alpha 0.0



    transform kissingBarragePulse:
        alpha 0.0
        linear 0.25 alpha 0.1
        linear 0.25 alpha 0.0
        repeat

    image kissingBarrage:
        "screenKiss.png"
        0.25
        "screenKiss2.png"
        0.25
        "screenKiss3.png"
        0.25
        "screenKiss4.png"
        0.25
        "screenKiss5.png"
        0.25
        repeat
    image kissingBarrageFade:
        0.25
        "screenKiss.png"
        0.25
        "screenKiss2.png"
        0.25
        "screenKiss3.png"
        0.25
        "screenKiss4.png"
        0.25
        "screenKiss5.png"
        repeat
    transform kissingBarrage:
        linear 0.1 alpha 1.0
        0.15
        alpha 0.0
        repeat
    transform kissingBarrageFade:
        alpha 1.0
        0.05
        linear 0.2 alpha 0.0
        repeat

    transform kissingBarrageOnce:
        linear 0.1 alpha 1.0
        0.15
        alpha 0.0
        linear 0.1 alpha 1.0
        0.15
        alpha 0.0
        linear 0.1 alpha 1.0
        0.15
        alpha 0.0
        linear 0.1 alpha 1.0
        0.15
        alpha 0.0
        linear 0.1 alpha 1.0
        0.15
        alpha 0.0
    transform kissingBarrageFadeOnce:
        alpha 1.0
        0.05
        linear 0.2 alpha 0.0
        alpha 1.0
        0.05
        linear 0.2 alpha 0.0
        alpha 1.0
        0.05
        linear 0.2 alpha 0.0
        alpha 1.0
        0.05
        linear 0.2 alpha 0.0
        alpha 1.0
        0.05
        linear 0.2 alpha 0.0

    image kissingBarrageCustom = DynamicDisplayable(nextBarrageImgSelect)
    image kissingBarrageFadeCustom = DynamicDisplayable(nextBarrageFadeImgSelect)

    image kissingBarrageCustom2 = DynamicDisplayable(nextBarrageImgSelect2)
    image kissingBarrageFadeCustom2 = DynamicDisplayable(nextBarrageFadeImgSelect2)

    image kissingBarrageCustomOld:
        "[KissImg1]"
        pause BarrageSpeed
        "[KissImg2]"
        pause BarrageSpeed
        "[KissImg3]"
        pause BarrageSpeed
        "[KissImg4]"
        pause BarrageSpeed
        "[KissImg5]"
        pause BarrageSpeed
        repeat
    image kissingBarrageFadeCustomOLD:
        pause BarrageSpeed
        "[KissImg1]"
        pause BarrageSpeed
        "[KissImg2]"
        pause BarrageSpeed
        "[KissImg3]"
        pause BarrageSpeed
        "[KissImg4]"
        pause BarrageSpeed
        "[KissImg5]"
        repeat
    transform kissingBarrageCustom:
        linear BarrageSpeed/4 alpha BarrageOpacity
        pause (BarrageSpeed/2+BarrageSpeed/4)
        alpha 0.0
        repeat
    transform kissingBarrageFadeCustom:
        alpha BarrageOpacity
        pause BarrageSpeed/2
        linear BarrageSpeed/2 alpha 0.0
        repeat

    transform kissingBarrageCustom2:
        linear BarrageSpeed2/4 alpha BarrageOpacity2
        pause (BarrageSpeed2/2+BarrageSpeed2/4)
        alpha 0.0
        repeat
    transform kissingBarrageFadeCustom2:
        alpha BarrageOpacity2
        pause BarrageSpeed2/2
        linear BarrageSpeed2/2 alpha 0.0
        repeat


    image ImagePulseLoopingListOLD:
        on show:
            parallel:
                zoom 1
                linear pulsingSpeed zoom pulseZoom
                repeat
            parallel:
                alpha 0.0
                ease pulsingSpeed/2 alpha pulsingOpacity
                ease pulsingSpeed/2 alpha 0.0
                repeat
            parallel:
                "[pulsingChoice]"
                pulsingSpeed
                function IncrementImgSelect
                repeat

        on hide, replaced:
            linear 0.5 alpha 0.0
    image displayVFX = "[vfx]"
    image displayVFX2 = "[vfx2]"
    image displayVFX3 = "[vfx3]"
    image hypnosisSpiral = "[spiralVFX]"
    image PulsingVFX = "[pulsingChoice]"
    image pendulum = "[pendulumVFX]"

    image pleasureHit:
        "pink.png"

    image dark:
        "blankScreen.png"

    image flash:
        "white.png"

    image kiss:
        "screenKiss.png"
    
    image lvlDown:
        "LevelDrainVFX.png" 
    image lvlDownPulse:
        "LevelDrainVFX.png" 

    transform LevelDrainEffect:
        alpha 0.0 
        xalign 0.25
        yalign 0.70
        yoffset -60 

        easein 0.3 alpha 1.0 yoffset -30
        2.5
        easein 0.3 alpha 0.0 yoffset 0
        
        on hide:
            linear 1.0 alpha 0.0
    transform LevelDrainEffectPulse:
        alpha 0.0 
        xalign 0.25
        yalign 0.70
        yoffset -30
        zoom 1

        0.3  
        alpha 0.45 
        linear 2.4 zoom 1.3 alpha 0.0
        easein 0.3 alpha 0.0 yoffset 0
        
        on hide:
            linear 1.0 alpha 0.0
    
 
 


    define slowBounceScreen = Move((0, 10), (0, -10), .60, bounce=True, repeat=True, delay=1.35)
    define bounceScreen = Move((0, 10), (0, -10), .50, bounce=True, repeat=True, delay=1.12)
    define swayScreen = Move((10, 0), (-10, 0), .6, bounce=True, repeat=True, delay=1.35)
    #define slowBounceLoop = Move((0, 10), (0, -10), .60, bounce=True, repeat=True, delay=0)
    #define bounceLoop = Move((0, 10), (0, -10), .50, bounce=True, repeat=True, delay=0)
    #define swayLoop = Move((10, 0), (-10, 0), .6, bounce=True, repeat=True, delay=0)


    python:
        class Shaker(object):
            anchors = {
                'top' : 0.0,
                'center' : 0.5,
                'bottom' : 1.0,
                'left' : 0.0,
                'right' : 1.0,
                }
            def __init__(self, start, child, dist):
                if start is None:
                    start = child.get_placement()
                #
                self.start = [ self.anchors.get(i, i) for i in start ]  # central position
                self.dist = dist    # maximum distance, in pixels, from the starting point
                self.child = child
            def __call__(self, t, sizes):
                # Float to integer... turns floating point numbers to
                # integers.
                def fti(x, r):
                    if x is None:
                        x = 0
                    if isinstance(x, float):
                        return int(x * r)
                    else:
                        return x

                xpos, ypos, xanchor, yanchor = [ fti(a, b) for a, b in zip(self.start, sizes) ]

                xpos = xpos - xanchor
                ypos = ypos - yanchor

                nx = xpos + (1.0-t) * self.dist * (renpy.random.random()*2-1)
                ny = ypos + (1.0-t) * self.dist * (renpy.random.random()*2-1)

                return (int(nx), int(ny), 0, 0)
        def _Shake(start, time, child=None, dist=100.0, **properties):

            move = Shaker(start, child, dist=dist)

            return renpy.display.layout.Motion(move,
                          time,
                          child,
                          add_sizes=True,
                          **properties)

        Shake = renpy.curry(_Shake)
    return

label playSpecialEffects(VisualEffect, showing):

    if showing == 1:
        $ displayingVFX = "displayVFX"
    elif showing == 2:
        $ displayingVFX = "displayVFX2"
    elif showing == 3:
        $ displayingVFX = "displayVFX3"

    if VisualEffect == "StartHaze":
        $ renpy.show(displayingVFX, at_list=[startHaze, truecenter], layer="visualEffects")
    if VisualEffect == "GrowingHaze":
        $ renpy.show(displayingVFX, at_list=[growingHaze, truecenter], layer="visualEffects")
    if VisualEffect == "FadingHaze":
        $ renpy.show(displayingVFX, at_list=[fadingHaze, truecenter], layer="visualEffects")
    if VisualEffect == "IncreasingHaze":
        $ renpy.show(displayingVFX, at_list=[increasingHaze, truecenter], layer="visualEffects")
    if VisualEffect == "DecreasingHaze":
        $ renpy.show(displayingVFX, at_list=[decreasingHaze, truecenter], layer="visualEffects")
    if VisualEffect == "MajorHazeToBlackOut":
        $ renpy.show(displayingVFX, at_list=[MajorHazeToBlackOut, truecenter], layer="visualEffects")
    if VisualEffect == "SuddenHaze":
        $ renpy.show(displayingVFX, at_list=[suddenHaze, truecenter], layer="visualEffects")
    if VisualEffect == "MinorHaze":
        $ renpy.show(displayingVFX, at_list=[minorHaze, truecenter], layer="visualEffects")
    if VisualEffect == "MidHaze":
        $ renpy.show(displayingVFX, at_list=[midHaze, truecenter], layer="visualEffects")
    if VisualEffect == "MajorHaze":
        $ renpy.show(displayingVFX, at_list=[majorHaze, truecenter], layer="visualEffects")

    if VisualEffect == "BlackOut":
        $ renpy.show(displayingVFX, at_list=[BlackOut, truecenter], layer="visualEffects")
    if VisualEffect == "BlackedOut":
        $ renpy.show(displayingVFX, at_list=[BlackedOut, truecenter], layer="visualEffects")
    if VisualEffect == "SlowImagePulse":
        $ renpy.show(displayingVFX, at_list=[SlowImagePulse, truecenter], layer="visualEffects")
    if VisualEffect == "ImagePulse":
        $ renpy.show(displayingVFX, at_list=[ImagePulse, truecenter], layer="visualEffects")
    if VisualEffect == "FastImagePulse":
        $ renpy.show(displayingVFX, at_list=[FastImagePulse, truecenter], layer="visualEffects")
    if VisualEffect == "SlowImagePulseLooping":
        $ renpy.show(displayingVFX, at_list=[SlowImagePulseLooping, truecenter], layer="visualEffects")
    if VisualEffect == "ImagePulseLooping":
        $ renpy.show(displayingVFX, at_list=[ImagePulseLooping, truecenter], layer="visualEffects")
    if VisualEffect == "FastImagePulseLooping":
        $ renpy.show(displayingVFX, at_list=[FastImagePulseLooping, truecenter], layer="visualEffects")

    if VisualEffect == "Kiss":
        $ renpy.show(displayingVFX, at_list=[kiss, truecenter], layer="visualEffects")

    if VisualEffect == "ScreenPulse":
        $ renpy.show(displayingVFX, at_list=[screenPulse, truecenter], layer="visualEffects")
    if VisualEffect == "DoublePulse":
        $ renpy.show(displayingVFX, at_list=[DoublePulse, truecenter], layer="visualEffects")
    if VisualEffect == "TriplePulse":
        $ renpy.show(displayingVFX, at_list=[TriplePulse, truecenter], layer="visualEffects")
    if VisualEffect == "RepeatingPulse":
        $ renpy.show(displayingVFX, at_list=[repeatingPulse, truecenter], layer="visualEffects")
        #show displaySelectedVFX onlayer overlay at repeatingPulse
    if VisualEffect == "kissingBarragePulse":
        $ renpy.show(displayingVFX, at_list=[kissingBarragePulse, truecenter], layer="visualEffects")
    if VisualEffect == "ScreenFlash":
        $ renpy.show(displayingVFX, at_list=[screenFlash, truecenter], layer="visualEffects")
    if VisualEffect == "BlindingFlash":
        $ renpy.show(displayingVFX, at_list=[screenBlindingFlash, truecenter], layer="visualEffects")

    if VisualEffect == "OrgasmPulse":
        $ renpy.show(displayingVFX, at_list=[OrgasmPulse, truecenter], layer="visualEffects")
    return

label postSpecialEffectsCall(VisualEffects, showing):
    if persistent.showVFX == True:
        if VisualEffects == "StartHaze":
            $ VisualEffects = "MinorHaze"
        elif VisualEffects == "GrowingHaze":
            $ VisualEffects = "MidHaze"
        elif VisualEffects == "IncreasingHaze":
            $ VisualEffects = "MajorHaze"
        elif VisualEffects == "SuddenHaze":
            $ VisualEffects = "MajorHaze"
        elif VisualEffects == "FadingHaze":
            $ VisualEffects = "MinorHaze"
        elif VisualEffects == "DecreasingHaze":
            $ VisualEffects = "MidHaze"
        elif VisualEffects == "MajorHazeToBlackOut":
            $ VisualEffects = "BlackedOut"

        if VisualEffects == "BlackOut":
            $ VisualEffects = "BlackedOut"

        if VisualEffects != "MidHaze" and VisualEffects != "MinorHaze" and VisualEffects != "MajorHaze" and VisualEffects != "repeatingPulse" and VisualEffects != "kissingBarragePulse" and VisualEffects != "BlackOut" and VisualEffects != "BlackedOut":
            if showing == 1:
                hide displayVFX onlayer visualEffects
                $ VisualEffects = ""
            elif showing == 2:
                hide displayVFX2 onlayer visualEffects
                $ VisualEffects = ""
            elif showing == 3:
                hide displayVFX3 onlayer visualEffects
                $ VisualEffects = ""


        if showing == 1:
            $ VisualEffect = VisualEffects
        elif showing == 2:
            $ VisualEffect2 = VisualEffects
        elif showing == 3:
            $ VisualEffect3 = VisualEffects
    else:
        hide displayVFX onlayer visualEffects
        $ VisualEffect = ""
        hide displayVFX2 onlayer visualEffects
        $ VisualEffect2 = ""
        hide displayVFX3 onlayer visualEffects
        $ VisualEffect3 = ""


    return

label EndAllEffects:
    hide displayVFX onlayer visualEffects
    hide displayVFX2 onlayer visualEffects
    hide displayVFX3 onlayer visualEffects
    $ VisualEffect = ""
    $ VisualEffect2 = ""
    $ VisualEffect3 = ""
    hide kissingBarrage onlayer visualEffects
    hide dark onlayer visualEffects
    hide kiss onlayer visualEffects
    hide lvlDown onlayer visualEffects
    hide lvlDownPulse onlayer visualEffects
    $ MotionEffect = ""
    $ GlobalMotion = ""
    $ motionSpeed = 0
    $ motionDistance = 0
    $ MotionEffectLoop = 0
    stop loopingSound2 fadeout 1.0
    stop loopingSound fadeout 1.0
    hide hypnosisSpiral onlayer visualEffects
    hide hypnosisSpiral behind EnemyCard
    hide hypnosisSpiral behind ON_CharacterDialogueScreen
    hide pendulum onlayer visualEffects
    hide ImagePulseLoopingList onlayer visualEffects
    hide ImagePulseLoopingListRandom onlayer visualEffects
    hide ImagePulseLoopingList2 onlayer visualEffects
    hide kissingBarrageCustom onlayer visualEffects
    hide kissingBarrageFadeCustom onlayer visualEffects
    hide kissingBarrageCustom2 onlayer visualEffects
    hide kissingBarrageFadeCustom2 onlayer visualEffects

    return
