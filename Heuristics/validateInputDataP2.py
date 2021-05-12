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
        for paramName in ['nTasks', 'nCPUs', 'rt', 'rc']:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter/Set(%s) not contained in Input Data' % str(paramName))

        # Validate nTasks
        nTasks = data.nTasks
        if not isinstance(nTasks, int) or (nTasks <= 0):
            raise AMMMException('nTasks(%s) has to be a positive integer value.' % str(nTasks))

        # Validate nCPUs
        nCPUs = data.nCPUs
        if not isinstance(nCPUs, int) or (nCPUs <= 0):
            raise AMMMException('nCPUs(%s) has to be a positive integer value.' % str(nCPUs))

        # Validate rt
        data.rt = list(data.rt)
        rt = data.rt
        if len(rt) != nTasks:
            raise AMMMException('Size of rt(%d) does not match with value of nTasks(%d).' % (len(rt), nTasks))

        for value in rt:
            if not isinstance(value, (int, float)) or (value < 0):
                raise AMMMException('Invalid parameter value(%s) in rt. Should be a float greater or equal than zero.' % str(value))

        # Validate rc
        data.rc = list(data.rc)
        rc = data.rc
        if len(rc) != nCPUs:
            raise AMMMException('Size of rc(%d) does not match with value of nCPUs(%d).' % (len(rc), nCPUs))

        for value in rc:
            if not isinstance(value, (int, float)) or (value < 0):
                raise AMMMException('Invalid parameter value(%s) in rc. Should be a float greater or equal than zero.' % str(value))

