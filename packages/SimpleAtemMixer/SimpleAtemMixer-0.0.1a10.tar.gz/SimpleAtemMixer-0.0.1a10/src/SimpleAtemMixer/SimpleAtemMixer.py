
class SimpleAtemMixer:

    def __init__(self, ip):
        self.connectionIP = ip

    def __str__(self):
        return "Connection to " + self.connectionIP