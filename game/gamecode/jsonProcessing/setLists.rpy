init -1 python:
    try:
        import orjson
        json_loads = orjson.loads
    except ImportError:
        import json
        print("orjson not found, using fallback.")
        json_loads = json.loads
    import re
    import os
    import time
    if renpy.windows:
        gamedir = renpy.config.gamedir.replace("\\", "/")
    else:
        gamedir = renpy.config.gamedir
    dpardir = os.path.join(os.path.pardir, os.path.pardir)


    def json_scouting(spot):
        return [thing for thing in renpy.list_files() if thing.startswith(spot)]
    def mods_scouting():
        gamemoddirname = os.path.join(gamedir, os.path.join(os.path.pardir, 'Mods'))
        #print(gamemoddirname)
        gamemoddir = []
        for root, dirs, files in os.walk(gamemoddirname, followlinks=True, topdown=False):
            for name in files:
                gamemoddir.append(os.path.relpath(os.path.join(root, name), gamemoddirname))
        if renpy.windows:
            listOfMods = [os.path.join(os.path.pardir, os.path.join('Mods', x)).replace("\\", "/") for x in gamemoddir]
        else:
            listOfMods = [os.path.join(os.path.pardir, os.path.join('Mods', x)) for x in gamemoddir]
        return listOfMods
    def set_lists():
        global jsonList
        jsonDirList = []
        jsonDir = json_scouting("Json/")
        #print(jsonDir)
        for dirData in jsonDir:
            if re.match(".*/_.*", dirData):
                pass
            else:
                jsonDirList.append(dirData)
        if renpy.android:
            modDirList = []
            modDir = json_scouting("Mods/")
            for dirData in modDir:
                if re.match(".*/_.*", dirData):
                    pass
                else:
                    modDirList.append(dirData)
        else:
            modDirList = []
            modDir = mods_scouting()
            #print(modDir)
            for dirData in modDir:
                if re.match(".*/_.*", dirData):
                    pass
                else:
                    if dirData.endswith(".json"):
                        modDirList.append(dirData)
        jsonList = jsonDirList + modDirList
        #print(jsonList)
    def dynamic_loader(where):
        global jsonList
        return [thing for thing in jsonList if re.match(where, thing)]
