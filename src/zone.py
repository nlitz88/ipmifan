
class Zone:
    
    def __init__(self, name):
        self.name = name
        self.zones = []

    def addZone(self, newZone):
        self.zones.append(newZone)