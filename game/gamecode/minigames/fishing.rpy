init python:
    def AppendFishQTE(btn):
        global FishQTECheck
        global FishQTE
        global FishQTEActive
        if FishQTECheck == 0 and FishQTEActive:
            if FishQTE[0] == btn:
                FishQTECheck = 1
            else:
                FishQTECheck = 0
                renpy.jump("FailFishing")
        elif FishQTECheck == 1 and FishQTEActive:
            if FishQTE[1] == btn:
                FishQTECheck = 0
                renpy.jump("FishReel")
            else:
                FishQTECheck = 0
                renpy.jump("FailFishing")

screen FishingGameScreen():
    vbox:
        xalign FishLocationX
        yalign FishLocationY
        xanchor 0.5
        yanchor 0.5
        add "gui/SplashParticle.png" at SplashRipple

    vbox:
        xalign FishLocationX
        yalign FishLocationY
        xanchor 0.5
        yanchor 0.5
        add "gui/SplashParticle.png" at SplashRipple2

    vbox:
        xalign FishLocationX
        yalign FishLocationY
        xanchor 0.5
        yanchor 0.5
        add "gui/SplashParticle.png" at SplashRipple3

    vbox:
        xalign FishLocationX
        yalign FishLocationY
        xanchor 0.5
        yanchor 0.5
        imagebutton:
            idle "gui/fishbutton.png"
            hover "gui/fishbutton.png"
            insensitive "gui/fishbutton.png"
            action Jump("FishReel")
            at fishAppear
        if FishQTEActive:
            hbox:
                xalign 0.5
                imagebutton:
                    idle "gui/PadButton" + FishQTE[0][0] + "_idle.png"
                    hover "gui/PadButton" + FishQTE[0][0] + "_idle.png"
                    insensitive "gui/PadButton" + FishQTE[0][0] + "_idle.png"
                    alt FishQTE[0]  + " " + FishQTE[1]
                imagebutton:
                    idle "gui/PadButton" + FishQTE[1][0] + "_idle.png"
                    hover "gui/PadButton" + FishQTE[1][0] + "_idle.png"
                    insensitive "gui/PadButton" + FishQTE[1][0] + "_idle.png"

    key ["focus_left"] action Function(AppendFishQTE, "Left")
    key ["focus_right"]  action Function(AppendFishQTE, "Right")
    key ["focus_up"] action Function(AppendFishQTE, "Up")
    key ["focus_down"] action Function(AppendFishQTE, "Down")
        
    timer FishDifficultyTimer action Jump("FailFishing")

screen FishingHitEffect():
    vbox:
        xalign FishFeedbackX
        yalign FishFeedbackY
        xanchor 0.5
        yanchor 0.5
        add "gui/SplashParticle.png" at SplashRippleHit

    vbox:
        xalign FishFeedbackX
        yalign FishFeedbackY
        xanchor 0.5
        yanchor 0.5
        add "gui/SplashBubbleParticle.png" at SplashBubbleHit



screen FishingGameDelay():
    timer FishAppearTimer action Jump("FishAppear")

label fishingMiniGame:

    if persistent.lastInput in ["Touch", "Mouse"]:
        "Fishing Start! [PlayersInput] to begin!"
    else:
        "Fishing Start! Correctly [playersinput] in the order of the arrows that appear on the screen. [PlayersInput] to begin!"
    $ minigameQuickMenuHide = 1
    $ ReelCount = 0
    $ StrainCount = 0
    $ FishAppearTimer = (renpy.random.randint(AppearTimerMin, AppearTimerMax))*0.01
    $ FishDifficultyTimer = (renpy.random.randint(175, 250))*0.01
    $ FishLocationX = (renpy.random.randint(20, 80))*0.01
    $ FishLocationY = (renpy.random.randint(20, 80))*0.01
    $ FishQTE = [renpy.random.choice(["Up", "Down", "Left", "Right"]), renpy.random.choice(["Up", "Down", "Left", "Right"])]
    $ FishQTECheck = 0
    if not persistent.lastInput in ["Touch", "Mouse"]:
        $ FishQTEActive = True
    else:
        $ FishQTEActive = False
    hide screen FishingHitEffect
    hide screen ON_HealthDisplay
    hide screen ON_HealthDisplayBacking
    show screen FishingGameDelay #(_layer="sayScreen")


label fishingMiniGameLoop:
    if not persistent.lastInput in ["Touch", "Mouse"]:
        $ FishQTEActive = True
    else:
        $ FishQTEActive = False
    window hide
    pause
    $ StrainCount += 1
    if StrainCount >= 3:
        jump FishTooManyMiss
    play soundChannel2 "sfx/ThreadStrainHard.wav" fadeout 0.25
    jump fishingMiniGameLoop

label FishAppear:
    hide screen FishingGameDelay
    show screen FishingGameScreen
    play sound "sfx/heal02.mp3" fadeout 0.25 fadein 0.25
    jump fishingMiniGameLoop


label FishReel:
    hide screen FishingGameScreen
    $ ReelCount += 1
    if ReelCount >= ReelsNeeded:
        jump FishGet
    else:
        $ FishAppearTimer = (renpy.random.randint(AppearTimerMin, AppearTimerMax)*0.2)*0.01
        $ FishDifficultyTimer = (renpy.random.randint(175, 250))*0.01
        $ FishFeedbackX = FishLocationX
        $ FishFeedbackY = FishLocationY
        $ FishLocationX = (renpy.random.randint(20, 80))*0.01
        $ FishLocationY = (renpy.random.randint(20, 80))*0.01
        $ FishQTE = [renpy.random.choice(["Up", "Down", "Left", "Right"]),renpy.random.choice(["Up", "Down", "Left", "Right"])]
        hide screen FishingHitEffect
        show screen FishingGameDelay
        show screen FishingHitEffect
        play soundChannel2 "sfx/ThreadStrainLight.wav" fadeout 0.25
        jump fishingMiniGameLoop

label FishGet:
    hide screen FishingGameScreen
    hide screen FishingGameDelay
    hide screen FishingHitEffect
    $ FishFeedbackX = FishLocationX
    $ FishFeedbackY = FishLocationY
    show screen FishingHitEffect
    show screen ON_HealthDisplay
    show screen ON_HealthDisplayBacking
    stop soundChannel2
    play sound "sfx/Magic/steam01.mp3" fadeout 0.25 fadein 0.25
    $ minigameQuickMenuHide = 0
    $ FishingJump = FishingPassJump
    return

label FishTooManyMiss:
    hide screen FishingGameScreen
    hide screen FishingGameDelay
    hide screen FishingHitEffect
    show screen ON_HealthDisplay
    show screen ON_HealthDisplayBacking
    stop soundChannel2
    play sound "sfx/finger snap_ reverb (long) woman.mp3" fadeout 0.25
    "You pull on your rod too much and your line snaps!"
    $ FishingJump = FishingFailJump
    return


label FailFishing:
    hide screen FishingGameScreen
    hide screen FishingGameDelay
    hide screen FishingHitEffect
    show screen ON_HealthDisplay
    show screen ON_HealthDisplayBacking
    stop soundChannel2
    play sound "sfx/Magic/drowning.mp3" fadeout 0.25
    "The fish got away..."
    $ minigameQuickMenuHide = 0
    $ FishingJump = FishingFailJump
    return
