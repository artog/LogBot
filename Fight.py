

class Fight:
    id = ""
    bossName = ""
    report = ""
    killed = True

    def __init__(self, id, bossName ="", report = "", killed = True):
        self.id = id
        self.bossName = bossName
        self.report = report
        self.killed = killed