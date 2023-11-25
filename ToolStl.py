from yade import ymport

class Tool():
    def __init__(self, path, material, pos, color=(1, 0.16, 0.16)) -> None:
        self.stl = ymport.stl(path, color=color, material=material)
        for point in self.stl:
            point.state.pos += pos
        self.tool = O.bodies.append(self.stl)
