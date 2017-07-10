import requests
import sys
import json
import uuid

class DiscordApi():
    baseUrl = "https://discordapp.com/api"

    def get(self, url):
        return self.client.get(self.baseUrl+url)

    def post(self,url, payload):
        return self.client.post(
            self.baseUrl+url,
            data=json.dumps(payload),
            headers={'Content-Type':'application/json'}
        )

    def __init__(self, config):
        try:
            self.config = config
            self.token   = config['token']
            self.channel = config['channel']
            
            self.client = requests.session()
            self.client.headers.update({
                'Authorization': "Bot "+self.token,
                'User-Agent': "DiscordBot (artog.ddns.net, 1.0) Python/{0[0]}.{0[1]} requests".format(sys.version_info),
            })

        except Exception as e:
            raise e

    def getChannel(self):
        url = "/channels/{channelId}".format(channelId=self.channel)
        print(self.get(url).text)


    def sendMessage(self, message):
        url = "/channels/{channelId}/messages".format(channelId=self.channel)
        payload = {
            "content":message,
            "nonce": str(uuid.uuid1())[0:25]
        }
        r = self.post(url, payload)
        print(r.status_code)
        print(r.text)
        print("\"sent\" %s" % (message))
        pass
        