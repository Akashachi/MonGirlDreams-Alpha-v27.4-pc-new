
init python:
    on_shoppingtooltip = ""
    shopSticky = ""
    shopTopRowAlignmentY = 0.25
    shopBottomRowAlignmentY = 0.75
    buying = 1
    ConsumOrEquip = 1
    RuneOrAccessory = 0
    ListOfItems = []
    SkillShopping = 0
    junkLeftoverAmount = 3
    Feedback = ""
    ShoppingItemList = []
    ShoppingSkillList = []

transform invertY:
    yzoom -1.0

label Shopping:
    show screen ON_ShoppingScreen
    #window hide dissolve
    "[shopSticky]"
    #pause
    $ shopSticky = ""

    jump Shopping

label endShopping:
    return


label buyItem:
    #$ ItemNumber -= 1
    $ PriceChange = 0
    python:
        for perk in player.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "BetterPrices":
                    PriceChange += perk.EffectPower[p]
                if buying == 1:
                    if perk.PerkType[p] == "BuyPrices":
                        PriceChange += perk.EffectPower[p]
                else:
                    if perk.PerkType[p] == "SellPrices":
                        PriceChange += perk.EffectPower[p]
                p += 1


    if SkillShopping == 0:
        if buying == 1:
            if player.inventory.money >= (int(math.floor((ShoppingItemList[ItemNumber].cost*amountToBuy))*(1-PriceChange*0.01))):
                $ player.inventory.give(ShoppingItemList[ItemNumber].name, amountToBuy)
                if player.inventory.has_item(ShoppingItemList[ItemNumber]):
                    $ Holding =  getFromName(ShoppingItemList[ItemNumber].name, player.inventory.items)
                    $ Feedback = "You bought a " + ShoppingItemList[ItemNumber].name + ".\nYou have " + str(player.inventory.items[Holding].NumberHeld) + "."
                $ shopSticky = Feedback
                $ player.inventory.earn(int(math.floor((-1*(ShoppingItemList[ItemNumber].cost*amountToBuy))*(1-PriceChange*0.01))))
                if PurchasesToProgress == 1:
                    $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
                    $ ProgressEvent[DataLocation].eventProgress += int(math.floor(((ShoppingItemList[ItemNumber].cost*amountToBuy))*(1-PriceChange*0.01)))
            else:
                $ Feedback = "You don't have enough Eros."
                $ shopSticky = Feedback
        else:
            $ amountOwned = player.inventory.items[ItemNumber].NumberHeld
            $ Feedback  = "You sold a " + player.inventory.items[ItemNumber].name + ".\nYou have " + str(amountOwned-amountToBuy) + " Left."
            $ shopSticky = Feedback
            $ player.inventory.earn(int(math.floor(((player.inventory.items[ItemNumber].cost*amountToBuy)/2)*(1+PriceChange*0.01))))
            $ i = 0
            if player.inventory.items[ItemNumber].NumberHeld - amountToBuy <= 0:
                $ purchasing = 0
            while i <amountToBuy:
                $ player.inventory.useItem(player.inventory.items[ItemNumber].name)
                $ i += 1

            if amountOwned-amountToBuy > 0:
                if amountToBuy > player.inventory.items[ItemNumber].NumberHeld:
                    $ amountToBuy = player.inventory.items[ItemNumber].NumberHeld



    else:
        $ player.learnSkill(ShoppingSkillList[ItemNumber])
        $ Feedback = "You learned " + ShoppingSkillList[ItemNumber].name + "!"
        $ shopSticky = Feedback
        $ player.inventory.earn(int(math.floor((-1*(ShoppingSkillList[ItemNumber].learningCost*amountToBuy))*(1-PriceChange*0.01))))
        if PurchasesToProgress == 1:
            $ DataLocation = getFromName(ProgressEvent[DataLocation].name, ProgressEvent)
            $ ProgressEvent[DataLocation].eventProgress += int(math.floor(((ShoppingSkillList[ItemNumber].cost*amountToBuy))*(1-PriceChange*0.01)))
    $ purchasing = 0
    $ amountToBuy = 0
    #hide screen ON_ShoppingScreen
    jump Shopping


label sellExcess:
    #$ ItemNumber -= 1
    $ PriceChange = 0
    python:
        for perk in player.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "BetterPrices":
                    PriceChange += perk.EffectPower[p]
                if buying == 1:
                    if perk.PerkType[p] == "BuyPrices":
                        PriceChange += perk.EffectPower[p]
                else:
                    if perk.PerkType[p] == "SellPrices":
                        PriceChange += perk.EffectPower[p]
                p += 1

    $ totalEros = 0
    $ p = 0

    while p < len(player.inventory.items):
        if player.inventory.items[p].itemType == "Rune":
            $ NumberFullyHeld = 0
            if player.inventory.RuneSlotOne.name == player.inventory.items[p].name:
                $ NumberFullyHeld += 1
            if player.inventory.RuneSlotTwo.name == player.inventory.items[p].name:
                $ NumberFullyHeld += 1
            if player.inventory.RuneSlotThree.name == player.inventory.items[p].name:
                $ NumberFullyHeld += 1
            if (player.inventory.items[p].NumberHeld + NumberFullyHeld) > 3:
                $ totalEros += int(math.floor(((player.inventory.items[p].cost)/2)*(1+PriceChange*0.01)))
                $ player.inventory.useItem(player.inventory.items[p].name)
                $ p-=1
        elif player.inventory.items[p].itemType == "Accessory":
            $ NumberFullyHeld = 0
            if player.inventory.AccessorySlot.name == player.inventory.items[p].name:
                $ NumberFullyHeld += 1
            if (player.inventory.items[p].NumberHeld + NumberFullyHeld) > 1:
                $ totalEros += int(math.floor(((player.inventory.items[p].cost)/2)*(1+PriceChange*0.01)))
                $ player.inventory.useItem(player.inventory.items[p].name)
                $ p-=1
        $ p+=1

    $ player.inventory.earn(totalEros)

    $ shopSticky = "You sold your excess items and earned: " + str(totalEros) + " Eros."

    #hide screen ON_ShoppingScreen
    jump Shopping

label sellJunk:
    $ PriceChange = 0
    python:
        for perk in player.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "BetterPrices":
                    PriceChange += perk.EffectPower[p]
                if buying == 1:
                    if perk.PerkType[p] == "BuyPrices":
                        PriceChange += perk.EffectPower[p]
                else:
                    if perk.PerkType[p] == "SellPrices":
                        PriceChange += perk.EffectPower[p]
                p += 1

    $ totalEros = 0
    $ p = 0

    while p < len(player.inventory.items):
        if player.inventory.items[p].itemType == "Loot":
            if player.inventory.items[p].NumberHeld > junkLeftoverAmount:
                $ totalEros += int(math.floor(((player.inventory.items[p].cost)/2)*(1+PriceChange*0.01)))
                $ player.inventory.useItem(player.inventory.items[p].name)
                $ p-=1
        $ p+=1

    $ player.inventory.earn(totalEros)
    $ junkLeftoverAmount = 3
    $ shopSticky = "You sold your junk items and earned: " + str(totalEros) + " Eros."
    #hide screen ON_ShoppingScreen
    jump Shopping

screen confirmJunkSell():
    modal True
    zorder 300
    style_prefix "confirm"
    add "gui/overlay/confirm.png"
    dismiss action Hide("confirmJunkSell")
    frame:
        xminimum 1440
        xmaximum 1440
        yminimum 420
        ymaximum 420

        vbox:
            first_spacing 20
            spacing 50
            yalign 0.1
            xalign 0.5
            label _("While unable to be consumed or equipped, these loot items can be important for side quests, be sure you're okay with that before selling {i}all{/i} of them."):
                style "confirm_prompt"
            vbox:
                xalign 0.5
                label _("Keep excess:")
                hbox:
                    bar value VariableValue("junkLeftoverAmount", 5, step=1):
                        xmaximum 400
                        ymaximum 40
                        style "slider_slider"
                        thumb Solid("#E470B2") xsize 15 ysize 40
                    text " [junkLeftoverAmount] per loot item."
            hbox:
                spacing 300
                xalign 0.5
                use ON_TextButton(text="Sell Junk", action=[Hide("confirmJunkSell"), Jump("sellJunk")])
                use ON_TextButton(text="Cancel", action=Hide("confirmJunkSell"))

# Single shop entry - handles skills, buying, selling
screen ON_ShopSingleItem(item, index):

    # Get adjusted item price and tooltip
    python:
        PriceChange = 0
        ItemToolTip = ""

        # Defeat the Demon Queen through the power of LEWD ARBITRAGE
        for perk in player.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "BetterPrices":
                    PriceChange += perk.EffectPower[p]
                if buying == 1:
                    if perk.PerkType[p] == "BuyPrices":
                        PriceChange += perk.EffectPower[p]
                else:
                    if perk.PerkType[p] == "SellPrices":
                        PriceChange += perk.EffectPower[p]

                p += 1

        # Stick price in a single var so we're not putting if's everywhere
        if buying == 1:
            if SkillShopping == 0:
                itemPrice = int(math.floor(item.cost*(1-PriceChange*0.01)))
            else:
                itemPrice = int(math.floor(item.learningCost*(1-PriceChange*0.01)))
        else:
            itemPrice = int(math.floor((item.cost/2)*(1+PriceChange*0.01)))

        # Build skill tooltip
        if SkillShopping:
            ItemToolTip = item.descrips

            if player.has_skill(item.name) == True:
                ItemToolTip += "\nYou already know this skill."
            else:
                if item.requiredStat > 0:
                    hasEnoughStat = player.stats.getStat(item.statType)-player.getStatBonusReduction(item.statType) >= item.requiredStat
                    ItemToolTip += "\nYou need " + str(item.requiredStat) + " " + item.statType + " to learn this skill. "
                    if hasEnoughStat:
                        ItemToolTip += "You have " + str(player.stats.getStat(item.statType)-player.getStatBonusReduction(item.statType)) + "."
                    else:
                        ItemToolTip += "{color=#f20}You only have " + str(player.stats.getStat(item.statType)-player.getStatBonusReduction(item.statType)) + ".{/color}"

                if item.requiredLevel > 1:
                    hasEnoughLevel = player.stats.lvl >= item.requiredLevel
                    ItemToolTip += "\nYou must be at least level " + str(item.requiredLevel) + " to learn this skill. "
                    if hasEnoughLevel:
                        ItemToolTip += "You are level " + str(player.stats.lvl) + "."
                    else:
                        ItemToolTip += "{color=#f20}You are only level " + str(player.stats.lvl) + ".{/color}"
            
            ItemToolTip = getSkillToolTip(item, player, ItemToolTip)


        # Build item tooltip
        else:

            if item.itemType == "Consumable" or item.itemType == "DissonantConsumable" or item.itemType == "CombatConsumable"  or item.itemType == "CombatConsumable":
                if len(item.skills) > 0:
                    fetchSkill = getFromName(item.skills[0], SkillsDatabase)
                    skillToCheck = copy.deepcopy(SkillsDatabase[fetchSkill])
                    skillToCheck.isSkill = item.itemType
                    ItemToolTip = getSkillToolTip(skillToCheck, player, item.descrips)
                else:
                    ItemToolTip = item.descrips
            else:
                ItemToolTip = item.descrips

            if player.inventory.has_item(item):
                Holding = getFromName(item.name, player.inventory.items)
                ItemToolTip += "\nYou have " + str(player.inventory.items[Holding].NumberHeld) + "."

        # Add cost and can't-afford warning to the tooltip

        #if buying or SkillShopping:
        #    ItemToolTip += "\nPrice: " + str(itemPrice) + " eros."
        #    if player.inventory.money < itemPrice:
        #        ItemToolTip += "{color=#f20} You can't afford it...{/color}"

        # Set buyable for skill or item
        buyable = False
        if SkillShopping == 0:
            if player.inventory.money >= itemPrice or buying == 0:
                buyable = True
            else:
                buyable = False
        else:
            buyable = True
            if player.inventory.money < itemPrice:
                buyable = False

            if player.has_skill(item.name) == True:
                buyable = False

            if item.requiredLevel > player.stats.lvl:
                buyable = False

            if item.requiredStat > player.stats.getStat(item.statType)-player.getStatBonusReduction(item.statType):
                buyable = False

        if SkillShopping:
            itemname = item.name
        elif buying:
            hasThing = 0
            numberheld = 0
            for each in player.inventory.items:
                if each.name == item.name:
                    hasThing = 1
                    numberheld = each.NumberHeld
            if hasThing == 1:
                itemname = item.name + " (" + str(numberheld) + " Owned)"
            else:
                itemname = item.name
        else:
            # Sell screen - show how many you have
            itemname = item.name + " (" + str(player.inventory.items[index].NumberHeld) + ")"


    # Display the actual list entry
    hbox:
        xfill True
        ysize on_listEntryHeight

        if SkillShopping == 0:
            if renpy.variant("touch"):
                button:
                    ysize on_listEntryHeight
                    xfill True
                    action [SetVariable("itemEnergyAmount", item.ep), SetVariable("itemArousalAmount", item.hp), SetVariable("itemSpiritAmount", item.sp), SetVariable("on_shoppingtooltip", ItemToolTip), Jump("Shopping") ]
                    alternate [SensitiveIf(purchasing==0), NullAction(), If(buyable, true=[SetVariable("ItemNumber", index), SetVariable("purchasing", 1), SetVariable ("amountToBuy", 1), SetVariable("on_shoppingtooltip", ItemToolTip) ])]

                    text "  " + itemname:
                        size on_listTextSize ysize on_listEntryHeight
                        idle_color (gui.idle_color if buyable else gui.insensitive_color)
                        hover_color (gui.hover_color if buyable else gui.insensitive_color)
                        insensitive_color gui.insensitive_color

                    text u"ξ " + str(itemPrice) + " " xalign 1.0
            else:
                button:
                    hovered [SetVariable("itemEnergyAmount", item.ep), SetVariable("itemArousalAmount", item.hp), SetVariable("itemSpiritAmount", item.sp), SetVariable("on_shoppingtooltip", ItemToolTip), Jump("Shopping")]
                    unhovered SetVariable("on_shoppingtooltip", "")
                    ysize on_listEntryHeight
                    xfill True
                    action [SensitiveIf(purchasing==0), NullAction(), If(buyable, true=[SetVariable("ItemNumber", index), SetVariable("purchasing", 1), SetVariable ("amountToBuy", 1), SetVariable("on_shoppingtooltip", ItemToolTip) ])]

                    text "  " + itemname:
                        size on_listTextSize ysize on_listEntryHeight
                        idle_color (gui.idle_color if buyable else gui.insensitive_color)
                        hover_color (gui.hover_color if buyable else gui.insensitive_color)
                        insensitive_color gui.insensitive_color

                    text u"ξ " + str(itemPrice) + " " xalign 1.0
        else:
            if renpy.variant("touch"):
                button:
                    ysize on_listEntryHeight
                    xfill True
                    action [SetVariable("on_shoppingtooltip", ItemToolTip), Jump("Shopping") ]
                    alternate [SensitiveIf(purchasing==0), NullAction(), If(buyable, true=[SetVariable("ItemNumber", index), SetVariable ("amountToBuy", 1), Jump("buyItem") ])]

                    text "  " + itemname:
                        size on_listTextSize ysize on_listEntryHeight
                        idle_color (gui.idle_color if buyable else gui.insensitive_color)
                        hover_color (gui.hover_color if buyable else gui.insensitive_color)
                        insensitive_color gui.insensitive_color

                    text u"ξ " + str(itemPrice) + " " xalign 1.0
            else:
                button:
                    hovered [SetVariable("on_shoppingtooltip", ItemToolTip)]
                    unhovered SetVariable("on_shoppingtooltip", "")
                    ysize on_listEntryHeight
                    xfill True
                    action [SensitiveIf(purchasing==0), NullAction(), If(buyable, true=[SetVariable("ItemNumber", index), SetVariable ("amountToBuy", 1), Jump("buyItem") ])]

                    text "  " + itemname:
                        size on_listTextSize ysize on_listEntryHeight
                        idle_color (gui.idle_color if buyable else gui.insensitive_color)
                        hover_color (gui.hover_color if buyable else gui.insensitive_color)
                        insensitive_color gui.insensitive_color

                    text u"ξ " + str(itemPrice) + " " xalign 1.0


# Shopping screen, like character menu and combat menu, uses scrollboxes instead of pagination
screen ON_ShoppingScreen:
    key "keydown_K_RSHIFT" action SetVariable("shifting", 5)
    key "keyup_K_RSHIFT" action SetVariable("shifting", 1)
    key "keydown_K_LSHIFT" action SetVariable("shifting", 5)
    key "keyup_K_LSHIFT" action SetVariable("shifting", 1)
    if len(ShoppingItemList) != 0 or len(ShoppingSkillList) != 0:
        on "show" action [SetVariable ("RuneOrAccessory", 0)]
    zorder 100
    fixed:
        xpos 561
        ypos 52

        vbox:
            # Buying/selling tabs and display for the amount of money you have

            # Item list window
            frame:
                xsize 1275
                ysize 435
                vbox:
                    hbox:
                        ysize 45

                        if SkillShopping == 0:
                            fixed xsize 10 # spacing
                            fixed:
                                xsize 240
                                ysize 45
                                imagebutton:
                                    idle "gui/tab_idle_outline.png"
                                    hover "gui/tab_hover.png"
                                    insensitive "gui/tab_selected.png"
                                    action [SensitiveIf(not buying and purchasing==0), SetVariable ("buying", 1)]
                                text "Buy" xalign 0.5 yalign 0.5
                        if NoSelling==0 and SkillShopping == 0:
                            fixed:
                                xsize 240
                                ysize 45
                                imagebutton:
                                    idle "gui/tab_idle_outline.png"
                                    hover "gui/tab_hover.png"
                                    insensitive "gui/tab_selected.png"
                                    action [SensitiveIf(buying and purchasing==0), SetVariable ("buying", 0)]
                                text "Sell" xalign 0.5 yalign 0.5

                        fixed:
                            xsize 420
                            ysize 45
                            text " Eros: ξ [player.inventory.money]"

                        if buying==0:
                            fixed:
                                xoffset 30
                                yoffset 8
                                xsize 162
                                ysize 36
                                imagebutton:
                                    idle "gui/smallertab_idle_outline.png"
                                    hover "gui/smallertab_hover_outline.png"
                                    insensitive "gui/smallertab_insensitive.png"
                                    hovered SetScreenVariable("on_shoppingtooltip", "Sell all Runes in excess of 3 and all Accessories in excess of 1.")
                                    action [SensitiveIf(player.inventory.HasExcess()==1), Jump("sellExcess")]
                                text "Sell Excess":
                                    xalign 0.5 yalign 0.5 size 22
                            fixed:
                                xoffset 30
                                yoffset 8
                                xsize 162
                                ysize 36
                                imagebutton:
                                    idle "gui/smallertab_idle_outline.png"
                                    hover "gui/smallertab_hover_outline.png"
                                    insensitive "gui/smallertab_insensitive.png"
                                    hovered SetScreenVariable("on_shoppingtooltip", "Sell all junk loot items that can't be used as a consumable or equipment.")
                                    action [SensitiveIf(player.inventory.HasLoot()==True), ToggleScreen("confirmJunkSell")]
                                text "Sell Junk":
                                    xalign 0.5 yalign 0.5 size 22
                    add "gui/framedividerhoriz846.png" xpos -2

                    fixed:
                        xsize 1260

                        # Get item lists
                        if SkillShopping:
                            $ ListOfItems = ShoppingSkillList
                        elif buying:
                            $ ListOfItems = ShoppingItemList
                        else:
                            $ ListOfItems = player.inventory.items

                        # Show big scrollbox of skills
                        if SkillShopping:
                            $ skills = []
                            $ columns = 2
                            for skill in ListOfItems:
                                if not player.has_skill(skill.name):
                                    $ skills.append(skill)

                            use ON_Scrollbox("Skills"):
                                grid columns 1:
                                    xfill True
                                    for c in range(0, columns):
                                        vbox:
                                            xfill True
                                            for i in range(c, len(skills), columns):
                                                use ON_ShopSingleItem(skills[i], getFromName(skills[i].name, ListOfItems))
                                #for index, item in enumerate(ListOfItems):
                                #    if not player.has_skill(item.name):
                                #        use ON_ShopSingleItem(item, index)

                            for c in range(0, columns-1):
                                $ pct = (1.0+c)/columns
                                add Solid("#962870") xsize 3 ysize 330 xalign pct yoffset 15 yalign 0.5

                        # Otherwise, display two scrollboxes for consumables and gear
                        else:
                            fixed:
                                xalign 1.012
                                xsize 627
                                vbox:
                                    hbox:
                                        xalign 1.0
                                        text "Equipment:" size on_listTitleSize xoffset -69 # It's accurate I swear

                                        fixed:
                                            xsize 192
                                            ysize 36
                                            imagebutton:
                                                at invertY
                                                idle "gui/smalltab_idle_outline.png"
                                                hover "gui/smalltab_hover_outline.png"
                                                insensitive "gui/smalltab_selected.png"
                                                action [SensitiveIf(RuneOrAccessory != 0), SetVariable ("RuneOrAccessory", 0)]
                                            text "Runes" xalign 0.5 yalign 0.5 size 22

                                        fixed:
                                            xsize 192
                                            ysize 36
                                            imagebutton:
                                                at invertY
                                                idle "gui/smalltab_idle_outline.png"
                                                hover "gui/smalltab_hover_outline.png"
                                                insensitive "gui/smalltab_selected.png"
                                                action [SensitiveIf(RuneOrAccessory == 0), SetVariable ("RuneOrAccessory", 1)]
                                            text "Accessories" xalign 0.5 yalign 0.5 size 22

                                    use ON_Scrollbox(""):

                                        for index, item in enumerate(ListOfItems):
                                            $ hasReq = 0
                                            $ hasReq = requiresCheck(item.requires, item.requiresEvent, player, ProgressEvent)


                                            if ((hasReq >= len(item.requires) + len(item.requiresEvent) or not buying) and (
                                                    (item.itemType == "Rune" and RuneOrAccessory == 0)
                                                    or (item.itemType == "Accessory" and RuneOrAccessory == 1))):
                                                use ON_ShopSingleItem(item, index)

                            fixed:
                                xsize 8 xalign 0.49541
                                add "gui/framedivider256.png"

                            fixed:
                                xalign 0.0
                                xsize 620
                                use ON_Scrollbox("Consumables:", titleAlign=0.036):
                                    for index, item in enumerate(ListOfItems):
                                        $ hasReq = 0
                                        $ hasReq = requiresCheck(item.requires, item.requiresEvent, player, ProgressEvent)

                                        if (hasReq >= len(item.requires) + len(item.requiresEvent)  or not buying) and (item.itemType == "Consumable" or item.itemType == "DissonantConsumable" or item.itemType == "NotCombatConsumable" or item.itemType == "CombatConsumable" or item.itemType == "Loot"):
                                            use ON_ShopSingleItem(item, index)







            fixed ysize 5 # spacing

            # Display tooltip for items separately to the usual tooltip (which has "You bought..." text)
            frame:
                xsize 1275
                ysize 247
                xpadding 12
                ypadding 10
                text on_shoppingtooltip

    $ PriceChange = 0
    python:
        for perk in player.perks:
            p = 0
            while  p < len(perk.PerkType):
                if perk.PerkType[p] == "BetterPrices":
                    PriceChange += perk.EffectPower[p]
                if buying == 1:
                    if perk.PerkType[p] == "BuyPrices":
                        PriceChange += perk.EffectPower[p]
                else:
                    if perk.PerkType[p] == "SellPrices":
                        PriceChange += perk.EffectPower[p]
                p += 1

    if purchasing == 1:
        $ shopSticky = ""
        if buying == 1:
            $ totalPrice = int(math.floor(((ShoppingItemList[ItemNumber].cost*amountToBuy))*(1-PriceChange*0.01)))
            $ display = "Purchase " + str(amountToBuy) + " " + ShoppingItemList[ItemNumber].name + " for " + str(totalPrice) + " eros?"
        else:
            $ totalPrice = int(math.floor(((player.inventory.items[ItemNumber].cost*amountToBuy)/2)*(1+PriceChange*0.01)))
            $ display = "Sell " + str(amountToBuy) + " " + player.inventory.items[ItemNumber].name + " for " + str(totalPrice) + " eros?"

        frame:
            xpadding theXpadding
            ypadding theYpadding
            xalign 0.5
            yalign 0.35
            xminimum 825
            xmaximum 825
            ymaximum 202
            yminimum 202
            text "[display!i]":
                xalign 0.5
                yalign 0.2
            if renpy.variant("touch"):
                $ xali = 0.87
            else:
                $ xali = 0.75
            if buying == 1:
                textbutton "Buy":
                    xalign xali
                    yalign 0.83
                    action [SelectedIf(False), Jump("buyItem")]
            else:
                textbutton "Sell":
                    xalign xali
                    yalign 0.83
                    action [SelectedIf(False), Jump("buyItem")]
            if renpy.variant("touch"):
                $ xali = 0.10
            else:
                $ xali = 0.25
            textbutton "Cancel":
                xalign xali
                yalign 0.83
                action [SelectedIf(False), SetVariable ("amountToBuy", 1), SetVariable("purchasing", 0)]



            add "gui/circlebutton.png" xalign 0.5 yalign 0.90
            if renpy.variant("touch"):
                imagebutton:
                    idle "gui/Button_dec_idle_Jumbo.png"
                    hover "gui/Button_dec_hover_Jumbo.png"
                    insensitive "gui/Button_dec_insensitive_Jumbo.png"
                    xalign 0.41
                    yalign 0.9
                    action [SensitiveIf(amountToBuy >= 1 + shifting),  SetVariable ("amountToBuy", amountToBuy - 1*shifting)]
                imagebutton:
                    idle "gui/Button_dec_idle_Jumbo5.png"
                    hover "gui/Button_dec_hover_Jumbo5.png"
                    insensitive "gui/Button_dec_insensitive_Jumbo5.png"
                    xalign 0.31
                    yalign 0.9
                    action [SensitiveIf(amountToBuy >= 5 + shifting),  SetVariable ("amountToBuy", amountToBuy - 5*shifting)]

            else:
                imagebutton:
                    idle "gui/Button_dec_idle.png"
                    hover "gui/Button_dec_hover.png"
                    insensitive "gui/Button_dec_insensitive.png"
                    xalign 0.44
                    yalign 0.83
                    action [SensitiveIf(amountToBuy >= 1 + shifting),  SetVariable ("amountToBuy", amountToBuy - 1*shifting)]

            if buying == 1:
                if renpy.variant("touch"):
                    imagebutton:
                        idle "gui/Button_inc_idle_Jumbo.png"
                        hover "gui/Button_inc_hover_Jumbo.png"
                        insensitive "gui/Button_inc_insensitive_Jumbo.png"
                        xalign 0.59
                        yalign 0.9
                        action SetVariable ("amountToBuy", amountToBuy + 1*shifting)
                    imagebutton:
                        idle "gui/Button_inc_idle_Jumbo5.png"
                        hover "gui/Button_inc_hover_Jumbo5.png"
                        insensitive "gui/Button_inc_insensitive_Jumbo5.png"
                        xalign 0.69
                        yalign 0.9
                        action SetVariable ("amountToBuy", amountToBuy + 5*shifting)
                else:
                    imagebutton:
                        idle "gui/Button_inc_idle.png"
                        hover "gui/Button_inc_hover.png"
                        insensitive "gui/Button_inc_insensitive.png"
                        xalign 0.56
                        yalign 0.83
                        action SetVariable ("amountToBuy", amountToBuy + 1*shifting)
            else:
                if renpy.variant("touch"):
                    imagebutton:
                        idle "gui/Button_inc_idle_Jumbo.png"
                        hover "gui/Button_inc_hover_Jumbo.png"
                        insensitive "gui/Button_inc_insensitive_Jumbo.png"
                        xalign 0.59
                        yalign 0.9
                        action [SensitiveIf(amountToBuy+shifting <= player.inventory.items[ItemNumber].NumberHeld), SetVariable ("amountToBuy", amountToBuy + 1*shifting)]
                    imagebutton:
                        idle "gui/Button_inc_idle_Jumbo5.png"
                        hover "gui/Button_inc_hover_Jumbo5.png"
                        insensitive "gui/Button_inc_insensitive_Jumbo5.png"
                        xalign 0.69
                        yalign 0.9
                        action [SensitiveIf(amountToBuy+5*shifting <= player.inventory.items[ItemNumber].NumberHeld), SetVariable ("amountToBuy", amountToBuy + 5*shifting)]

                else:
                    imagebutton:
                        idle "gui/Button_inc_idle.png"
                        hover "gui/Button_inc_hover.png"
                        insensitive "gui/Button_inc_insensitive.png"
                        xalign 0.56
                        yalign 0.83
                        action [SensitiveIf(amountToBuy+shifting <= player.inventory.items[ItemNumber].NumberHeld), SetVariable ("amountToBuy", amountToBuy + 1*shifting)]

            text "[amountToBuy]" xalign 0.5 yalign 0.87

    # Return button
    fixed:
        xpos 1158
        xanchor 0.5
        ypos 720
        xsize 240
        ysize 60
        use ON_TextButton(text="Return", action=[SetVariable("Feedback", ""), SetVariable("shopSticky", ""),Jump("endShopping")])
