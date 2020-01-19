class Task(object):
    """description of class"""
    def __init__(self, id, name, duration, day, startTime, levelRequired):
        self.id = id
        self.name = name
        self.duration = duration
        self.day = day
        self.startTime = startTime
        self.levelRequired = levelRequired
        time = int(startTime.replace(":",""));
        self.numberStartTime = time
        self.shiftTurn = 0

    def toString(self):
        s = self.id + "-" + self.name + ", shift " + str(self.shiftTurn) + ", " + str(self.duration) + "mins " + str(self.levelRequired) + "lvl"
        return s  