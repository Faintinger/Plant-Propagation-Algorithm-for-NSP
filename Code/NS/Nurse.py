class Nurse(object):
    """description of class"""
    def __init__(self, id, workDays, costPerHour, hoursShift, Skill, shifts):
        self.id = id
        self.workDays = workDays
        self.costPerHour = costPerHour
        self.hoursShift = hoursShift
        self.skill = Skill
        self.schedule = []
        self.matrixSchedule = []
        self.scheduleCost = 0
        self.penalty = 0
        self.maxShifts = shifts
        for i in range(len(workDays)):
            self.schedule.append([])
            self.matrixSchedule.append([])

    def isAssignable(self, task):
        #Validate if its a working day
        assignable = (self.workDays[task.day] == 1);
        assignable = assignable & (self.isAValidShift(task))
        #Validate if the nurse is free in that time
        #Validate if the sum of the tasks do not exceed
        if assignable:
            assignable = (assignable & self.isFree(task.day, task.numberStartTime, task.duration))
        #If the nurse has the skill level to cover the task
        if assignable:
            assignable = (assignable & task.levelRequired <= self.skill)
        return assignable

    def isFree(self, day, hour, length):
        free = False;
        if len(self.schedule) > day:
            workDay = self.schedule[day]
            freeSpace = True
            totalTime = 0
            for t in range(len(workDay)):
                totalTime += workDay[t].duration
                if workDay[t].numberStartTime <= hour & hour <= (workDay[t].numberStartTime + ((workDay[t].duration / 60) * 100)):
                    freeSpace = False
                    break
                elif (hour + ((length/60)*100)) > workDay[t].numberStartTime:
                    freeSpace = False
                    break
            if ((totalTime + length)/60) > self.hoursShift:
                freeSpace = False
            free = freeSpace
        return free

    def AssignTask(self, task):
        assigned = False
        day = self.schedule[task.day]
        if(len(day) == 0):
            self.schedule[task.day].append(task)
            assigned = True
        for i in range(len(day)):
            if(day[i].numberStartTime > task.numberStartTime):
                self.schedule[task.day].insert(i, task)
                assigned = True
                break
        if not assigned:
            self.schedule[task.day].append(task)

    def CalculateCost(self):
        self.scheduleCost = 0;
        lS = len(self.schedule)
        for i in range(lS):
            l2 = len(self.schedule[i])
            for j in range(l2):
                if(self.schedule[i][j].shiftTurn != self.maxShifts):
                    self.scheduleCost += (self.schedule[i][j].duration / 60) * self.costPerHour
        return self.scheduleCost

    def RemoveTask(self, day, task):
        if(day < len(self.schedule)):
            for i in range(len(self.schedule[day])):
                #print("day " + str(day) + " " + str(len(self.schedule[day])) + " - " + str(i))
                if self.schedule[day][i].id == task.id:
                    self.schedule[day].pop(i)
                    break

    def getScheduleString(self):
        s = ""
        s += self.id + " - " + str(self.skill) + " lvl hours: " + str(self.hoursShift) + "\n"
        d = len(self.schedule)
        for i in range(d):
            s += "day " + str(i + 1) + "\t"
            tasks = len(self.schedule[i])
            for j in range(tasks):
                s += self.schedule[i][j].toString() + " | "
            s += "\n"
        return s

    def getCoverage(self):
        days = len(self.workDays)
        coverage = []
        for d in range(days):
            taskList = len(self.schedule[d])
            if(taskList > 0):
                coverage.append(self.schedule[d][0])
        return coverage

    def getNurseScheduleShifts(self):
        s = []
        d = len(self.schedule)
        for i in range(d):
            tasks = len(self.schedule[i])
            for j in range(tasks):
                s.append(self.schedule[i][j].shiftTurn)
        return s

    def isAValidShift(self, task):
        day1 = self.schedule[task.day];
        day2 = self.schedule[task.day -1];
        shift1 = task.shiftTurn; s1 = -1;
        shift2 = 0; s2 = 0;
        for i in range(len(day1)):
            if(day1[i].shiftTurn > shift1):
                shift1 = day1[i].shiftTurn
                s1 = i
        for i in range(len(day2)):
            if(day2[i].shiftTurn > shift2):
                shift2 = day2[i].shiftTurn
                s2 = i
        if(shift2 == 0):
            return True;
        else:
            return (shift1 != 1) | (shift2 != (self.maxShifts - 1))