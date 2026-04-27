init offset = -1

## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):
   
    style_prefix "say"
    key "K_c" action [
        ShowMenu("ON_CharacterDisplayScreen"),
        Function(cmenu_resetMenu),
        SelectedIf(_game_menu_screen=="ON_CharacterDisplayScreen")
        ]

    window:        
        id "window"
        xpos 960 + textboxCGXAdjust #needed to adjust text box pos for CG movement, if better way is found, do that instead, 960 should be exactly 0.5 xalign
        if who is not None:

            window:

                style "namebox"
                text who id "who"

        text what id "what"


    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5 
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Transform(Image("gui/textbox.png", xalign=0.5, yalign=1.0), alpha=0.86)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos


## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## http://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xalign gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input" copypaste True

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## http://www.renpy.org/doc/html/screen_special.html#choice

transform choiceHover():
    on idle:
        easein 0.1 zoom 1.0
    on hover:
        linear 0.1 zoom 1.034

screen choice(items):
    style_prefix "choice"
    key "K_c" action [
        ShowMenu("ON_CharacterDisplayScreen"),
        Function(cmenu_resetMenu),
        SelectedIf(_game_menu_screen=="ON_CharacterDisplayScreen")
        ]
    vbox:
        for i in items:
            fixed:
                fit_first True
                textbutton i.caption:
                    at transform:
                        zoom 1.034
                        alpha 0.0
                textbutton i.caption:
                    xalign 0.5
                    yalign 0.5
                    action i.action
                    if persistent.animatedUI:
                        at [choiceHover]


## When this is true, menu captions will be spoken by the narrator. When false,
## menu captions will be displayed as empty buttons.
define config.narrator_menu = True


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")

init offset = 0

init python:

    LeftMenuScrollButtonX = 0.1750
    RightMenuScrollButtonX = 0.8250

    if renpy.variant("touch"):
        LeftMenuScrollButtonX = 0.1200
        RightMenuScrollButtonX = 0.8800


    def PlacementFunction(mC, placementGroup, xAdjustBase, alternating):
        yMonpos = -0.16
        xMonAdjust = xAdjustBase
        xMonPos = 0.0
        if len(placementGroup) == 2:
            xMonAdjust = xAdjustBase
            if showOnSide == 1:
                    xMonAdjust -= 0.05
            if mC == 0:
                xMonPos -=  xMonAdjust
            else:
                xMonPos +=  xMonAdjust 

        elif len(placementGroup) > 2:
            if len(placementGroup) > 3:
                yMonpos +=  0.04
            if mC > 0:
                if ((mC == 1 or mC == 2) and len(placementGroup) > 10):
                    yMonpos +=  0.24
                    xMonAdjust += xMonAdjust*0.5
                elif (mC >= 8 and len(placementGroup) <= 10) or mC >= 10:
                    yMonpos -=  0.24
                elif (mC >= 7 and len(placementGroup) <= 10) or mC >= 9:
                    yMonpos -=  0.24
                    xMonAdjust = 0
                elif (mC >= 5  and len(placementGroup) <= 10) or mC >= 7:
                    yMonpos -=  0.12
                    xMonAdjust += xMonAdjust*0.5
                elif (mC >= 3 and len(placementGroup) <= 10) or mC >= 5:
                    yMonpos -=  0.12
                    xMonAdjust -= xMonAdjust*0.55

               
                if mC % 2 == 0:
                    alternating *= -1
                xMonAdjust *=  alternating
                xMonPos +=  xMonAdjust
        return [xMonPos, yMonpos]

    def initiateImageLayers(character):
        if len(character.ImageSets) >= 1:
            for layers in character.ImageSets[character.currentSet].ImageSet:
                layers.currentImage = 0

            for layers in character.ImageSets[character.currentSet].ImageSet:
                if layers.StartOn == 1 and len(layers.Images) >= 1 and layers.currentImage <= 0:
                    layers.currentImage = 1
                    if layers.Overlay != "No" and layers.Overlay != "":
                        layers.overlayOn = 1
                        for overlays in character.ImageSets[character.currentSet].ImageSet:
                            if overlays.name == layers.Overlay:
                                layers.currentImage = getFromName(overlays.Images[overlays.currentImage].name, layers.Images)
                elif layers.StartOn == 0:
                    layers.currentImage = 0




        return character
    def initiateOverlays(character):
        if len(character.ImageSets) >= 1:
            for layers in character.ImageSets[character.currentSet].ImageSet:
                if layers.StartOn == 1 and len(layers.Images) >= 1:
                    if layers.Overlay != "No" and layers.Overlay != "":
                        layers.overlayOn = 1
                        for overlays in character.ImageSets[character.currentSet].ImageSet:
                            if overlays.name == layers.Overlay:
                                layers.currentImage = getFromName(overlays.Images[overlays.currentImage].name, layers.Images)
        return character

    def changeImgSet(sceneCharacters, settingCharcter, layerToChange, settingToImage):
        imgI = 0


        global persistantMonSetData, textboxCGXAdjust
        for each in sceneCharacters:           
            if imgI == settingCharcter:
                if layerToChange == "ImageSetPersist":
                    if getFromName(each.IDname, persistantMonSetData) == -1:
                        persistantMonSetData.append(PersistantImgSetData(each.IDname, settingToImage))
                    else:
                        persistantMonSetData[getFromName(each.IDname, persistantMonSetData)].startingSet = settingToImage

                carryOver = copy.deepcopy(each.ImageSets[each.currentSet].ImageSet)

                each.currentSet = getFromName(settingToImage, each.ImageSets)
                layerNum = 0
                textboxCGXAdjust = each.ImageSets[each.currentSet].TextBoxXAdjust

                if layerToChange != "ImageSetDontCarryOver":
                    for ImageGroup in carryOver:
                       
                        try:
                            each.ImageSets[each.currentSet].ImageSet[layerNum].currentImage = ImageGroup.currentImage
                            if each.ImageSets[each.currentSet].ImageSet[layerNum].Overlay != "No" and each.ImageSets[each.currentSet].ImageSet[layerNum].Overlay != "":
                                each.ImageSets[each.currentSet].ImageSet[layerNum].overlayOn = ImageGroup.overlayOn
                        except:
                            each.ImageSets[each.currentSet].ImageSet[layerNum].currentImage = 0
                            if each.ImageSets[each.currentSet].ImageSet[layerNum].AlwaysOn == 1 and each.ImageSets[each.currentSet].ImageSet[layerNum].currentImage <= 0:
                                each.ImageSets[each.currentSet].ImageSet[layerNum].currentImage = 1
                                if layers.Overlay != "No" and layers.Overlay != "":
                                    layers.overlayOn = 1

                        layerNum += 1
                else:
                    each = initiateImageLayers(each)

            imgI += 1
        return sceneCharacters

    def changeImgLayer(sceneCharacters, settingCharcter, layerToChange, settingToImage):
        imgI = 0

        for each in sceneCharacters:
            if imgI == settingCharcter:
                for layers in each.ImageSets[each.currentSet].ImageSet:
                    if layerToChange == layers.name:
                        if settingToImage == "ActivateOverlay":
                            layers.overlayOn = 1
                            for overlays in each.ImageSets[each.currentSet].ImageSet:
                                if overlays.name == layers.Overlay:
                                    try:
                                        if getFromName(overlays.Images[overlays.currentImage].name, layers.Images) != -1:
                                            layers.currentImage = getFromName(overlays.Images[overlays.currentImage].name, layers.Images)
                                        else:
                                            layers.currentImage = -1
                                    except:
                                        pass

                        elif settingToImage == "DeactivateOverlay":
                            layers.overlayOn = 0
                        elif settingToImage == "" or settingToImage == "None":
                            layers.currentImage = 0
                            for overlays in each.ImageSets[each.currentSet].ImageSet:
                                if overlays.Overlay == layers.name:
                                    if overlays.overlayOn != 0:
                                        overlays.currentImage = -1
                        else:
                            if settingToImage != "_Default":
                                layers.currentImage = getFromName(settingToImage, layers.Images)
                            else:
                                if layers.currentImage <= 0:
                                    layers.currentImage = 1
                            if layers.AlwaysOn == 1 and layers.currentImage <= 0:
                                layers.currentImage = 1

                            for overlays in each.ImageSets[each.currentSet].ImageSet:
                                if overlays.Overlay == layers.name:
                                    if overlays.overlayOn != 0:
                                        if getFromName(settingToImage, overlays.Images) != -1:
                                            overlays.currentImage = getFromName(settingToImage, overlays.Images)
                                        else:
                                            overlays.currentImage = -1

            imgI += 1
        return sceneCharacters
    def AnimateImgLayer(searchingCharacters, settingCharcter, layerToChange, settingAnimate):
        imgI = 0

        for each in searchingCharacters:
            if imgI == settingCharcter:
                for layers in each.ImageSets[each.currentSet].ImageSet:
                    if layerToChange == layers.name:
                        layers.animating = settingAnimate

            imgI += 1
        return searchingCharacters

    def UpdateCGRoles(monsterEncounterCG, monsterEncounter):
        global CGRoleBuffer, RoledCGOn, CgRoleKeeper, combatMonUIoveride
        settingCharcter = 0
        combatMonUIoveride =[]
        combatMonUIoveride.append([0.0,0.0])
        RoleList = []

        if RoledCGOn == 1:

            for each in monsterEncounter:
                combatMonUIoveride.append([0.0,0.0])

            requiresStance = 0
            requiresStanceMet = 0
            CGRoleBuffer -= 1
            for each in CgRoleKeeper:
                stancePass = 0
                enemycounter = 0
                if each.NeedOne == "Yes":
                    requiresStance += 1

                for foe in monsterEncounter:
                    if enemycounter not in RoleList and stancePass != 1:
                        if foe.IDname == each.MonsterReq or each.MonsterReq == "":
                            for stance in foe.combatStance:
                                if stance.Stance == each.StanceReq:
                                    stancePass = 1
                                    RoleList.append(enemycounter)
                                    combatMonUIoveride[enemycounter] = [float(each.SpecificUIPlacementX), float(each.SpecificUIPlacementY)]
                                elif each.StanceReq == "" or each.StanceReq == "None" or each.StanceReq == "Any":
                                    stancePass = 1
                                    RoleList.append(enemycounter)
                                    combatMonUIoveride[enemycounter] = [float(each.SpecificUIPlacementX), float(each.SpecificUIPlacementY)]

                    enemycounter += 1

                if stancePass == 1:
                    if each.NeedOne == "Yes":
                        requiresStanceMet += 1
                    if len(each.ToggledOnPartsWhenReqMet) > 0:
                        for activatingLayers in each.ToggledOnPartsWhenReqMet:
                            settingToImage = "_Default"
                            changeImgLayer(monsterEncounterCG, settingCharcter, activatingLayers, settingToImage)
                else:
                    if len(each.ToggledOnPartsWhenReqMet) > 0:
                        for activatingLayers in each.ToggledOnPartsWhenReqMet:
                            settingToImage = ""
                            changeImgLayer(monsterEncounterCG, settingCharcter, activatingLayers, settingToImage)
            if requiresStance > 0:
                if requiresStanceMet == 0:
                    if CGRoleBuffer <= 0:
                        monsterEncounterCG = []
                        RoledCGOn = 0
                        CgRoleKeeper = []
        return monsterEncounterCG

screen DisplayBG:
    frame:
        xalign 0.5
        yalign 0.5
        #xmaximum 10
        #ymaximum 10
        if bg != "":
            imagebutton:
                idle bg
                hover bg
                insensitive bg
                at truecenter


screen fakeTextBox:
    style_prefix "say"
    window:
        id "window"
        xpos 960 + textboxCGXAdjust
        if Speaker.name is not None and LastLine != "":

            window:
                style "namebox"
                text Speaker.name id "who" size gui.name_text_size
        if Speaker.name != "" and LastLine != "":
            $ DisplayedLine = Speaker.what_prefix + LastLine + Speaker.what_suffix
            text DisplayedLine id "what" xpos gui.dialogue_xpos xsize gui.dialogue_width ypos gui.dialogue_ypos
        else:
            text LastLine id "what" xpos gui.dialogue_xpos xsize gui.dialogue_width ypos gui.dialogue_ypos


    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0



screen MenuPageButtons:
    $ buttonIdleImgDown = "gui/Button_DecMenuIdle.png"
    $ buttonHoverImgDown = "gui/Button_DecMenuHover.png"
    $ buttonIdleImgUp = "gui/Button_IncMenuIdle.png"
    $ buttonHoverImgUp = "gui/Button_IncMenuHover.png"


    fixed:
        xalign LeftMenuScrollButtonX
        yalign 0.369
        imagebutton:
            idle buttonIdleImgDown
            hover buttonHoverImgDown
            xalign LeftMenuScrollButtonX
            yalign 0.369
            action  Jump("lastMenuPage")
    fixed:
        xalign RightMenuScrollButtonX
        yalign 0.369
        imagebutton:
            idle buttonIdleImgUp
            hover buttonHoverImgUp
            xalign RightMenuScrollButtonX
            yalign 0.369
            action  Jump("nextMenuPage")

screen FetPageButtons:
    $ buttonIdleImgDown = "gui/Button_dec_idle_Jumbo.png"
    $ buttonHoverImgDown = "gui/Button_dec_hover_Jumbo.png"
    $ buttonIdleImgUp = "gui/Button_inc_idle_Jumbo.png"
    $ buttonHoverImgUp = "gui/Button_inc_hover_Jumbo.png"


    fixed:
        xalign LeftMenuScrollButtonX
        yalign 0.369
        imagebutton:
            idle buttonIdleImgDown
            hover buttonHoverImgDown
            xalign LeftMenuScrollButtonX
            yalign 0.369
            action  Jump("lastFetPage")
    fixed:
        xalign RightMenuScrollButtonX
        yalign 0.369
        imagebutton:
            idle buttonIdleImgUp
            hover buttonHoverImgUp
            xalign RightMenuScrollButtonX
            yalign 0.369
            action  Jump("nextFetPage")

screen SenPageButtons:
    $ buttonIdleImgDown = "gui/Button_dec_idle_Jumbo.png"
    $ buttonHoverImgDown = "gui/Button_dec_hover_Jumbo.png"
    $ buttonIdleImgUp = "gui/Button_inc_idle_Jumbo.png"
    $ buttonHoverImgUp = "gui/Button_inc_hover_Jumbo.png"


    fixed:
        xalign LeftMenuScrollButtonX
        yalign 0.369
        imagebutton:
            idle buttonIdleImgDown
            hover buttonHoverImgDown
            xalign LeftMenuScrollButtonX
            yalign 0.369
            action  Jump("lastSenPage")
    fixed:
        xalign RightMenuScrollButtonX
        yalign 0.369
        imagebutton:
            idle buttonIdleImgUp
            hover buttonHoverImgUp
            xalign RightMenuScrollButtonX
            yalign 0.369
            action  Jump("nextSenPage")

screen NPCPageButtons:
    $ buttonIdleImgDown = "gui/Button_dec_idle_Jumbo.png"
    $ buttonHoverImgDown = "gui/Button_dec_hover_Jumbo.png"
    $ buttonIdleImgUp = "gui/Button_inc_idle_Jumbo.png"
    $ buttonHoverImgUp = "gui/Button_inc_hover_Jumbo.png"

    fixed:
        xalign LeftMenuScrollButtonX
        yalign 0.369
        imagebutton:
            idle buttonIdleImgDown
            hover buttonHoverImgDown
            xalign LeftMenuScrollButtonX
            yalign 0.369
            action  Jump("lastNPCPage")
    fixed:
        xalign RightMenuScrollButtonX
        yalign 0.369
        imagebutton:
            idle buttonIdleImgUp
            hover buttonHoverImgUp
            xalign RightMenuScrollButtonX
            yalign 0.369
            action  Jump("nextNPCPage")




# Screen using NPCCArd to replace the normal dislpgue screen
# Very similar to CharacterDialogueScreen except for using NPCCard instead of frames
screen ON_CharacterDialogueScreen:
    $ alternating = 1
    $ xAdjustBase = -0.22
    if len(SceneCharacters) == 2:
        $ xAdjustBase = 0.15
    elif len(SceneCharacters) > 3:
        $ xAdjustBase =-0.27

    for mC, mon in reversed(list(enumerate(SceneCharacters))):
        $ placement = PlacementFunction(mC, SceneCharacters, xAdjustBase, alternating)
        use SceneCard(mC, mon, placement[0], placement[1])
    for mC, mon in reversed(list(enumerate(SceneCharacters))):
        $ placement = PlacementFunction(mC, SceneCharacters, xAdjustBase, alternating)
        use SceneCGCard(mC, mon, placement[0], placement[1])


screen SceneCard(mC, mon, xMonPos, yMonpos):
    $ ShuntOver = 0
    if showOnSide == 1:
        $ ShuntOver = -0.35 

    $ picCheck = 0
    if mon.name != "?":
        python:
            try:
                if mon.ImageSets[mon.currentSet].ImageSet[0].name != "" and  mon.ImageSets[mon.currentSet].ImageSet[0].name != "None":
                    picCheck = 1
            except:
                pass
        if picCheck == 0 or persistent.showCharacterImages == False:
            $ showName = ""

            if DialogueIsFrom == "Event" or DialogueIsFrom == "Monster":
                $ showName = mon.name
            else:
                if introduced == 0 :
                    $ showName = mon.preIntroName
                else:
                    $ showName = mon.name
            $ transformsList = []
            if GlobalMotion == "Bounce":
                $ transformsList.append(bounceTest)
            fixed:
                xalign 0.5 + xMonPos*1.25 +ShuntOver
                #xpos
                yalign yMonpos + 0.34
                xsize 378
                ysize 540
                if len(transformsList) > 0:
                    at transformsList
                use NPCCard(showName, mon.description, mC, mon.name)

        else:
            #if has picture
            $ bodyX = 0
            $ bodyY = 0
            for layers in mon.ImageSets[mon.currentSet].ImageSet:
                if layers.currentImage == 0 and len(layers.Images) >= 1 and layers.AlwaysOn == 1:
                    $ layers.currentImage = 1

                if layers.Overlay != "No" and layers.Overlay != "":
                    if len(layers.Images) >= 1 and layers.currentImage == 0:
                        $ overlaying = getFromName(settingToImage, mon.ImageSets[mon.currentSet].ImageSet)
                        $ layers.currentImage = getFromName(mon.ImageSets[mon.currentSet].ImageSet[overlaying].Images[mon.ImageSets[mon.currentSet].ImageSet[overlaying].currentImage].name, layers.Images)
                        #$ layers.overlayOn = 1

                if layers.TheBody == 1:
                    $ bodyX = layers.setXalign
                    $ bodyY = layers.setYalign

            #fixed:
            #    #xalign 0.5
            #    yalign yMonpos
            #    ypos bodyY
            #    xpos bodyX + ShuntOver + xMonPos
            #    if len(transformsList) > 0:
            #        at transformsList
                #at Vibrate

            for layers in mon.ImageSets[mon.currentSet].ImageSet:
                $ showimage = 1

                if layers.overlayOn == 0 and layers.Overlay != "No" and layers.Overlay != "":
                    $ showimage = 0
                if layers.player == "Yes" or layers.player == "Hair":
                    if player_display == "Silhouette":
                        $ showimage = 0
                elif layers.player == "Silhouette":
                    if player_display == "Body":
                        $ showimage = 0
                if layers.currentImage > 0 and showimage == 1 and layers.IsScene == 0:
                    if layers.animating == "Animation":
                        $ imageShown = "animatingLayer"
                    elif layers.animating == "Animation2":
                        $ imageShown = "animatingLayer2"
                    elif layers.animating == "Animation3":
                        $ imageShown = "animatingLayer3"
                    else:
                        $ imageShown = layers.Images[layers.currentImage].file

                    $ transformsList = [characterPlacement(yMonpos, bodyY, bodyX, ShuntOver, xMonPos)]
                    if GlobalMotion != "" or layers.motion != "":
                        if GlobalMotion == "Bounce" or layers.motion == "Bounce":
                            $ transformsList.append(Bounce)
                        elif GlobalMotion == "BounceSlow" or layers.motion == "BounceSlow":
                            $ transformsList.append(BounceSlow)
                        elif GlobalMotion == "BounceFast" or layers.motion == "BounceFast":
                            $ transformsList.append(BounceFast)
                        elif GlobalMotion == "BounceOnce" or layers.motion == "BounceOnce":
                            $ transformsList.append(BounceOnce)
                        elif GlobalMotion == "BounceCustom" or layers.motion == "BounceCustom":
                            $ transformsList.append(BounceCustom)
                        elif GlobalMotion == "Sway" or layers.motion == "Sway":
                            $ transformsList.append(Sway)
                        elif GlobalMotion == "SwaySlow" or layers.motion == "SwaySlow":
                            $ transformsList.append(SwaySlow)
                        elif GlobalMotion == "SwayFast" or layers.motion == "SwayFast":
                            $ transformsList.append(SwayFast)
                        elif GlobalMotion == "SwayOnce" or layers.motion == "SwayOnce":
                            $ transformsList.append(SwayOnce)
                        elif GlobalMotion == "SwayCustom" or layers.motion == "SwayCustom":
                            $ transformsList.append(SwayCustom)
                        elif GlobalMotion == "Pump" or layers.motion == "Pump":
                            $ transformsList.append(Pump)
                        elif GlobalMotion == "PumpSlow" or layers.motion == "PumpSlow":
                            $ transformsList.append(PumpSlow)
                        elif GlobalMotion == "PumpFast" or layers.motion == "PumpFast":
                            $ transformsList.append(PumpFast)
                        elif GlobalMotion == "PumpCustom" or layers.motion == "PumpCustom":
                            $ transformsList.append(PumpCustom)
                        elif GlobalMotion == "Ride" or layers.motion == "Ride":
                            $ transformsList.append(Ride)
                        elif GlobalMotion == "RideSlow" or layers.motion == "RideSlow":
                            $ transformsList.append(RideSlow)
                        elif GlobalMotion == "RideFast" or layers.motion == "RideFast":
                            $ transformsList.append(RideFast)
                        elif GlobalMotion == "RideCustom" or layers.motion == "RideCustom":
                            $ transformsList.append(RideCustom)
                        elif GlobalMotion == "Vibrate" or layers.motion == "Vibrate":
                            $ transformsList.append(Vibrate)
                        elif GlobalMotion == "VibrateCustom" or layers.motion == "VibrateCustom":
                            $ transformsList.append(VibrateCustom)
                        elif GlobalMotion == "Realign" or layers.motion == "Realign":
                            $ transformsList.append(Realign)
                        #$ transformsList.append(shakeTest)
                    imagebutton:
                        idle imageShown
                        hover imageShown
                        insensitive imageShown
                        if layers.TheBody == 0:
                            xalign 0.5 + layers.setXalign + layers.Images[layers.currentImage].setXalign
                            ypos layers.setYalign + layers.Images[layers.currentImage].setYalign
                        else:
                            xalign 0.5 + layers.Images[layers.currentImage].setXalign
                            ypos layers.Images[layers.currentImage].setYalign
                        if len(transformsList) > 0:
                            if layers.player != "No":
                                if player_display == "Silhouette":
                                    at transformsList + [CharacterSilPicker, CharacterSilOpacity, CharacterSilSaturation]
                                elif layers.player == "Yes":
                                    at transformsList + [CharacterPicker, CharacterOpacity, CharacterSaturation]
                                elif layers.player == "Hair":
                                    at transformsList + [CharacterHairPicker, CharacterOpacity, CharacterSaturation]
                            else:
                                at transformsList

screen SceneCGCard(mC, mon, xMonPos, yMonpos):
    $ picCheck = 0
    if mon.name != "?":
        python:
            try:
                if mon.ImageSets[mon.currentSet].ImageSet[0].name != "" and  mon.ImageSets[mon.currentSet].ImageSet[0].name != "None":
                    picCheck = 1
            except:
                pass
        if picCheck == 1 and persistent.showCharacterImages == True:
            $ getCorrectBody = 0
            for layers in mon.ImageSets[mon.currentSet].ImageSet:
                if layers.IsScene == 1:
                    if layers.currentImage > 0:
                        $ showimage = 1

                        if layers.overlayOn == 0 and layers.Overlay != "No" and layers.Overlay != "":
                            $ showimage = 0

                        if layers.player == "Yes" or layers.player == "Hair":
                            if player_display == "Silhouette":
                                $ showimage = 0
                        elif layers.player == "Silhouette":
                            if player_display == "Body":
                                $ showimage = 0
                        if showimage == 1:
                            if layers.animating == "Animation":
                                $ imageShown = "animatingLayer"
                            elif layers.animating == "Animation2":
                                $ imageShown = "animatingLayer2"
                            elif layers.animating == "Animation3":
                                $ imageShown = "animatingLayer3"
                            else:
                                $ imageShown = layers.Images[layers.currentImage].file

                            $ transformsList = [truecenter]
                            if GlobalMotion != "" or layers.motion != "":
                                if GlobalMotion == "Bounce" or layers.motion == "Bounce":
                                    $ transformsList.append(Bounce)
                                elif GlobalMotion == "BounceSlow" or layers.motion == "BounceSlow":
                                    $ transformsList.append(BounceSlow)
                                elif GlobalMotion == "BounceFast" or layers.motion == "BounceFast":
                                    $ transformsList.append(BounceFast)
                                elif GlobalMotion == "BounceOnce" or layers.motion == "BounceOnce":
                                    $ transformsList.append(BounceOnce)
                                elif GlobalMotion == "BounceCustom" or layers.motion == "BounceCustom":
                                    $ transformsList.append(BounceCustom)
                                elif GlobalMotion == "Sway" or layers.motion == "Sway":
                                    $ transformsList.append(Sway)
                                elif GlobalMotion == "SwaySlow" or layers.motion == "SwaySlow":
                                    $ transformsList.append(SwaySlow)
                                elif GlobalMotion == "SwayFast" or layers.motion == "SwayFast":
                                    $ transformsList.append(SwayFast)
                                elif GlobalMotion == "SwayOnce" or layers.motion == "SwayOnce":
                                    $ transformsList.append(SwayOnce)
                                elif GlobalMotion == "SwayCustom" or layers.motion == "SwayCustom":
                                    $ transformsList.append(SwayCustom)
                                elif GlobalMotion == "Pump" or layers.motion == "Pump":
                                    $ transformsList.append(Pump)
                                elif GlobalMotion == "PumpSlow" or layers.motion == "PumpSlow":
                                    $ transformsList.append(PumpSlow)
                                elif GlobalMotion == "PumpFast" or layers.motion == "PumpFast":
                                    $ transformsList.append(PumpFast)
                                elif GlobalMotion == "PumpCustom" or layers.motion == "PumpCustom":
                                    $ transformsList.append(PumpCustom)
                                elif GlobalMotion == "Ride" or layers.motion == "Ride":
                                    $ transformsList.append(Ride)
                                elif GlobalMotion == "RideSlow" or layers.motion == "RideSlow":
                                    $ transformsList.append(RideSlow)
                                elif GlobalMotion == "RideFast" or layers.motion == "RideFast":
                                    $ transformsList.append(RideFast)
                                elif GlobalMotion == "RideCustom" or layers.motion == "RideCustom":
                                    $ transformsList.append(RideCustom)
                                elif GlobalMotion == "Vibrate" or layers.motion == "Vibrate":
                                    $ transformsList.append(Vibrate)
                                elif GlobalMotion == "VibrateCustom" or layers.motion == "VibrateCustom":
                                    $ transformsList.append(VibrateCustom)
                                elif GlobalMotion == "Realign" or layers.motion == "Realign":
                                    $ transformsList.append(Realign)
                                #$ transformsList.append(shakeTest)
                            imagebutton:
                                idle imageShown
                                hover imageShown
                                insensitive imageShown
                                xpos layers.setXalign + layers.Images[layers.currentImage].setXalign
                                ypos layers.setYalign + layers.Images[layers.currentImage].setYalign
                                if layers.player != "No":
                                    if player_display == "Silhouette":
                                        at transformsList + [CharacterSilPicker, CharacterSilOpacity, CharacterSilSaturation]
                                    elif layers.player == "Yes":
                                        at transformsList + [CharacterPicker, CharacterOpacity, CharacterSaturation]
                                    elif layers.player == "Hair":
                                        at transformsList + [CharacterHairPicker, CharacterOpacity, CharacterSaturation]
                                else:
                                    at transformsList