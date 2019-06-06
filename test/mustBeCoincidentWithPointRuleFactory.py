# encoding: utf-8

import gvsig
from gvsig import uselib
uselib.use_plugin("org.gvsig.topology.app.mainplugin")

from org.gvsig.fmap.geom import Geometry
from org.gvsig.tools.util import ListBuilder
from org.gvsig.topology.lib.api import TopologyLocator
from org.gvsig.topology.lib.api import TopologyManager
from org.gvsig.topology.lib.spi import AbstractTopologyRuleFactory
from org.gvsig.topology.lib.api import TopologyPlan
from org.gvsig.topology.lib.api import TopologyRule

from gvsig import logger
from gvsig import LOGGER_WARN,LOGGER_INFO,LOGGER_ERROR

from mustBeCoincidentWithPointRule import MustBeCoincidentWithPointRule
from org.gvsig.topology.lib.api import TopologyLocator


class MustBeCoincidentWithPointRuleFactory(AbstractTopologyRuleFactory):
  #NAME = "MustBeCoincidentWithPoint"
    
  def __init__(self):
    AbstractTopologyRuleFactory.__init__(
      self,
      "MustBeCoincidentWithPoint",
      "Must Be Coincident With", 
      "This rule requires that the points in both datasets must be coincident, if not, a points errors layer is created. This rule is used when points must coincide. It is useful for modelling networks like electricity. For example in an electricity or water supply network, the water and light meters must match with the service points.", 
      ListBuilder().add(Geometry.TYPES.SURFACE).add(Geometry.TYPES.MULTISURFACE).asList()
      )
  def createRule(self, plan, dataSet1, dataSet2, tolerance):
    #TopologyPlan plan, String dataSet1, String dataSet2, double tolerance
    rule = MustBeCoincidentWithPointRule(plan, self, tolerance, dataSet1)
    return rule

def selfRegister():
    try:
      manager = TopologyLocator.getTopologyManager()
      manager.addRuleFactories(MustBeCoincidentWithPointRuleFactory())
    except Exception as ex:
      logger("Can't register topology rule from MustBeCoincidentWithPointRuleFactory."+str(ex), LOGGER_WARN)

def main(*args):
  print "* Executing MustBeCoincidentWithPointRuleFactory main."
  selfRegister()
  pass
