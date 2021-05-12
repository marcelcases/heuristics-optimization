'''
AMMM P3 Instance Generator v2.0
Main function.
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

import sys
from Heuristics.datParser import DATParser
from Instances.InstanceGenerator import InstanceGenerator
from AMMMGlobals import AMMMException

def run():
    try:
        configFile = "config\config.dat"
        print("AMMM Instance Generator")
        print("-----------------------")
        print("Reading Config file %s..." % configFile)
        config = DATParser.parse(configFile)
        print("Creating Instances...")
        instGen = InstanceGenerator(config)
        instGen.generate()
        print("Done")
        return 0
    except AMMMException as e:
        print("Exception: %s", e)
        return 1

if __name__ == '__main__':
    sys.exit(run())
