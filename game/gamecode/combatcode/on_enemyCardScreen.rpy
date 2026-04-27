
# Function and transforms for the random cloud gfx on the corners
init python:
    import random
    def getRandomCornerDeco():
        if renpy.random.randint(0, 100) > 50:
            return "None"
        else:
            return "gui/enemycardcorner" + str(renpy.random.randint(0, 9)) + ".png"
    ttTarget = ""

    def getMonsterToolTip(mon):
        monsterToolTip = mon.name
        if mon.encyclopedia == "_Analyze":
            monsterToolTip += "\n{color=#F7B}Arousal: " + str(mon.stats.hp) + "/" + str(mon.stats.max_true_hp) + "{/color}      {color=#7DF}Energy: " + str(mon.stats.ep) + "/" + str(mon.stats.max_true_ep) + "{/color}      Spirit: " + str(mon.stats.sp) + "/" + str(mon.stats.max_true_sp) + "\n"
            monsterToolTip += "Pow: " + str(mon.stats.Power) + "   "
            monsterToolTip += "Tec: " + str(mon.stats.Tech) + "   "
            monsterToolTip += "Int: " + str(mon.stats.Int) + "   "
            monsterToolTip += "Allu: " + str(mon.stats.Allure) + "   "
            monsterToolTip += "Will: " + str(mon.stats.Willpower) + "   "
            monsterToolTip += "Luc: " + str(mon.stats.Luck) + "\n\n"



            WeakArray = []
            for fetishE in mon.FetishList:
                if fetishE.Level >= 1:
                    WeakArray.append(fetishE.name)
            if  len(WeakArray) > 0:
                ri = 0
                monsterToolTip += "Fetishes: "
                for each in WeakArray:
                    monsterToolTip += each
                    if ri + 1 < len(WeakArray):
                        monsterToolTip += ", "
                    else:
                        monsterToolTip += ".\n"
                    ri += 1

            monsterToolTip += "{u}{i}Sensitive{/i}:{/u} "

            resArray = ["Sex", "Ass", "Breasts", "Mouth", "Seduction", "Magic", "Pain", "Holy"]
            WeakArray = []
            StrongArray = []
            for res in resArray:
                if mon.BodySensitivity.getRes(res) >= 125:
                    WeakArray.append(res)
                elif mon.BodySensitivity.getRes(res) <= 75:
                    StrongArray.append(res)

            if  len(WeakArray) > 0:
                ri = 0
                for each in WeakArray:
                    monsterToolTip += each
                    if ri + 1 < len(WeakArray):
                        monsterToolTip += ", "
                    else:
                        monsterToolTip += ".     "
                    ri += 1
            else:
                monsterToolTip += "None.     "

            monsterToolTip += "{u}{i}Insensitive{/i}:{/u} "
            if  len(StrongArray) > 0:
                ri = 0
                for each in StrongArray:
                    monsterToolTip += each
                    if ri + 1 < len(StrongArray):
                        monsterToolTip += ", "
                    else:
                        monsterToolTip += ".\n"
                    ri += 1
            else:
                monsterToolTip += "None.\n"


            monsterToolTip += "{i}{u}Status Vuln{/i}:{/u} "

            effectResArray = ["Stun", "Charm", "Aphrodisiac", "Restraints", "Sleep", "Trance", "Paralysis", "Debuff"]
            WeakArray = []
            StrongArray = []
            immuneArray = []
            for res in effectResArray:
                if mon.resistancesStatusEffects.getRes(res) < 0:
                    WeakArray.append(res)
                elif mon.resistancesStatusEffects.getRes(res) >= 150:
                    immuneArray.append(res)
                elif mon.resistancesStatusEffects.getRes(res) > 0:
                    StrongArray.append(res)
            if  len(WeakArray) > 0:
                ri = 0
                for each in WeakArray:
                    monsterToolTip += each
                    if ri + 1 < len(WeakArray):
                        monsterToolTip += ", "
                    else:
                        monsterToolTip += ".     "
                    ri += 1
            else:
                monsterToolTip += "None.     "
            monsterToolTip += "{u}{i}Status Res{/i}:{/u} "
            resDoubleChek=0
            if  len(StrongArray) > 0:
                ri = 0
                for each in StrongArray:
                    if mon.resistancesStatusEffects.getRes(each) < 150:
                        resDoubleChek=1
                        monsterToolTip += each
                        if ri + 1 < len(StrongArray):
                            monsterToolTip += ", "
                        else:
                            monsterToolTip += ".\n"
                    ri += 1
                if resDoubleChek == 0:
                    monsterToolTip += "None.\n"
            else:
                monsterToolTip += "None.\n"
            monsterToolTip += "{u}{i}Status Immune{/i}:{/u} "
            resDoubleChek=0
            if  len(immuneArray) > 0:
                ri = 0
                for each in immuneArray:
                    if mon.resistancesStatusEffects.getRes(each) >= 150:
                        resDoubleChek=1
                        monsterToolTip += each
                        if ri + 1 < len(immuneArray):
                            monsterToolTip += ", "
                        else:
                            monsterToolTip += ".\n"
                    ri += 1
                if resDoubleChek == 0:
                    monsterToolTip += "None.\n"
            else:
                monsterToolTip += "None.\n"

        return monsterToolTip

transform CardTopLeft:
    ypos -50
    xpos -50

transform CardBottomLeft:
    xpos -50
    yalign 1.0
    ypos 450
    yzoom -1.0

transform CardTopRight:
    ypos -50
    xalign 1.0
    xpos 330
    xzoom -1.0

transform CardBottomRight:
    xalign 1.0
    xpos 330
    yalign 1.0
    ypos 450
    zoom -1.0



# Unified screen for any NPC (both dialogue and combat use this)
screen NPCCard(name, description, mC, seed=None):

    python:
        if seed is None:
            renpy.random.seed(name + str(mC))
        else:
            renpy.random.seed(str(seed) + str(mC))

    default topLeft = getRandomCornerDeco()
    default topRight = getRandomCornerDeco()
    default bottomLeft = getRandomCornerDeco()
    default bottomRight = getRandomCornerDeco()

    if persistent.showCardBubbles == True:
        # Display cloud gfx
        if topLeft != "None":
            add topLeft at CardTopLeft
        if topRight != "None":
            add topRight at CardTopRight
        if bottomLeft != "None":
            add bottomLeft at CardBottomLeft
        if bottomRight != "None":
            add bottomRight at CardBottomRight

    # Backdrop img
    add "gui/enemycard.png" xalign 0.5 ypos 0

    # NPC name at top
    fixed:
        xsize 324
        xalign 0.5
        ypos 2
        use ON_TextButtonBackgroundNoClouds(name)

    # Scrollbox with description text
    fixed:
        xalign 0.5
        ypos 95
        xsize 330
        ysize 350
        viewport:
            #scrollbars "vertical"
            mousewheel True
            draggable True
            side_yfill True
            scrollbars "vertical"
            if not renpy.variant("touch"):
                vscrollbar_xoffset 2
            vbox:
                xalign 0.5
                text description size 23





# EnemyCard for combat - uses NPCCard
screen EnemyCard(mC, mon, xMonPos,yMonpos):
    $ picCheck = 0
    python:
        try:
            if mon.ImageSets[mon.currentSet].ImageSet[0].name != "" and  mon.ImageSets[mon.currentSet].ImageSet[0].name != "None":
                picCheck = 1
        except:
            pass

    if picCheck == 0 or persistent.showCharacterImages == False:

        fixed:
            xalign 0.5 +xMonPos*1.25
            #xpos
            yalign yMonpos + 0.34
            xsize 378
            ysize 540

            use NPCCard(mon.name, mon.description, mC)



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
                        $ layers.overlayOn = 1
            if layers.TheBody == 1:
                $ bodyX = layers.setXalign
                $ bodyY = layers.setYalign
        #fixed:
            #xalign 0.5
            #yalign yMonpos

            #ypos bodyY
            #xpos bodyX + xMonPos

        $ monsterToolTip = getMonsterToolTip(mon)

        if target == -1 and RoledCGOn == 0:
            imagebutton:
                hovered SetVariable("ttCombat", monsterToolTip)
                unhovered SetVariable("ttCombat", "")
                idle "blankButton.png"
                hover "blankButton.png"
                insensitive "blankButton.png"
                xalign 0.5
                yalign -0.3
                xsize 235
                ysize 300
                if MenuLineSceneCheckMark == -1 and inTownMenu == 0 and npcCount == 0  and senCount == 0 and fetCount == 0:
                    action SetVariable("ttCombat", ""), renpy.curry(renpy.end_interaction)(True)
                else:
                    action SetVariable("ttCombat", "")
                at characterPlacement(yMonpos, bodyY, bodyX, 0, xMonPos)
                #yalign mon.pictures[mon.currentPicture].setYalign
                #at CharacterZoom
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

                $ transformsList = [characterPlacement(yMonpos, bodyY, bodyX, 0, xMonPos)]

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
                    if len(transformsList) == 1 and layers.player in ["Yes", "Hair"]:
                        idle imageShown
                        hover imageShown
                        insensitive imageShown
                    else:
                        idle imageShown
                        hover imageShown
                        insensitive imageShown
                    if layers.TheBody == 0:
                        xalign 0.5 + layers.setXalign
                        ypos layers.setYalign
                    else:
                        xalign 0.5
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

screen EnemyCardCG(mC, mon, xMonPos,yMonpos):
    $ picCheck = 0
    python:
        try:
            if mon.ImageSets[mon.currentSet].ImageSet[0].name != "" and  mon.ImageSets[mon.currentSet].ImageSet[0].name != "None":
                picCheck = 1
        except:
            pass

    if picCheck == 1 and persistent.showCharacterImages == True:
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
                            if len(transformsList) == 1 and layers.player == "Yes":
                                idle imageShown
                                hover imageShown
                                insensitive imageShown
                            else:
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

screen EnemyCardUI(mC, mon, xMonPos,yMonpos):
    if _windows_hidden == False:
        fixed:
            #xalign 0.5
            yalign 0.16
            ypos 160
            xpos xMonPos
            fixed:
                xalign 0.5
                xsize 500
                ysize 1100

                $ layerY = 0
                if ((mC == 1 or mC == 2) and len(monsterEncounter) > 10):
                    $ layerY += yMonpos*1.15
                if mC > 8 and len(monsterEncounter) > 10:
                    $ layerY = yMonpos*1.15
                elif mC > 6 and len(monsterEncounter) <= 10:
                    $ layerY = yMonpos*1.15
                elif (mC > 4 and len(monsterEncounter) > 10):
                    $ layerY = yMonpos*0.4
                elif (mC > 2 and len(monsterEncounter) <= 10):
                    $ layerY = yMonpos*0.4

                if targeting == 1 and stanceBreaking == 0:
                    $ canUse = skillIsUsableForTarget(combatChoice, mon)
                    $ monsterToolTip = getMonsterToolTip(mon)
                    fixed: ##istargeting
                        xalign 0.5
                        yalign 0.605 + layerY
                        xsize 324
                        ysize 81
                        use ON_TextButton(text="Target", action=[SensitiveIf(canUse), SetVariable ("target", mC), Jump("combatEnemies")], hovered=[SetVariable("ttTarget", monsterToolTip)], unhovered=[SetVariable("ttTarget", "")])
                else:
                    if mon.combatStance[0].Stance != "None":
                        use stanceList(mon, 0.605+ layerY, mC)
                use CardDamageNumberDisplay(mon, 0.450+layerY)
                $ layerYmul = 1
                if mC > 8 and len(monsterEncounter) > 10:
                    $ layerYmul = 0.75
                elif mC > 6 and len(monsterEncounter) <= 10:
                    $ layerYmul = 0.75

                use StatusBar(mon, yalign=0.550+ layerY*layerYmul)

screen EnemyCardUIOverride(mC, mon, xMonPos, yMonpos):
    if _windows_hidden == False:
        fixed:
            xalign xMonPos #modifiable X
            yalign yMonpos #modifiable Y
            xsize 1
            ysize 1
            $ layerY = 0
            $ monsterToolTip = getMonsterToolTip(mon)
            if target == -1:
                imagebutton:
                    hovered SetVariable("ttCombat", monsterToolTip)
                    unhovered SetVariable("ttCombat", "")
                    idle "blankButton.png"
                    hover "blankButton.png"
                    insensitive "blankButton.png"
                    xalign 0.5
                    yalign 0.5
                    xsize 235
                    ysize 300
                    action SetVariable("ttCombat", ""), renpy.curry(renpy.end_interaction)(True)

                    #yalign mon.pictures[mon.currentPicture].setYalign
                    #at CharacterZoom

            if targeting == 1 and stanceBreaking == 0:
                $ canUse = skillIsUsableForTarget(combatChoice, mon)
                fixed: ##istargeting
                    xalign 0.5
                    yalign 0.5
                    xsize 324
                    ysize 81
                    use ON_TextButton(text="Target", action=[SensitiveIf(canUse), SetVariable ("target", mC), Jump("combatEnemies")], hovered=[SetVariable("ttTarget", monsterToolTip)], unhovered=[SetVariable("ttTarget", "")])
            else:
                if mon.combatStance[0].Stance != "None":
                    use stanceList(mon, 0.5, mC)
            
        fixed:
            xalign xMonPos #modifiable X
            yalign yMonpos+0.05 #modifiable Y
            xsize 1
            ysize 1
            use StatusBar(mon, yalign=0.65)
        fixed:
            xalign xMonPos #modifiable X
            yalign yMonpos+0.075 #modifiable Y
            xsize 1
            ysize 1
            use CardDamageNumberDisplay(mon, 0.45)
            

screen EnemyCardUICG(mC, mon, xMonPos, yMonpos):
    $ yMonpos = 0.81
    if mC > 2:
        $ yMonpos = 0.88
    if mC > 4:
        $ yMonpos = 0.95
    $ xMonpos = 0.3
    if (mC % 2 == 0):
        $ xMonpos = 0.7

    if mC > 6:
        $ xMonpos = 0.5
        $ yMonpos = 0.91
    if mC > 7:
        $ xMonpos = 0.5
        $ yMonpos = 0.98

    if _windows_hidden == False:
        fixed:
            xalign xMonpos #modifiable X
            yalign yMonpos #modifiable Y
            xsize 1
            ysize 1
            $ monsterToolTip = getMonsterToolTip(mon)

            if targeting == 1 and stanceBreaking == 0:
                $ canUse = skillIsUsableForTarget(combatChoice, mon)
                fixed: ##istargeting
                    xalign 0.5
                    yalign 0.5
                    xsize 324
                    ysize 81
                    use ON_TextButton(text="Target", action=[SensitiveIf(canUse), SetVariable ("target", mC), Jump("combatEnemies")], hovered=[SetVariable("ttTarget", monsterToolTip)], unhovered=[SetVariable("ttTarget", "")])
            else:
                if mon.combatStance[0].Stance != "None":
                    use stanceList(mon, 0.5, mC)

            use StatusBar(mon, yalign=1.2)
            use CardDamageNumberDisplay(mon, 0.4)


# Damage number display!!!
screen CardDamageNumberDisplay(char, yalign, menuCall=0):
    zorder 201
     
    if attacker.species == "Player" and char.name == defender.name and (finalDamage > 0 or statusEffectiveText):
        $ positioningOfText = 0
        if effectiveText == "Weakspot" or effectiveText == "Frigid": 
            $ positioningOfText += 1
        if critText != "":
            $ positioningOfText += 1
        if statusEffectiveText != "":
            $ positioningOfText += 1
        $ lastMonDamage = finalDamage
        $ lastMonDamageCrit = critText
        $ lastMonDamageWeak = effectiveText
        $ lastMonStatusRes = statusEffectiveText
        use CardDamageNumberDisplayActual(yalign, finalDamage, critText, effectiveText, statusEffectiveText, "in")           
    else:
        use CardDamageNumberDisplayActual(yalign, lastMonDamage, lastMonDamageCrit, lastMonDamageWeak, lastMonStatusRes, "out")

    if recoilHit > 0 and attacker.species != "Player" and char.name == attacker.name: 
        $ lastMonRecoil = recoilHit
        use CardDamageNumberDisplayActual(yalign, recoilHit, "", "", "", "in")   
    else:  
        use CardDamageNumberDisplayActual(yalign, lastMonRecoil, "", "", "", "out")      

transform damageTextIn():
    xanchor 0.5
    yanchor 0.5
    #rotate 180
    yoffset 30
    alpha 0.1
    easein 0.4 alpha 0.85 yoffset 0 #rotate 360
    
transform damageTextOut():
    xanchor 0.5
    yanchor 0.5
    #rotate 360 
    yoffset 0
    alpha 0.85
    easein 0.4 yoffset -30 alpha 0.0 #rotate 180

transform damageTextInCrit():
    xanchor 0.5
    yanchor 0.5
    #rotate 180
    yoffset 30
    alpha 0.1
    easein 0.39 alpha 0.85 yoffset 0 #rotate 360
    linear 0.01 xoffset -10 yoffset 10 
    linear 0.01 xoffset 10 yoffset -10 
    linear 0.01 xoffset 10 yoffset 10
    linear 0.01 xoffset -10 yoffset -10
    linear 0.01 xoffset -10 yoffset 10
    linear 0.01 xoffset 10 yoffset -10 
    linear 0.01 xoffset 10 yoffset 10
    linear 0.01 xoffset -10 yoffset -10
    linear 0.01 xoffset 0 yoffset 0
 
        
screen CardDamageNumberDisplayActual(yalign, damage, crit, weakspot, statusEffectiveness, inout, player=-1, xOffset=0) :
    if damage != 0 or statusEffectiveness != "":
        if len(str(damage)) >=4:
                $ xOffset -= 15
        frame: 
            #background Solid("#3F0056") 
            
            yminimum 50
            if inout == "in":
                if crit != "":
                    at damageTextInCrit
                else:
                    at damageTextIn
            else:
                at damageTextOut
               

            
 
            if player == -1:
                xalign 0.5
                yalign yalign 
            elif player == 0:
                xpos xOffset - 330 ypos 53 #- for 1
            elif player == 1:
                xpos xOffset - 350 ypos 53 #- for 2
            elif player == 2:
                xpos xOffset - 370 ypos 53 #- for 3
            elif player == 3:
                xpos xOffset - 390 ypos 53 #- for 3
             
            #xsize 1 ysize 1
            hbox:
                yminimum 50
                if weakspot == "Weakspot":
                    use statusEffectIcon("Weakspot! - A fetish or high sensitivity has been targeted!", charmIcon)
                elif weakspot == "Frigid":
                    use statusEffectIcon("Frigid! - The pleasure is heavily resisted!", damageResIcon)
                if crit != "":
                    use statusEffectIcon("Passionate! - Critical pleasure has been dealt!", critIcon)
                if statusEffectiveness == "Effect Immune!":
                    use statusEffectIcon("Immune to status effect!", statusImmuneIcon)
                elif statusEffectiveness == "Effect Resistant!":
                    use statusEffectIcon("Resistant against status effect!", statusResIcon)
                elif statusEffectiveness == "Effect Weak!":
                    use statusEffectIcon("Weak against status effect!", statusWeakIcon)
                if damage != 0:
                    if inout == "in":
                        text " {i}{color=#ff587d}[damage]{/color}{/i} " size 28 xalign 0.5 yalign 0.5
                    else:
                        text " {noalt}{i}{color=#ff587d}[damage]{/color}{/i}{/noalt} " size 28 xalign 0.5 yalign 0.5
                        #alt ""
     


# StanceList - displayed in each EnemyCard
screen stanceList(mon, yalign, mC):

    # pushing away implemented in combat menu
    #$ canBreakFree = targeting != 0 and stanceBreaking != 0 and mon.combatStance[0].Stance != "None"

    fixed: ##istargeting
        xalign 0.5
        yalign yalign # 0.885 or 0.075
        xsize 324
        ysize 81
        #if canBreakFree:
        #    use ON_TextButton(action=[SetVariable("target", mC), Jump("combatPushAway")])
        fixed: ##istargeting
            xalign 0.5
            yalign 0.98
            xsize 324
            ysize 81
            use ON_TextButtonBackground()
            at combatStanceOpacity

        if mon.combatStance[0].Stance == "None":
            text "":
                xalign 0.5
                yalign 0.5
        else:
            $ stances = ""
            for i, monStance in enumerate(mon.combatStance):

                if i > 0:
                    $ stances += ",  "

                $ stances += monStance.Stance

            text stances:
                xalign 0.5
                yalign 0.5

                if len(mon.combatStance) == 2:
                    size 20
                elif len(mon.combatStance) > 2:
                    size 16



# StatusBar is a wrapper for StatusIcons that just includes an hbox or vbox
# Will automatically use a vbox positioned over the health display if char == player
# Otherwise, will just add an hbox to be positioned in the EnemyCard
screen StatusBar(char, yalign=1.06, menuCall=0):
    zorder 201
    $ statusPerk = 0
    for perk in char.perks:
        $ p = 0
        for x in perk.PerkType:
            if perk.PerkType[p] == "StatusIcon":
                $ statusPerk = 1

    if char.statusEffects.hasStatusEffect() == True or statusPerk == 1 :
        if menuCall==1:
            frame:
                xalign 0.0
                xanchor 0.5
                ycenter 140
                hbox:
                    use StatusIcons(char)
        elif (char == player):
            frame:
                xpos 1372
                xanchor 0.5
                ycenter 784
                hbox:
                    use StatusIcons(char)
        else:
            frame:
                xalign 0.5
                yalign yalign
                hbox:
                    use StatusIcons(char)


screen statusEffectIcon(statusText, Icon):
    imagebutton:
        if renpy.variant("touch"):
            if ttCombat == statusText:
                action [SetVariable("ttCombat", "")]
            else:
                action [SetVariable("ttCombat", statusText), SetVariable("charSticky", statusText)]
        else:
            hovered [SetVariable("ttCombat", statusText), SetVariable("charSticky", statusText)]
            unhovered [SetVariable("ttCombat", ""), SetVariable("charSticky", "")]
            action [SetVariable("ttCombat", statusText), SetVariable("charSticky", statusText)]
        idle Icon
        insensitive Icon
        hover Icon
        at statusIconZoom

screen statusEffectStacked(statusEffectType, theWord, percentage, mathType, upIcon, downIcon):
    $ usedNameBucket = []
    for e, each in enumerate(statusEffectType):
        $ multigo = 0
        for bucket in usedNameBucket:
            if each.skillText == bucket:
                $ multigo = 1

        if each.duration > 0 and multigo == 0:
            $ e2 = 0
            $ potencyTotal = each.potency
            $ durationTotal = str(each.potency) + " potency lasts " + str(each.duration) + " more turns.\n"
            $ durationMax = 0
            for e2, extras in enumerate(statusEffectType):
                if e != e2:
                    if extras.skillText == each.skillText:
                        $ potencyTotal += extras.potency
                        if durationMax < 2:
                            $ durationTotal += str(extras.potency) + " potency lasts " + str(extras.duration) + " more turns.\n"
                        elif durationMax >= 2:
                            $ durationTotal += "..."
                        $ durationMax += 1
            $ usedNameBucket.append(each.skillText)
            $ firstPotencyValue = each.potency * -1 if mathType[0] else each.potency
            $ TotalFirstPotencyValue = potencyTotal * -1 if mathType[1] else potencyTotal
            $ secondPotencyValue = each.potency * -1 if mathType[2] else each.potency
            $ totalSecondPotencyValue = potencyTotal * -1 if mathType[3] else potencyTotal
            if firstPotencyValue > 0: # "{:.2f}".format(getBaseEvade(player, 10, 1))
                if durationMax == 0 :
                    use statusEffectIcon("Source: " + each.skillText + "\nIncreases " + theWord + " by " + "{:.2f}".format(firstPotencyValue) + percentage + "!\nLasts " + str(each.duration) + " more turns.", upIcon)
                else:
                    use statusEffectIcon("Source: " + each.skillText + "\nIncreases " + theWord + " by " + "{:.2f}".format(TotalFirstPotencyValue) + percentage + "!\n" + durationTotal, upIcon)
            else:
                if durationMax == 0:
                    use statusEffectIcon("Source: " + each.skillText + "\nDecreases " + theWord + " by " + "{:.2f}".format(secondPotencyValue) + percentage + "!\nLasts " + str(each.duration) + " more turns.", downIcon)
                else:
                    use statusEffectIcon("Source: " + each.skillText + "\nDecreases " + theWord + " by " + "{:.2f}".format(totalSecondPotencyValue) + percentage + "!\n" + durationTotal, downIcon)


# StatusIcons just adds the whole list of status icons with no positioning/containers. Used by StatusBar
# This is just so we don't have the same massive list multiple places in the code
screen StatusIcons(char):
    if char.statusEffects.defend.duration > 0:
        $ DefendBonus = 0
        python:
            for perk in char.perks:
                p = 0
                while  p < len(perk.PerkType):
                    if perk.PerkType[p] == "DefendPower":
                        DefendBonus += (perk.EffectPower[p])
                    p += 1
        if char.statusEffects.defend.potency == 3:
            use statusEffectIcon("Source: Defending\nLowering arousal taken by " + str(75+DefendBonus) + "%, increases evade stat by 50%, and increase int, will, power, and tech stat checks by +5.\nLasts " + str(char.statusEffects.defend.duration) + " more turns.", defendIcon)
        elif char.statusEffects.defend.potency == 2:
            use statusEffectIcon("Source: Defending\nLowering arousal taken by " + str(50+DefendBonus) + "%, and increases evade stat by 50%, and increase int, will, power, and tech stat checks by +3.\nLasts " + str(char.statusEffects.defend.duration) + " more turns.", defendIcon2)
        elif char.statusEffects.defend.potency == 1:
            use statusEffectIcon("Source: Defending\nLowering arousal taken by " + str(25+DefendBonus) + "%, and increases evade stat by 50%, and increase int, will, power, and tech stat checks by +1.\nLasts " + str(char.statusEffects.defend.duration) + " more turns.", defendIcon3)
    if char.statusEffects.surrender.duration > 0:
        use statusEffectIcon("You gave up and can no longer act!", surrenderIcon)
    if char.statusEffects.charmed.duration > 0:
        if difficulty == "Hard":
            use statusEffectIcon("Charmed! Stops attempts from escaping stances and running, weakens attempts to break restraints, lowers escape and stance removal skills chance of working by 75%, and increases the difficulty of temptation checks by 5!\nLasts " + str(char.statusEffects.charmed.duration) + " more turns.", charmIcon)
        else:
            use statusEffectIcon("Charmed! Stops attempts from escaping stances and running, weakens attempts to break restraints, lowers escape and stance removal skills chance of working by half, and increases the difficulty of temptation checks by 1!\nLasts " + str(char.statusEffects.charmed.duration) + " more turns.", charmIcon)
    if char.statusEffects.restrained.duration > 0:
        use statusEffectIcon("Restrained! Heavily limits usable skills, reduces damage dealt from skills by 50%, using a skill helps to escape at 10% of the amount Struggle does.\nLasts until escaped!", restrainedIcon)
    if char.statusEffects.aphrodisiac.duration > 0:
        use statusEffectIcon("Affected by an aphrodisiac!\nPotency: " + str( int(math.floor(char.statusEffects.aphrodisiac.potency))) + "!\nLasts " + str(char.statusEffects.aphrodisiac.duration) + " more turns.", poisonIcon)
    if char.statusEffects.stunned.duration > 0:
        use statusEffectIcon("Stunned and unable to act!\nLasts " + str(char.statusEffects.stunned.duration) + " more turns.", stunnedIcon)
    if char.statusEffects.sleep.duration > 0:
        if char.species == "Player":
            if char.statusEffects.sleep.potency >= 1 :
                use statusEffectIcon("You're losing " + str(int(math.floor(char.statusEffects.sleep.potency))) + " energy every turn, and will fall asleep at 0 energy.\nLasts " + str(int(math.floor(char.statusEffects.sleep.duration))) + " more turns.\nYou regain 50% of max energy if you fall asleep, but lose 25% of spirit on orgasm if you're sleeping when you cum.", sleepIcon0)
            else:
                use statusEffectIcon("Fast asleep...", sleepIcon3)
        else:
            if char.statusEffects.sleep.potency >= 1 :
                use statusEffectIcon("Is losing " + str(int(math.floor(char.statusEffects.sleep.potency))) + " energy every turn, and will fall asleep at 0 energy.\nLasts " + str(int(math.floor(char.statusEffects.sleep.duration))) + " more turns.\n" + str(char.stats.ep) + "/" + str(char.stats.max_true_ep) +" energy remaining.", sleepIcon0)
            else:
                use statusEffectIcon("Fast asleep...", sleepIcon3)


    if char.statusEffects.trance.duration > 0:
        if char.statusEffects.trance.potency == 1:
            use statusEffectIcon("Drifting into trance...", tranceIcon10)
        elif char.statusEffects.trance.potency == 2:
            use statusEffectIcon("Drifting into trance...", tranceIcon9)
        elif char.statusEffects.trance.potency == 3:
            use statusEffectIcon("Falling into trance...", tranceIcon8)
        elif char.statusEffects.trance.potency == 4:
            use statusEffectIcon("Falling into trance...", tranceIcon7)
        elif char.statusEffects.trance.potency == 5:
            use statusEffectIcon("Falling into trance...", tranceIcon6)
        elif char.statusEffects.trance.potency == 6:
            use statusEffectIcon("Falling into trance...", tranceIcon5)
        elif char.statusEffects.trance.potency == 7:
            use statusEffectIcon("Falling into trance...", tranceIcon4)
        elif char.statusEffects.trance.potency == 8:
            use statusEffectIcon("Falling into deep trance...", tranceIcon3)
        elif char.statusEffects.trance.potency == 9:
            use statusEffectIcon("Falling into deep trance...", tranceIcon2)
        elif char.statusEffects.trance.potency == 10:
            use statusEffectIcon("Falling into deep trance...", tranceIcon1)
        else:
            use statusEffectIcon("Completely entranced, may not be able to act...", tranceIcon0)

    if char.statusEffects.paralysis.duration > 0:
        #$ Paraboost = getParalysisBoost(player)
        $ Paraboost =  int(math.floor(100*GetParalEnergyChange(char)))-100
        $ ParaboostFlat = int(math.floor(GetParalFlatEnergyChange(char)))
        $ initLoss = int(math.floor(char.statusEffects.paralysis.potency*5))
        $ evadeLoss = int(math.floor(char.statusEffects.paralysis.potency*3))

        $ paralDescrip = "Paralysis lowers your initiative and run chance by " + str(initLoss) + ", lowers evasion by " + str(evadeLoss) + ", and increases your energy costs by " + str(Paraboost) +"%, and all actions except Wait by " + str(ParaboostFlat) + " energy!\nEffects continue to increase with every stack. Lasts until removed with items, or dissipates slowly out of combat."

        if char.statusEffects.paralysis.potency == 1:
            use statusEffectIcon(paralDescrip, paralysisIcon1)
        elif char.statusEffects.paralysis.potency == 2:
            use statusEffectIcon(paralDescrip, paralysisIcon2)
        elif char.statusEffects.paralysis.potency == 3:
            use statusEffectIcon(paralDescrip, paralysisIcon3)
        elif char.statusEffects.paralysis.potency == 4:
            use statusEffectIcon(paralDescrip, paralysisIcon4)
        elif char.statusEffects.paralysis.potency == 5:
            use statusEffectIcon(paralDescrip, paralysisIcon5)
        elif char.statusEffects.paralysis.potency == 6:
            use statusEffectIcon(paralDescrip, paralysisIcon6)
        elif char.statusEffects.paralysis.potency == 7:
            use statusEffectIcon(paralDescrip, paralysisIcon7)
        elif char.statusEffects.paralysis.potency == 8:
            use statusEffectIcon(paralDescrip, paralysisIcon8)
        elif char.statusEffects.paralysis.potency == 9:
            use statusEffectIcon(paralDescrip, paralysisIcon9)
        else:
            use statusEffectIcon(paralDescrip, paralysisIcon10)

    use statusEffectStacked(char.statusEffects.tempAtk, "arousal dealt", "%", [0,0,1,1], atkUpIcon, atkDownIcon)
    use statusEffectStacked(char.statusEffects.tempDefence, "arousal taken", "%", [1,1,0,0], defDownIcon, defUpIcon)
    use statusEffectStacked(char.statusEffects.tempPower, "Power", "", [0,0,1,1], powUpIcon, powDownIcon)
    use statusEffectStacked(char.statusEffects.tempTech, "Technique", "", [0,0,1,1], techUpIcon, techDownIcon)
    use statusEffectStacked(char.statusEffects.tempWillpower, "Willpower", "", [0,0,1,1], willUpIcon, willDownIcon)
    use statusEffectStacked(char.statusEffects.tempInt, "Intelligence", "", [0,0,1,1], intUpIcon, intDownIcon)
    use statusEffectStacked(char.statusEffects.tempAllure, "Allure", "", [0,0,1,1], allureUpIcon, allureDownIcon)
    use statusEffectStacked(char.statusEffects.tempLuck, "Luck", "", [0,0,1,1], luckUpIcon, luckDownIcon)
    use statusEffectStacked(char.statusEffects.tempCrit, "crit chance", "%", [0,0,1,1], critIcon, critDownIcon)

    for perk in char.perks:
        $ p = 0
        for x in perk.PerkType:
            if perk.PerkType[p] == "StatusIcon":
                $ timeType = ""
                for y in perk.PerkType:
                    if y == "TimeDuration" or y == "TurnDuration":
                        $ timeType = y
                $ perkDescrip = perkDurationDisplay( perk.description, perk.duration, timeType)
                use statusEffectIcon("Source: " + perk.name + "\n" + perkDescrip, perk.EffectPower[p])

            $ p += 1
