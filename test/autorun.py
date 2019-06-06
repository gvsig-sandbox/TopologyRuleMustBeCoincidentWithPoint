# encoding: utf-8

import gvsig
from gvsig import uselib
uselib.use_plugin("org.gvsig.topology.app.mainplugin")

from mustBeCoincidentWithPointRuleFactory import selfRegister

from org.gvsig.topology.lib.api import TopologyLocator

def main(*args):
  selfRegister()