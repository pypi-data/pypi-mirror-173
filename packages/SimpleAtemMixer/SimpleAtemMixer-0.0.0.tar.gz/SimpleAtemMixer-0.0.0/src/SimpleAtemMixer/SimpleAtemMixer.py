
from tokenize import String


class SimpleAtemMixer:

    def __init__(self, ip: String):
        self.connectionIP = ip

    def __str__(self):
        return "Connection to " + self.connectionIP