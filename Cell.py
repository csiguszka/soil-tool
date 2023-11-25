from yade import Vector3

class Cell():
    def __init__(self, x:int, y:int, z:int, cellSize:float) -> None:
        self.pos = Vector3(x, y, z)
        self.MaxcornerPos = Vector3(x+cellSize, y+cellSize, z+cellSize) #right top
        self.MincornerPos = Vector3(x-cellSize, y-cellSize, z-cellSize)  #left bottom
        self.spheres = []
        self.velocity = Vector3(0, 0, 0)