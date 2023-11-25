import typing
from SpherePack import SpherePack
from yade import pack
from Sphere import Sphere

class SphereCloud:
    def __init__(self, spherePack: SpherePack, sphereNumber: int, sphereRadius: float, sphereSizeScatter:float, sphereMaterial, sphereColor=(0.64, 0.16, 0.16)) -> None:
        self.Pack = pack.SpherePack()
        self.spherePack = spherePack
        self.sphereNumber:int = sphereNumber
        self.sphereRadius:float = sphereRadius
        self.sphereSizeScatter = sphereSizeScatter
        
        #
        self.Pack.makeCloud(spherePack.MinCorner, spherePack.MaxCorner, rMean=sphereRadius, rRelFuzz=sphereSizeScatter, num=sphereNumber)
        self.Pack.toSimulation(material=sphereMaterial, color=sphereColor)
        
        def setSphere() -> typing.List[Sphere]:
            spheres = []
            for i in range(self.sphereNumber):
                spheres.append(Sphere(O.bodies[(i*-1)-1]))
            
            return spheres
        
        self.spheres = setSphere()
    
                