from yade import pack, plot, ymport, export, Vector3
import sys

sys.path.append("/home/hernyo/Dokumentumok/Yade_Teddy/Innovacio") #gyökér könyvtár

import time
from SpherePack import SpherePack
from SphereCloud import SphereCloud
from Clump import Clump
from ToolStl import Tool
from streamLine import StreamLineVolume
from Cell import Cell
import engine
import typing


###func:

#engine:
def setClumpEngineDeposition(OdtTimeStepMultipl=0.5, newtonIntergratorDamping=0.9, pyRunnerCase=5):
    O.engines=[
        ForceResetter(),
        InsertionSortCollider([Bo1_Sphere_Aabb(),Bo1_Facet_Aabb()]),
        InteractionLoop(
            [Ig2_Sphere_Sphere_ScGeom6D(),Ig2_Facet_Sphere_ScGeom()],
            [Ip2_FrictMat_FrictMat_FrictPhys(),Ip2_CohFrictMat_CohFrictMat_CohFrictPhys(label="cohesiveIp")],
            [Law2_ScGeom_FrictPhys_CundallStrack(),Law2_ScGeom6D_CohFrictPhys_CohesionMoment(
                useIncrementalForm=True, always_use_moment_law=True, creep_viscosity=.0, shear_creep=False, twist_creep=False, label='cohesiveLaw')]
        ),
        NewtonIntegrator(gravity=(0,0,-9.81),damping=newtonIntergratorDamping, label='Newton'),
    ]
    for i in range(pyRunnerCase):
        i = str(i)
        O.engines += PyRunner(command='base()',iterPeriod=99999,label="base"),
    O.dt=OdtTimeStepMultipl*PWaveTimeStep()

def MoveStl(StlObject):
    O.engines=O.engines+[CombinedKinematicEngine(ids=StlObject.tool,label='combEngine') + TranslationEngine(translationAxis=StltranslationAxis,velocity=StlVelocity,ids=StlObject.tool) + HarmonicMotionEngine(A=[0,.0,0.0], f=[0,0.00,0.0], fi = [0.0,0.0,pi], ids = StlObject.tool),
    NewtonIntegrator(gravity=(0,0,-9.81),damping=0.00)]
    O.dt=StlMoveTimeStepMultipl*PWaveTimeStep()
    O.run()


def addPyRuner(command, iterPeriod=1, label='PyRunner'):
    for i in range(len(O.engines)):
        CurrentLabel = O.engines[i].label
        if CurrentLabel == 'base':
            
            O.engines[i].label = label
            O.engines[i].iterPeriod = iterPeriod
            
            if "()" in command:
                O.engines[i].command = command 
            else:
                O.engines[i].command = command + "()"
            break


def deletePyRunner(label='PyRunner', command=None):
    for i in range(len(O.engines)):
        CurrentLabel = O.engines[i].label
        try:
            CurrentCommand = O.engines[i].command
        except:
            CurrentCommand = "null"
        if CurrentLabel == label or CurrentCommand == command or CurrentCommand + "()" == command:
            O.engines[i].label = '1'
            O.engines[i].iterPeriod = 99999
            O.engines[i].command = "base()"
            break

def CheckUnbalanced():
    print(unbalancedForce(), O.time)
    if O.iter<minIter or unbalancedForce()>unbalancedDeposit: return
    deletePyRunner('unbalance')
    EndCheckUnbalaced()

def stopStl():
    # if (O.bodies[-1].state.pos[0] < StlEndPos[0] or O.bodies[-1].state.pos[1] < StlEndPos[1] or O.bodies[-1].state.pos[2] < StlEndPos[2]) and unbalancedForce() < StlEndUnbalanced:
    if (O.bodies[-1].state.pos[0] < StlEndPos[0] or O.bodies[-1].state.pos[1] < StlEndPos[1] or O.bodies[-1].state.pos[2] < StlEndPos[2]):
        global cells
        cells = calculateCell()
        O.pause()
        deletePyRunner(command='stopStl()')
        print("UwU")

def EndCheckUnbalaced():
    O.pause()
    # slice()
    SetCoch()
    global tool
    tool = Tool(ToolPath, StlMater, StlPos, StlColor)
    MoveStl(tool)
    toolSizeX = XSizeCalculateTool(tool)
    toolSizeY = YSizeCalculateTool(tool)
    toolSizeZ = ZSizeCalculateTool(tool)
    global volumes
    volumes = StreamLineVolume(toolSizeY*2, toolSizeY*4, toolSizeX*1.5, spherePack.MinCorner[2], toolSizeZ)
    addPyRuner('stopStl()', 500, "stopStl")
    


def SetCoch():
    O.engines[2].physDispatcher.functors[1].setCohesionNow = True
    O.engines[2].physDispatcher.functors[1].setCohesionOnNewContacts = False

def slice():
    for clump in clumps.clumps:
        if clump.sphere.state.pos[2] > AfterUnbalancedSliceZ:
            O.bodies.erase(clump.sphere.id)

def YSizeCalculateTool(tool):
    pos = []
    for i in tool.tool:
        pos.append(O.bodies[i].state.pos[1])
    toolMin = min(pos)
    toolMax = max(pos)
    return toolMax-toolMin

def XSizeCalculateTool(tool):
    pos = []
    for i in tool.tool:
        pos.append(O.bodies[i].state.pos[0])
    toolMin = min(pos)
    toolMax = max(pos)
    return toolMax-toolMin

def ZSizeCalculateTool(tool):
    pos = []
    for i in tool.tool:
        pos.append(O.bodies[i].state.pos[2])
    toolMin = min(pos)
    toolMax = max(pos)
    return toolMax-toolMin

def MaxYIndexCalculate(tool):
    Zindex = 0
    Zmin = O.bodies[tool.tool[0]].state.pos[2]
    for i in range(len(tool.tool)):
        if Zmin > O.bodies[tool.tool[i]].state.pos[2]:
            Zmin = O.bodies[tool.tool[i]].state.pos[2]
            Zindex = i
    return Zindex

def CreateVolumeOne_eighth(maxCellCorner, minCellCorner, variation):
    MaxYIndex = MaxYIndexCalculate(tool)
    startPos = O.bodies[tool.tool[MaxYIndex]].state.pos
    currentPos = O.bodies[tool.tool[MaxYIndex]].state.pos
    cells = set()
    while(currentPos[0] < maxCellCorner[0]) if variation[0] else currentPos[0] > minCellCorner[0]:
        cells.add(Cell(currentPos[0], currentPos[1], currentPos[2], cellSize))
        while(currentPos[1] < maxCellCorner[1]) if variation[1] else currentPos[1] > minCellCorner[1]:
            cells.add(Cell(currentPos[0], currentPos[1], currentPos[2], cellSize))
            while(currentPos[2] < maxCellCorner[2]) if variation[2] else currentPos[2] > minCellCorner[2]:
                cells.add(Cell(currentPos[0], currentPos[1], currentPos[2], cellSize))
                if variation[2]:
                    currentPos[2] += cellSize
                else:
                    currentPos[2] -= cellSize
            if variation[1]:
                currentPos[1] += cellSize
            else:
                currentPos[1] -= cellSize
            currentPos[2] = startPos[2]
        if variation[0]:
            currentPos[0] += cellSize
        else:
            currentPos[0] -= cellSize
        currentPos[1] = startPos[1]
    return cells

def variations():
    combinations = []
    for i in [True, False]:
        for j in [True, False]:
            for k in [True, False]:
                combinations.append([i, j, k])

    return combinations

def IsClumpInCell(ClumpPos, minCorner, maxCorner):
    # Az x, y, z pontnak mindegyik dimenzióban a megfelelő tartományban kell lennie
    if minCorner[0] <= ClumpPos[0] <= maxCorner[0] and \
       minCorner[1] <= ClumpPos[1] <= maxCorner[1] and \
       minCorner[2] <= ClumpPos[2] <= maxCorner[2]:
        return True
    else:
        return False

def calculateCell():
    maxCellCorner = [volumes.side, volumes.behind, volumes.top] #right top
    minCellCorner = [-volumes.side, -volumes.ahead, -volumes.bottom] #left bottom

    cells = set()
    combinations = variations()
    for combination in combinations:
        cells = cells.union(CreateVolumeOne_eighth(maxCellCorner, minCellCorner, combination))
    
    for clump in clumps.clumps:
        pos = clump.sphere.state.pos
        for cell in cells:
            inCell = IsClumpInCell(pos, cell.MincornerPos, cell.MaxcornerPos)
            if inCell:
                cell.spheres.append(clump)
                break
    for cell in cells:
        sum = Vector3(0, 0, 0)
        for clump in cell.spheres:
            sum += clump.sphere.state.vel
        if len(cell.spheres) != 0:
            cell.velocity = sum/len(cell.spheres)
        with open("Kakaoscsiga.txt", "a", encoding="utf-8") as f:
            f.write(f"{cell.pos[0]};{cell.pos[1]};{cell.pos[2]};{cell.velocity[0]};{cell.velocity[1]};{cell.velocity[2]}\n")
    return cells

        
###Params:

#Box:
BoxExtensionXYZ: typing.List[float] = [1.5, 2.0, 1]
BoxMaterial = FrictMat(young=1e12,poisson=0.3,density=7850,frictionAngle=radians(20))

#Sphere:
sphereColor = (0.64, 0.16, 0.16)
sphereRadius: float = 0.03
sphereSizeScatter: float = 0.3
sphereNumber: int = 7000
sphereFrictionAngle:float = 20 # 10-40  !
sphereNormalCohesion:float = 30000 # 4000-40000  !
sphereEtaRoll_etaTwist:float = 0.02 # 0.0001-0.4
sphereMater = CohFrictMat(young=5e6, poisson=0.4,density=3200, frictionAngle=radians(sphereFrictionAngle),normalCohesion=sphereNormalCohesion,shearCohesion=sphereNormalCohesion/2, momentRotationLaw=True,etaRoll=sphereEtaRoll_etaTwist, etaTwist=sphereEtaRoll_etaTwist, label='spheres')

#Clump:
ClumpPersent:float = float(10)
ClumpGap:float = 0.008/100*ClumpPersent
relRedList: typing.List[list] = [[.004, .004, .004, .004]]
relPosList:list = [[[0,0,0], [0,ClumpGap,0], [0,ClumpGap*2,0], [0,ClumpGap*3,0]]]
percent:list = [0.99999]

#tool:
ToolPath = "stl/kozepes25.stl"
StlColor = (1, 0.16, 0.16)
StlPos = Vector3(0, 1, 0.1)
StlMater = FrictMat(young=1e12,poisson=0.3,density=7850,frictionAngle=radians(20))
StlMoveTimeStepMultipl:float = 0.1
StlEndPos:typing.List[float] = [0, 0.37, 0] #[0, -1.24, 0]
StltranslationAxis:typing.List[float] = [0, -1, 0]
StlVelocity:float = 6.5/3.6 #[m/s]
tool = None
StlEndUnbalanced = 0.2

#engine:
timeStepMultiplDeposition:float = 0.5
dampingDeposition:float = 0.9

#unbalanced:
minIter:float = 8000
unbalancedDeposit:float = 0.02
AfterUnbalancedSliceZ:float = 1

#streamLine:
cellSize:float = sphereRadius*2*3 #[m]
toolSize:float = None
volumes: StreamLineVolume = None
cells = None

#####
spherePack: SpherePack = SpherePack(geom, BoxExtensionXYZ, BoxMaterial)
sphereCloud: SphereCloud = SphereCloud(spherePack, sphereNumber, sphereRadius, sphereSizeScatter, sphereMater)
clumps = Clump(clumpTemplate, relRedList, relPosList, percent)
setClumpEngineDeposition(timeStepMultiplDeposition, dampingDeposition, 3)
addPyRuner('CheckUnbalanced()', 500, "unbalance")


# addPyRuner('calculateCell()', 1000, "stopStl")
# O.bodies.append(sphere(center=[0, 0, 0],radius=0.2))
O.run()
