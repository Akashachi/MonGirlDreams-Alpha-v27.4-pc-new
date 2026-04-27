label AdventuringDeckClass:
    python:
        class AdventuringDeck:
            def __init__(self, name="", description="", requires=[""], requiresEvent=[], deck=[], randomEvents=[], randomMonsters=[], monsterGroups=[], Treasure=[], Eros=[], questComplete=0):
                self.name = name #the event name
                self.description = description
                self.requires = requires
                self.requiresEvent = requiresEvent
                self.deck = deck
                self.randomEvents = randomEvents
                self.randomMonsters = randomMonsters
                self.monsterGroups = monsterGroups
                self.Treasure = Treasure
                self.Eros = Eros
                self.questComplete = questComplete

        class theSpeaker:
            def __init__(self, name="", postName="", SpeakerType=""):
                self.name = name #the speaker name
                self.postName = postName
                self.SpeakerType = SpeakerType


        class Event:
            def __init__(self, name="", description="", CardType="", CardLimit=0, Speakers=[], theEvents=[], timesSeen=0, lastChoice="", eventProgress=0, choices=[], requires=[""], requiresEvent=[], questComplete=0):
                self.name = name #the event name
                self.description = description
                self.CardType = CardType
                self.CardLimit = CardLimit
                self.Speakers = Speakers
                self.theEvents = theEvents
                self.timesSeen = timesSeen
                self.lastChoice = lastChoice
                self.eventProgress = eventProgress
                self.choices = choices
                self.requires = requires
                self.requiresEvent = requiresEvent
                self.questComplete = questComplete

        class Location:
            def __init__(self, name="", exploreTitle="",
                mapIcon="", mapIconXpos="", mapIconYpos="", mapIconZorder="", mapClouds="", mapCloudsXpos="", mapCloudsYpos="",
                Monsters=[],  MonsterGroups=[], Events=[], Quests=[],Adventures=[], Treasure=[], Eros=[],
                MinimumDeckSize=0, MaximumMonsterDeck=0, MaximumEventDeck=0,  picture="", requires = [""], requiresEvent = [], FullyUnlockedBy= [""], FullyUnlockedByEvent=[], MusicList=[""], ExplorationUnlockedBy= [""], ExplorationUnlockedByEvent= [], nightmare=0):
                self.name = name #the kind of trigger, usesMove, OpponentHpLow, OwnHpLow, Onloss,
                self.exploreTitle = exploreTitle
                self.mapIcon = mapIcon
                self.mapIconXpos = mapIconXpos
                self.mapIconYpos = mapIconYpos
                self.mapIconZorder = mapIconZorder
                self.mapClouds = mapClouds
                self.mapCloudsXpos = mapCloudsXpos
                self.mapCloudsYpos = mapCloudsYpos
                self.Monsters = Monsters
                self.MonsterGroups = MonsterGroups #name of move that triggers the line
                self.Events = Events #full scene text
                self.Quests = Quests
                self.Adventures = Adventures
                self.Treasure = Treasure
                self.Eros = Eros
                self.MinimumDeckSize = MinimumDeckSize
                self.MaximumMonsterDeck = MaximumMonsterDeck
                self.MaximumEventDeck = MaximumEventDeck

                self.MusicList=MusicList

                self.picture = picture
                self.requires = requires
                self.requiresEvent = requiresEvent
                self.FullyUnlockedBy = FullyUnlockedBy
                self.FullyUnlockedByEvent = FullyUnlockedByEvent
                self.ExplorationUnlockedBy = ExplorationUnlockedBy
                self.ExplorationUnlockedByEvent = ExplorationUnlockedByEvent

                self.nightmare = nightmare
