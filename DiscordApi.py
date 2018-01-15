import discord
import asyncio
import threading
import Message
import Data


class DiscordApi(threading.Thread):

    ids = []

    def __init__(self, config, data : Data):
        threading.Thread.__init__(self)
        self.config = config
        self.token   = config['token']
        self.channelId = str(config['channel'])
        self.client = discord.Client()
        self.data = data
        self.channel = discord.Object(id=self.channelId)

    async def handleMessages(self):
        await self.client.wait_until_ready()
        counter = 0
        while not self.client.is_closed:
            # print("Starting discord iteration")
            counter += 1
            for id, report in self.data.reports.items():
                if report.isDirty():
                    # print("Report ",id,"is dirty.")
                    if report.messageId == 0:
                        # print("Sending:",report.message)
                        self.data.reports[id].messageId = await self.sendMessage(report.message)
                    else:
                        # print("Editing ",report.messageId,":",report.message)
                        await self.editMessage(report.messageId, report.message)
                    self.data.reports[id].clean()
            await asyncio.sleep(15)  # task runs every 15 seconds

    def run(self):
        self.client.loop.create_task(self.handleMessages())
        self.client.run(self.token)

    async def sendMessage(self, message):
        # print("Sent",message)
        try:
            msg = await  self.client.send_message(self.channel ,message)
            return msg
        except discord.DiscordException as ex:
            print("Error when sending message:",ex)
        return 0

    async def editMessage(self,msgId, newMessage):
        self.client.edit_message(msgId, newMessage)



