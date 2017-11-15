import time
import threading

from WarcraftLogApi import WarcraftLogApi
from DiscordApi import DiscordApi
from Fight import Fight
from Report import Report
from Data import Data
from Message import Message

class PollingThread(threading.Thread):
    active = True
    latestTime = 0
    latestLog = ""
    latestFight = 0
    latestFightStart = 0
    latestMessage = 0
    currentMessage = ""

    # @type data: Data
    data = []

    def __init__(self, delay : int, api : WarcraftLogApi, data : Data):
        """
          @type api: WarcraftLogApi
          @type discord: DiscordApi
          """
        threading.Thread.__init__(self)
        self.delay = delay
        self.lock = threading.Lock()
        self.active = True
        self.data = data
        self.api = api

    def start(self):
        threading.Thread.start(self)
        self.active = True

    def run(self):
        print("Starting polling")
        while self.active:
            print("Polling server")
            self.doPoll()
            time.sleep(self.delay)

    def doPoll(self):

        oneDay = 60*60*24
        startTime = (time.time() - 7*oneDay) * 1000
        reports = self.api.getReports(startTime).json()
        if (len(reports) == 0):
            return

        for report in reports:
            id = report['id']
            fights = self.api.getFights(id)
            if not report['id'] in self.data.reports.keys():
                self.data.reports[id] = Report(
                    id,
                    report['title'],
                    report['owner'],
                    int(report['start']))
                print("New log!")
            if len(self.data.reports[id].fights) < len(fights):
                print("New fight!")
                self.data.reports[id].dirty = True
                for fight in fights:
                    fightId = fight['id']
                    if not fightId in self.data.reports[id].fights.keys():
                        newFight = Fight(fightId, fight['name'],id)
                        self.data.reports[id].addFight(newFight)
            for id, report in self.data.reports.items():
                if report.isDirty():
                    self.data.reports[id].message = report.getFormattedChatMessage()
                if report.startTime < (time.time() - 14*oneDay) * 1000:
                    self.data.reports.pop(id, None)


    def sendMessage(self,message):
        self.data.messages.append(Message(message))

    def editMessage(self,messageId, message):
        self.data.messages.append(Message(messageId, message))