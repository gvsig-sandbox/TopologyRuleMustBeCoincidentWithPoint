import gvsig
import sys

from gvsig import commonsdialog
from org.gvsig.tools.dispose import DisposeUtils

def main(*args):
    currentProject = gvsig.currentProject()
    if currentProject.getView("MustBeCoincidentWith") == None:
        currentProject.createView("MustBeCoincidentWith")
    view = currentProject.getView("MustBeCoincidentWith")
    view.showWindow()
    message = ""
    if view.getLayer("Input layer") == None:
        try:
            gvsig.loadShapeFile(gvsig.getResource(__file__, "data", "Input layer.shp"))
        except:
            message += "\n'Input layer.shp'"
    if view.getLayer("Coverage layer") == None:
        try:
            gvsig.loadShapeFile(gvsig.getResource(__file__, "data", "Coverage layer.shp"))
        except:
            message += "\n'Coverage layer.shp'"
    if message == "":
        inputLayer = view.getLayer("Input layer")
        coverageLayer = view.getLayer("Coverage layer")
        if inputLayer != None and coverageLayer != None:
            schema = inputLayer.getSchema()
            outputSchema = gvsig.createSchema(schema)
            outputLayer = gvsig.createShape(outputSchema)
            outputLayer.edit()
            try:
                inputFeatures = inputLayer.features()
                for inputFeature in inputFeatures:
                    coverageFeatures = coverageLayer.features().iterator()
                    point = dict()
                    flag = False
                    while coverageFeatures.hasNext() and not flag:
                        coverageFeature = coverageFeatures.next()
                        if inputFeature.geometry().intersects(coverageFeature.geometry()):
                            flag = True
                    if not flag:
                        for field in schema:
                            if str(field.getDataTypeName()) != "Long":
                                point[field.getName()] = inputFeature.get(field.getName())
                            else:
                                point[field.getName()] = long(inputFeature.get(field.getName()))
                        outputLayer.append(point)
                    else:
                        flag = False
                message = "Points not coincident with:"
                features = output.features()
                for feature in features:
                    message += "\n" + feature.get("NAME")
                title = "MustBeCoincidentWith"
                messageType = commonsdialog.IDEA
                root = None
                commonsdialog.msgbox(message, title, messageType, root)
                print message
                if features != None:
                    DisposeUtils.disposeQuietly(features)
            except:
                ex = sys.exc_info()[1]
                print ex.__class__.__name__ + " - " + str(ex)
            finally:
                DisposeUtils.disposeQuietly(inputFeatures)
                DisposeUtils.disposeQuietly(coverageFeatures)
            
            outputLayer.commit()
            outputLayer.setName("Points not coincident with")
            view.addLayer(outputLayer)
            view.getMapContext().getViewPort().setEnvelope(outputLayer.getFullEnvelope())
            view.showWindow()
    else:
        message = "It wasn't possible to load:" + message
        title = "MustBeCoincidentWith"
        messageType = commonsdialog.FORBIDEN
        root = None
commonsdialog.msgbox(message, title, messageType, root)
