init python:
    def gridVision(maze, start, sightrange, tileset, ActiveGridNPCs):

        v = 1
        getVisibleGrid = []

        VisionPointArrayGet = []
        VisionPointArray = []

        if sightrange == 1:
            leftSight = 1
            rightSight = 1
            downSight = 1
            upSight = 1
        else:
            if  tileset[FindTileType(maze[start[1]][start[0]+1], tileset)][2] == "Wall":
                leftSight = (int(sightrange*0.5))
            else:
                leftSight = sightrange
            if  tileset[FindTileType(maze[start[1]][start[0]-1], tileset)][2] == "Wall":
                rightSight = -(int(sightrange*0.5))
            else:
                rightSight = -sightrange
            if  tileset[FindTileType(maze[start[1]+1][start[0]], tileset)][2] == "Wall":
                downSight = (int(sightrange*0.5))
            else:
                downSight = sightrange
            if  tileset[FindTileType(maze[start[1]-1][start[0]], tileset)][2] == "Wall":
                upSight = -(int(sightrange*0.5))
            else:
                upSight = -sightrange

        leftPos = [leftSight+start[0], 0+start[1]]
        rightPos = [rightSight+start[0], 0+start[1]]
        downPos = [0+start[0], downSight+start[1]]
        upPos = [0+start[0], upSight+start[1]]

        NWPath = astar(maze, (leftPos[0], leftPos[1]), (upPos[0], upPos[1]), tileset, ActiveGridNPCs, 1, [[1, 1], [1, -1], [-1, 1], [-1, -1], [0, -1], [0, 1], [-1, 0], [1, 0]] )
        NEPath = astar(maze, (rightPos[0], rightPos[1]), (upPos[0], upPos[1]), tileset, ActiveGridNPCs, 1, [[1, 1], [1, -1], [-1, 1], [-1, -1], [0, -1], [0, 1], [-1, 0], [1, 0]] )
        SEPath = astar(maze, (rightPos[0], rightPos[1]), (downPos[0], downPos[1]), tileset, ActiveGridNPCs, 1, [[1, 1], [1, -1], [-1, 1], [-1, -1], [0, -1], [0, 1], [-1, 0], [1, 0]] )
        SWPath = astar(maze, (leftPos[0], leftPos[1]), (downPos[0], downPos[1]), tileset, ActiveGridNPCs, 1, [[1, 1], [1, -1], [-1, 1], [-1, -1], [0, -1], [0, 1], [-1, 0], [1, 0]] )

        NWPathFuzz = astar(maze,  (upPos[0], upPos[1]), (leftPos[0], leftPos[1]), tileset, ActiveGridNPCs, 1, [[1, 1], [1, -1], [-1, 1], [-1, -1], [0, -1], [0, 1], [-1, 0], [1, 0]] )
        NEPathFuzz = astar(maze,  (upPos[0], upPos[1]),(rightPos[0], rightPos[1]), tileset, ActiveGridNPCs, 1, [[1, 1], [1, -1], [-1, 1], [-1, -1], [0, -1], [0, 1], [-1, 0], [1, 0]] )
        SEPathFuzz = astar(maze,  (downPos[0], downPos[1]), (rightPos[0], rightPos[1]), tileset, ActiveGridNPCs, 1, [[1, 1], [1, -1], [-1, 1], [-1, -1], [0, -1], [0, 1], [-1, 0], [1, 0]] )
        SWPathFuzz = astar(maze,  (downPos[0], downPos[1]), (leftPos[0], leftPos[1]), tileset, ActiveGridNPCs, 1, [[1, 1], [1, -1], [-1, 1], [-1, -1], [0, -1], [0, 1], [-1, 0], [1, 0]] )

        for each in NWPath:
            VisionPointArrayGet.append(each)
        for each in NEPath:
            VisionPointArrayGet.append(each)
        for each in SEPath:
            VisionPointArrayGet.append(each)
        for each in SWPath:
            VisionPointArrayGet.append(each)

        for each in NWPathFuzz:
            VisionPointArrayGet.append(each)
        for each in NEPathFuzz:
            VisionPointArrayGet.append(each)
        for each in SEPathFuzz:
            VisionPointArrayGet.append(each)
        for each in SWPathFuzz:
            VisionPointArrayGet.append(each)


        [VisionPointArray.append(x) for x in VisionPointArrayGet if x not in VisionPointArray]

        for each in VisionPointArray:
            getVisibleGrid = gridCheck(maze, start, each, tileset, ActiveGridNPCs, getVisibleGrid, sightrange)


        wallChecker = copy.copy(getVisibleGrid)
        adjacentVis = [[0, -1], [0, 1], [-1, 0], [1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
        for each in wallChecker:
            for sight in adjacentVis:
                location = [each[0]+sight[0], each[1]+sight[1]]
                location = gridPosLimit(maze, location)
                if  tileset[FindTileType(maze[location[1]][location[0]], tileset)][2] == "Wall":
                    getVisibleGrid.append(location)

        rangeChecker = copy.copy(getVisibleGrid)
        getVisibleGrid = []
        for each in rangeChecker:
            if each[0] <= start[0]+sightrange and each[0] >= start[0]-sightrange:
                if each[1] <= start[1]+sightrange and each[1] >= start[1]-sightrange:
                    getVisibleGrid.append(each)

        #getVisibleGrid = gridCheck(maze, start, [sightrange+start[0], 0+start[1]], tileset, ActiveGridNPCs, getVisibleGrid, sightrange)
        #getVisibleGrid = gridCheck(maze, start, [-sightrange+start[0], 0+start[1]], tileset, ActiveGridNPCs, getVisibleGrid, sightrange)
        #getVisibleGrid = gridCheck(maze, start, [0+start[0], sightrange+start[1]], tileset, ActiveGridNPCs, getVisibleGrid, sightrange)
        #getVisibleGrid = gridCheck(maze, start, [0+start[0], -sightrange+start[1]], tileset, ActiveGridNPCs, getVisibleGrid, sightrange)



        return getVisibleGrid

    def gridPosLimit(maze, position):
        positionAcceptable = 1
        while positionAcceptable != 0:
            if positionAcceptable == 1:
                if position[0] < 0:
                    position[0] += 1
                elif position[0] > len(maze[0])-1:
                    position[0] -= 1
                elif  position[1] < 0:
                    position[1] += 1
                elif  position[1] > len(maze)-1:
                    position[1] -= 1
                else:
                    positionAcceptable = 0

        return position


    def gridCheck(maze, start, sightrange, tileset, ActiveGridNPCs, getVisibleGrid, PlayerGridSight):
        passCheck = 1
        positionAcceptable = 1

        sightrange = gridPosLimit(maze, sightrange)

        Path = astar(maze, (start[0], start[1]), (sightrange[0], sightrange[1]), tileset, ActiveGridNPCs, 1, [[0, -1], [0, 1], [-1, 0], [1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]] )
        if len(Path) > PlayerGridSight+1:
            passCheck = 0
        if passCheck == 1:
            for each in Path:
                if passCheck == 1:
                    if  tileset[FindTileType(maze[each[1]][each[0]], tileset)][2] == "Wall":
                        passCheck = 0
                    else:
                        getVisibleGrid.append(each)


        return getVisibleGrid
