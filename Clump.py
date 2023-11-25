import typing
from Sphere import Sphere

class Clump:
    def __init__(self, YadeClumpTemplateVariable, relRedList, relPosList, percent, clumpColor=(0.64, 0.16, 0.16)) -> None:
        
        def createClump() -> None:
            templates=[]
            for i in range(len(relRedList)):
                templates.append(YadeClumpTemplateVariable(relRadii=relRedList[i],relPositions=relPosList[i]))
            O.bodies.replaceByClumps(templates, percent)
        
        def setClumpandSphere() -> typing.List:
            clumps = []
            spheres = []
            for i in range(CurrentOLen, len(O.bodies)):
                O.bodies[i].shape.color = clumpColor
                if O.bodies[i].isClump:
                    clumps.append(Sphere(O.bodies[i]))
                else:
                    spheres.append(Sphere(O.bodies[i]))
            return clumps, spheres

        CurrentOLen = len(O.bodies)
        createClump()
        self.clumps, self.spheres = setClumpandSphere()