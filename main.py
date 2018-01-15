
from PollingThread import *
from DiscordApi import *
from Data import *
from Message import *
import configparser
from sys import exit
import logging

log = logging.getLogger()
print(log.handlers)

class LogBot():

    configFile = "config.ini"

    def __init__(self):
        print ("Starting LogBot")

        config = configparser.ConfigParser()
        print("Reading config file {0}".format(self.configFile))
        config.read(self.configFile)

        try:

            self.data = Data()

            print("Starting Discord API")
            self.discordApi = DiscordApi(config['discord'],self.data)
            self.discordApi.start()

            print("Starting WarcraftLogs API")
            self.logApi = WarcraftLogApi(config['warcraftlogs'], self.data)

            print("Initializing polling thread")
            self.pollingThread = PollingThread(2,self.logApi, self.data)

            startCLI()

        except Exception as e:
            print("Error starting apis: {0}".format(repr(e)))
            exit(1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pollingThread.active = False

    def printHelp(self):
        print("----------- LogBot Help -----------")
        print("git gud. noob.")
        #print(self.logApi.getFights("kFzACTYJbcmXLGqB"))
        #print(self.logApi.getReports(1499277098372).json())

    def sendMessage(self, msg):
        self.data.messages.append(msg)

    def startPolling(self):
        self.pollingThread.start()

    def stopPolling(self):
        self.pollingThread.active = False

    def startCLI(self):

        while True:
            print("LogBot> ",end="")
            parts = input("").split(" ")
            cmd = parts[0]
            args = parts[1:]
            if cmd in ["q","quit"]:
                self.stopPolling()
                print("Bye bye.")
                break

            if cmd in ["help","?","h"]:
                self.printHelp()
                
            elif cmd in ["send"]:
                self.sendMessage(Message(args[0]))

            elif cmd in ["start"]:
                self.startPolling()

            elif cmd in ["stop"]:
                self.stopPolling()

            elif cmd in ["debug"]:
                self.pollingThread.doPoll()


        

def main():
     bot = LogBot()

if __name__ == "__main__":
    logging.getLogger('discord').addHandler(logging.StreamHandler())
    main()