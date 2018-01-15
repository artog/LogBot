import requests
from Data import *

class WarcraftLogApi():
    """
    @type data: Data
    """
    baseUrl = "https://www.warcraftlogs.com:443/v1/"
    reportsUrl = "reports/guild/{guildName}/{serverName}/{serverRegion}"
    fightsUrl = "report/fights/{code}"
    encounterRankingsUrl = "rankings/encounter/{encounterID}"
    data = 0
    # lastCheck = 0

    def __init__(self, config, data : Data):
        self.guild = config['guild']
        self.server = config['server']
        self.region = config['region']
        self.apikey = config['apikey']
        self.data = data

    def getRankings(self, encounterId):
        url = self.baseUrl + self.encounterRankingsUrl.format(
            encounterID=encounterId
        )
        # print("Sending", url)
        response = requests.get(url, params={'api_key': self.apikey})
        return response

    def getFights(self, reportCode, killsOnly=True, start=0):
        url = self.baseUrl + self.fightsUrl.format(
            code=reportCode,
        )
        #print("Sending", url)
        response = requests.get(url, params={'api_key': self.apikey, 'start': round(start)})
        # print(response.json()['fights'])
        fights = []
        for fight in response.json()['fights']:
            # print(fight)
            if (fight['boss'] == 0):
                continue
            if (not killsOnly or fight['kill']):
                fights.append(fight)

        return fights

    def getReports(self, start=0):
        url = "{0}{1}".format(self.baseUrl, self.reportsUrl.format(
			guildName=self.guild,
			serverName=self.server,
			serverRegion=self.region
		))
        # print("Sending", url)
        response = requests.get(url, params={'api_key': self.apikey, 'start': round(start)})
        return response
