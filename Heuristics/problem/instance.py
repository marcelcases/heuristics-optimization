"""
AMMM Lab Heuristics
Representation of a problem instance
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

from Heuristics.problem.Task import Task
from Heuristics.problem.CPU import CPU
from Heuristics.problem.solution import Solution


class Instance(object):
    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData
        self.n = inputData.n
        self.t = inputData.t
        self.r = inputData.r
        self.d = inputData.d
        self.p = inputData.P
        self.q = inputData.Q

    def getN(self):
        return self.n

    def getT(self):
        return self.t

    def getR(self):
        return self.r

    def getP(self):
        return self.r

    def getD(self):
        return self.d

    def computeNPair(self, talk):
        contador = 0
        for j in self.p[talk]:
            if j == 1:
                contador += 1
        return contador

    def createSolution(self):
        solution = Solution(self.n, self.t, self.r, self.d, self.p, self.q)
        solution.setVerbose(self.config.verbose)
        return solution

    def checkInstance(self):
        """""
        totalCapacityCPUs = 0.0
        maxCPUCapacity = 0.0
        for cpu in self.cpus:
            capacity = cpu.getTotalCapacity()
            totalCapacityCPUs += capacity
            maxCPUCapacity = max(maxCPUCapacity, capacity)

        totalResourcesTasks = 0.0
        for task in self.tasks:
            resources = task.getTotalResources()
            totalResourcesTasks += resources
            if resources > maxCPUCapacity: return False

        return totalCapacityCPUs >= totalResourcesTasks
        """""
        #TODO check desabilitado temporalmente
        return True

