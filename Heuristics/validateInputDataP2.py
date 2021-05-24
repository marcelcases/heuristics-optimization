"""
AMMM Lab Heuristics
Instance file validator v2.0
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

from AMMMGlobals import AMMMException


# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the instance.
class ValidateInputData(object):
    @staticmethod
    def validate(data):
        # Validate that all input parameters were found
        for paramName in ['n', 't', 'r', 'd', 'P', 'S']:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter/Set(%s) not contained in Input Data' % str(paramName))

        # Validate n
        n = data.n
        if not isinstance(n, int) or (n <= 0):
            raise AMMMException('n must be int > 0')

        # Validate t
        t = data.t
        if not isinstance(t, int) or (t <= 0):
            raise AMMMException('t must be int > 0')

        # Validate d
        d = data.d
        if not isinstance(d, int) or (d <= 0):
            raise AMMMException('distance must be bigger than 0')

        # Validate p
        data.P = list(data.P)
        p = data.P
        if len(p) != n:
            raise AMMMException('Size of p does not match with value of n')
        contador = 0
        for value in p:
            data.P[contador] = list(value)
            if len(data.P[contador]) != n:
                raise AMMMException('Invalid parameter p, each row must have n columns')
            for item in data.P[contador]:
                if not isinstance(item, int) or (item < 0) or (item > 1):
                    raise AMMMException('Invalid parameter p, row/column must have a binary value 0,1')
            contador += 1

        # Validate Q
        data.S = list(data.S)
        s = data.S
        if len(s) != n:
            raise AMMMException('Size of s does not match with value of n')
        contador = 0
        for value in s:
            data.S[contador] = list(value)
            if len(data.S[contador]) != n:
                raise AMMMException('Invalid parameter s, each row must have n columns')
            for item in data.S[contador]:
                if not isinstance(item, int) or (item < 0) or (item > 1):
                    raise AMMMException('Invalid parameter q, row/column must have a binary value 0,1')
            contador += 1


