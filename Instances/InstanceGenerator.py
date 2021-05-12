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

        # Populate P matrix
        P = np.zeros((n,n), dtype=int)
        for i in range(n):
            for j in range(n):
                if i==j:
                    P[i][j]=0 # zeros diagonal
                elif i<j:
                    P[i][j]=np.random.choice([0,1], p=[0.75,0.25])
                    P[j][i]=P[i][j] # make symmetric

        # Populate S matrix
        S = np.zeros((n,n), dtype=int)
        for i in range(n):
            for j in range(n):
                if i==j:
                    S[i][j]=0 # zeros diagonal
                elif i<j:
                    S[i][j]=np.random.choice([0,1], p=[0.75,0.25])
                    S[j][i]=S[i][j] # make symmetric

        fInstance.write('P = {};\n\n'.format(P))
        fInstance.write('Q = {};\n\n'.format(S))

        fInstance.close()
