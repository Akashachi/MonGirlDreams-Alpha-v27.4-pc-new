# Validator started by dfs on hypnopics collective, reworked and greatly expanded three and a half times by fcmcl for game updates, features, maintainability, and performance.

"""renpy
init python:
"""
import copy
import json
import re

class LoadValidator:
    def __init__(self, enabled=True):
        self.enabled = enabled

        self.eventFileName = ""

        self.inLoop = False
        self.currentFunc = ""
        self.lastLoopedFunc = ""

        self.jumpSourceCounters = dict()
        self.jumpTargetCounters = dict()

        self.choiceSourceDatabase = dict()
        self.choiceTargetDatabase = dict()

        self.IDDatabase = {
            "Fetishes": dict(),
            "Skills": dict(),
            "Perks": dict(),
            "Items": dict(),
            "Monsters": dict(),
            "Events": dict(),
            "Locations": dict(),
            "Adventures": dict(),
            "Stances": dict()
        }
        self.IDDatabaseChecks = {
            "Fetishes": dict(),
            "Skills": dict(),
            "Perks": dict(),
            "Items": dict(),
            "Monsters": dict(),
            "Events": dict(),
            "Locations": dict(),
            "Adventures": dict(),
            "Stances": dict()
        }
        self.delayedChecks = list()
        self.ignoredChoices = dict()


        # Choice funcs to do additional checks on.
        self.choiceChecks = {
            "RequiresChoice": None,
            "RequiresChoiceFromEvent": None,
            "IfChoice": None,
            "GetEventAndIfChoice": None
        }
        self.choiceSets = {
            "SetChoice": None,
            "GetEventAndSetChoice": None
        }

        # Name checks
        self.skillNameChecks = {
            "IfMonsterHasSkill": None,
            "IfHasSkill": None,
            "GiveSkillToMonster": None,
            "RemoveSkillFromMonster": None,
            "IfPlayerIsUsingThisSkill": None,
            "ApplyStatusEffectToMonster": None,
            "HitMonsterWith": None,
            "HitPlayerWith": None,
            "SetAttack": None,
            "GiveSkill": None,
            "RemoveSkillFromPlayer": None,
            "GiveSkillQuietly": None,
            "RemoveSkillFromPlayerQuietly": None,
            "RemoveSkillFromPlayerTemporarily": None,
            "ApplyStatusEffect": None
        }
        self.skillNameChecks00 = {
            "CallMonsterAttack": None, # has gotcha, pends on SpecificAttack which is conditional so be cautious of code causing index errors
            "DamagePlayerFromMonster": None,
            "DamageMonsterFromMonster": None
        }
        self.skillNameChecksLoops = {
            "SkillShoppingMenu": None,
            "IfHasSkills": None
        }

        self.eventNameChecks = {
            "GetEventAndIfChoice": None,
            "GetEventAndSetChoice": None,
            "ChoiceToDisplayPlayerFromOtherEvent": None,
            "SetChoiceToPlayerNameFromOtherEvent": None,
            "GetEventAndChangeProgress": None,
            "GetEventAndSetProgress": None,
            "GetAnEventsProgressThenIfEquals": None,
            "GetAnEventsProgressThenIfEqualsOrGreater": None,
            "GetAnEventsProgressThenIfEqualsOrLess": None,
            "EventsProgressEqualsOtherEventsProgress": None,
            "EventJump": None,
            "RequiresMinimumProgressFromEvent": None,
            "RequiresLessProgressFromEvent": None,
            "RequiresChoiceFromEvent": None,
            "IfEventExists": None,
            "JumpToEvent": None,
            "JumpToNPCEvent": None,
            "JumpToLossEvent": None,
            "JumpToEventThenScene": None,
            "CallCombatEventAndScene": None,
            "JumpToNPCEventThenScene": None,
            "CallEventAndSceneThenReturn": None,
            "OtherEventsChoice": None,
            "OtherEventsProgress": None
        }
        self.eventNameChecksTwo = {
            "EventsProgressEqualsOtherEventsProgress": None,
            "IfEventsProgressEqualsOrLessThanOtherEventsProgress": None,
            "EventsProgressEqualsOrGreaterThanOtherEventsProgress": None
        }

        self.itemNameChecks = {
            "IfHasItemEquipped": None,
            "IfDoesntHaveItemEquipped": None,
            "IfHasItems": None,
            "IfDoesntHaveItems": None,
            "IfHasItem": None,
            "IfDoesntHaveItem": None,
            "IfHasItemInInventory": None,
            "IfHasRunesEquipped": None,
            "IfDoesntHaveItemInInventory": None,
        }
        self.itemNameChecksTwo = {
            "GiveItem": None,
            "GiveItemQuietly": None
        }
        self.itemNameChecksLoop = {
            "ShoppingMenu": None,
            "IfHasSkills": None
        }

        self.monsterNameChecks = {
            "IfThisMonsterIsInEncounter": None,
            "IfOtherMonsterHasStatusEffect": None,
            "ApplyStanceToOtherMonster": None,
            "IfOtherMonsterHasStance": None,
            "IfOtherMonsterDoesntHaveStance": None,
            "DamagePlayerFromMonster": None,
            "DamageMonsterFromMonster": None
        }
        self.monsterNameChecks00 = {
            "AddMonsterToEncounter": None
        }
        self.monsterNameCheckLoop = {
            "DisplayCharacters": None
        }

        self.perkNameChecks = {
            "RequiresPerk": None,
            "IfHasPerk": None,
            "GivePerkToMonster": None,
            "IfMonsterHasPerk": None,
            "ChangePerkDuration": None,
            "GivePerk": None,
            "RemovePerk": None,
            "GivePerkQuietly": None,
            "RemovePerkQuietly": None
        }
        self.fetishNameChecks = {
            "SetFetish": None,
            "IfHasFetish": None,
            "IfFetishLevelEqualOrGreater": None,
            "ChangeMonsterFetish": None,
            "ChangeFetish": None,
            "PermanentlyChangeFetish": None,
            "HasFetishLevelEqualOrGreater": None
        }

        self.monsterNameEncounter = {
            "NoRunning": None,
            "RunningWontSkipEvent": None,
            "DenyInventory": None,
            "Restrainer": None
        }
        self.monsterNameEncounter00 = {
            "SetBGOnRun": None,
        }
        # "Menu"
        self.listSkipCurrent = {
            "HideOptionOnRequirementFail": None,
            "FinalOption": None,
            "InverseRequirement": None,
            "ShuffleMenu": None,
            "ThenJumpToScene": None
        }
        self.listSkip0 = {
            "RequiresEnergy": None,
            "RequiresSkill": None,
            "RequiresVirility": None,
            "RequiresPerk": None,
            "RequiresItem": None,
            "RequiresItemEquipped": None,
            "RequiresMinimumProgress": None,
            "RequiresLessProgress": None,
            "RequiresTime": None,
            "MaxMenuSlots": None,
            "EventJump": None
        }
        self.listSkip00 = {
            "RequiresChoice": None,
            "RequiresFetishLevelEqualOrGreater": None,
            "RequiresFetishLevelEqualOrLess": None,
            "RequiresMinimumProgressFromEvent": None,
            "RequiresLessProgressFromEvent": None,
            "RequiresStat": None
        }
        self.listSkip000 = {
            "RequiresChoiceFromEvent": None
        }

        # "StatCheck"
        self.statListSkip00 = {
            "IfPlayerHasStatusEffect": None,
            "IfHasPerk": None,
            "IfHasFetish": None,
            "IfVirilityEqualOrGreater": None,
            "IfMonsterLevelGreaterThan": None,
            "IfEncounterSizeGreaterOrEqualTo": None,
            "IfEncounterSizeLessOrEqualTo": None,
            "IfProgressEqualsOrGreater": None
        }
        self.statListSkip000 = {
            "IfFetishLevelEqualOrGreater": None,
            "IfPlayerHasStatusEffectWithPotencyEqualOrGreater": None,
            "GetAnEventsProgressThenIfEqualsOrGreater": None,
            "IfChoice": None
        }
        self.statListSkip0000 = {
            "GetEventAndIfChoice": None
        }
        # self.stanceNameChecks = {
        #     "ApplyStance": None
        #     "ClearStanceFromMonsterAndPlayer": None
        #     "IfPlayerHasStance": None
        #     "IfPlayerDoesntHaveStance": None
        #     "IfMonsterHasStance": None
        #     "IfPlayerHasStances": None
        #     "IfMonsterDoesntHaveStance": None
        # }
        # self.stanceNameChecks00 = {
        #     "ApplyStanceToOtherMonster": None
        #     "IfOtherMonsterHasStance": None
        #     "IfOtherMonsterDoesntHaveStance": None
        # }
        # self.monsterNameEncounterStance = {
        #     "ApplyStance": None
        # }
        self.funcMap = {
            # Skills
            "IfMonsterHasSkill": [(self.handleJump01, []), (lambda **kwargs: self.handleNameChecks(database="Skills", **kwargs), [])],
            "IfHasSkill": [(self.handleJump01, []), (lambda **kwargs: self.handleNameChecks(database="Skills", **kwargs), [])],
            "GiveSkillToMonster": [(lambda **kwargs: self.handleNameChecks(database="Skills", **kwargs), [])],
            "RemoveSkillFromMonster": [(lambda **kwargs: self.handleNameChecks(database="Skills", **kwargs), [])],
            "IfPlayerIsUsingThisSkill": [(self.handleJump01, []), (lambda **kwargs: self.handleNameChecks(database="Skills", **kwargs), [])],
            "ApplyStatusEffectToMonster": [(lambda **kwargs: self.handleNameChecks(database="Skills", **kwargs), [])],
            "HitMonsterWith": [(lambda **kwargs: self.handleNameChecks(database="Skills", **kwargs), [])],
            "HitPlayerWith": [(lambda **kwargs: self.handleNameChecks(database="Skills", **kwargs), [])],
            "SetAttack": [(lambda **kwargs: self.handleNameChecks(database="Skills", **kwargs), [])],
            "GiveSkill": [(lambda **kwargs: self.handleNameChecks(database="Skills", **kwargs), [])],
            "RemoveSkillFromPlayer": [(lambda **kwargs: self.handleNameChecks(database="Skills", **kwargs), [])],
            "GiveSkillQuietly": [(lambda **kwargs: self.handleNameChecks(database="Skills", **kwargs), [])],
            "RemoveSkillFromPlayerQuietly": [(lambda **kwargs: self.handleNameChecks(database="Skills", **kwargs), [])],
            "RemoveSkillFromPlayerTemporarily": [(lambda **kwargs: self.handleNameChecks(database="Skills", **kwargs), [])],
            "ApplyStatusEffect": [(lambda **kwargs: self.handleNameChecks(database="Skills", **kwargs), [])],

            "CallMonsterAttack": [(lambda **kwargs: self.handleNameChecks00(database="Skills", **kwargs), [])],
            "DamagePlayerFromMonster": [(lambda **kwargs: self.handleNameChecks(database="Monsters", **kwargs), []), (lambda **kwargs: self.handleNameChecks00(database="Skills", **kwargs), [])],
            "DamageMonsterFromMonster": [(lambda **kwargs: self.handleNameChecks(database="Monsters", **kwargs), []), (lambda **kwargs: self.handleNameChecks00(database="Skills", **kwargs), [])],


            "SkillShoppingMenu": [(lambda **kwargs: self.handleNameChecksLoop(database="Skills", optionalIgnores=["PurchasesToProgress"], **kwargs), [])],
            "IfHasSkills": [(self.handleLoopedJump, []), (lambda **kwargs: self.handleNameChecksLoop(database="Skills", **kwargs), [])],

            # Events
            "GetEventAndIfChoice": [(self.handleJump0001, []), (self.handleChoiceCheck, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "GetEventAndSetChoice": [(self.handleChoiceSet, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "ChoiceToDisplayPlayerFromOtherEvent": [(lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "SetChoiceToPlayerNameFromOtherEvent": [(lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "GetEventAndChangeProgress": [(lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "GetEventAndSetProgress": [(lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "GetAnEventsProgressThenIfEquals": [(self.handleJump001, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "GetAnEventsProgressThenIfEqualsOrGreater": [(self.handleJump001, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "GetAnEventsProgressThenIfEqualsOrLess": [(self.handleJump001, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "EventsProgressEqualsOtherEventsProgress": [(self.handleJump001, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), []), (lambda **kwargs: self.handleNameChecksTwo(database="Events", **kwargs), [])],
            "IfEventsProgressEqualsOrLessThanOtherEventsProgress": [(self.handleJump001, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), []), (lambda **kwargs: self.handleNameChecksTwo(database="Events", **kwargs), [])],
            "EventsProgressEqualsOrGreaterThanOtherEventsProgress": [(self.handleJump001, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), []), (lambda **kwargs: self.handleNameChecksTwo(database="Events", **kwargs), [])],
            "EventJump": [(self.handleJump01, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "RequiresMinimumProgressFromEvent": [(self.handleJump01, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "RequiresLessProgressFromEvent": [(self.handleJump01, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "RequiresChoiceFromEvent": [(self.handleJump001, []), (self.handleChoiceCheck, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "IfEventExists": [(self.handleJump01, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "JumpToEvent": [(lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "JumpToNPCEvent": [(lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "JumpToLossEvent": [(lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "JumpToEventThenScene": [(self.handleEventJumps21, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "CallCombatEventAndScene": [(self.handleEventJumps21, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "JumpToNPCEventThenScene": [(self.handleEventJumps21, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "CallEventAndSceneThenReturn": [(self.handleEventJumps21, []), (lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "OtherEventsChoice": [(lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],
            "OtherEventsProgress": [(lambda **kwargs: self.handleNameChecks(database="Events", **kwargs), [])],

            # Items
            "IfHasItemEquipped": [(self.handleTagJumps, []), (lambda **kwargs: self.handleNameChecks(database="Items", optionalIgnores=["Tags"], **kwargs), [])],
            "IfDoesntHaveItemEquipped": [(self.handleTagJumps, []), (lambda **kwargs: self.handleNameChecks(database="Items", optionalIgnores=["Tags"], **kwargs), [])],
            "IfHasItems": [(self.handleLoopedJump, []), (lambda **kwargs: self.handleNameChecks(database="Items", optionalIgnores=["Tags"], **kwargs), [])],
            "IfDoesntHaveItems": [(self.handleLoopedJump, []), (lambda **kwargs: self.handleNameChecks(database="Items", optionalIgnores=["Tags"], **kwargs), [])],
            "IfHasItem": [(self.handleTagJumps, []), (lambda **kwargs: self.handleNameChecks(database="Items", optionalIgnores=["Tags"], **kwargs), [])],
            "IfDoesntHaveItem": [(self.handleTagJumps, []), (lambda **kwargs: self.handleNameChecks(database="Items", optionalIgnores=["Tags"], **kwargs), [])],
            "IfHasItemInInventory": [(self.handleTagJumps, []), (lambda **kwargs: self.handleNameChecks(database="Items", optionalIgnores=["Tags"], **kwargs), [])],
            "IfHasRunesEquipped": [(self.handleTagJumps, []), (lambda **kwargs: self.handleNameChecks(database="Items", optionalIgnores=["Tags"], **kwargs), [])],
            "IfDoesntHaveItemInInventory": [(self.handleTagJumps, []), (lambda **kwargs: self.handleNameChecks(database="Items", optionalIgnores=["Tags"], **kwargs), [])],

            "GiveItem": [(lambda **kwargs: self.handleNameChecksTwo(database="Items", **kwargs), [])],
            "GiveItemQuietly": [(lambda **kwargs: self.handleNameChecksTwo(database="Items", **kwargs), [])],

            "ShoppingMenu": [(lambda **kwargs: self.handleNameChecksLoop(database="Items", optionalIgnores=["PurchasesToProgress", "NoSelling"], **kwargs), [])],

            # Monsters
            "IfThisMonsterIsInEncounter": [(self.handleJump01, []), (lambda **kwargs: self.handleNameChecks(database="Monsters", **kwargs), [])],
            "IfOtherMonsterHasStatusEffect": [(self.handleJump01, []), (lambda **kwargs: self.handleNameChecks(database="Monsters", **kwargs), [])],
            "ApplyStanceToOtherMonster": [(self.handleJump001, []), (lambda **kwargs: self.handleNameChecks(database="Monsters", **kwargs), [])],
            "IfOtherMonsterHasStance": [(self.handleJump001, []), (lambda **kwargs: self.handleNameChecks(database="Monsters", **kwargs), [])],
            "IfOtherMonsterDoesntHaveStance": [(self.handleJump001, []), (lambda **kwargs: self.handleNameChecks(database="Monsters", **kwargs), [])],

            "AddMonsterToEncounter": [(lambda **kwargs: self.handleNameChecks(database="Monsters", **kwargs), [])],

            "DisplayCharacters": [(lambda **kwargs: self.handleNameCheckLoop(database="Monsters", ignoreNumbers=True, **kwargs), [])],

            # Perks
            "RequiresPerk": [(self.handleJump01, []), (lambda **kwargs: self.handleNameChecks(database="Perks", **kwargs), [])],
            "IfHasPerk": [(self.handleJump01, []), (lambda **kwargs: self.handleNameChecks(database="Perks", **kwargs), [])],
            "GivePerkToMonster": [(lambda **kwargs: self.handleNameChecks(database="Perks", **kwargs), [])],
            "IfMonsterHasPerk": [(self.handleJump01, []), (lambda **kwargs: self.handleNameChecks(database="Perks", **kwargs), [])],
            "ChangePerkDuration": [(lambda **kwargs: self.handleNameChecks(database="Perks", **kwargs), [])],
            "GivePerk": [(lambda **kwargs: self.handleNameChecks(database="Perks", **kwargs), [])],
            "RemovePerk": [(lambda **kwargs: self.handleNameChecks(database="Perks", **kwargs), [])],
            "GivePerkQuietly": [(lambda **kwargs: self.handleNameChecks(database="Perks", **kwargs), [])],
            "RemovePerkQuietly": [(lambda **kwargs: self.handleNameChecks(database="Perks", **kwargs), [])],

            # Fetishes
            "SetFetish": [(lambda **kwargs: self.handleNameChecks(database="Fetishes", **kwargs), [])],
            "IfHasFetish": [(self.handleJump01, []), (lambda **kwargs: self.handleNameChecks(database="Fetishes", **kwargs), [])],
            "IfFetishLevelEqualOrGreater": [(self.handleJump001, []), (lambda **kwargs: self.handleNameChecks(database="Fetishes", **kwargs), [])],
            "ChangeMonsterFetish": [(lambda **kwargs: self.handleNameChecks(database="Fetishes", **kwargs), [])],
            "ChangeFetish": [(lambda **kwargs: self.handleNameChecks(database="Fetishes", **kwargs), [])],
            "PermanentlyChangeFetish": [(lambda **kwargs: self.handleNameChecks(database="Fetishes", **kwargs), [])],
            "HasFetishLevelEqualOrGreater": [(self.handleJump01, []), (lambda **kwargs: self.handleNameChecks(database="Fetishes", **kwargs), [])],

            # TODO: Organize
            "ForEvery": [(lambda **kwargs: self.handleNameChecks(database="Monsters", **kwargs), [])],
            "ForSpecific": [(lambda **kwargs: self.handleNameChecks(database="Monsters", **kwargs), [])],
            "IfInExploration": [(self.handleJump1, [])],
            "IfRanAway": [(self.handleJump1, [])],
            "FishingPassJump": [(self.handleJump1, [])],
            "FishingFailJump": [(self.handleJump1, [])],
            "IfMonsterOrgasm": [(self.handleJump1, [])],
            "IfMonsterSpiritGone": [(self.handleJump1, [])],
            "IfMonsterEnergyGone": [(self.handleJump1, [])],
            "IfPlayerOrgasm": [(self.handleJump1, [])],
            "IfPlayerEnergyGone": [(self.handleJump1, [])],
            "IfPlayerSpiritGone": [(self.handleJump1, [])],
            "IfPlayerStunnedByParalysis": [(self.handleJump1, [])],
            "IfHealingSickness": [(self.handleJump1, [])],
            "IfDelayingNotifications": [(self.handleJump1, [])],
            "IfAttackCrits": [(self.handleJump1, [])],
            "IfGridPlayerStunned": [(self.handleJump1, [])],
            "IfGridVisonOn": [(self.handleJump1, [])],
            "JumpToScene": [(self.handleJump1, [])],
            "CallSceneThenReturn": [(self.handleJump1, [])],
            "HasErosLessThanInput": [(self.handleJump1, [])],

            "EncounterSizeGreaterOrEqualTo": [(self.handleJump01, [])],
            "EncounterSizeLessOrEqualTo": [(self.handleJump01, [])],
            "IfDifficultyIs": [(self.handleJump01, [])],
            "IfTimeIs": [(self.handleJump01, [])],
            "IfPlayerEnergyLessThanPercent": [(self.handleJump01, [])],
            "IfPlayerLevelGreaterThan": [(self.handleJump01, [])],
            "IfPlayerArousalOverPercentOfMax": [(self.handleJump01, [])],
            "HasErosLessThan": [(self.handleJump01, [])],
            "IfProgressEquals": [(self.handleJump01, [])],
            "IfProgressEqualsOrGreater": [(self.handleJump01, [])],
            "IfProgressEqualsOrLess": [(self.handleJump01, [])],
            "VirilityEqualsOrGreater": [(self.handleJump01, [])],
            "IfGridNPCThere": [(self.handleJump01, [])],
            "IfInputEquals": [(self.handleJump01, [])],
            "IfInputEqualsOrLessThan": [(self.handleJump01, [])],

            "IfMonsterHasStance": [(self.handleJump01, [])],
            "IfMonsterDoesntHaveStance": [(self.handleJump01, [])],
            "IfMonsterLevelGreaterThan": [(self.handleJump01, [])],
            "IfMonsterArousalGreaterThan": [(self.handleJump01, [])],
            "IfPlayerHasStances": [(self.handleLoopedJump, [])],
            "IfPlayerHasStance": [(self.handleJump01, [])],
            "IfPlayerDoesntHaveStance": [(self.handleJump01, [])],

            "SetChoice": [(self.handleChoiceSet, [])],
            "IfChoice": [(self.handleJump001, []), (self.handleChoiceCheck, [])],
            "IfSensitivityEqualOrGreater": [(self.handleJump001, [])],
            "StatEqualsOrMore": [(self.handleJump001, [])],

            "IfPlayerHasStatusEffectWithPotencyEqualOrGreater": [(self.handleStatusJumpPotency, [])],
            "IfMonsterHasStatusEffectWithPotencyEqualOrGreater": [(self.handleStatusJumpPotency, [])],

            "IfPlayerHasStatusEffect": [(self.handleStatusJumpLoop, [])],
            "IfPlayerDoesntHaveStatusEffect": [(self.handleStatusJumpLoop, [])],
            "IfMonsterHasStatusEffect": [(self.handleStatusJumpLoop, [])],
            "IfMonsterDoesntHaveStatusEffect": [(self.handleStatusJumpLoop, [])],
            "IfOtherMonsterHasStatusEffect": [(self.handleStatusJumpLoop, [])],
            "IfOtherMonsterDoesntHaveStatusEffect": [(self.handleStatusJumpLoop, [])],

            "TurnEvent": [(self.handleEventJumps21, [])],

            "IfGridNPCSeesPlayer": [(self.handleIfGridNpcSeesPlayer, [])],
            "CombatEncounter": [(self.handleCombatEncounter, [])],

            "Menu": [(self.handleMenu, [])],
            "JumpToRandomScene": [(self.handleMenu, [])],
            "MenuAddition": [(self.handleMenu, [])],
            "StatCheck": [(self.handleStatCheck, [])],
            "StatCheckRollUnder": [(self.handleStatCheck, [])],
            "SwapLineIf": [(self.handleSwapLineIf, [])],
            "GoToMap": [(self.handleGoToMap, [])]
        }
        self.listTagJumps = {
            "IfHasItem": None,
            "IfDoesntHaveItem": None,
            "IfHasItemEquipped": None,
            "IfDoesntHaveItemEquipped": None
        }
        self.listTagJumps01 = {
            "IfHasItemInInventory": None,
            "IfDoesntHaveItemInInventory": None,
            "IfHasRunesEquipped": None
        }
        self.listTimeParams = {
            "Day": None,
            "Night": None,
            "DayFaked": None,
            "NightFaked": None,
            "NightTrue": None,
            "DayTrue": None,
            "Morning": None,
            "Noon": None,
            "Afternoon": None,
            "Dusk": None,
            "Evening": None,
            "Midnight": None
        }

    # Name Funcs
    def handleNameChecks(self, database, optionalIgnores=[], eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            self.storeIDCheck(eventText.theScene[index + 1], eventName, database, "Events", eventText.NameOfScene, jsonType=jsonType, optionalIgnores=optionalIgnores)
    def handleNameChecks00(self, database, optionalIgnores=[], eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            if index + 1 < len(eventText.theScene):
                if value == "CallMonsterAttack":
                    if eventText.theScene[index + 1] == "SpecificAttack":
                        self.storeIDCheck(eventText.theScene[index + 2], eventName, database, "Events", eventText.NameOfScene, jsonType=jsonType, optionalIgnores=optionalIgnores)
                else:
                    self.storeIDCheck(eventText.theScene[index + 2], eventName, database, "Events", eventText.NameOfScene, jsonType=jsonType, optionalIgnores=optionalIgnores)
    def handleNameChecksTwo(self, database, optionalIgnores=[], eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            self.storeIDCheck(eventText.theScene[index + 2], eventName, database, "Events", eventText.NameOfScene, jsonType=jsonType, optionalIgnores=optionalIgnores)
    def handleNameChecksLoop(self, database, optionalIgnores=[], eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            tempIndex = index + 1
            while tempIndex < len(eventText.theScene):
                if eventText.theScene[tempIndex] == "EndLoop":
                    break
                self.storeIDCheck(eventText.theScene[tempIndex], eventName, database, "Events", eventText.NameOfScene, jsonType=jsonType, optionalIgnores=optionalIgnores)
                tempIndex += 1
    def handleNameCheckLoop(self, database, optionalIgnores=[], ignoreNumbers=False, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            tempIndex = index + 1
            while tempIndex < len(eventText.theScene):
                if eventText.theScene[tempIndex] == "EndLoop":
                    break
                self.storeIDCheck(eventText.theScene[tempIndex], eventName, database, "Events", eventText.NameOfScene, ignoreNumbers=ignoreNumbers, jsonType=jsonType, optionalIgnores=optionalIgnores)
                tempIndex += 1

    # Choice Funcs
    def ignoreChoice(self, eventName, choiceNumber, choiceValue):
        if eventName in self.ignoredChoices and str(choiceNumber) in self.ignoredChoices[eventName]:
            ignored = self.ignoredChoices[eventName][str(choiceNumber)]
            return not ignored or choiceValue in ignored
    def filterChoices(self, choiceDatabase):
        filtered = {}
        for eventName, choices in choiceDatabase.items():
            filtered[eventName] = {}
            for choiceNumber, choiceValues in choices.items():
                filtered[eventName][choiceNumber] = {
                    value for value in choiceValues
                    if not self.ignoreChoice(eventName, choiceNumber, value)
                }
                if not filtered[eventName][choiceNumber]:
                    del filtered[eventName][choiceNumber]
            if not filtered[eventName]:
                del filtered[eventName]
        return filtered

    def addChoiceSource(self, eventName, choiceNumber, choiceValue):
        if eventName != "" and choiceNumber != "-1":
            if eventName not in self.choiceSourceDatabase:
                self.choiceSourceDatabase[eventName] = {}
            if choiceNumber not in self.choiceSourceDatabase[eventName]:
                self.choiceSourceDatabase[eventName][choiceNumber] = set()
            self.choiceSourceDatabase[eventName][choiceNumber].add(choiceValue)

    def addChoiceTarget(self, eventName, choiceNumber, choiceValue):
        if eventName not in self.choiceTargetDatabase:
            self.choiceTargetDatabase[eventName] = {}
        if choiceNumber not in self.choiceTargetDatabase[eventName]:
            self.choiceTargetDatabase[eventName][choiceNumber] = set()
        self.choiceTargetDatabase[eventName][choiceNumber].add(choiceValue)

    # Scene Funcs
    def addSource(self, eventName, sceneName):
        source = (eventName, sceneName)
        self.jumpSourceCounters[source] = self.jumpSourceCounters.get(source, 0) + 1

    def addTarget(self, eventName, sceneName, optional=False):
        if sceneName[0] == '_' or sceneName[:5] in ["Debug", "debug", "Event", "event"]:
            optional = True

        target = (eventName, sceneName)
        if optional:
            self.jumpTargetCounters[target] = 0
        elif target in self.jumpTargetCounters:
            self.jumpTargetCounters[target] += 1
        else:
            self.jumpTargetCounters[target] = 1

    # IDname Funcs
    def addIDToDatabase(self, IDname, database):
        if database in self.IDDatabase:
            self.IDDatabase[database][IDname] = True
        else:
            raise ValueError(f"'{database}' does not exist.")

    def validateIDname(self, IDnameCheck, IDnameSource, databaseInput, databaseOutput, theKey, optionalIgnores=[], ignoreNumbers=False, jsonType="Events"):
        if IDnameCheck != "":
            if databaseInput in self.IDDatabase:
                if IDnameCheck in self.IDDatabase[databaseInput]:
                    pass
                elif IDnameCheck in optionalIgnores:
                    pass
                elif ignoreNumbers and IDnameCheck.isdigit():
                    pass
                elif jsonType == "Events" and theKey not in ["CardType", "Description", "requires", "Speakers"]:
                    if IDnameSource not in self.IDDatabaseChecks[jsonType]:
                        self.IDDatabaseChecks[jsonType][IDnameSource] = dict()
                    if "EventText" not in self.IDDatabaseChecks[jsonType][IDnameSource]:
                        self.IDDatabaseChecks[jsonType][IDnameSource]["EventText"] = dict()
                    if theKey not in self.IDDatabaseChecks[jsonType][IDnameSource]["EventText"]:
                        self.IDDatabaseChecks[jsonType][IDnameSource]["EventText"][theKey] = list()
                    self.IDDatabaseChecks[jsonType][IDnameSource]["EventText"][theKey].append(IDnameCheck)
                elif IDnameCheck not in self.IDDatabase[databaseInput]:
                    if IDnameSource not in self.IDDatabaseChecks[jsonType]:
                        self.IDDatabaseChecks[jsonType][IDnameSource] = dict()
                    if theKey not in self.IDDatabaseChecks[jsonType][IDnameSource]:
                        self.IDDatabaseChecks[jsonType][IDnameSource][theKey] = list()
                    self.IDDatabaseChecks[jsonType][IDnameSource][theKey].append(IDnameCheck)
            else:
                raise ValueError(f"'{databaseInput}' does not exist.")

    # Delayed Check Funcs
    def storeIDCheck(self, IDnameCheck, IDnameSource, databaseInput, databaseOutput, theKey, optionalIgnores=[], ignoreNumbers=False, jsonType=""):
        self.delayedChecks.append((IDnameCheck, IDnameSource, databaseInput, databaseOutput, theKey, optionalIgnores, ignoreNumbers, jsonType))

    def beginDelayedChecks(self):
        for check in self.delayedChecks:
            IDnameCheck, IDnameSource, databaseInput, databaseOutput, theKey, optionalIgnores, ignoreNumbers, jsonType = check
            self.validateIDname(IDnameCheck, IDnameSource, databaseInput, databaseOutput, theKey, list(optionalIgnores), ignoreNumbers, jsonType)
    # Event Validation
    def checkEventText(self, eventName, eventText, fileName, jsonType): # Third and a half rewrite, in totality by fcmcl, second by dfs, thresh does not remember the first.
        if not self.enabled:
            return

        is_first_in_file = (self.eventFileName != fileName)
        self.eventFileName = fileName
        the_scene = eventText.theScene
        scene_len = len(the_scene)

        self.inLoop = False
        for index in range(scene_len):
            value = the_scene[index]
            if value == "EndLoop" and self.inLoop == True:
                self.inLoop = False
                self.lastLoopedFunc = ""
            elif value in self.funcMap:
                for func, funcArgs in self.funcMap[value]:
                    self.currentFunc = value
                    # print(f"Debug value: '{value}'")
                    # print(f"  func: {func.__name__}")
                    # print(f"  funcArgs: {funcArgs}")
                    # print(f"  eventName: {eventName}")
                    # print(f"  index: {index}")
                    # print(f"  jsonType: {jsonType}")
                    # try:
                    func(*funcArgs, eventName=eventName, eventText=eventText, index=index, jsonType=jsonType, value=value)
                    # except TypeError as e:
                    #     print(f"TypeError occurred: {str(e)}")
                    #     print(f"Value: {value}")
                    #     print(f"Function: {func.__name__}")
                    #     print(f"Arguments: {funcArgs}")
                    #     raise
            else:
                pass
                # TODO: Optional word count stuff minus markup n other things.
            if self.inLoop == True and not self.lastLoopedFunc:
                self.lastLoopedFunc = self.currentFunc

        # Lastly, save this scene's name as a potential jump command target
        if eventText.NameOfScene != "":
            is_victory_loss = isinstance(eventText, LossScene)  # type: ignore
            self.addTarget(eventName, eventText.NameOfScene, is_victory_loss or is_first_in_file)


    def handleJump1(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            try:
                self.addSource(eventName, eventText.theScene[index + 1])
            except IndexError:
                pass
        else:
            pass

    def handleJump01(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            try:
                self.addSource(eventName, eventText.theScene[index + 2])
            except IndexError:
                pass
        else:
            pass

    def handleJump001(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            try:
                self.addSource(eventName, eventText.theScene[index + 3])
            except IndexError:
                pass
        else:
            pass

    def handleJump0001(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            try:
                self.addSource(eventName, eventText.theScene[index + 4])
            except IndexError:
                pass
        else:
            pass

    def handleStatusJumpPotency(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            try:
                self.addSource(eventName, eventText.theScene[index + 3])
            except IndexError:
                pass
        else:
            pass

    def handleLoopedJump(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            tempIndex = copy.copy(index)
            while tempIndex < len(eventText.theScene):
                if eventText.theScene[tempIndex] == "EndLoop":
                    self.addSource(eventName, eventText.theScene[tempIndex + 1])
                    break
                else:
                    tempIndex += 1
        else:
            pass

    def handleSwapLineIf(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            self.inLoop = True
            tempIndex = copy.copy(index)
            while tempIndex < len(eventText.theScene):
                if eventText.theScene[tempIndex] == "EndLoop":
                    break
                else:
                    if "|f|" in eventText.theScene[tempIndex]:
                        self.checkCombatLine(eventText.theScene[tempIndex], eventName)
                    tempIndex += 1
        else:
            pass

    def handleMenu(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            self.inLoop = True
            tempIndex = copy.copy(index + 1)
            while tempIndex < len(eventText.theScene):
                if eventText.theScene[tempIndex] == "EndLoop":
                    break
                elif eventText.theScene[tempIndex] in self.listSkipCurrent:
                    tempIndex += 1
                elif eventText.theScene[tempIndex] in self.listSkip0:
                    tempIndex += 2
                elif eventText.theScene[tempIndex] in self.listSkip00:
                    tempIndex += 3
                elif eventText.theScene[tempIndex] in self.listSkip000:
                    tempIndex += 4
                else:
                    self.addSource(eventName, eventText.theScene[tempIndex])
                    tempIndex += 1
        else:
            pass

    def handleCombatEncounter(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            tempIndex = copy.copy(index + 1)
            while tempIndex < len(eventText.theScene):
                currentValue = eventText.theScene[tempIndex]
                if currentValue == "StartCombat":
                    break
                elif currentValue in self.monsterNameEncounter00:
                    tempIndex += 2
                elif currentValue in self.monsterNameEncounter:
                    tempIndex += 1
                elif currentValue in ["ApplyStance", "SetAttack", "IfRanAway"]:
                    tempIndex += 2  # TODO: Implement stance stuff properly.
                else:
                    self.storeIDCheck(currentValue, eventName, "Monsters", "Events", eventText.NameOfScene, jsonType)
                    tempIndex += 1
        else:
            pass

    def handleStatCheck(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            self.inLoop = True
            tempIndex = copy.copy(index)
            while tempIndex < len(eventText.theScene):
                if eventText.theScene[tempIndex] == "Fail":
                    self.addSource(eventName, eventText.theScene[tempIndex + 1])
                    self.addSource(eventName, eventText.theScene[tempIndex - 1])
                    break
                else:
                    tempIndex += 1
        else:
            pass

    def handleStatusJumpLoop(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            tempIndex = copy.copy(index)
            if value in ["IfOtherMonsterHasStatusEffect", "IfOtherMonsterDoesntHaveStatusEffect"]:
                tempIndex += 1
            if eventText.theScene[tempIndex + 1] == "RequireAll":
                tempIndex += 2
            else:
                tempIndex += 1
            while tempIndex < len(eventText.theScene):
                if isStatusEffect(eventText.theScene[tempIndex]):  # type: ignore
                    tempIndex += 1
                else:
                    self.addSource(eventName, eventText.theScene[tempIndex])
                    break
        else:
            pass

    def handleTagJumps(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            tempIndex = copy.copy(index)
            if eventText.theScene[tempIndex + 1] == "Tags":
                while tempIndex < len(eventText.theScene):
                    if eventText.theScene[tempIndex] == "EndLoop":
                        if value in self.listTagJumps:
                            self.addSource(eventName, eventText.theScene[tempIndex + 1])
                        elif value in self.listTagJumps01:
                            self.addSource(eventName, eventText.theScene[tempIndex + 2])
                        break
                    else:
                        tempIndex += 1
            else:
                if value in self.listTagJumps:
                    self.addSource(eventName, eventText.theScene[index + 2])
                elif value in self.listTagJumps01:
                    self.addSource(eventName, eventText.theScene[index + 3])
        else:
            pass

    def handleEventJumps21(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            self.addSource(eventText.theScene[index + 1], eventText.theScene[index + 2])
        else:
            pass

    def handleIfGridNpcSeesPlayer(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            tempIndex = copy.copy(index) + 1
            while tempIndex < len(eventText.theScene):
                if eventText.theScene[tempIndex] == "IgnoreWalls":
                    tempIndex += 1
                elif eventText.theScene[tempIndex] == "NPC":
                    tempIndex += 2
                elif eventText.theScene[tempIndex] == "Range":
                    tempIndex += 2
                else:
                    self.addSource(eventName, eventText.theScene[tempIndex])
                    break
        else:
            pass

    def handleGoToMap(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if not self.inLoop:
            self.inLoop = True
            tempIndex = copy.copy(index + 1)
            while tempIndex < len(eventText.theScene):
                if eventText.theScene[tempIndex] == "NPC":
                    while tempIndex < len(eventText.theScene):
                        if eventText.theScene[tempIndex] in ["Event", "Timer"]:
                            self.addSource(eventText.theScene[tempIndex + 2], eventText.theScene[tempIndex + 3])
                            tempIndex += 3
                        elif eventText.theScene[tempIndex] in ["TurnEvent"]:
                            self.addSource(eventText.theScene[tempIndex + 1], eventText.theScene[tempIndex + 2])
                            tempIndex += 2
                        elif eventText.theScene[tempIndex] == "EndLoop":
                            break
                        else:
                            tempIndex += 1
                elif eventText.theScene[tempIndex] == "Tileset":
                    while tempIndex < len(eventText.theScene):
                        if eventText.theScene[tempIndex] in ["Auto", "Interactable"]:
                            self.addSource(eventText.theScene[tempIndex + 1], eventText.theScene[tempIndex + 2])
                            tempIndex += 2
                        elif eventText.theScene[tempIndex] == "EndLoop":
                            break
                        else:
                            tempIndex += 1
                elif eventText.theScene[tempIndex] == "StartMap":
                    self.inLoop = False
                    break
                else:
                    tempIndex += 1
        else:
            pass

    def handleChoiceCheck(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if value in ["RequiresChoice", "IfChoice"]:
            self.addChoiceSource(eventName, eventText.theScene[index + 1], eventText.theScene[index + 2])
        elif value in ["RequiresChoiceFromEvent", "GetEventAndIfChoice"]:
            self.addChoiceSource(eventText.theScene[index + 1], eventText.theScene[index + 2], eventText.theScene[index + 3])
    def handleChoiceSet(self, eventName="", eventText=[], index=0, jsonType="", value=""):
        if value == "SetChoice":
            self.addChoiceTarget(eventName, eventText.theScene[index + 1], eventText.theScene[index + 2])
        elif value == "GetEventAndSetChoice":
            self.addChoiceTarget(eventText.theScene[index + 1], eventText.theScene[index + 2], eventText.theScene[index + 3])

    def checkCombatLine(self, line, fileName):
        if not self.enabled:
            return
        if "|f|" not in line:
            return
        if "CallCombatEventAndScene" in line or "JumpToScene" in line or "CallEventAndSceneThenReturn" in line:
            tokens = re.compile(r"\|f\||\|n\||\|/\|").split(line)
            for index, token in enumerate(tokens):
                if token == "CallCombatEventAndScene":
                    self.addSource(tokens[index + 1], tokens[index + 2])
                elif token == "JumpToScene":
                    self.addSource(fileName, tokens[index + 1])
                elif token == "CallEventAndSceneThenReturn":
                    self.addSource(tokens[index+1], tokens[index+2])
        self.eventFileName = fileName

    def writeToFiles(self):
        if not self.enabled:
            return

        self.beginDelayedChecks()

        filteredSourceChoices = self.filterChoices(self.choiceSourceDatabase)
        filteredTargetChoices = self.filterChoices(self.choiceTargetDatabase)

        scenes_result = {
            "noSceneForLink": [],
            "tooManyScenes": [],
            "noLinkForScene": []
        }
        choices_result  = {
            "UnusedChoicesForEvent": [],
            "UnusedChoiceNumberForEvent": [],
            "UnusedChoiceValueForChoiceNumber": []
        }

        for jump_name, count in sorted(self.jumpSourceCounters.items()):
            if jump_name not in self.jumpTargetCounters:
                scenes_result["noSceneForLink"].append({
                    "theEvent": jump_name[0],
                    "theScene": jump_name[1]
                })

        for jump_name, count in sorted(self.jumpTargetCounters.items()):
            if count > 1:
                scenes_result["tooManyScenes"].append({
                    "count": count,
                    "theEvent": jump_name[0],
                    "theScene": jump_name[1]
                })
            if jump_name not in self.jumpSourceCounters and count > 0:
                scenes_result["noLinkForScene"].append({
                    "theEvent": jump_name[0],
                    "theScene": jump_name[1]
                })

        for eventName, sourceChoices in filteredSourceChoices.items():
            if eventName not in filteredTargetChoices:
                choices_result["UnusedChoicesForEvent"].append({
                    "theUnusedEvent": eventName,
                    "eventChoices": [
                        {"choiceNumber": choiceNumber, "choiceValue": choiceValue}
                        for choiceNumber, choiceValues in sourceChoices.items()
                        for choiceValue in choiceValues
                    ]
                })
            else:
                targetChoices = filteredTargetChoices[eventName]
                for choiceNumber, choiceValues in sourceChoices.items():
                    if choiceNumber not in targetChoices:
                        choices_result["UnusedChoiceNumberForEvent"].append({
                            "theEvent": eventName,
                            "choiceNumber": choiceNumber
                        })
                    else:
                        for choiceValue in choiceValues:
                            if choiceValue and choiceValue not in targetChoices[choiceNumber]:
                                choices_result["UnusedChoiceValueForChoiceNumber"].append({

                        "theEvent": eventName,
                                    "choiceNumber": choiceNumber,
                                    "choiceValue": choiceValue
                                })

        with open(gamedir + "/debug/idname_validation.json", "w") as IDname_output_file: # type: ignore
            json.dump(self.IDDatabaseChecks, IDname_output_file, indent=4)

        with open(gamedir + "/debug/scene_validation.json", "w") as scene_output_file: # type: ignore
            json.dump(scenes_result, scene_output_file, indent=4)

        with open(gamedir + "/debug/choices_validation.json", "w") as choice_output_file: # type: ignore
            json.dump(choices_result, choice_output_file, indent=4)
