# Rewritten from previous image button spam state, to this renpy displayable. - FCMCL.

init:

    default paradeInterval = 0.5
    default paradeExplodingOver = True

    transform mobileUItransparency:
        alpha 0.6

    transform fruitMonchVFX(cellSize):
        xanchor 0.5
        yanchor 0.5
        rotate 0
        xysize (50, 50)
        alpha 1.0
        linear paradeInterval alpha 0.0 xysize (cellSize // 2, cellSize // 2) rotate 720 yoffset -40

    transform fruitDropVFX(cellSize, timing):
        xanchor 0.5
        yanchor 0.5
        rotate 200
        xysize (cellSize // 2, cellSize // 2)
        alpha 0.2
        yoffset -40
        parallel:
            easein 0.6 alpha 1.0
        parallel:
            easein_elastic timing xysize (cellSize, cellSize) rotate 0 yoffset 0

init python:
    # I did not bother to figure out how to tell old saves to forget about this.
    # Snake -> Parade keywords was done to avoid potential save overlap, but it also seemed more fun.
    class ParadeNPC():
        pass
    class SnakeNPC():
        pass
    class monchVFX(renpy.store.object):
        pass

    # Vroom vroom use gpu to tuck renpy to bed each frame.
    renpy.register_shader("bounce_shader", variables="""
        uniform float u_time;
        uniform float u_paradeInterval;
        uniform sampler2D tex0;

        varying vec2 v_tex_coord;
        varying vec2 v_position;
    """, vertex_300="""
        v_tex_coord = a_tex_coord;
        v_position = a_position.xy;
    """, fragment_300="""
        vec2 uv = v_tex_coord;
        float bounceSpeed = 6.28318530718 / u_paradeInterval;
        float delayTime = 0.04;
        float cycleTime = mod(u_time, u_paradeInterval);
        float phase;
        if (cycleTime < u_paradeInterval * 0.4) {
            phase = cycleTime / (u_paradeInterval * 0.4); // Zoom in
        } else if (cycleTime < u_paradeInterval * 0.4 + delayTime) {
            phase = 1.0; // Hold at max zoom
        } else if (cycleTime < u_paradeInterval * 0.8 + delayTime) {
            phase = 1.0 - (cycleTime - u_paradeInterval * 0.4 - delayTime) / (u_paradeInterval * 0.4); // Zoom out
        } else {
            phase = 0.0; // Hold at min zoom
        }

        float zoomRange = 0.075;
        float xzoom = 1.0 + (zoomRange * phase);
        float yzoom = 1.0 - (zoomRange * phase);
        vec2 centered_uv = uv - vec2(0.5, 0.5);
        vec2 scaled_uv = centered_uv * vec2(1.0/xzoom, 1.0/yzoom);
        scaled_uv += vec2(0.5, 0.5);

        gl_FragColor = texture2D(tex0, scaled_uv);
    """)


    # All fruit spawned use this initialized object to track their individual stats.
    # You can call a transform onto a image using it as if it is a function.
    # Transforms must be done in init, not done on the fly, else it'll not apply warps, just static transform effects.
    class ParadeFruit(renpy.store.object):
        def __init__(self, fruitRect, fruit="Blueberry", pos=(0,0), paradeCellSize=50, score=0):
            self.fruit = fruit
            self.rect = fruitRect
            self.score = score
            self.dropping = True
            self.monching = False
            self.startTime = None
            self.monchStartTime = None
            self.paradeCellSize = 50
            self.halfCellSize = self.paradeCellSize / 2

            if self.fruit == "Blueberry":
                self.baseImage = "Snake/blueberry.png"
            elif self.fruit == "Cherry":
                self.baseImage = "Snake/cherry.png"
            elif self.fruit == "Appel":
                self.baseImage = "Snake/appel.png"
            elif self.fruit == "Marshmallow":
                self.baseImage = "Snake/marshmallow.png"
            elif self.fruit == "Peach":
                self.baseImage = "Snake/peach.png"
            elif self.fruit == "Grape":
                self.baseImage = "Snake/grape.png"

            self.dropEffect = At(self.baseImage, fruitDropVFX(paradeCellSize, 0.69))
            self.startTime = None
            self.image = renpy.displayable(self.baseImage)

        def monchTime(self):
            self.monchEffect = At(self.baseImage, fruitMonchVFX(self.paradeCellSize))

        def getImage(self, st):
            if self.dropping:
                if st - self.startTime > 0.69:
                    self.dropping = False
                return self.dropEffect
            elif self.monching:
                if st - self.monchStartTime > paradeInterval:
                    self.monching = False
                return self.monchEffect
            return self.image

    # The parade minigame, Ren'Py calls it a creator defined displayable.
    class SlimeParade(renpy.Displayable):
        def __init__(self, **kwargs):
            super(SlimeParade, self).__init__(**kwargs)
            global paradeInterval
            # I am keeping constants that never change here.

            # Snake is grid-based, so defining cells will allow for more straight forward code that can be more easily refined.

            self.paradeCellsX = 30
            self.paradeCellsY = 20
            self.paradeCellSize = 50
            self.halfCellSize = self.paradeCellSize // 2

            # Coordinates are put in tuples.
            self.paradeUp = (0, -50)
            self.paradeDown = (0, 50)
            self.paradeLeft = (-50, 0)
            self.paradeRight = (50, 0)
            self.gameover = False


            # This tells renpy how much of the game should be
            self.render_size = (1920,1080)
            # Turns out 50px doesn't divide cleanly into full HD, so we use this instead for math stuff.
            self.area_size = (1900,1000)

            self.newParade()

        # Mutable values are here, is maybe useful if this minigame gets improved as a 'slot more eros' feature too.
        def newParade(self):
            global paradeInterval
            paradeInterval = 0.55
            self.paradePositions = [(19*self.paradeCellSize, 11*self.paradeCellSize)]
            self.paradeMemberTypes = ["Leader"]
            self.paradeMembers = [renpy.displayable("Snake/BlueSlime.png")]
            self.monchingFruit = []
            self.currentFruit = []

            for _ in range(5):
                self.currentFruit.append(self.createFruit(manualChoice="Blueberry"))

            self.currentDirection = (0,0)
            self.requestedDirection = (0,0)
            self.lastRequestedDirection = (0,0)

            self.score = 0
            self.tickets = 0
            self.musicPhase = 0
            self.pacingCheck()

            self.paradeCanMove = True
            self.paradeCanStart = False
            self.paradeFreeze = False

            # Need lots of npcs fast for debugging? Uncomment this.
            tailPosI = 0
            # for _ in range(20):
            #     tailPos = tuple(map(lambda i, j: i-j, (self.paradePositions[tailPosI][0], self.paradePositions[tailPosI][1]), (0, -50)))
            #     tailPosI += 1
            #     self.paradePositions.append(tailPos)
            #     self.paradeMemberTypes.append("Cherry")
            #     self.paradeMembers.append(self.getNPCImage("Cherry"))

            return

        @staticmethod
        def getNPCImage(fruit):
            if fruit == "Blueberry":
                image = renpy.displayable(renpy.random.choice(["Snake/BlueSlime2.png", "Snake/BlueSlime3.png", "Snake/BlueSlime4.png"]))
            elif fruit == "Cherry":
                image = renpy.displayable(renpy.random.choice(["Snake/Perpo1.png", "Snake/Perpo2.png"]))
            elif fruit == "Appel":
                image = renpy.displayable("Snake/GreenSlime1.png")
            elif fruit == "Marshmallow":
                image = renpy.displayable("Snake/GhostSlime.png")
            elif fruit == "Peach":
                image = renpy.displayable("Snake/Gren.png")
            elif fruit == "Grape":
                image = renpy.displayable("Snake/Noir.png")
            elif fruit ==  "Leader":
                image = renpy.displayable("Snake/BlueSlime.png")
            return image

        # Fruit score worth is calculated here.
        def createFruit(self, manualChoice = "None"):
            fruitPos = self.getFruitPos()
            fruitRect = pygame.Rect(fruitPos, (self.paradeCellSize, self.paradeCellSize))
            newFruit = renpy.random.randint(0, 100)
            if manualChoice != "None":
                if manualChoice == "Blueberry":
                    return ParadeFruit(fruitRect, fruit="Blueberry", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=100)
                elif manualChoice == "Cherry":
                    return ParadeFruit(fruitRect, fruit="Cherry", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=250)
                elif manualChoice == "Appel":
                    return ParadeFruit(fruitRect, fruit="Appel", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=500)
                elif manualChoice == "Marshmallow":
                    return ParadeFruit(fruitRect, fruit="Marshmallow", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=1000)
                elif manualChoice == "Peach":
                    return ParadeFruit(fruitRect, fruit="Peach", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=2500)
                elif manualChoice == "Grape":
                    return ParadeFruit(fruitRect, fruit="Grape", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=5000)
            if newFruit <= 40:
                return ParadeFruit(fruitRect, fruit="Blueberry", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=100)
            elif newFruit <= 65:
                return ParadeFruit(fruitRect, fruit="Cherry", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=250)
            elif newFruit <= 80:
                return ParadeFruit(fruitRect, fruit="Appel", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=500)
            elif newFruit <= 90:
                if self.score <= 1000:
                    return ParadeFruit(fruitRect, fruit="Cherry", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=250)
                return ParadeFruit(fruitRect, fruit="Marshmallow", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=1000)
            elif newFruit <= 95:
                if self.score <= 5000:
                    return ParadeFruit(fruitRect, fruit="Appel", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=500)
                return ParadeFruit(fruitRect, fruit="Peach", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=2500)
            elif newFruit <= 100:
                if self.score <= 5000:
                    return ParadeFruit(fruitRect, fruit="Marshmallow", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=1000)
                if self.score <= 10000:
                    return ParadeFruit(fruitRect, fruit="Peach", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=2500)
                return ParadeFruit(fruitRect, fruit="Grape", pos=fruitPos, paradeCellSize=self.paradeCellSize, score=5000)

        # We check for potential overlap with the parade or fruits already spawned, repeat till we get an empty spot.
        def getFruitPos(self):
            while True:
                fruitPosX = (renpy.random.randint(1, self.paradeCellsX)*self.paradeCellSize)
                fruitPosY = (renpy.random.randint(1, self.paradeCellsY)*self.paradeCellSize)
                overlap = False
                for fruit in self.currentFruit:
                    if (fruitPosX, fruitPosY) == (fruit.rect.x, fruit.rect.y):
                        overlap = True
                        break
                for position in self.paradePositions:
                    if (fruitPosX, fruitPosY) == position:
                        overlap = True
                        break
                if not overlap:
                    return fruitPosX, fruitPosY

        def requestMove(self):
            # Tuple checks to see if player is attempting to defy nature by
            # turning a snake into a turtle via 180 degree turn, stops them if so.
            # If all is well, we tell the game the intended movement direction for next interval.
            # This can be changed by the player at the last millisecond before, so it's as responsive as it gets without input buffer
            # shennanigans.
            if tuple(map(lambda x, y: x + y, self.requestedDirection, self.lastRequestedDirection)) != (0,0):
                if self.requestedDirection == self.paradeUp:
                    self.currentDirection = (0, -50)
                    self.paradeCanStart = True
                elif self.requestedDirection == self.paradeDown:
                    self.currentDirection = (0, 50)
                    self.paradeCanStart = True
                elif self.requestedDirection == self.paradeLeft:
                    self.currentDirection = (-50, 0)
                    self.paradeCanStart = True
                elif self.requestedDirection == self.paradeRight:
                    self.currentDirection = (50, 0)
                    self.paradeCanStart = True
            self.requestedDirection = (0,0)

        # Score calculation, sfx, parade member appending, fruit spawn/despawn, monch vfx, and pacing call is done here
        def monch(self, fruitRect):
            global paradeInterval
            if paradeInterval <= 0.1:
                paradeInterval = 0.1
            if fruitRect.fruit == "Marshmallow":
                renpy.play("sfx/Erotic/Bouncy/Motion-Pop05-1.mp3")
            elif fruitRect.fruit == "Grape":
                renpy.play("sfx/Magic/status01.mp3")
            else:
                random = renpy.random.randint(1, 2)
                if random == 1:
                    renpy.play("sfx/heal01.mp3")
                elif random == 2:
                    renpy.play("sfx/heal02.mp3")
            self.score += fruitRect.score

            fruitRect.monching = True
            fruitRect.monchTime()
            self.monchingFruit.append(fruitRect)
            self.currentFruit.remove(fruitRect)

            self.paradePositions.append(self.lastTailPos)
            self.paradeMemberTypes.append(fruitRect.fruit)
            self.paradeMembers.append(self.getNPCImage(fruitRect.fruit))

            self.currentFruit.append(self.createFruit())
            self.pacingCheck()

        # This manages game speed and music according to score thus far.
        # If we add a in-game restart mechanic, this will need to be updated to handle that.
        def pacingCheck(self):
            global paradeInterval, paradeExplodingOver
            if self.musicPhase != 5:
                if self.score >= 100000:
                    paradeExplodingOver = False
                    paradeInterval = 0.1
                    paradeExplodingOver = True
                elif self.score >= 50000:
                    paradeExplodingOver = False
                    if self.musicPhase != 5:
                        self.musicPhase = 5
                        renpy.music.play("music/Capital/Purple_Planet_Music_-_Retro_Gamer_1_16_120bpm_L-50%faster.mp3", channel='music')
                        self.currentFruit.append(self.createFruit(manualChoice="Grape"))
                        self.currentFruit.append(self.createFruit(manualChoice="Blueberry"))
                        self.currentFruit.append(self.createFruit(manualChoice="Blueberry"))
                        self.currentFruit.append(self.createFruit(manualChoice="Blueberry"))
                        self.currentFruit.append(self.createFruit(manualChoice="Blueberry"))
                    paradeInterval = 0.175
                    paradeExplodingOver = True
                elif self.score >= 25000:
                    paradeExplodingOver = False
                    if self.musicPhase != 4:
                        self.musicPhase = 4
                        renpy.music.play("music/Capital/Purple_Planet_Music_-_Retro_Gamer_1_16_120bpm_L-40%faster.mp3", channel='music')
                        self.currentFruit.append(self.createFruit(manualChoice="Peach"))
                        self.currentFruit.append(self.createFruit(manualChoice="Blueberry"))
                        self.currentFruit.append(self.createFruit(manualChoice="Blueberry"))
                        self.currentFruit.append(self.createFruit(manualChoice="Blueberry"))
                    paradeInterval = 0.225
                    paradeExplodingOver = True
                elif self.score >= 10000:
                    paradeExplodingOver = False
                    if self.musicPhase != 3:
                        self.musicPhase = 3
                        renpy.music.play("music/Capital/Purple_Planet_Music_-_Retro_Gamer_1_16_120bpm_L-30%faster.mp3", channel='music')
                        self.currentFruit.append(self.createFruit(manualChoice="Marshmallow"))
                        self.currentFruit.append(self.createFruit(manualChoice="Blueberry"))
                        self.currentFruit.append(self.createFruit(manualChoice="Blueberry"))
                    paradeInterval = 0.275
                    paradeExplodingOver = True
                elif self.score >= 5000:
                    paradeExplodingOver = False
                    if self.musicPhase != 2:
                        self.musicPhase = 2
                        renpy.music.play("music/Capital/Purple_Planet_Music_-_Retro_Gamer_1_16_120bpm_L-20%faster.mp3", channel='music')
                        self.currentFruit.append(self.createFruit(manualChoice="Appel"))
                        self.currentFruit.append(self.createFruit(manualChoice="Blueberry"))
                    paradeInterval = 0.35
                    paradeExplodingOver = True
                elif self.score >= 500:
                    paradeExplodingOver = False
                    if self.musicPhase == 0:
                        self.musicPhase = 1
                        renpy.music.play("music/Capital/Purple_Planet_Music_-_Retro_Gamer_1_16_120bpm_L-10%faster.mp3", channel='music')
                        self.currentFruit.append(self.createFruit(manualChoice="Cherry"))
                        self.currentFruit.append(self.createFruit(manualChoice="Blueberry"))
                    paradeInterval = 0.45
                    paradeExplodingOver = True

        # All movement and collision checks are done here.
        def move(self):
            oldParadePos = self.paradePositions[:]
            self.lastTailPos = oldParadePos[-1]
            headPos = self.paradePositions[0]
            newHeadPos = (headPos[0] + self.currentDirection[0],
                        headPos[1] + self.currentDirection[1])
            self.paradePositions = [newHeadPos] + oldParadePos[:-1]
            headRect = pygame.Rect(newHeadPos, (self.paradeCellSize, self.paradeCellSize))

            self.lastRequestedDirection = self.currentDirection

            # Using pygame rect stuff to find collisions, maybe not needed anymore.
            for fruitRect in self.currentFruit:
                if not fruitRect.monching and headRect.colliderect(fruitRect.rect):
                    self.monch(fruitRect)

            # Checking collisions with parade body
            for i in range(1, len(self.paradePositions)):
                if newHeadPos == self.paradePositions[i]:
                    self.gameover = True

            # Checking if the rect is out of bounds on the left or right
            if newHeadPos[0] < (0 + self.paradeCellSize) or (newHeadPos[0] + self.paradeCellSize) > (self.area_size[0]):
                self.gameover = True
            # Checking if the rect is out of bounds on the top or bottom
            elif newHeadPos[1] < (0 + self.paradeCellSize) or (newHeadPos[1] - self.paradeCellSize) > (self.area_size[1] - self.paradeCellSize):
                self.gameover = True

            self.paradeCanMove = False

        # Event is based on pygame events, this is being checked independent of render rate,
        # so input code and gameover checks went here for optimal reaction timing
        def event(self, ev, x, y, st):

            # If the player inputs a movement, it calls for a check to see if it is legal first.
            if self.requestedDirection != (0,0):
                self.requestMove()

            # This avoids non-minigame inputs being clamped up.
            renpy.restart_interaction()

            # Constantly checks to see if gameover is True, if it does, it tallies up the score, freezes the parade movement,
            # and jumps out to the label.
            if self.gameover:
                if theParade.score > 0:
                    self.tickets = int(math.floor(theParade.score/300))
                renpy.play("sfx/Magic/poison.mp3", channel='sound')
                self.paradeFreeze = True
                renpy.jump("ParadeGameFinish")

        # This tells Ren'Py to cache all displayables that are currently alive in the minigame. Without it, huuuge stutters.
        # This is only needed because we spawn new stuff that needs blitted (i.e. render.place) into the renderer outside of init.
        def visit(self):
            parade = [renpy.displayable(member) for member in self.paradeMembers]
            fruit = [renpy.displayable(fruit.image) for fruit in self.currentFruit]
            monching = [renpy.displayable(fruit.image) for fruit in self.monchingFruit]
            return fruit + parade + monching

        # Where Ren'Py actually is told to render stuff.
        def render(self, width, height, st, at):
            # This is the canvas that the displayable will put on the screen,
            # all things happen within its walls, otherwise you don't see it even if it exists.
            render = renpy.Render(self.render_size[0], self.render_size[1])
            render_canvas = render.canvas()

            # Do the snake/parade movements provided the player has given at least one input,
            # has not already given a direction, and if the game wasn't frozen from losing.
            if self.paradeCanMove and self.paradeCanStart and not self.paradeFreeze:
                self.move()

            # Add all the objects to the canvas render. The standard bounce effect is a shader for performance.
            for pos, member in zip(self.paradePositions, self.paradeMembers):
                shader = renpy.render(member, self.paradeCellSize, self.paradeCellSize, st, at)
                shader.add_shader("bounce_shader")
                shader.add_uniform("u_paradeInterval", paradeInterval)
                render.blit(shader, pos)
            for fruit in self.currentFruit:
                if fruit.dropping:
                    if fruit.startTime is None:
                        fruit.startTime = st
                    render.place(fruit.getImage(st), x=fruit.rect.x + self.halfCellSize, y=fruit.rect.y + self.halfCellSize)
                else:
                    shader = renpy.render(fruit.getImage(st), self.paradeCellSize, self.paradeCellSize, st, at)
                    shader.add_shader("bounce_shader")
                    shader.add_uniform("u_paradeInterval", paradeInterval)
                    render.blit(shader, (fruit.rect.x, fruit.rect.y))
            for fruit in self.monchingFruit[:]:
                if fruit.monchStartTime is None:
                    fruit.monchStartTime = st
                monch_time = st - fruit.monchStartTime
                if monch_time > paradeInterval:
                    self.monchingFruit.remove(fruit)
                    continue
                render.place(fruit.getImage(st), x=fruit.rect.x + self.halfCellSize, y=fruit.rect.y + self.halfCellSize)

            # redraw ensures it is refreshing at maximum performance.
            renpy.redraw(self, 0.0)
            # We're done.
            return render

screen crtEffect():
    zorder 200
    vbox:
        xalign 0.5
        yalign 0.5
        xanchor 0.5
        yanchor 0.5
        add "crtOverlay.png"

screen ParadeGameScreen():

    key ["focus_left"] action [SetVariable("theParade.requestedDirection", (-50, 0))]
    key ["focus_right"] action [SetVariable("theParade.requestedDirection", (50, 0))]
    key ["focus_up"] action [SetVariable("theParade.requestedDirection", (0, -50))]
    key ["focus_down"] action [SetVariable("theParade.requestedDirection", (0, 50))]

    if paradeExplodingOver:
        timer paradeInterval repeat True action SetVariable("theParade.paradeCanMove", True)

    add theParade:
        align(0.5, 0.5)
        anchor(0.5, 0.5)

    hbox:
        style_prefix "quick"

        xalign 0.5
        yalign 0.01
        text _("Score: " + str(theParade.score)) size 25

    hbox:
        style_prefix "quick"
        xalign 0.5
        yalign 0.04
        text _("High Score: " + str(slimeSnakeHighScore)) size 20

    if renpy.variant("mobile"):
        fixed:
            xpos 175
            ypos 175
            imagebutton:
                idle "gui/circlebuttonlarge.png"
                hover "gui/circlebuttonlarge_Hover.png"
                insensitive "gui/circlebuttonlarge_insensitive.png"
                xpos -6
                at mobileUItransparency
            imagebutton:
                idle "gui/PadButtonR_idle.png"
                hover "gui/PadButtonR_Hover.png"
                insensitive "gui/PadButtonR_idle.png"
                xpos 100
                ypos 5
                action [SetVariable("theParade.requestedDirection", (50, 0))]
                at mobileUItransparency
            imagebutton:
                idle "gui/PadButtonU_idle.png"
                hover "gui/PadButtonU_Hover.png"
                insensitive "gui/PadButtonU_idle.png"
                #xpos 100
                ypos -95
                action [SetVariable("theParade.requestedDirection", (0, -50))]
                at mobileUItransparency
            imagebutton:
                idle "gui/PadButtonL_idle.png"
                hover "gui/PadButtonL_Hover.png"
                insensitive "gui/PadButtonL_idle.png"
                xpos -100
                ypos 5
                action [SetVariable("theParade.requestedDirection", (-50, 0))]
                at mobileUItransparency
            imagebutton:
                idle "gui/PadButtonD_idle.png"
                hover "gui/PadButtonD_Hover.png"
                insensitive "gui/PadButtonD_idle.png"
                #xpos 0
                ypos 105
                action [SetVariable("theParade.requestedDirection", (0, 50))]
                at mobileUItransparency
        fixed:
            xpos 1675
            ypos 175
            imagebutton:
                idle "gui/circlebuttonlarge.png"
                hover "gui/circlebuttonlarge_Hover.png"
                insensitive "gui/circlebuttonlarge_insensitive.png"
                xpos -6
                at mobileUItransparency
            imagebutton:
                idle "gui/PadButtonR_idle.png"
                hover "gui/PadButtonR_Hover.png"
                insensitive "gui/PadButtonR_idle.png"
                xpos 100
                ypos 5
                action [SetVariable("theParade.requestedDirection", (50, 0))]
                at mobileUItransparency
            imagebutton:
                idle "gui/PadButtonU_idle.png"
                hover "gui/PadButtonU_Hover.png"
                insensitive "gui/PadButtonU_idle.png"
                #xpos 100
                ypos -95
                action [SetVariable("theParade.requestedDirection", (0, -50))]
                at mobileUItransparency
            imagebutton:
                idle "gui/PadButtonL_idle.png"
                hover "gui/PadButtonL_Hover.png"
                insensitive "gui/PadButtonL_idle.png"
                xpos -100
                ypos 5
                action [SetVariable("theParade.requestedDirection", (-50, 0))]
                at mobileUItransparency
            imagebutton:
                idle "gui/PadButtonD_idle.png"
                hover "gui/PadButtonD_Hover.png"
                insensitive "gui/PadButtonD_idle.png"
                #xpos 0
                ypos 105
                action [SetVariable("theParade.requestedDirection", (0, 50))]
                at mobileUItransparency

    use crtEffect


label ParadeGameInit():
    $ lastReturn = copy.deepcopy(renpy.get_return_stack())
    $ renpy.set_return_stack([])
    $ showTimeofDay = 0
    if renpy.variant("touch"):
        $ minigameQuickMenuHide = 1
    $ theParade = SlimeParade()
    hide screen ON_HealthDisplay
    hide screen ON_HealthDisplayBacking
    show screen ParadeGameScreen
    jump ParadeGameLoop

label ParadeGameLoop:
    window hide
    pause
    jump ParadeGameLoop

label ParadeGameFinish:
    $ theParade.gameover = False
    $ paradeExplodingOver = True
    $ renpy.set_return_stack(lastReturn)
    if slimeSnakeHighScore < theParade.score:
        $ slimeSnakeHighScore = theParade.score
        "The parade of the Slime Queen has ended! \n\nGAME OVER - You earned [theParade.tickets] tickets!\n\nYou got a new high score of [slimeSnakeHighScore]!!!"
    else:
        "The parade of the Slime Queen has ended! \n\nGAME OVER - You earned [theParade.tickets] tickets!"
    $ ProgressEvent[DataLocation].eventProgress += theParade.tickets
    $ CheckEvent = getFromName("GameSkillTracker", ProgressEvent) #jank hard coding to account game skill things
    $ ProgressEvent[CheckEvent].eventProgress += int(math.floor(theParade.tickets*0.05))
    show screen ON_HealthDisplay
    show screen ON_HealthDisplayBacking
    hide screen ParadeGameScreen
    hide screen crtEffect
    $ minigameQuickMenuHide = 0
    $ showTimeofDay = 1
    return
