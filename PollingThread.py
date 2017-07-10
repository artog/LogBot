import time
import threading
import requests
from WarcraftLogApi import WarcraftLogApi
from DiscordApi import DiscordApi

class PollingThread(threading.Thread):
    active = True
    latestTime = 0
    latestLog = ""
    latestFight = 0
    latestFightStart = 0

    def __init__(self, delay, api, discord):
        """
          @type api: WarcraftLogApi
          @type discord: DiscordApi
          """
        threading.Thread.__init__(self)
        self.delay = delay
        self.lock = threading.Lock()
        self.active = True
        self.discord = discord
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
        report = self.api.getReports(self.latestTime).json()
        if (len(report) == 0):
            return

        latest = report[-1]
        if (latest['start'] > self.latestTime):
            self.latestTime = latest['start']
            self.latestLog = latest['id']
            print("New log!")
            print(latest)
            wlUrl = "https://www.warcraftlogs.com/reports/"
            self.discord.sendMessage("{0}: {1}{2}".format(latest['title'],wlUrl, latest['id']))

        fights = self.api.getFights(self.latestLog)
        if (len(fights) == 0):
            return

        fight = fights[-1]
        if (self.latestFightStart > fight['start_time']):
            self.latestFight = fight['id']
            self.latestFightStart = fight['start_time']

        print(latest)
        print(fights)