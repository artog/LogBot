from WarcraftLogApi import WarcraftLogApi
from PollingThread import PollingThread
from DiscordApi import DiscordApi
import configparser
import time
from sys import exit

class LogBot():

    configFile = "config.ini"


    def __init__(self):
        print ("Starting LogBot")

        config = configparser.ConfigParser()
        config.read(self.configFile)

        try:
            self.discordApi = DiscordApi(config['discord'])
            self.logApi = WarcraftLogApi(config['warcraftlogs'])
        except Exception as e:
            print("Error starting apis: {0}".format(repr(e)))
            exit(1)

    def printHelp(self):
        print("----------- LogBot Help -----------")
        print("git gud. noob.")
        print(self.logApi.getFights("kFzACTYJbcmXLGqB"))
        print(self.logApi.getReports(1499277098372).json())

    def sendMessage(self, msg):
        self.discordApi.sendMessage(msg)

    def getChannel(self):
        self.discordApi.getChannel()

    def startPolling(self):
        pass

    def stopPolling(self):
        pass

    def startCLI(self):
        while True:
            parts = input("LogBot> ").split(" ")
            cmd = parts[0]
            args = parts[1:]
            if cmd in ["q","quit"]:
                print("Bye bye.")
                break

            if cmd in ["help","?","h"]:
                self.printHelp()
                
            elif cmd in ["send"]:
                self.sendMessage(args[0])

            elif cmd in ["chan"]:
                self.getChannel()

            elif cmd in ["start"]:
                self.startPolling()

            elif cmd in ["stop"]:
                self.stopPolling()

        

def main():
    LogBot().startCLI()

if __name__ == "__main__":
    main()