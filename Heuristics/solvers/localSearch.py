"""
AMMM Lab Heuristics
Local Search algorithm
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
import time
from Heuristics.solver import _Solver
from AMMMGlobals import AMMMException


# A change in a solution in the form: move taskId from curCPUId to newCPUId.
# This class is used to perform sets of modifications.
# A new solution can be created based on an existing solution and a list of
# changes using the createNeighborSolution(solution, moves) function.
class Move(object):
    def __init__(self, talkId, curTimeSlot, curRoom ,newTimeSlot, newRoom):
        self.talkId = talkId
        self.curTimeSlot = curTimeSlot
        self.curRoom = curRoom
        self.newTimeSlot = newTimeSlot
        self.newRoom = newRoom


    def __str__(self):
        return "talk: %d Move: %d -> %d" % (self.talkId, self.curTimeSlot, self.newTimeSlot)


# Implementation of a local search using two neighborhoods and two different policies.
class LocalSearch(_Solver):
    def __init__(self, config, instance):
        self.enabled = config.localSearch
        self.nhStrategy = config.neighborhoodStrategy
        self.policy = config.policy
        self.maxExecTime = config.maxExecTime
        super().__init__(config, instance)

    def createNeighborSolution(self, solution, moves):

        newSolution = copy.deepcopy(solution)

        for move in moves:
            newSolution.unassign(move.talkId, move.curTimeSlot, move.curRoom)

        for move in moves:
            newSolution.assign(move.talkId, move.newTimeSlot, move.newRoom)

        return newSolution

    def evaluateNeighbor(self, solution, moves):
        bestCost = solution.cost
        newSolution = copy.deepcopy(solution)
        for move in moves:
            newSolution.unassign(move.talkId, move.curTimeSlot, move.curRoom)

        for move in moves:
            feasible = newSolution.assign(move.talkId, move.newTimeSlot, move.newRoom)
            if feasible and newSolution.cost <= bestCost:
                bestCost = newSolution.cost

        return bestCost

    def getTimeSlotswithAssignments(self, solution):
        time_slots = list(range(0, solution.t))

        # create vector of assignments <task, <time_slot/room>>
        timeSlotsWithAssignments = []
        for time_slot in time_slots:
            assignedTalks = solution.getAssignedTalksToTimeSlot(time_slot)
            if assignedTalks is None: assignedTalks = []
            assignedTalksWithPenalizationVal = []
            for talk in assignedTalks:
                talkPair = (talk, self.instance.computePPair(talk),
                            list(solution.talkToTimeSlotRoom[talk][time_slot].keys())[0])
                assignedTalksWithPenalizationVal.append(talkPair)

            assignedTalksWithPenalizationVal.sort(key=lambda y: y[1], reverse=True)
            timeSlotWithAssignments = (time_slot, assignedTalksWithPenalizationVal)
            timeSlotsWithAssignments.append(timeSlotWithAssignments)

        # Sort assignments by the load of the assigned CPU in descending order.
        timeSlotsWithAssignments.sort(key=lambda aux: sum([v[1] for v in aux[1]]), reverse=True)
        return timeSlotsWithAssignments



    def exploreExchange(self, solution):

        curLowestCost = solution.getCost()
        bestNeighbor = solution

        # For the Exchange neighborhood and first improvement policy, try exchanging
        # two talks assigned to two different Assignments

        timeSlotswithAssignments = self.getTimeSlotswithAssignments(solution)
        nTimeSlots = len(timeSlotswithAssignments)

        for h in range(0, nTimeSlots-1):  # i = 0..(nCPUs-2)
            timeSlotPair_h = timeSlotswithAssignments[h]
            #availCapacityCPU_h = CPUPair_h[2]
            for th in range(0, len(timeSlotPair_h[1])):
                talkPair_h = timeSlotPair_h[1][th]
                for l in range(1, nTimeSlots):  # i = 1..(nCPUs-1)
                    timeSlotPair_l = timeSlotswithAssignments[l]
                    #availCapacityCPU_l = CPUPair_l[2]
                    for tl in range(0, len(timeSlotPair_l[1])):
                        talkPair_l = timeSlotPair_l[1][tl]
                        if (talkPair_l[1] != talkPair_h[1]) :
                            moves = [Move(talkPair_h[0], timeSlotPair_h[0], talkPair_h[2], timeSlotPair_l[0], talkPair_l[2]),
                                     Move(talkPair_l[0], timeSlotPair_l[0], talkPair_l[2], timeSlotPair_h[0], talkPair_h[2],)]
                            neighborLowestCost = self.evaluateNeighbor(solution, moves)
                            if neighborLowestCost <= curLowestCost:
                                neighbor = self.createNeighborSolution(solution, moves)
                                if neighbor is None:
                                    raise AMMMException('[exploreExchange] No neighbouring solution could be created')
                                if self.policy == 'FirstImprovement': return neighbor
                                else:
                                    bestNeighbor = neighbor
                                    curLowestCost = neighborLowestCost
        return bestNeighbor

    def exploreNeighborhood(self, solution):
        if self.nhStrategy == 'TaskExchange': return self.exploreExchange(solution)
        else: raise AMMMException('Unsupported NeighborhoodStrategy(%s)' % self.nhStrategy)

    def solve(self, **kwargs):
        initialSolution = kwargs.get('solution', None)
        if initialSolution is None:
            raise AMMMException('[local search] No solution could be retrieved')

        if not initialSolution.isFeasible(): return initialSolution
        self.startTime = kwargs.get('startTime', None)
        endTime = kwargs.get('endTime', None)

        incumbent = initialSolution
        incumbentCost = incumbent.getCost()
        iterations = 0

        # keep iterating while improvements are found
        while time.time() < endTime:
            iterations += 1
            neighbor = self.exploreNeighborhood(incumbent)
            if neighbor is None: break
            neighborCost = neighbor.cost
            if incumbentCost <= neighborCost: break
            incumbent = neighbor
            incumbentCost = neighborCost

        return incumbent
