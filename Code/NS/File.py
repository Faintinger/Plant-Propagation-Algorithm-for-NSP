from NS.Task import Task
from NS.Nurse import Nurse
import math

class File(object):
    """description of class"""
    def __init__(self, path):
        self.file = ""
        self.path = path
        self.nurses = 0
        self.days = 0
        self.shifts = 0
        self.skills = 0
        self.tasks = 0
        self.hoursPerShift = 0

    def readFile(self):
        f = open(self.path, "r")
        self.file = f.read()
        text = ""
        lines = self.file.split("\n")
        for i in range(len(lines)):
            if not lines[i].strip().startswith("$"):
                if not lines[i].strip() == "":
                    text += lines[i].strip()
                    if i < (len(lines) - 1):
                        text += "\n"
        f.close()
        self.file = text

    def writeInFile(self, text):
        f = open(self.path, "a+")
        f.write(text)
        f.close()

    def loadFile(self):
        if(self.file != ""):
            lines = self.file.split("\n")
            details = lines[0].split("\t")
            self.nurses = int(details[0])
            self.days = int(details[1])
            self.shifts = int(details[2])
            self.skills = int(details[3]) if(len(details) > 3) else 0
            self.tasks = self.nurses * self.days

    def getCoverage(self):
        coverage = []
        if(self.file != ""):
            lines = self.file.split("\n")
            for i in range(1, self.days + 1):
                cover = lines[i].split("\t")
                c = []
                for j in range(self.shifts):
                    c.append(int(cover[j]))
                coverage.append(c)
        return coverage

    def getSkillMatrix(self):
        skill = []
        if(self.file != "") & (self.skills > 0):
            lines = self.file.split("\n")
            for i in range(1, self.days + 1):
                cover = lines[i].split("\t")
                c = []
                for j in range(self.shifts, (self.shifts+self.skills)):
                    c.append(int(cover[j]))
                skill.append(c)
        return skill


    def getTasks(self):
        tasks = []
        if(self.file != ""):
            lines = self.file.split("\n")
            i = self.days + 1;
            idCont = 0
            while idCont < (self.days * self.nurses + 1):
                id = str(idCont + 1)
                name = "Shift"
                duration = (24 / (self.shifts - 1)) * 60
                day = math.floor(idCont / self.nurses)
                startTime = "0:0"
                levelRequired = 0
                t = Task(id, name, duration, day, startTime, levelRequired);
                tasks.append(t)
                i = i + 1
                idCont = idCont + 1
        return tasks

    def getNurses(self):
        nurses = []
        if(self.file != ""):
            lines = self.file.split("\n")
            self.hoursPerShift = 24 / (self.shifts - 1)
            i = 1;
            nurseDetails = self.getNurseDetails()
            cost = 0
            level = 0
            id = ""
            while i <= self.nurses:
                #temp = lines[i].split("\t")
                if (len(nurseDetails) > 0):
                    id = nurseDetails[i - 1][0]
                    cost = float(nurseDetails[i - 1][1])
                    level = int(nurseDetails[i - 1][2]) if(len(nurseDetails[i - 1]) > 2) else 0
                else: 
                    id = str(i)
                    cost = 0
                    level = 0
                daysWork = []
                for j in range(self.days):
                    work = 1
                    daysWork.append(work)
                n = Nurse(id, daysWork, cost, self.hoursPerShift, level, self.shifts)
                nurses.append(n)
                i = i + 1
        return nurses

    def getPreferences(self):
        preferences = []
        if(self.file != ""):
            start = self.days + 1
            lines = self.file.split("\n")
            for i in range(start, start + self.nurses):
                prefs = lines[i].split("\t")
                temp = []
                for j in range(self.days * self.shifts):
                    temp.append(int(prefs[j]))
                preferences.append(temp)
        return preferences

    def getNurseDetails(self):
        nurseDetails = []
        if(self.file != ""):
            lines = self.file.split("\n")
            start = self.days + self.nurses + 1
            if(len(lines) >= start):
                for i in range(start, start + self.nurses):
                    l = lines[i].split("\t")
                    nurseDetails.append(l)
        return nurseDetails

    def getNurseQuantity(self):
        nurses = 0
        if(self.file != ""):
            nurses = self.nurses
        return nurses

    def getDaysOfSchedule(self):
        days = 0
        if(self.file != ""):
            days = self.days
        return days

    def getShiftsPerDay(self):
        shifts = 0
        if(self.file != ""):
            shifts = self.shifts
        return shifts

    def getHoursPerShift(self):
        hoursPerShift = 0
        if(self.file != ""):
            hoursPerShift = self.hoursPerShift
        return hoursPerShift

    def getTasksQuantity(self):
        tasks = 0
        if(self.file != ""):
            tasks = self.tasks
        return tasks

