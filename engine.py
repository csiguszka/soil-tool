

def setShapeEngineDeposition():
    pass

def setClumpEngineDeposition(OdtTimeStepMultipl=0.5, newtonIntergratorDamping=0.9):
    O.engines=[
        ForceResetter(),
        InsertionSortCollider([Bo1_Sphere_Aabb(),Bo1_Facet_Aabb()]),
        InteractionLoop(
            [Ig2_Sphere_Sphere_ScGeom6D(),Ig2_Facet_Sphere_ScGeom()],
            [Ip2_FrictMat_FrictMat_FrictPhys(),Ip2_CohFrictMat_CohFrictMat_CohFrictPhys(label="cohesiveIp")],
            [Law2_ScGeom_FrictPhys_CundallStrack(),Law2_ScGeom6D_CohFrictPhys_CohesionMoment(
                useIncrementalForm=True, always_use_moment_law=True, creep_viscosity=.0, shear_creep=False, twist_creep=False, label='cohesiveLaw')]
        ),
        NewtonIntegrator(gravity=(0,0,-9.81),damping=newtonIntergratorDamping),
    ]
    O.dt=OdtTimeStepMultipl*PWaveTimeStep()


