from typing import Dict, List
from Report import Report
from Message import Message

class Data:

    reports = {} # type: Dict[str, Report]
    messages = {} # type: Dict[str,Message]

    def __init__(self):
        self.reports = {}
        self.messages = {}