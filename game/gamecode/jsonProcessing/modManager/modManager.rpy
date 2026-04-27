rpy python 3

## Mods screen ##########################################################
## Made by Noeru#0001, modified and thwacked in by feltcutemightcleanlater.
##
## Leftover note from Noeru: Once Python 3 releases, it's mayhaps more clean to use https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object (SimpleNamespace)
##
## # 1) Download Zip
## # 2) look for meta.json in zip
## # 3) if not found: error (no error!)
## # 4) if found, display filelist (checkboxes) + install folder (+ update options) + install button
#########################################################################
init:
    default disableMods = True
    default onlyMetaMods = True
init python:
    import os
    import re
    import requests
    import threading
    import ssl
    import zipfile
    import shutil

    # if renpy.android:
    #     from jnius import autoclass
    #     VER = autoclass('android.os.Build$VERSION')
    #     sdk = VER.SDK_INT

    # setup variables

    dlStatus = "Waiting"
    dlPercentage = 0
    dlPercentageText = 0
    dlPercentageStatusText = "0B / 0B"
    dlPercentageActuallyPercentage = True
    url = ""
    warning = ""
    mod_folder = os.path.join(gamedir, os.path.join(os.path.pardir, 'Mods')) + os.path.sep
    if renpy.windows:
        mod_folder = mod_folder.replace("\\", "/")

    thread = ""

    persistent.checkUrl = {
        "dlStatus" : "wait",
        "error" : "",
        "url" : "",
        "size" : 0,
        "fileName" : "",
    }

init 1 python:
    persistent.modView = {}
    persistent.readmePage = "overview"
    persistent.fileAccess = checkModFolderAccess()
    persistent.genModData = False
    mods = retrieveModList()
    persistent.modCount = countModList()
    modNum = str(len(mods))
    zips = retrieveModInstallList()

screen mods():

    if persistent.fileAccess:
        default modScreen = "list"
    else:
        default modScreen = "error"

    tag menu

    use game_menu(_("Mods"), scroll="viewport"):

        text "Ensure the save you're loading is in the town square before updating your mod selection!" color "#FFC62C" size 26

        frame:
            background Color(rgb=(0, 0, 0), alpha=0.0)
            padding (10, 5, 10, 0)
            ymaximum 50
            hbox:
                spacing 1
                if persistent.fileAccess:
                    textbutton _("Manage") + " ([modNum] Installed)" action SetScreenVariable("modScreen", "list") style "tab" text_style "text_tab"
                else:
                    textbutton _("Error") action SetScreenVariable("modScreen", "error") style "tab" text_style "text_tab"
                textbutton _("Help") action SetScreenVariable("modScreen", "readme") style "tab" text_style "text_tab"

            if not modScreen == "readme":
                if persistent.fileAccess:
                    textbutton _("Refresh"):
                        action Function(updateModMetadata, True)
                        xalign 1.0
        if modScreen == "list":
            use modList
        elif modScreen == "error":
            if persistent.fileAccess:
                use modList
            else:
                use modError
        elif modScreen == "readme":
            use modReadme

    if persistent.genModData == True:
        key "game_menu" action Show("confirmModLoad")

screen modError():

    tag modmenu

    on "show" action [SetScreenVariable("modScreen", "error")]

    frame:
        vbox:
            spacing 40
            ymaximum 830
            xfill True
            yfill True
            frame:
                yalign 0.05
                xalign 0.5
                padding (100, 10, 10, 10)
                hbox:
                    spacing 50

                    add "waifububble_Harpy.png"

                    vbox:
                        yalign 0.5
                        text "{b}File Access Error!{/b}"
                        text ""
                        text "Readability / Writability / Executability could not be verified on Folder:" size 24
                        text "{b}" + mod_folder.replace("\\", "/") + "{/b}" size 18
                        if renpy.macintosh:
                            text "The game's mod menu functionality requires the game to be in the {a=https://support.apple.com/guide/mac-help/open-apps-with-launchpad-mh35840/14.0/mac/14.0}Applications{/a} folder on MacOS!" size 24
                            text ""
                        else:
                            text ""
                        textbutton _("Check Again") action Function(checkModFolderAccess, ass=True)

screen modList():

    tag modmenu

    on "show" action [Function(updateModMetadata), SetScreenVariable("modScreen", "list")]
    if renpy.variant("pc"):
        add modDragNDrop
    frame:
        padding (20,20,20,20)
        vbox:
            spacing 20

            hbox:
                spacing 20
                if len(url) > 0:
                    vbox:
                        yalign 0.5
                        textbutton _("Download") action Function(download, url, _update_screens=True) align (0.5, 0.5) text_size 26
                        textbutton _("Edit") action Function(editUrl) align (0.5, 0.5) text_size 26
                        textbutton _("Clear") action Function(clearUrl) align (0.5, 0.5) text_size 26
                else:
                    vbox:
                        yalign 0.5
                        textbutton _("Download from URL") action Function(editUrl) text_size 26
                        text "{b}OR{/b}" size 26 xalign 0.5
                        hbox:
                            text "Drag and drop {b}.zip{/b} " size 26
                            image "gui/dragndrop.png"

                if not thread == "":
                    textbutton _("Cancel") action Function(stopThread, _update_screens=True) yalign 0.5 text_size 26
                
                vbox:
                    xfill True
                    yalign 0.5
                    spacing 5

                    hbox:
                        spacing 2

                        text dlStatus size 26
                        text "." at delayed_blink(0.0, 1.0)
                        text "." at delayed_blink(0.2, 1.0)
                        text "." at delayed_blink(0.4, 1.0)
                        if dlPercentageStatusText != "0B / 0B":
                            text dlPercentageStatusText size 26
                        text warning color "#FFC62C" size 26

                    if dlPercentageActuallyPercentage == True:
                        fixed:
                            xfill True
                            ysize 30
                            bar value AnimatedValue(dlPercentage, 100, 0.5) style "bar" ysize 26
                            text url size 26
    if len(zips) > 0:
        frame:
            top_margin 10
            padding (20, 20, 20, 20)

            vbox:
                spacing 30

                for i, zip in enumerate( zips ):
                    vbox:
                        spacing 10
                        hbox:
                            xfill True
                            text zip["path"][zip["path"].rfind("/")+1:] size 26
                            hbox:
                                xalign 1.0 spacing 10
                                textbutton _("Install") action Function(showZipInstallModal, zips[i]) text_size 26
                                textbutton _("Delete") action Function(displayDeletePrompt, zip["path"][zip["path"].rfind("/")+1:], zip["path"], folder=False) text_size 26

                        hbox:
                            xfill True
                            text zip["path"].replace("\\", "/") size 16
                            text zip["contents"] size 16 xalign 1.0


    frame:
        top_margin 10
        frame:
            background Color(rgb=(0, 0, 0), alpha=0.0)
            padding (100, 10, 10, 10)
            if modNum != "0":
                vbox:
                    spacing 10
                    $ mods = retrieveModList()
                    for i, nextmod in enumerate(mods):
                        python:
                            if mods[i]["name"] not in persistent.modView:
                                persistent.modView[mods[i]["name"]] = mods[i]["view"]
                        frame:
                            background Color(rgb=(0, 0, 0), alpha=0.3)
                            padding (20, 10, 20, 10)
                            right_margin 90
                            vbox:
                                spacing 20
                                hbox:
                                    spacing 40
                                    vbox:
                                        first_spacing 10 spacing 0
                                        ycenter 0.5

                                        add nextmod["image"].replace("\\", "/") size (150,150) xalign 0.5

                                        if "testedFor" in nextmod:
                                            if meta_key_has_dic(nextmod["testedFor"]):
                                                if nextmod["testedFor"]["patch"] != 0:
                                                    $ patchSemVer = chr(ord('a') + nextmod["testedFor"]["patch"] - 1)
                                                else:
                                                    $ patchSemVer = ""
                                                $ combinedSemVer = ".".join(["v" + str(nextmod["testedFor"]["major"]),
                                                str(nextmod["testedFor"]["minor"]) + patchSemVer])
                                                if compare_semver(gameVersion, breakingGameVersion, nextmod["testedFor"]) == "Compatible":
                                                        text "Tested for:" size 16 xalign 0.5
                                                        text str(combinedSemVer) size 16 xalign 0.5
                                                elif compare_semver(gameVersion, breakingGameVersion, nextmod["testedFor"]) == "Breaking":
                                                        text "Tested for:" size 16 xalign 0.5 color "#D10C0C"
                                                        text str(combinedSemVer) size 16 xalign 0.5 color "#D10C0C"
                                                        text "Breaking game update:" size 16 xalign 0.5 color "#D10C0C"
                                                        text "v" + str(breakingVersion) size 16 xalign 0.5 color "#D10C0C"
                                                elif compare_semver(gameVersion, breakingGameVersion, nextmod["testedFor"]) == "DatedSevere":
                                                    text "Tested for:" size 16 xalign 0.5 color "#FFC62C"
                                                    text str(combinedSemVer) size 16 xalign 0.5 color "#FFC62C"
                                                    text "Dated game version:" size 16 xalign 0.5 color "#FFC62C"
                                                    text "v" + str(gameVersionABC) size 16 xalign 0.5 color "#FFC62C"
                                                elif compare_semver(gameVersion, breakingGameVersion, nextmod["testedFor"]) == "DatedMinor":
                                                    text "Tested for:" size 16 xalign 0.5
                                                    text str(combinedSemVer) size 16 xalign 0.5
                                                    text "Dated patch version:" size 16 xalign 0.5
                                                    text "v" + str(gameVersionABC) size 16 xalign 0.5
                                                elif compare_semver(gameVersion, breakingGameVersion, nextmod["testedFor"]) == "CompatibleOlder":
                                                    text "Tested for:" size 16 xalign 0.5
                                                    text str(combinedSemVer) size 16 xalign 0.5
                                                    text "Current game version:" size 16 xalign 0.5
                                                    text "v" + str(gameVersionNoABC) size 16 xalign 0.5
                                            else:
                                                if float(nextmod["testedFor"]) >= breakingVersion:
                                                    text "Tested for:" size 16 xalign 0.5
                                                    text "v" + str(nextmod["testedFor"]) size 16 xalign 0.5
                                                else:
                                                    text "Tested for:" size 16 xalign 0.5 color "#D10C0C"
                                                    text str(nextmod["testedFor"]) size 16 xalign 0.5 color "#D10C0C"
                                                    text "Breaking game update:" size 16 xalign 0.5 color "#D10C0C"
                                                    text "v" + str(breakingVersion) size 16 xalign 0.5 color "#D10C0C"
                                    frame:
                                        ysize 300
                                        xmaximum 700
                                        padding (20, 10, 20, 10)

                                        use ON_Scrollbox(nextmod["name"]):
                                            hbox:
                                                spacing 20

                                                textbutton _("Description") action SetDict(persistent.modView, mods[i]["name"], "desc") text_size 20 style "button"

                                                if "credits" in nextmod:
                                                    textbutton _("Credits") action SetDict(persistent.modView, mods[i]["name"], "credits") text_size 20 style "button"

                                                if "authors" in nextmod:
                                                    textbutton _("Authors") action SetDict(persistent.modView, mods[i]["name"], "authors") text_size 20 style "button"

                                                if "url" in nextmod:
                                                    if "urlLabel" in nextmod:
                                                        textbutton nextmod["urlLabel"] action Function(displayUrlPrompts, mods[i]["url"]) text_size 20 style "button"
                                                    else:
                                                        textbutton _("Website") action Function(displayUrlPrompts, mods[i]["url"]) text_size 20 style "button"

                                            if (persistent.modView[mods[i]["name"]] == "desc"):
                                                vbox:

                                                    if "description" in mods[i]:
                                                        text mods[i]["description"] size 26
                                                    else:
                                                        text "Not possible to determine if the mod works as expected on latest game version. See error below.\n" color "#D10C0C" size 26
                                                        if "error" in nextmod:
                                                            text "Error: " + nextmod["error"] color "#D10C0C" size 20
                                                            if nextmod["error"] == "Mod folder is not correctly extracted! Fix path?":
                                                                textbutton _("Fix Path") action Function(fixPath, nextmod["path"]):
                                                                    text_style "gui_green_text"
                                                                    text_size 26 xalign 0.5
                                                                    
                                            elif (persistent.modView[mods[i]["name"]] == "credits"):
                                                if "credits" in mods[i]:
                                                    $ modCredit = []
                                                    $ modCreditIsString = 0
                                                    for each in mods[i]["credits"]:
                                                        if len(each) != 1:
                                                            $ modCredit.append(each)
                                                        else:
                                                            $ modCreditIsString = 1

                                                    if modCreditIsString == 0:
                                                        for each in modCredit:
                                                            vbox:
                                                                xfill True
                                                                text each size 26 xalign 0.5
                                                    else:
                                                        vbox:
                                                            text mods[i]["credits"] size 26

                                            elif (persistent.modView[mods[i]["name"]] == "authors"):
                                                if "authors" in mods[i]:
                                                    vbox:
                                                        xfill True
                                                        spacing 20
                                                        for author in mods[i]["authors"]:
                                                            text author size 26 xalign 0.5
                                    vbox:
                                        spacing 10

                                        text "Manage"

                                        if isDeactivated(nextmod["path"]):
                                            textbutton _("Activate") action Function(switchStateMod, nextmod["path"], nextmod["name"]) text_size 26
                                        else:
                                            textbutton _("Deactivate") action Function(switchStateMod, nextmod["path"], nextmod["name"]) text_size 26

                                        textbutton _("Delete"):
                                            action Function(displayDeletePrompt, mods[i]["name"], mods[i]["path"])
                                            text_size 26
                                if "tags" in nextmod:
                                    hbox:
                                        spacing 30
                                        for t in nextmod["tags"]:
                                            text t size 20
                                hbox:
                                            xfill True
                                            text nextmod["path"].replace("\\", "/") size 16 yalign 0.5
                                            if "semVersion" in nextmod:
                                                $ modSemVersion = ".".join(str(int(nextmod["semVersion"][key])) for key in ["major", "minor", "patch"])
                                                text "Mod Version: " + modSemVersion size 20 xalign 1.0
                                            elif "version" in nextmod:
                                                text "Mod Version: " + str(nextmod["version"]) size 20 xalign 1.0
            else:
                vbox:
                    spacing 40
                    yminimum 800
                    xfill True
                    frame:
                        background Color(rgb=(0, 0, 0), alpha=0.3)
                        padding (20, 10, 282, 65)
                        vbox:
                            spacing 30
                            hbox:
                                spacing 40
                                vbox:
                                    first_spacing 10 spacing 0
                                    ycenter 0.5
                                    add "waifububble_Mika.png" size (150,150) xalign 0.5
                                frame:
                                    ysize 300
                                    padding (20, 10, 20, 10)
                                    xfill True
                                    xmaximum 700
                                    text "No installed mods found.\nTry using the refresh button on the top right, nya!" size 25 yalign 0.5

screen urlInput():
    modal True

    zorder 300

    style_prefix "confirm"
    tag  urlInput
    add "gui/overlay/confirm.png"

    frame:
        padding (20, 20, 20, 20)
        xmaximum 1000

        vbox:
            first_spacing 0
            spacing 50

            hbox:
                xfill True
                if persistent.checkUrl["dlStatus"] == "ok":
                    text "Press Accept to Confirm URL"
                else:
                    text "Give URL for Download"
                add modDragNDrop
                textbutton "X" text_size 30 xalign 1.0 action ToggleScreen("urlInput") text_style "modbutton"
            hbox:
                if persistent.checkUrl["dlStatus"] == "ok":
                        text "Then you can press 'Download' to begin!" size 20
                else:
                    if renpy.macintosh:
                        text "(⌘+v to paste clipboard)" size 20
                    else:
                        text "(ctrl+v to paste clipboard)" size 20

            hbox:
                spacing 30
                text "Mod URL:"
                frame:
                    padding (2, 2, 2, 2)
                    xfill True
                    if (persistent.checkUrl["dlStatus"] == "wait" or persistent.checkUrl["dlStatus"] == "error") and not renpy.android:
                        input copypaste True exclude " {}[]\\()" size 20 yalign 0.5 xalign 0.01:
                                value DictInputValue(persistent.checkUrl, "url")
                                if ( isUrl( persistent.checkUrl["url"] ) ):
                                    color "#31CA0E"
                                else:
                                    color "#ffffff"
                    else:
                        text persistent.checkUrl["url"] color "#31CA0E" size 20 yalign 0.5

                # if renpy.android:
                #     textbutton _("Paste Clipboard") xalign 1.0 action Function(getClipboard)


            vbox:
                xfill True
                spacing 10

                if persistent.checkUrl["dlStatus"] == "error":
                    hbox:
                        xalign 0.5

                        text persistent.checkUrl["error"] size 22

                if persistent.checkUrl["dlStatus"] == "wait" or persistent.checkUrl["dlStatus"] == "check":
                    hbox:
                        xalign 0.5

                        text "." at delayed_blink(0.0, 1.0) size 40
                        text "." at delayed_blink(0.2, 1.0) size 40
                        text "." at delayed_blink(0.4, 1.0) size 40

                if(persistent.checkUrl["dlStatus"] == "ok"):
                    hbox:
                        xalign 0.5
                        spacing 30

                        text "{b}File Size{/b}" size 20
                        text str(persistent.checkUrl["size"]) size 20

            hbox:
                spacing 50

                textbutton _("Check URL"):
                    if (persistent.checkUrl["dlStatus"] == "wait" or persistent.checkUrl["dlStatus"] == "error") and isUrl( persistent.checkUrl["url"] ):
                        text_style "modbutton"
                        action Function(checkUrl, persistent.checkUrl["url"])

                textbutton _("Accept"):
                    if persistent.checkUrl["dlStatus"] == "ok":
                        text_style "modbutton"
                        action Function(acceptUrl)

                textbutton _("Clear") text_style "modbutton":
                        action Function(clearCheckUrl)

screen zipDetail(zip, modOverride):
    default deleteZipAfterInstall = True

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 300

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:
        padding (20, 20, 20, 20)
        xmaximum 1000

        vbox:
            spacing 30

            hbox:
                xfill True

                hbox:
                    spacing 20

                    if ( zip["name"] != "n/A" ):
                        text zip["name"] size 35
                    else:
                        text zip["path"][zip["path"].rfind("/")+1:] size 35
                    if ( zip["version"] != "n/A" ):
                        text "Version {b}" + str(zip["version"]) + "{/b}" size 20 yalign 0.5

                textbutton "X" text_size 30 xalign 1.0 action ToggleScreen("zipDetail") text_style "modbutton"

            frame:
                padding (10, 10, 10, 10)
                xalign 0.0

                ymaximum 300

                use ON_Scrollbox("Files to Unpack"):

                    vbox:
                        spacing 5
                        for line in getFilteredNamelist(zip["namelist"]):
                            text line size 18

            if ( len(modOverride) > 0 ):
                text "This Mod will replace the following folders: {b}" + ",".join(modOverride) + "{/b}." size 16

            hbox:
                spacing 20

                if deleteZipAfterInstall == False:
                    imagebutton:
                        auto "gui/circlebuttonsmall_%s.png"
                        idle "gui/circlebuttonsmall.png"
                        action ToggleScreenVariable("deleteZipAfterInstall")
                else:
                    imagebutton:
                        auto "gui/circlebuttonsmallchecked_%s.png"
                        idle "gui/circlebuttonsmallchecked.png"
                        action ToggleScreenVariable("deleteZipAfterInstall")

                text "Delete {b}" + zip["path"][zip["path"].rfind("/")+1:] + "{/b} after Install?" size 20 yalign 0.5

            hbox:
                spacing 20

                textbutton "Install" text_style "modbutton" action Function(unzip, zip["path"], zip["namelist"], modOverride, ToggleScreen=True, removeZip=deleteZipAfterInstall)
                textbutton "Cancel" action ToggleScreen("zipDetail") text_style "modbutton"

style modbutton:
    color gui.idle_color
    hover_color gui.hover_color

screen modReadme():

    tag modmenu

    default readmePage = "overview"

    frame:
        vbox:
            frame:
                background Color(rgb=(0, 0, 0), alpha=0.0)
                padding (5, 5, 5, 0)
                hbox:
                    spacing 2
                    textbutton _("Overview") action SetVariable("persistent.readmePage", "overview") style "tab_outline" text_style "text_small_tab"
                    textbutton _("Resources") action SetVariable("persistent.readmePage", "resources") style "tab_outline" text_style "text_small_tab"
                    textbutton _("How To") action SetVariable("persistent.readmePage", "howto") style "tab_outline" text_style "text_small_tab"
            frame:
                style "bottom_frame"
                ysize 3
                xfill True
            frame:
                background Color(rgb=(0, 0, 0), alpha=0.0)
                padding (20, 10, 20, 10)
                vbox:
                    if persistent.readmePage == "overview":
                        use overviewReadme
                    elif persistent.readmePage == "resources":
                        use resourcesReadme
                    elif persistent.readmePage == "howto":
                        use howtoReadme

screen overviewReadme():
    text _("Mods are user-made content, using the same methods Threshold uses for base game content. They can add new skills, characters, items, perks, fetishes, locations, and expand and alter existing base game content.")
    text _("")
    text _("They only utilize the functionality Threshold exposes, making them more resilient to game update breakage, and can be individually disabled if issues occur.")
    text _("")
    text _("The mod manager downloads and installs mods via {b}.zip{/b} files through web links, and ensures valid files are installed to the correct location.")
    text _("")
    text _("The Resources section will detail where to find mods, and how to make mods.")
    text _("The How To section above will give step by step instructions on how to download and install mods.")
    text _("")
    text _("{b}Tips{/b}")
    text _("- You can name saves via the button in the bottom right of the save menu to organize base game saves from modded saves.")
    text _("- It is unlikely a modded save will become unstable, but it could influence the stats of your character in a undesirable way.")
    text _("- If you're experiencing an issue with a mod, first check if the game and mod is fully up to date.")
    text _("- If you want to temporarily stop using a mod, you can disable it in the Installed Mods section by pressing the 'Deactivate' button.")
    text _("- If the mod is still causing issues, you can head to the {a=https://discord.com/invite/Md5n5KJ}MGD Discord{/a} in {i}#modding-help{/i}.")

screen howtoReadme():
    text _("1) {color=#FFC62C}Ensure the save you're loading is in the town square before updating your mod selection!{/color}")
    text _("2) Check the Resources section for links to find mods, or how to make mods.")
    text _("3) Copy the mod link to your clipboard. It must end with the {b}.zip{/b} extension to work.{b}.rar will not work!{/b}")
    if renpy.macintosh:
        text _("4) Paste (⌘+v) the link into the 'Mod URL' box from the 'Download from URL' pop up in Manage.")
    else:
        text _("4) Paste (ctrl+v) the link into the 'Mod URL' box from the 'Download from URL' pop up in Manage.")
    text _("3.5) If the url is not supported, download in browser, then drag and drop the {b}.zip{/b} onto the game window.") 
    text _("5) Once it has finished downloading, press Install in the listed zip in Manage below the download box.")
    text _("6) Review the mods information in the Installed Mods section.")
    text _("7) Leave the mod menu to prompt loading, then start a new game or load a save {color=#FFC62C}in the town square{/color}!")

screen resourcesReadme():
    text _("{b}Finding Mods{/b}")
    text _("See the community-maintained list on the wiki at {a=https://monstergirldreams.miraheze.org/wiki/Category:List_Of_Mods}List of Mods{/a}.")
    text _("You can also find mods on the {a=https://discord.com/invite/Md5n5KJ}MGD Discord{/a} in {i}#mod-posting{/i}.")
    text _("")
    text _("{b}Making Mods{/b}")
    text _("See the online {a=https://thresholdmgd.github.io/ModdingDocsMGD}modding documentation{/a}.")
    if renpy.windows or renpy.linux:
        vbox:
            text _("The game also comes bundled with the documentation for offline viewing.")
            text _("   1) Extract {i}ModdingDocs.zip{/i}, found in the same spot as the game executable.")
            text _("   2) Open {i}ModdingDocs/Homepage.html{/i} located in the extracted folder.")
    elif renpy.macintosh:
        vbox:
            text _("The game comes bundled with the documentation for offline viewing.")
            text _("   1) Right click the MonGirlDreams application, select {i}Show Package Contents{/i}.")
            text _("   2) Extract {i}ModdingDocs.zip{/i}, located {i}Contents/Resources/autorun/{/i}.")
            text _("   3) Open {i}ModdingDocs/Homepage.html{/i} located in the extracted folder.")
    text _("")
    text _("Guides from other modders can be found on the wiki at {a=https://monstergirldreams.miraheze.org/wiki/Category:Modder_Guides}Modder Guides{/a}.")

screen confirmModLoad():
    modal True
    zorder 300
    style_prefix "confirm"
    add "gui/overlay/confirm.png"
    dismiss action Hide("confirmModLoad")

    frame:
        xminimum 1440
        xmaximum 1440
        yminimum 340
        ymaximum 340
        vbox:
            first_spacing 20
            spacing 10
            yalign 0.1
            xalign 0.5
            label _("Changes to list of mods require reloading data. Begin?"):
                style "confirm_prompt"
            vbox:
                style_prefix "check_label"
                xoffset -250
                textbutton _("Deactivate dated mods") action ToggleVariable("disableMods", true_value=True, false_value=False) style "check_button"
                textbutton _("Deactivate mods without meta.json") action ToggleVariable("onlyMetaMods", true_value=True, false_value=False) style "check_button"
        hbox:
            yalign 1.0
            xalign 0.5
            spacing 30
            use ON_TextButton(text="Start", action=Function(startModLoading))
            use ON_TextButton(text="Start + Debug Log", action=[SetVariable("persistent.validatorAtReload", True), Function(startModLoading)])
            use ON_TextButton(text="Cancel", action=Hide("confirmModLoad"))
            # (persistent.modCount, true=Notify("[persistent.modCount] mods loaded."), false=NullAction()), Hide("confirmModLoad"),
    key "game_menu" action Hide("confirmModLoad")
# functions for screens
init python:
    def meta_key_has_dic(thekey):
        dumby = None
        try:
            dumby = thekey["major"]
            return True
        except:
            return False
    def meta_key_is_iterable(obj):
        # TODO: Ren'Py doesn't accept type checking, not even in python funcs.
        # If Ren'Py ever addresses this, we should go further in this direction.
        try:
            iter(obj)
            return True
        except TypeError:
            return False

    def compare_semver(game_version, breaking_version, tested_version):
        if breaking_version[0] > tested_version["major"]:
            return "Breaking"
        elif game_version[0] < tested_version["major"]:
            return "DatedSevere"
        elif game_version[0] > tested_version["major"]:
            return "CompatibleOlder"
        else:
            if breaking_version[1] > tested_version["minor"] and not breaking_version[0] < tested_version["major"]:
                return "Breaking"
            elif game_version[1] < tested_version["minor"]:
                return "DatedSevere"
            elif game_version[1] > tested_version["minor"]:
                return "CompatibleOlder"
            else:
                if game_version[2] < tested_version["patch"]:
                    return "DatedMinor"
                elif game_version[2] >= tested_version["patch"]:
                    return "Compatible"
                else:
                    return "Compatible"

    def checkModFolderAccess(ass=False):
        global mod_folder

        if ass:
            persistent.fileAccess = os.access(mod_folder, os.R_OK | os.W_OK | os.X_OK)
            return
        else:
            return os.access(mod_folder, os.R_OK | os.W_OK | os.X_OK)

    def clearUrl():
        global url

        url = ""

    def clearCheckUrl():
        persistent.checkUrl = {
            "dlStatus" : "wait",
            "error" : "",
            "url" : "",
            "size" : 0,
            "fileName" : "",
        }

    def acceptUrl():
        global url

        url = persistent.checkUrl["url"]
        clearCheckUrl()
        renpy.hide_screen("urlInput")

    def magicCheck(magicBytes):
        if isinstance(magicBytes, str):
            checkMagicBytes = str(magicBytes[0:4])
        else:
            checkMagicBytes = bytes(magicBytes[0:4])
        print(checkMagicBytes)
        zipMagicBytes = [b'\x50\x4B\x03\x04']
        for magicByte in zipMagicBytes:
            if checkMagicBytes.startswith(magicByte):
                return True
        return False

    def checkUrl(url):
        persistent.checkUrl["dlStatus"] = "wait"
        persistent.checkUrl["error"] = ""
        chunkSize = 4
        try:
            req = requests.Session().get(url, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
            if 'Content-Length' in req.headers:
                urlInfo = req.headers['Content-Length']
            else:
                urlInfo = None
            magicInfo = req.raw.read(4)
            if url.startswith("https://mega.nz"):
                raise Exception("Mega links cannot be downloaded by URL. Compatible URLs must end in '.zip'.\n{b}You can still use the mod manager though!{/b}\nDownload in browser, then drag and drop the zip file onto the game window here or back in the Downloads section.")
        except Exception as e:
            # print(e)
            persistent.checkUrl["dlStatus"] = "error"
            persistent.checkUrl["error"] = "Error occured!\n" + str(e).replace("[", "(").replace("]", ")")
            return

        if magicCheck(magicInfo):
            if urlInfo == None:
                size = None
                persistent.checkUrl["size"] = "Zip file size not found."
            else:
                size = int(urlInfo)
                power = 1024
                n = 0
                power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
                while size > power:
                    size /= power
                    n += 1
                persistent.checkUrl["size"] = "~" + str(round(size, 1)) + power_labels[n]+"B"
            persistent.checkUrl["dlStatus"] = "ok"
        else:
            persistent.checkUrl["dlStatus"] = "error"
            persistent.checkUrl["error"] = "Not a {b}zip{/b} file link. Check if opening the link in a browser starts a download of a zip file."
            return


    def isUrl(url):
        return re.match(r"(((https|http):\/\/)|(^|\s))([a-zA-Z0-9\-]+\.)+[a-z]{2,13}[\.\?\=\&\%\/\w\-]*\b([^@]|$)", url)

    def editUrl():
        global url

        if len(url) > 0:
            persistent.checkUrl["url"] = url
        renpy.show_screen("urlInput")

    def showZipInstallModal(zip):
        modOverride = checkOverride(zip["namelist"])
        renpy.show_screen("zipDetail", zip, modOverride)

    def validateAndRenameZip(path):
        global mod_folder

        zF = zipfile.ZipFile(path)
        meta = getMetaJsonInfoFromZip( zF )
        namelist = zF.namelist()
        zF.close()
        # try renaming via meta.json
        if ( meta["name"] != "n/A" ):
            try:
                os.rename(path, os.path.join(mod_folder, meta["name"] + str(meta["version"]) + ".zip") )
            except Exception as e:
                print(e)
        # rename via first-level folder
        else:
            for f in namelist:
                if f[-1] == "/":
                    foldername = f
                    while foldername.count("/") > 0:
                        foldername = f[0:f.find("/")]
                    break
            if len(foldername) > 0:
                try:
                    os.rename( path, os.path.join(mod_folder, foldername + ".zip") )
                except Exception as e:
                    print(os.path.join(mod_folder, foldername + ".zip"))
                    print(e)

    def getFilteredNamelist(namelist):

        allowedFiletypes = ["png", "jpg", "webp", "avif", "opus", "mp3", "ogg", "wav", "txt", "json", "md", ""]

        filterlist = [file for file in namelist if file[file.rfind(".")+1:] in allowedFiletypes] # applying of whitelist

        filterlist = [file for file in filterlist if file.count("/") > 0] # NO first level items (who are not in a folder)

        return filterlist

    # @see getFilteredNamelist(namelist)
    # unzipping + applying whitelist:
    #   .png, .jpg, .webp, .avif,
    #   .opus, .mp3, .ogg, .wav,
    #   .txt, .json, .md
    #   .ttf, .otf
    # might be important to NOT have dots in foldernames!
    def unzip(zipPath, namelist, override, ToggleScreen=False, removeZip=True):
        for folder in override:
            try:
                shutil.rmtree(os.path.join(mod_folder, folder))
            except Exception as e:
                renpy.notify("Not able to override {b}" + folder + "{/b}! Cancelling Mod-Installation!")
                print(e)
                return

        possible_folders = ["Events", "Skills", "Perks", "Locations", "Adventures", "Fetishes", "Items", "Monsters"]
        allowed_filetypes = ["png", "jpg", "webp", "avif", "ttf", "otf", "opus", "mp3", "ogg", "wav", "txt", "json", "md"]
        identified_folder = None

        with zipfile.ZipFile(zipPath, 'r') as zip_ref:
            for item in zip_ref.infolist():
                if any(folder in item.filename for folder in possible_folders):
                    identified_folder = item.filename
                    break
            if identified_folder:
                target_directory = os.path.join(os.path.dirname(identified_folder), os.pardir)
                norm_target_directory = os.path.normpath(target_directory)
                norm_root_directory = os.path.normpath(os.path.join(target_directory, os.pardir))
                if renpy.windows:
                    norm_target_directory = norm_target_directory.replace("\\", "/")
                    norm_root_directory = norm_root_directory.replace("\\", "/")
                for ffile in zip_ref.infolist():
                    if norm_target_directory in ffile.filename:
                        rel_path = os.path.relpath(ffile.filename, norm_root_directory)
                        target_path = os.path.join(mod_folder, rel_path)
                        check_dir = ffile.filename.replace("\\", "/")
                        if renpy.windows:
                            target_path = target_path.replace("\\", "/")
                            check_dir = ffile.filename.replace("\\", "/")
                        if ffile.filename.endswith("/"):
                            if not os.path.exists(target_path):
                                os.makedirs(target_path)
                        elif any(ffile.filename.endswith(filetype) for filetype in allowed_filetypes):
                            with zip_ref.open(ffile) as zip_file, open(target_path, "wb") as target_file:
                                target_file.write(zip_file.read())
                        else: pass
            zip_ref.close()

        if ToggleScreen == True:
            renpy.hide_screen("zipDetail")

        if removeZip == True:
            try:
                os.remove( zipPath )
            except Exception as e:
                print(e)

        renpy.notify("Unpacked " + zipPath[zipPath.rfind("/")+1:] + "!")
        updateModMetadata(True)
        renpy.restart_interaction()

    def fixPath(modPath):
        possible_folders = ["Events", "Skills", "Perks", "Locations", "Adventures", "Fetishes", "Items", "Monsters"]
        
        for root, dirs, files in os.walk(modPath):
            for dir in dirs:
                if dir in possible_folders:
                    shutil.move(root, os.path.dirname(modPath))
                    shutil.rmtree(modPath)
                    break
        
        renpy.notify("Path fixed!")
        updateModMetadata(True)
        renpy.restart_interaction()
    def download(urlp):
        global url, thread
        url = ""
        thread = DownloadThread(urlp)
        thread.start()
        renpy.restart_interaction()

    def stopThread():
        global thread
        try:
            thread.stop()
        except Exception as e:
            print(e)

    def displayDeletePrompt(name, path, folder=True):
        if folder:
            layout.yesno_screen("{size=25}Delete {b}"+name+"{/b}?{/size}", yes=Function(removeMod, path, name), no=None)
        else:
            layout.yesno_screen("{size=25}Delete {b}"+name+"{/b}?{/size}", yes=Function(removeZip, path, name), no=None)

    # Opens URL with prompt
    def displayUrlPrompts(url):
        layout.yesno_screen("You're about to visit\n{b}{size=20}"+url+"{/size}{/b}\nContinue?", yes=OpenURL(url), no=None)

    # reads out the FIRST meta.json that's found in the zip and returns its contents as a dict
    def getMetaJsonInfoFromZip(zip):
        metaObj = {
            "name" : "n/A",
            "version" : "n/A",
            "testedFor" : "n/A",
        }

        for file in zip.namelist():
            if ( file[file.rfind("/")+1:] == "meta.json" ):
                try:
                    f = zip.open(file)
                    data = f.read()
                    metaObj.update(json_loads(data))
                    f.close()
                except Exception as e:
                    print(e)
            elif ( file[file.rfind("/")+1:] == "Meta.json" ):
                try:
                    f = zip.open(file)
                    data = f.read()
                    metaObj.update(json_loads( data))
                    f.close()
                except Exception as e:
                    print(e)

        return metaObj

    # returns a String containing the following format
    #
    # ( countOfFileType fileType | -iteration- .. )
    #
    # infolist - from ZipFile
    def createPreformattedContentsString(infolist):
        returnS = "( "
        typeCount = {}

        for file in infolist:
            # folder
            if( file.filename[-1] == "/" ):
                if("folder" in typeCount):
                    typeCount["folder"] += 1
                else:
                    typeCount["folder"] = 1
            # everything else
            else:
                type = file.filename[file.filename.rfind(".")+1:]
                if(type in typeCount):
                    typeCount[type] += 1
                else:
                    typeCount[type] = 1

        for type in typeCount:
            returnS += "{b}" + str(typeCount[type]) + "{/b} " + type + " I "

        return returnS[:-3] + " )"

    # returns list of folder that will be overriden if zip is unpacked
    def checkOverride(namelist):
        override = []

        for file in namelist:
            if ( file.count("/") > 1 ):
                foldername = file[:file.find("/")]
                #print(foldername)
                if( os.path.exists( os.path.join( mod_folder, foldername ) ) ):
                    if( foldername not in override ):
                        override.append(foldername)
                elif ( os.path.exists( os.path.join( mod_folder, "_" + foldername ) ) ):
                    if( "_" + foldername not in override ):
                        override.append("_" + foldername)
                elif ( os.path.exists( os.path.join( mod_folder, foldername[1:] ) ) ):
                    if( foldername[1:] not in override ):
                        override.append(foldername[1:])

        return override

    # Extracts information from a zipfile and returns dict
    #
    # zipfile
    #
    #       string : ["path"]           - path to zipfile on disk
    #       string : ["contents"]       - pre-formatted string to display file-counts by type of the zip + file-size
    #
    #       # Those props are provided by ZipFile python functions
    #       array  : ["infolist"]       - contains detailed information about each file inside of zip
    #       array  : ["namelist"]       - contains zip-path to files, used to determine what to extract later
    #
    #       # Those props are generated via file checks
    #       array  : ["override"]       - if there's a folder with the same name in mods as a folder in the zip, it'll indicate so
    #
    #       # The following props are extracted from the meta.json inside the zip, if possible
    #       string : ["name"]           - name of mod
    #       float  : ["version"]        - version of mod
    #       dict   : ["semVersion"]     - semantic version of mod, using "major", "minor", and "patch" keys with int values.
    #       dict   : ["testedFor"]      - tested for which game version using semantic versioning: "major", "minor", and "patch" keys with int values.
    #       (+) all other information from the meta.json if available
    def extractZipInformation(path):
        zipObj = zipfile.ZipFile(path)

        zip = {
            "path" : path,
            "contents" : createPreformattedContentsString(zipObj.infolist()),
            "infolist" : zipObj.infolist(),
            "namelist" : zipObj.namelist(),
        }

        meta = getMetaJsonInfoFromZip(zipObj)

        zip.update( meta )

        zipObj.close()

        return zip

    # Goes through the /Mods folder and returns a list of installable mods
    def retrieveModInstallList():
        zips = []

        zipPaths = [os.path.join(mod_folder, o) for o in os.listdir(mod_folder) if o[o.rfind(".")+1:] == "zip"] # only .zip files

        for path in zipPaths:
            try:
                zips.append( extractZipInformation(path) )
            except Exception as e:
                print(e)

        return zips

    # Goes through the /Mods folder and returns a list of mod dicts:
    #
    #   mod     * = required      ° = set by script
    #
    #       string : ["name"]*          - name of the mod
    #       string : ["description"]*   - description
    #       dict   : ["testedFor"]*     - tested for which game version using semantic versioning: "major", "minor", and "patch" keys with int values.
    #       array  : ["authors"]*       - array of authors
    #
    #       string : ["urlLabel"]       - Website | Wiki | etc.
    #       string : ["url"]            - url to authors website / github etc.
    #       array  : ["tags"]           - array of relevant mod tags
    #       string : ["credits"]        - crediting notable people / other things
    #       float  : ["version"]        - version of the mod
    #
    #       string : ["path"]°          - path to modfolder on disk
    #       string : ["image"]°         - path to mod-image or placeholder-image
    #       string : ["name"]°          - if json isn't found, name will be set as the foldername
    #       string : ["view"]°          - the initial view for the information text field (desc, credits, ?)
    #       string : ["error"]°         - helper error to indicate if the json file is containing errors syntax-wise
    #
    # checks for if modfolder/meta.json exists - if yes, populates mod object with metadata
    # checks for if modfolder/icon.png - if yes & height = width, display it on left side of metadata ; if no, display placeholder img
    def countModList(genericCount=False):
        global modCount
        persistent.modCount = 0

        modfolders = [os.path.join(mod_folder, o) for o in os.listdir(mod_folder) if os.path.isdir(os.path.join(mod_folder, o))]
        if renpy.windows:
            modfolders = [os.path.join(mod_folder, o).replace("\\", "/") for o in os.listdir(mod_folder) if os.path.isdir(os.path.join(mod_folder, o))]

        for folder in modfolders:

            if folder[folder.rfind("/")+1:].startswith("_"):
                pass
            else:
                persistent.modCount += 1
        if genericCount == True:
            genericCount = persistent.modCount
            return genericCount

    def retrieveModList():

        modObjs = []

        modfolders = [os.path.join(mod_folder, o) for o in os.listdir(mod_folder) if os.path.isdir(os.path.join(mod_folder, o))]

        placeholder_path = "images/waifububble_mimic.png"

        for folder in modfolders:

            modObj = {
                "path" : folder,
                "image" : placeholder_path,
                "view" : "desc",
            }
            imgPath = retrieveIcon(folder)
            if (renpy.loadable(imgPath)):
                modObj["image"] = imgPath
            else:
                pass

            jsonPath = folder + "/meta.json"
            jsonPathAlt = folder + "/Meta.json"
            if (os.path.exists(jsonPath)):
                try:
                    fp = open(jsonPath,"r")
                    data = fp.read()
                    modObj.update(json_loads(data))
                    fp.close()
                except Exception as e:
                    modObj["name"] = folder[folder.rfind("/")+1:]
                    modObj["error"] = "meta.json could not be validated!"
                    print(e)
            elif (os.path.exists(jsonPathAlt)):
                try:
                    fp = open(jsonPathAlt,"r")
                    data = fp.read()
                    modObj.update(json_loads(data))
                    fp.close()
                except Exception as e:
                    modObj["name"] = folder[folder.rfind("/")+1:]
                    modObj["error"] = "meta.json could not be validated!"
                    print(e)
            else:
                possible_folders = ["Events", "Skills", "Perks", "Locations", "Adventures", "Fetishes", "Items", "Monsters"]
                intended_folder_location = False
                for possible_folder in possible_folders:
                    nested_path = os.path.join(folder, possible_folder)
                    if os.path.exists(nested_path):
                        intended_folder_location = True
                        break
                if not intended_folder_location:
                    modObj["error"] = "Mod folder is not correctly extracted! Fix path?"
                    modObj["name"] = folder[folder.rfind("/")+1:]
                else:
                    modObj["error"] = "meta.json not found!"
                    modObj["name"] = folder[folder.rfind("/")+1:]

            modObjs.append(modObj)

        return sorted(modObjs, key= lambda k: k["name"]) # sort by key "name"

    def retrieveIcon(folder):
        try:
            imgPath = os.path.join("../Mods", folder[folder.rfind("/")+1:]) + "/icon.png"
            if renpy.windows:
                imgPath = imgPath.replace("\\", "/")
            return imgPath
        except Exception as e:
            print(e)

    # returns whether the mod is deactivated (has underscore as first char)
    def isDeactivated(modpath):
        return modpath.startswith("_", modpath.rfind("/")+1)

    # switches state of a mod (renames the modfolder)
    def switchStateMod(modpath, name):
        stateBefore = isDeactivated(modpath)
        modName = modpath[modpath.rfind("/")+1:]
        if stateBefore:
            newpath = mod_folder + modpath[modpath.rfind("/")+1:].replace("_","",1) # remove underscore in front of foldername
        else:
            newpath = mod_folder + "_" + modpath[modpath.rfind("/")+1:] # add underscore in front of foldername

        try:
            os.rename(modpath, newpath)
            if stateBefore:
                renpy.notify(name + " was activated!")
            else:
                renpy.notify(name + " was deactivated!")
        except (OSError, Exception) as e:
            if isinstance(e, OSError) and e.errno == 39:
                renpy.notify(modName + " already exists! Check mod list and determine which to delete first.")
            else:
                renpy.notify("Couldn't switch state of " + name + "!")
                print(e)
        updateModMetadata(True)

    def removeZip(path, name):
        try:
            os.remove(path)
            renpy.notify(name + " was deleted!")
        except Exception as e:
            print(e)
            renpy.notify("Couldn't delete " + name + "!")

        updateModMetadata()

    def removeMod(modpath, name):
        try:
            shutil.rmtree(modpath)
            renpy.notify(name + " was deleted!")
        except Exception as e:
            print(e)
            renpy.notify("Couldn't delete " + name + "!")

        updateModMetadata(True)

    # grabs the Android clipboard
    # ToDo: Maybe it's necessary to verify it's a URL before changing the URL field
    # def getClipboard():
    #     global sdk
    #     if renpy.android:
    #         from jnius import autoclass, cast
    #         Context = autoclass('android.content.Context')
    #         PythonActivity = autoclass('org.renpy.android.PythonSDLActivity')
    #         Clipboard = cast('android.app.Activity',PythonActivity.mActivity).getSystemService(Context.CLIPBOARD_SERVICE)
    #         if sdk < 11:
    #             persistent.checkUrl["url"] = Clipboard.getText()
    #         else:
    #             primary_clip = Clipboard.getPrimaryClip()
    #             if primary_clip:
    #                 try:
    #                     url = primary_clip.getItemAt(0)
    #                     if url:
    #                         persistent.checkUrl["url"] = url.coerceToText(PythonActivity.mActivity.getApplicationContext())
    #                 except Exception as e:
    #                     print(e)

    # update the mod variables
    def startModLoading():
        global onlyMetaMods, disableMods, gameVersion, breakingGameVersion
        mods = retrieveModList()
        for i, nextmod in enumerate(mods):
            if not isDeactivated(nextmod["path"]):
                print(i, nextmod["name"])
                if 'error' in nextmod and onlyMetaMods:
                    if nextmod["error"] == "meta.json not found!":
                        switchStateMod(nextmod["path"], nextmod["name"])
                elif 'error' not in nextmod and disableMods:
                    if compare_semver(gameVersion, breakingGameVersion, nextmod["testedFor"]) in ["DatedSevere", "Breaking"]:
                        switchStateMod(nextmod["path"], nextmod["name"])
        renpy.reload_script() #camilla why #such is the way of camilla

        # global jsonList;jsonList = []

        # global AdventureDatabase;AdventureDatabase = []
        # global EventDatabase;EventDatabase = []
        # global FetishList;FetishList = []
        # global ItemDatabase;ItemDatabase = []
        # global LocationDatabase;LocationDatabase = []
        # global MonsterDatabase;MonsterDatabase = []
        # global PerkDatabase;PerkDatabase = []
        # global SkillsDatabase;SkillsDatabase = []

        # global LocationList;LocationList = []

        # global LevelingPerkDatabase;LevelingPerkDatabase = []
        # global PerkDatabaseLVLDisplay;PerkDatabaseLVLDisplay = []
        # global AdditionalLevelPerks;AdditionalLevelPerks = []

        # global EndOfDayList;EndOfDayList = []
        # global TimePassedList;TimePassedList = []
        # global StepTakenList;StepTakenList = []
        # global EndOfTurnList;EndOfTurnList = []
        # global EndOfCombatlist;EndOfCombatList = []
        # global StartOfTurnList;StartOfTurnList = []
        # global StartOfCombatList;StartOfCombatList = []
        # global OnPlayerClimaxList;OnPlayerClimaxList = []
        # global DreamList;DreamList = []

        # global WaiterBrothel;WaiterBrothel = []
        # global BarBrothel;BarBrothel = []
        # global GloryHoleBrothel;GloryHoleBrothel = []
        # global DayBrothel;DayBrothel = []
        # global loadingDatabaseType;loadingDatabaseType = 0
        # set_lists()
        # renpy.call_in_new_context("loadDatabase")

    def updateModMetadata(genMod=False):
        global mods, modNum, zips, genModData, numberouno, modCount
        if persistent.fileAccess:
            if genMod == True:
                persistent.genModData = True
            mods = retrieveModList()
            modCount = countModList()
            modNum = str(len(mods))
            zips = retrieveModInstallList()
        else:
            modScreen = "error"
            renpy.notify("Mod file access error on refresh!")
