# encoding: utf-8

import gvsig
import sys

from gvsig import uselib
uselib.use_plugin("org.gvsig.topology.app.mainplugin")

from org.gvsig.expressionevaluator import ExpressionEvaluatorLocator
from org.gvsig.topology.lib.api import TopologyLocator
from org.gvsig.topology.lib.spi import AbstractTopologyRule

from deletePointAction import DeletePointAction

class MustBeCoincidentWithPointRule(AbstractTopologyRule):
    
    geomName = None
    expression = None
    expressionBuilder = None
    
    def __init__(self, plan, factory, tolerance, dataSet1, dataSet2):
        AbstractTopologyRule.__init__(self, plan, factory, tolerance, dataSet1, dataSet2)
        #self.addAction(DeletePointAction())
    
    def check(self, taskStatus, report, feature1):
        try:
            store2 = self.getDataSet2().getFeatureStore()
            if self.expression == None:
                manager = ExpressionEvaluatorLocator.getManager()
                self.expression = manager.createExpression()
                self.expressionBuilder = manager.createExpressionBuilder()
                self.geomName = store2.getDefaultFeatureType().getDefaultGeometryAttributeName()
            point1 = feature1.getDefaultGeometry()
            tolerance1 = self.getTolerance()
            buffer1 = point1.buffer(tolerance1)
            theDataSet2 = self.getDataSet2()
            if theDataSet2.getSpatialIndex() != None:
                contains = False
                for featureReference in theDataSet2.query(buffer1):
                    feature2 = featureReference.getFeature()
                    point2 = feature2.getDefaultGeometry()
                    if buffer1.contains(point2):
                        contains = True
                        break
                if not contains:
                    report.addLine(self,
                                self.getDataSet1(),
                                self.getDataSet2(),
                                point1,
                                point1,
                                feature1.getReference(), 
                                None,
                                False,
                                "The point is not coincident."
                    )
            else:
                self.expression.setPhrase(
                    self.expressionBuilder.ifnull(
                        self.expressionBuilder.column(self.geomName),
                        self.expressionBuilder.constant(False),
                        self.expressionBuilder.ST_Contains(
                            self.expressionBuilder.geometry(buffer1),
                            self.expressionBuilder.column(self.geomName)
                        )
                    ).toString()
                )
                if theDataSet2.findFirst(self.expression) == None:
                    report.addLine(self,
                        self.getDataSet1(),
                        self.getDataSet2(),
                        point1,
                        point1,
                        feature1.getReference(),
                        None,
                        False,
                        "The point is not coincident."
                    )
        except:
            ex = sys.exc_info()[1]
            gvsig.logger("Can't execute rule. Class Name: " + ex.__class__.__name__ + ". Exception: " + str(ex), gvsig.LOGGER_ERROR)

def main(*args):
    pass
