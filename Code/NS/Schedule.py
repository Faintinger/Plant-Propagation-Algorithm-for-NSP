class Schedule(object):
    """description of class"""
    def __init__(self, days, costPerShift, skillLevel):
        self.days = days
        self.costPerShift = costPerShift
        self.skillLevel = skillLevel
        self.Shifts = []
