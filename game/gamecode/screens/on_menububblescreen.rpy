


# Screen to replace menu backgrounds - only has a solid color background and the overlay
screen menu_background(mainMenu=False):
    add "gui/new_menu_back.png"

    if (mainMenu):
        add MenuCircleOverlay(zoom=1024.0, mainMenu=True, yOffset=-mainMenuBubblesYPos) xpos mainMenuBubblesXPos ypos mainMenuBubblesYPos
        add MenuCircleOverlay(zoom=1024.0, mainMenu=False, yOffset=-100, rightSide=True) xpos 1220 ypos 100
        add CharacterBubbleOverlay(zoom=1024.0, mainMenu=True, yOffset=-mainMenuBubblesYPos, mainMenuBubblesXPos=mainMenuBubblesXPos, mainMenuBubblesYPos=mainMenuBubblesYPos) xpos mainMenuBubblesXPos ypos mainMenuBubblesYPos
        add "waifububble_main_larger.png" xcenter mainMenuBubblesXPos ycenter mainMenuBubblesYPos xoffset -50 yoffset -20
    else:
        add MenuCircleOverlay(zoom=1024.0, mainMenu=False, yOffset=-100) xpos 200 ypos 100
        add "waifububble_main_larger.png" xcenter 200 ycenter 100

# Screen for the bubbly circle stuff in the main menu!
# Basic rules: Circles gravitate upwards and towards each other, but
# also have a friction force applied so they don't go too fast.
# Basically I wanted a consistency somewhere between soap bubbles and fluffy clouds
init python:
    import math
    import random

    # Position of main menu widget is stored in vars because some of the code needs to know these offsets
    mainMenuBubblesXPos = 700
    mainMenuBubblesYPos = 320

    # Global variables:
    # Bubble locations are stored in two global arrays, one for the main menu and one for the pause menu.
    # They're global (rather than stored inside the MenuCircleOverlay class) so they don't get regenerated
    # every time the screen is recreated - this would cause odd-looking teleporting. The screen's render()
    # method updates one of these arrays, depending on whether self.mainMenu == True.

    # globals for the two screens
    # radius of a circle in the actual image file
    circleRadius = 64.0

    # Originally 30, increased thanks to performance improvements for objectively ideal number, including double on the main menu.
    numCircles = 34

    # list of bubbles
    # Format of each bubble is a tuple - (xpos, ypos, radius, xvel, yvel, bounce_start)
    mainMenuCircles = []
    pauseMenuCircles = []
    rightSideCircles = []



    # Code for the larger bubbles with character art
    # these don't interact with the physics system and only move upwards slowly
    numCharacterCircles = 10
    characterCircleSpeed = -0.4

    # Function and var for generating x positions for character art bubbles
    # Want to spread evenly between left and right, but have more on the right
    # Pure randomness can give long streaks on one side, looking unbalanced
    mmenu_placeOnRight = True
    def mmenu_getXPosition():
        global mmenu_placeOnRight # lol python

        # Flip between left and right with each placed bubble
        if mmenu_placeOnRight:
            xPosition = renpy.random.randint(1380, 1780)

            # But the right side "sticks" - only flip back to the left 50% of the time
            if renpy.random.randint(0, 1) != 1:
                mmenu_placeOnRight = False
        else:
            xPosition = renpy.random.randint(160, 460)
            mmenu_placeOnRight = True

        return xPosition

    # Random selection of art per circle - expand this as more art gets added!
    # Filenames from the images/ folder
    characterCircleArt = [
        "waifububble_Kyra.png",
        "waifububble_Perpetua.png",
        "waifububble_Nicci.png",
        "waifububble_Mika.png",
        "waifububble_mimic.png",
        "waifububble_lillian.png",
        "waifububble_Vivian.png",
        "waifububble_VivianTitty.png",
        "waifububble_Elena.png",
        "waifububble_Amber.png",
        "waifububble_Elly.png",
        "waifububble_Elf.png",
        "waifububble_Harpy.png",
        "waifububble_Nara.png",
        "waifububble_Trisha.png",
        "waifububble_Ancilla.png",
        "waifububble_Vili.png",
        "waifububble_Jora.png",
        "waifububble_Shizu.png",
        "waifububble_blank.png", # add in some blank circles for variety
        "waifububble_blank.png",
        "waifububble_blank.png",
        "waifububble_blank.png"
        ]

    # Cycle through the list of character art repeatedly using index
    # shuffling the list when we reach the end and start over
    characterCircleIndex = 0

    random.shuffle(characterCircleArt) # Also shuffle initially

    # Function to step through list and shuffle
    def mmenu_getNextBubbleArt():
        global characterCircleIndex # lol python

        characterCircleIndex += 1

        if characterCircleIndex >= len(characterCircleArt):
            characterCircleIndex = 0
            random.shuffle(characterCircleArt)

        return characterCircleArt[characterCircleIndex]



    # List of positions - only ever read and updated by the main menu's MenuCircleOverlay
    # Format for each bubble is a tuple - (xpos, ypos, radius, filename, xvel, yvel, bounce_start, bounce_zoom)
    characterCircles = []

    for i in range(0, numCharacterCircles):

        # Space them evenly along the screen, rather than purely randomly
        pct = (i+0.5)/numCharacterCircles

        # Generate the circle's tuple and add it
        characterCircles.append([
            mmenu_getXPosition(),
            pct*1080 - mainMenuBubblesYPos + renpy.random.randint(-100, 100) + 200,
            renpy.random.uniform(0.6, 1.0),
            mmenu_getNextBubbleArt(),
            0,  # xvel
            0,  # yvel
            0.0, # bounce_start
            1.0  # bounce_zoom
        ])

    # Get a random size for a single circle
    # Mostly add small ones, occasionally a larger one
    def mmenu_getRandomSize():
        big = renpy.random.randint(0, 6) == 1
        return renpy.random.uniform(0.7, 1.5) if big else renpy.random.uniform(0.4, 0.7)

    # Initialization: add some number of circles directly around the main circle
    for i in range(0, numCircles//3):
        theta = renpy.random.uniform(-1.5, 1)
        mainMenuCircles.append([
            200*math.cos(theta),
            200*math.sin(theta),
            mmenu_getRandomSize(),
            renpy.random.uniform(-0.1, 0.1),
            renpy.random.uniform(-0.5, -0.2),
            0.0  # bounce_start
        ])

    # Add the others on the path up to it
    for i in range(numCircles//3, numCircles):
        mainMenuCircles.append([
            renpy.random.uniform(0, 30),
            renpy.random.uniform(150, 1300),
            mmenu_getRandomSize(),
            renpy.random.uniform(-0.1, 0.1),
            renpy.random.uniform(-0.5, -0.2),
            0.0  # bounce_start
        ])

    # Initialization: add some number of circles directly around the main circle
    for i in range(0, numCircles//4):
        theta = renpy.random.uniform(0, 1)
        pauseMenuCircles.append([
            200*math.cos(theta),
            200*math.sin(theta),
            mmenu_getRandomSize(),
            renpy.random.uniform(-0.1, 0.1),
            renpy.random.uniform(-0.5, -0.2),
            0.0  # bounce_start
        ])

    # Add the others on the path up to it
    for i in range(numCircles//4, numCircles):
        pauseMenuCircles.append([
            renpy.random.uniform(0, 30),
            renpy.random.uniform(150, 1200),
            mmenu_getRandomSize(),
            renpy.random.uniform(-0.1, 0.1),
            renpy.random.uniform(-0.5, -0.2),
            0.0  # bounce_start
        ])

    # Initialize right-side circles (separate from pause menu)
    # Initialization: add some number of circles directly around the main circle
    for i in range(0, numCircles//4):
        theta = renpy.random.uniform(0, 1)
        rightSideCircles.append([
            200*math.cos(theta),
            200*math.sin(theta),
            mmenu_getRandomSize(),
            renpy.random.uniform(-0.1, 0.1),
            renpy.random.uniform(-0.5, -0.2),
            0.0  # bounce_start
        ])

    # Add the others on the path up to it
    for i in range(numCircles//4, numCircles):
        rightSideCircles.append([
            renpy.random.uniform(0, 30),
            renpy.random.uniform(150, 1200),
            mmenu_getRandomSize(),
            renpy.random.uniform(-0.1, 0.1),
            renpy.random.uniform(-0.5, -0.2),
            0.0  # bounce_start
        ])


    # Custom displayable to render circles with character bubbles, moved out of MainMenuCircleOverlay.
    class CharacterBubbleOverlay(renpy.Displayable):

        def __init__(self, mainMenu=False, yOffset=-100, mainMenuBubblesXPos=700, mainMenuBubblesYPos=320, **kwargs):
            super(CharacterBubbleOverlay, self).__init__(**kwargs)
            self.mainMenu = mainMenu
            self.yOffset = yOffset
            self.mainMenuBubblesXPos = mainMenuBubblesXPos
            self.mainMenuBubblesYPos = mainMenuBubblesYPos

        def updateCharacterBubbles(self, st):
            if not self.mainMenu:
                return
            for i in range(0, len(characterCircles)):
                # Moving up with velocity
                characterCircles[i][1] += characterCircleSpeed + characterCircles[i][5]
                characterCircles[i][0] += characterCircles[i][4]

                # Dampen velocity
                characterCircles[i][4] *= 0.95
                characterCircles[i][5] *= 0.95

                # Bounce
                if characterCircles[i][6] > 0:
                    time_since_bounce = st - characterCircles[i][6]
                    if time_since_bounce < 0.25:
                        # Calculating bounce zoom with sine wave (elastic inward bounce)
                        bounce_progress = time_since_bounce / 0.25
                        bounce_intensity = math.sin(bounce_progress * math.pi * 2) * 0.15  # % decrease
                        characterCircles[i][7] = 1.0 - bounce_intensity  # Shrink
                    else:
                        # Reset bounce
                        characterCircles[i][6] = 0.0  # Reset bounce_start
                        characterCircles[i][7] = 1.0  # Reset bounce_zoom

                # Bubble off screen, reset.
                if characterCircles[i][1] <= self.yOffset - 400:
                    characterCircles[i] = [
                        mmenu_getXPosition(),
                        self.yOffset + 1150,
                        renpy.random.uniform(0.6, 1.0),
                        mmenu_getNextBubbleArt(),
                        0,  # xvel
                        0,  # yvel
                        0.0, # bounce_start
                        1.0  # bounce_zoom
                    ]

        def render(self, width, height, st, at):
            if not self.mainMenu:
                return renpy.Render(width, height) # empty render if not main menu

            self.updateCharacterBubbles(st)  # update every frame
            renpy.redraw(self, 0)  # redraw every frame

            render = renpy.Render(width, height) 

            for i, circle in enumerate(characterCircles):
                if circle[6] > 0:  # bounce_start > 0 is active bounce
                    displayable = Transform(circle[3],
                        zoom=circle[2] * circle[7],
                        anchor=(0.5, 0.5),
                        xcenter=0, ycenter=0)
                else:
                    displayable = Transform(circle[3],
                        zoom=circle[2],
                        anchor=(0.5, 0.5),
                        xcenter=0, ycenter=0)

                x_pos = int((circle[0] - self.mainMenuBubblesXPos))
                y_pos = int(circle[1])

                render.place(displayable, x=x_pos, y=y_pos)

            return render

        def event(self, ev, x, y, st):
            if not self.mainMenu:
                return None

            # Handle mouse click events
            if ev.type == 1026 and ev.button == 1: # MOUSEBUTTONDOWN event with left click
                click_x = x
                click_y = y

                # Loop in reverse for recently spawned bubbles priority
                for i in reversed(range(len(characterCircles))):
                    circle = characterCircles[i]
                    bubble_size = int(circle[2] * 160)
                    overlay_center_x = circle[0] - self.mainMenuBubblesXPos
                    overlay_center_y = circle[1]
                    overlay_left = overlay_center_x - bubble_size/2
                    overlay_top = overlay_center_y - bubble_size/2
                    overlay_right = overlay_left + bubble_size
                    overlay_bottom = overlay_top + bubble_size
                    if (overlay_left <= click_x <= overlay_right and
                        overlay_top <= click_y <= overlay_bottom):
                        # Start bounce animation
                        circle[6] = st
                        break

            return None

    # Custom displayable to render circles
    # Better solution than using a screen with "add" statements with a timer tp update every frame
    class MenuCircleOverlay(renpy.Displayable):

        def __init__(self, zoom=1, mainMenu=False, yOffset=-100, rightSide=False, **kwargs):
            super(MenuCircleOverlay, self).__init__(**kwargs)
            self.zoom = zoom
            self.mainMenu = mainMenu
            self.rightSide = rightSide
            self.yOffset = yOffset
            self.counter = 0

            # Spatial grid parameters
            self.gridSize = 100
            self.gridWidth = 20  # 1920 / 100
            self.gridHeight = 15  # 1500 / 100
            self.spatialGrid = {}

            # list of other circles
            # Format is a tuple - (xpos, ypos, radius, xvel, yvel)
            if mainMenu:
                self.menuCircles = mainMenuCircles
                self.waifuCircle = [50, 0, 190/circleRadius, 0, 0, 0.0]
            elif rightSide:
                self.menuCircles = rightSideCircles
                self.waifuCircle = [0, 0, 0, 0, 0, 0.0]
            else:
                self.menuCircles = pauseMenuCircles
                self.waifuCircle = [0, 0, 190/circleRadius, 0, 0, 0.0]

        def updateMenuCircles(self):
            self.updatePhysicsCircles()

        def updatePhysicsCircles(self):
            self.buildSpatialGrid()

            for i in range(0, len(self.menuCircles)):
                self.moveCircle(i)
                self.doCircleDamping(self.menuCircles[i])

        def buildSpatialGrid(self):
            self.spatialGrid = {}
            for i, circle in enumerate(self.menuCircles):
                gx = int(circle[0] / self.gridSize)
                gy = int(circle[1] / self.gridSize)
                key = (gx, gy)
                if key not in self.spatialGrid:
                    self.spatialGrid[key] = []
                self.spatialGrid[key].append(i)

        def getNearbyCircles(self, i):
            circle = self.menuCircles[i]
            gx = int(circle[0] / self.gridSize)
            gy = int(circle[1] / self.gridSize)
            nearby = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    key = (gx + dx, gy + dy)
                    if key in self.spatialGrid:
                        nearby.extend(self.spatialGrid[key])
            return [j for j in nearby if j != i]

        # Moves a single circle. Does physics with all circles ahead of it in the array
        def moveCircle(self, i):
            c = self.menuCircles[i]

            # If we're at the top of the screen, shrink the circle
            if c[1] <= self.yOffset-6:
                c[1] = self.yOffset-6
                c[2] -= 0.001

                # If we've shrunk to nothing, use this slot for a new circle
                if c[2] < .1:
                    self.menuCircles[i] = [
                        renpy.random.uniform(0, 30),
                        self.yOffset+1250,
                        mmenu_getRandomSize(),
                        renpy.random.uniform(-0.2, 0.2),
                        renpy.random.uniform(-1.2, -0.7),
                        0.0
                    ]

            # Otherwise, add vertical velocity
            else:
                c[1] += c[4]

            # Add horizontal velocity
            c[0] += c[3]
            
            # Physics with nearby circles using spatial grid
            nearby = self.getNearbyCircles(i)
            for j in nearby:
                if j > i:  # only process each pair once
                    avgHeight = (c[1] + self.menuCircles[j][1]) / 2
                    self.doCircleCollision(c, self.menuCircles[j], True, avgHeight/100)

            # Collide with waifu circle but don't move it around or gravitate
            if not self.rightSide:
                self.doCircleCollision(c, self.waifuCircle, False, 0)

            # Stop from moving past horizontal boundary
            if c[0] < 30:
                c[0] = 30

                if c[3] < 0:
                    c[3] = 0

            ## gravitate towards middle if below waifu circle
            if c[1] > 250:
                c[3] -= c[0]/10000

            ## gravitate towards middle more if just above waifu circle
            if c[1] < 0 and c[1] > -150:
                c[3] -= .025

            # gravitate away from middle if near waifu circle so they don't bunch up there
            if c[1] > 99 and c[1] < 200:
                c[3] += .01

        def doCircleCollision(self, i, j, canMoveJ, gravityMult):
            # distance from i to j
            dx = i[0]-j[0]
            dy = i[1]-j[1]

            # distance minus circle radii, but adjusted
            # Only use part of smallr circle's radius, and multiply by 0.9
            maxRadius = (max(i[2], j[2]) + min(i[2], j[2])/4)*circleRadius*.9

            # total distance between circle centers
            totalDistance = math.sqrt(dx*dx + dy*dy)

            normalizedDx = dx/totalDistance
            normalizedDy = dy/totalDistance

            if (totalDistance-maxRadius < 0):
                # Collision: Move both circles away from each other by half the overlap distance
                i[0] -= normalizedDx*(totalDistance-maxRadius)/2
                i[1] -= normalizedDy*(totalDistance-maxRadius)/2
                if canMoveJ:
                    j[0] += normalizedDx*(totalDistance-maxRadius)/2
                    j[1] += normalizedDy*(totalDistance-maxRadius)/2

            # Do gravitation scaled by maxRadius
            # not physically 'correct': scaling is weird and range is not an inverse square law
            d = (totalDistance)/maxRadius
            if d < 3:
                if gravityMult >= 0:
                    gravity = (3-d) * 0.0001*gravityMult
                else:
                    gravity = (3-d) * -0.0001*gravityMult

                i[3] -= normalizedDx*gravity/i[2]
                i[4] -= normalizedDy*gravity/i[2]
                if canMoveJ:
                    j[3] += normalizedDx*gravity/j[2]
                    j[4] += normalizedDy*gravity/j[2]

        # Apply friction to everything to kepe them moving slow
        def doCircleDamping(self, i):
            # Damp velocity towards an upward vector - not towards (0, 0)
            # Remove this upward vector while damping is done
            i[4] += 0.3

            totalV = math.sqrt(i[3]*i[3] + i[4]*i[4])

            # If velocity is more than some value, cut off some of it
            if totalV > 0.1:
                normalizedVx = i[3]/totalV
                normalizedVy = i[4]/totalV
                i[3] -= normalizedVx*0.04
                i[4] -= normalizedVy*0.04

            # undo the upward vector adjustment so we're moving up again
            i[4] -= 0.3

        def render(self, width, height, st, at):
            self.updateMenuCircles() # update every frame

            renpy.redraw(self, 0) # redraw every frame
            render = renpy.Render(width, height) # create a new Render object with proper size

            im = Image("gui/menu_circle.png")

            # add everything to a new Fixed() rather than blitting it directly
            # This is so we can zoom out the Fixed in the last step
            f = Fixed()
            flip = -1 if self.mainMenu else 1

            for circle in self.menuCircles:
                transform = Transform(im,
                    zoom=circle[2]*self.zoom,
                    xcenter=int(circle[0]*self.zoom*flip),
                    ycenter=int(circle[1]*self.zoom))
                f.add(transform)

            if self.mainMenu:
                f.add(Transform(Image("gui/menu_column.png"),
                    zoom=self.zoom,
                    xpos=int(-70*self.zoom),
                    ypos=int(self.yOffset*self.zoom)))
            else:
                f.add(Transform(Image("gui/menu_sidebar.png"),
                    zoom=self.zoom,
                    xpos=int(-200*self.zoom),
                    ypos=int(self.yOffset*self.zoom)))

            # Zoom everything in then out so that the integer positions are more accurate
            # This does NOT result in drawing a larger image than necessary - only the positions are affected
            t = Transform(f, zoom=1/self.zoom)

            # Finally, blit the transform to the Render and return it
            render.blit(renpy.render(t, width, height, st, at), (0, 0))

            return render

        def event(self, ev, x, y, st):
            return None
