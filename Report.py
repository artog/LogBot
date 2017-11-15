from Fight import Fight
from typing import  Dict
from time import strftime, gmtime
class Report:
    fights = {} # type: Dict[str, Fight]
    id = ""
    dirty = False
    title = ""
    owner = ""
    startTime = 0
    message = ""
    messageId = 0

    def __init__(self, id, title, owner, startTime ):
        self.id = id
        self.title = title
        self.owner = owner
        self.startTime = startTime
        self.dirty = True



    def addFight(self, fight : Fight):
        self.fights[fight.id] = fight
        self.dirty = True

    def isDirty(self):
        return self.dirty

    def getFormattedChatMessage(self):
        wlUrl = "https://www.warcraftlogs.com/reports/"
        message = "{0} -- {1}: {2}{3}\n\nKills:\n".format(
            strftime("%Y-%m-%d", gmtime(self.startTime/1000)),
            self.title,
            wlUrl,
            self.id
        )
        for fightId in self.fights.keys():
            message += "**{0}**\n".format(self.fights[fightId].bossName)
        return message

    def clean(self):
        self.dirty = False