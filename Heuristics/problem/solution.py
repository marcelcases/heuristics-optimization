"""
AMMM Lab Heuristics
Representation of a solution instance
Copyright 2020 Luis Velasco.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import copy
from Heuristics.solution import _Solution


# This class stores the load of the highest loaded CPU
# when a task is assigned to a CPU.
class Assignment(object):
    def __init__(self, talk, time_slot, room, cost):
        self.talk = talk
        self.time_slot = time_slot
        self.room = room
        self.cost = cost

    def __str__(self):
        return "<n_%d, t_%d, r_%d >: cost: %.2f%%" % (self.talk, self.time_slot ,self.room, self.cost)


# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class Solution(_Solution):
    def __init__(self, n, t, r, d, P, S):
        self.n = n
        self.t = t
        self.r = r
        self.d = d
        self.talkToTimeSlotRoom = {}
        #self.timeSlotRoomTalk = {}
        self.cost = 0.0
        self.P = P
        self.S = S
        #self.taskIdToCPUId = {}  # hash table: task Id => CPU Id
        #self.cpuIdToListTaskId = {}  # hash table: CPU Id => list<task Id>
        # vector of available capacities per CPU initialized as a copy of maxCapacityPerCPUId vector.
        #self.availCapacityPerCPUId = copy.deepcopy(capacityPerCPUId)
        # vector of loads per CPU (nCPUs entries initialized to 0.0) 
        #self.loadPerCPUId = [0.0] * len(cpus)
        super().__init__()

    def isSecondaryRelated(self, t1, t2):
        return self.S[t1][t2] == 1

    def getAssignedTalksToTimeSlot(self, ts):
        res = []
        for k in self.talkToTimeSlotRoom.keys():
            if ts in self.talkToTimeSlotRoom[k]:
                res.append(k)
        return res

    def isPrimaryRelated(self, t1, t2):
        return self.P[t1][t2] == 1

    def updateHighestCost(self):
        self.cost = 0.0
        """""
        for cpu in self.cpus:
            cpuId = cpu.getId()
            totalCapacity = cpu.getTotalCapacity()
            usedCapacity = totalCapacity - self.availCapacityPerCPUId[cpuId]
            load = usedCapacity / totalCapacity
            self.loadPerCPUId[cpuId] = load
            self.fitness = max(self.fitness, load)
        """""
        #Todo se puede optimizar
        contador = 0
        for talk1 in range(0, self.n):
            for talk2 in range(0, self.n):
                talk1_time = self.getTimeSchedule(talk1)
                talk2_time = self.getTimeSchedule(talk2)
                if self.isSecondaryRelated(talk1, talk2) and talk1_time == talk2_time and talk1_time >= 0:
                    contador += 1
        self.cost = 1/2 * contador

    def getTimeSchedule(self, talk):
        time = -1
        if talk in self.talkToTimeSlotRoom:
            time = list(self.talkToTimeSlotRoom[talk].keys())[0]
        return time

    def isFeasibleToAssignTimeSlotRoom(self, talk, time_slot, room):
        #Constraint 1 talk can only be assigned once
        if talk in self.talkToTimeSlotRoom:
            return False

        #Optimizar
        #Constraint 2 -> 2 talks cannot be assigned to the same time_slot and room
        for i in range(0, self.n):
            if i not in self.talkToTimeSlotRoom:
                continue
            if time_slot in self.talkToTimeSlotRoom[i] and room in self.talkToTimeSlotRoom[i][time_slot]:
                return False

            #Constraint 3 Any other primary talks cannot be scheduled at the same time
            if self.isPrimaryRelated(i, talk) and time_slot in self.talkToTimeSlotRoom[i]:
                return False
            #Constraint 4 primary tasks cannot be too far away
            if self.isPrimaryRelated(i, talk) and abs(time_slot - list(self.talkToTimeSlotRoom[i].keys())[0]) > self.d:
                return False

        return True

    def isFeasibleToUnassignTaskFromCPU(self, talk, time_slot, room):
        """""
        if taskId not in self.taskIdToCPUId: return False
        if cpuId not in self.cpuIdToListTaskId: return False
        if taskId not in self.cpuIdToListTaskId[cpuId]: return False
        """""
        if talk not in self.talkToTimeSlotRoom: return False
        #Todo check

        return True

    def getCPUIdAssignedToTaskId(self, taskId):
        if taskId not in self.taskIdToCPUId: return None
        return self.taskIdToCPUId[taskId]

    def assign(self, talk, time_slot, room):
        if not self.isFeasibleToAssignTimeSlotRoom(talk, time_slot, room):return False

        if talk not in self.talkToTimeSlotRoom:
            self.talkToTimeSlotRoom[talk] = {}

        if time_slot not in self.talkToTimeSlotRoom[talk]:
            self.talkToTimeSlotRoom[talk][time_slot] = {}

        self.talkToTimeSlotRoom[talk][time_slot][room] = 1 #NTR equivalent
        # self.cpuIdToListTaskId = {}  # hash table: CPU Id => list<task Id>
        # self.timeSlotRoomTalk = {}  # hash table: [timeSlot][room] => talk
        # if cpuId not in self.cpuIdToListTaskId: self.cpuIdToListTaskId[cpuId] = []
        #self.timeSlotRoomTalk[time_slot][room] = talk
        #self.availCapacityPerCPUId[cpuId] -= self.tasks[taskId].getTotalResources()

        self.updateHighestCost()
        return True

    def unassign(self, talk, time_slot, room):
        if not self.isFeasibleToUnassignTaskFromCPU(talk, time_slot, room): return False

        del self.talkToTimeSlotRoom[talk]
        #self.cpuIdToListTaskId[cpuId].remove(taskId)
        #self.availCapacityPerCPUId[cpuId] += self.tasks[taskId].getTotalResources()

        self.updateHighestCost()
        return True

    def findFeasibleAssignments(self, talk):
        feasibleAssignments = []
        for time_slot in range(0, self.t):
            for room in range(0, self.r):
                feasible = self.assign(talk, time_slot, room)
                if not feasible: continue
                assignment = Assignment(talk, time_slot, room, self.cost)
                feasibleAssignments.append(assignment)
                self.unassign(talk, time_slot, room)
        return feasibleAssignments


    def findBestFeasibleAssignment(self, taskId):
        bestAssignment = Assignment(taskId, None, float('infinity'))
        for cpu in self.cpus:
            cpuId = cpu.getId()
            feasible = self.assign(taskId, cpuId)
            if not feasible: continue

            curHighestLoad = self.cost
            if bestAssignment.highestLoad > curHighestLoad:
                bestAssignment.cpuId = cpuId
                bestAssignment.highestLoad = curHighestLoad

            self.unassign(taskId, cpuId)

        return bestAssignment

    def __str__(self):
        strSolution = 'z = %10.8f;\n' % self.cost
        if self.cost == float('inf'): return strSolution

        for talk in self.talkToTimeSlotRoom:
            slot = list(self.talkToTimeSlotRoom[talk].keys())[0]
            room = list(self.talkToTimeSlotRoom[talk][slot].keys())[0]
            strSolution += "Talk %s --> slot %s, room %s\n" % (talk+1, slot+1, room+1)

        return strSolution

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()
