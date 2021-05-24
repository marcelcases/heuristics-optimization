'''
AMMM P3 Instance Generator v2.0
Instance Generator class.
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
'''

import os, random
from AMMMGlobals import AMMMException
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)

class InstanceGenerator(object):
    # Generate instances based on read configuration.

    def __init__(self, config):
        self.config = config

    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances

        n = self.config.n
        t = self.config.t
        r = self.config.r
        d = self.config.d

        if not os.path.isdir(instancesDirectory):
            raise AMMMException('Directory(%s) does not exist' % instancesDirectory)

        instancePath = os.path.join(instancesDirectory, '%s_%d.%s' % (fileNamePrefix, 0, fileNameExtension))
        fInstance = open(instancePath, 'w')

        fInstance.write('n = %d;\n' % n)
        fInstance.write('t = %d;\n' % t)
        fInstance.write('r = %d;\n' % r)
        fInstance.write('d = %d;\n\n' % d)

        load = n/(t*r)
        # p = [0.5, 0.5]
        # p = [0.55, 0.45]
        # p = [0.575, 0.425]
        # p = [0.585, 0.415]
        # p = [0.6, 0.4]
        p = [0.625, 0.375]
        # p = [0.65, 0.35]
        # p = [0.675, 0.325]
        # p = [0.68, 0.32]
        # p = [0.7, 0.3]
        # p = [0.75, 0.25]
        # p = [0.765, 0.235]
        # p = [0.775, 0.225]
        # p = [0.785, 0.215]
        # p = [0.8, 0.2]
        # p = [0.85, 0.15]
        # p = [0.875, 0.125]
        # p = [0.9, 0.1]

        # Populate P matrix
        P = np.zeros((n,n), dtype=int)
        for i in range(n):
            for j in range(n):
                if i==j:
                    P[i][j]=0 # zeros diagonal
                elif i<j:
                    P[i][j]=np.random.choice([0,1], p=p)
                    P[j][i]=P[i][j] # make symmetric

        # Populate S matrix
        S = np.zeros((n,n), dtype=int)
        for i in range(n):
            for j in range(n):
                if i==j:
                    S[i][j]=0 # zeros diagonal
                elif i<j:
                    S[i][j]=np.random.choice([0,1], p=p)
                    S[j][i]=S[i][j] # make symmetric

        fInstance.write('P = {};\n\n'.format(P))
        fInstance.write('S = {};\n\n'.format(S))

        fInstance.close()
