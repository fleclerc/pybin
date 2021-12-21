
class StatsCompute:
    def __init__(self, size) -> None:
        self.size = size
        self.entries = []
        self.nbDown = 0
        self.volume = 0

    def next(self, entry): 
        self.volume += entry["volume"]
        if len(self.entries) >= 1:
            self.nbDown += 1 if entry["minPrc"] < self.entries[len(self.entries)-1]["minPrc"] else 0
        self.entries.append(entry)
        if len(self.entries) > self.size:
            x = self.entries.pop(0)
            self.nbDown += -1 if x["minPrc"] > self.entries[0]["minPrc"] else 0
            self.volume -= x["volume"]
