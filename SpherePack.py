from yade import pack, plot, ymport, export
import typing

class SpherePack:
    def __init__(self, YadeGeomVariable, BoxExtension: typing.List[float], BoxMaterial ,CSYPos:int=0) -> None:
        self.Extension = BoxExtension
        self.Center = [0, 0, 1]
        self.MinCorner = (self.Center[0] - BoxExtension[0] , self.Center[1] - BoxExtension[1] , self.Center[2] - BoxExtension[2])
        self.MaxCorner = (self.Center[0] + BoxExtension[0] , self.Center[1] + BoxExtension[1] , self.Center[2] + BoxExtension[2])
        self.Mater = BoxMaterial
        O.bodies.append(YadeGeomVariable.facetBox(self.Center, self.Extension ,wallMask=31, material=BoxMaterial))

def CSYPosCalc(BoxExtension: typing.List[float], CSYPos:int) -> typing.List[float]:
    # -1 bal, 0 közép, 1 jobb
    if CSYPos == -1:
        return (BoxExtension[0]/2, 0, BoxExtension[2]/2)
    elif CSYPos == 1:
        return (BoxExtension[0]/-2, 0, BoxExtension[2]/2)
    else:
        return (0, 0, BoxExtension[2]/2)

