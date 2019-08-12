# encoding: utf-8

import gvsig
import sys

from org.gvsig.topology.lib.spi import AbstractTopologyRuleAction

class DeletePointAction(AbstractTopologyRuleAction):
    
    def __init__(self):
        AbstractTopologyRuleAction.__init__(
            self,
            "MustBeCoincidentWithPoint",
            "DeletePointAction",
            "Delete Point Action",
            "This action deletes the point errors, these are the no coincident points. Delete the entities that do not comply with the rule, always taking account the established tolerance."
        )
    
    def execute(self, rule, line, parameters):
		#TopologyRule rule, TopologyReportLine line, DynObject parameters) {
        try:
            dataSet = rule.getDataSet1()
            dataSet.delete(line.getFeature1())
        except:
            ex = sys.exc_info()[1]
            gvsig.logger("Can't execute action. Class Name: " + ex.__class__.__name__ + ". Exception: " + str(ex), gvsig.LOGGER_ERROR)

def main(*args):
    pass