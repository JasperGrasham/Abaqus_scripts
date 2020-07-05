
# FE analyses of a plate with a hole

# The first three lines are required to import the required ABAQUS modules and create references to the objects that are
# defined by the module. The second line means that you are importing the symbolic constants (variables with a constant
# value) that have been defined by the scripting interface of ABAQUS. It is a good practice to include these three lines
# at the top of every script that you write. The third line is used for accessing the objects of Region() method which is
# defined the region Toolset modules.

from abaqus import *
from abaqusConstants import *
import regionToolset

# This line is required to make the ABAQUS viewport display nothing
session.viewports['Viewport: 1'].setValues(displayedObject=None)

holeModel = mdb.models['Model-1']

# Part creation

# These two statements will provide access to all the objects related to sketch and part. Including this is not
# mandatory, but it is good practice.

from sketch import *
from part import *

# In this set of set of statements, we would define a sketch by using the ConstrainedSketch() method. This method in
# turn has Line() method which can be used to draw the lines that we want in the sketch. Enter a value for
# 'sheetSize' based on your overall problem size.

holePart = holeModel.Part(name='Holepart', dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
holeSketch = holeModel.ConstrainedSketch(name='Plate Sketch', sheetSize=25.0)
holeSketch.Line(point1=(0.01, 0.0), point2=(0.12, 0.0))
holeSketch.Line(point1=(0.12, 0.0), point2=(0.12, 0.05))
holeSketch.Line(point1=(0.12, 0.05), point2=(0.0, 0.05))
holeSketch.Line(point1=(0.0, 0.05), point2=(0.0, 0.01))
holeSketch.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 0.01), point2=(0.01, 0.0), direction=CLOCKWISE) # cirlce

holePart.BaseShell(sketch=holeSketch)

holePart = holeModel.Part(name='Holepart2', dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
holeSketch = holeModel.ConstrainedSketch(name='Plate Sketch', sheetSize=25.0)
holeSketch.Line(point1=(0.0, 0.0), point2=(0.01, 0.0))
holeSketch.Line(point1=(0.0, 0.0), point2=(0.0, 0.01))
holeSketch.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 0.01), point2=(0.01, 0.0), direction=CLOCKWISE) # cirlce

holePart.BaseShell(sketch=holeSketch)

# Material creation

# First get access to objects relating to materials by using the import statement. Define the name of the material,
# which would be used further in the script. The Density() and Elastic() objects are used to specify the density
# and elastic properties as the name suggests. The input arguments to Density() looks so as it is actually a table
# with respect to temperature. Here we don't need that. So we use blank spaces. The same logic applies to Elastic()
# where it is a table with Young's modulus values with respect to Poisson's ratio

from material import *

holeMaterial = holeModel.Material(name='Steel')
holeMaterial.Elastic(table=((1.9e11, 0.31),   ))
#holeMaterial.Density(table=((7915, ),   ))
#holeMaterial.SpecificHeat(table=((465, ),  ))
#holeMaterial.Conductivity(table=((54, ),  ))
holeMaterial.Expansion(table=((0.0000012, ),  ))

# Section creation and assignment

# Get access to the section objects by using the import statement. Then create a solid section by using the
# HomogenousSolidSection() method. You can see that we have refered to the material we created in the last step.

from section import *
holeModel.HomogeneousSolidSection(name='Plate Section', material='Steel', thickness=0.01)

face_on_plate = holeModel.parts['Holepart'].faces.findAt(((0.05, 0.02, 0.0),))
plate_region = (face_on_plate,)
holeModel.parts['Holepart'].SectionAssignment(region=plate_region, sectionName='Plate Section')

face_on_hole = holeModel.parts['Holepart2'].faces.findAt(((0.005, 0.005, 0.0),))
hole_region = (face_on_hole,)
holeModel.parts['Holepart2'].SectionAssignment(region=hole_region, sectionName='Plate Section')

# Assembly creation

# Get access to the assembly objects by using the import statement. The rootAssembly is an assembly object which
# is a member of the Model object. Create an instance of the part by using the Instance() method. By default, the
# 'dependent' parameter is set to OFF. Set this to ON. We have already defined the part name as 'steadyPart'.
# We will refer to that now.

from assembly import *

# Partitions

sketchTransform1 = holeModel.parts['Holepart'].MakeSketchTransform(sketchPlane=face_on_plate[0], sketchPlaneSide=SIDE1,
                                                         origin=(0.0, 0.0, 0.0))
        # square around circle
holeSketch.Line(point1=(0.0, 0.02), point2=(0.02, 0.02))
holeSketch.Line(point1=(0.02, 0.02), point2=(0.02, 0.0))
holeSketch.Line(point1=(0.004, 0.004), point2=(0.02, 0.02))
        # other
holeSketch.Line(point1=(0.0, 0.025), point2=(0.12, 0.025))
holeSketch.Line(point1=(0.025, 0.0), point2=(0.025, 0.5))
holeModel.parts['Holepart'].PartitionFaceBySketch(faces=face_on_plate, sketch=holeSketch)

sketchTransform2 = holeModel.parts['Holepart2'].MakeSketchTransform(sketchPlane=face_on_hole[0], sketchPlaneSide=SIDE1,
                                                         origin=(0.0, 0.0, 0.0))
        # square in cirlce
holeSketch.Line(point1=(0.0, 0.005), point2=(0.004, 0.004))
holeSketch.Line(point1=(0.004, 0.004), point2=(0.005, 0.0))
holeModel.parts['Holepart2'].PartitionFaceBySketch(faces=face_on_hole, sketch=holeSketch)

holeAssembly = holeModel.rootAssembly
PlateInstance = holeAssembly.Instance(name='Plate Instance', part=holeModel.parts['Holepart'], dependent=ON)
HoleInstance = holeAssembly.Instance(name='Hole Instance', part=holeModel.parts['Holepart2'], dependent=ON)

# holeAssembly.instances['Hole Instance'].translate(vector=(0.121, 0.0, 0.0))

# Step creation

# Get access to the step objects by using the import statement. The StaticStep() method is used to create a
# static step which could be used for loading. This is the step next to 'Initial' step created by dafault. Enter the
# initial increment and maximum increment as shown below.

from step import *

#holeModel.HeatTransferStep(name='Step-1', previous='Initial',
#                                       timePeriod=15000.0, initialInc=1.0, minInc=0.15, maxInc=15000.0,
#                                       deltmx=1000.0)

holeModel.StaticStep(name='Step-1', previous='Initial', description='Loads is applied now')

#holeModel.CoupledTempDisplacementStep(name='Step-1', previous='Initial', timePeriod=1000.0, maxNumInc=1000,
#                                      initialInc=1.0, minInc=0.000015, maxInc=1000.0, deltmx=0.1)


#holeModel.CoupledTempDisplacementStep(name='Step-1', previous='Initial', response=STEADY_STATE, deltmx=None, cetol=None,
#                                      creepIntegration=None, amplitude=RAMP)

#holeModel.CoupledTempDisplacementStep(name='Step-2', previous='Step-1', response=STEADY_STATE, deltmx=None, cetol=None,
#                                      creepIntegration=None, amplitude=RAMP)

# Field output and history output request left at default.

from interaction import *

side1Edges1 = holeAssembly.instances['Plate Instance'].edges.getSequenceFromMask(mask=('#30000 ]',), )
region1 = regionToolset.Region(side1Edges=side1Edges1)


#holeModel.FilmCondition(name='Int-1', createStepName='Step-1',
#                                    surface=region1, definition=EMBEDDED_COEFF, filmCoeff=0.01,
#                                    filmCoeffAmplitude='', sinkTemperature=20, sinkAmplitude='',
#                                    sinkDistributionType=UNIFORM, sinkFieldName='')

side1Edges2 = holeAssembly.instances['Hole Instance'].edges.getSequenceFromMask(mask=('[#102 ]',), )
region2 = regionToolset.Region(side1Edges=side1Edges2)
holeModel.Tie(name='Constraint-1', master=region1, slave=region2,
                          positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON,
                          thickness=ON)

# Application of boundary conditions -

# Horizontal allowance of movement (roller) for bottom edge and vertical allowance of movement (roller) on
# left edge

# For doing this, we will first identify the point and use the findAT() method to find the top face and then redefine
# the face and then define the region.

edge_on_bottomface1 = HoleInstance.edges.findAt(((0.002, 0.0, 0.0),))
edge_on_bottomface2 = HoleInstance.edges.findAt(((0.006, 0.0, 0.0),))
edge_on_bottomface3 = PlateInstance.edges.findAt(((0.015, 0.0, 0.0),))
edge_on_bottomface4 = PlateInstance.edges.findAt(((0.021, 0.0, 0.0),))
edge_on_bottomface5 = PlateInstance.edges.findAt(((0.04, 0.0, 0.0),))

bottomface_region1 = regionToolset.Region(edges=edge_on_bottomface1)
bottomface_region2 = regionToolset.Region(edges=edge_on_bottomface2)
bottomface_region3 = regionToolset.Region(edges=edge_on_bottomface3)
bottomface_region4 = regionToolset.Region(edges=edge_on_bottomface4)
bottomface_region5 = regionToolset.Region(edges=edge_on_bottomface5)

edge_on_leftface1 = HoleInstance.edges.findAt(((0.0, 0.002, 0.0),))
edge_on_leftface2 = HoleInstance.edges.findAt(((0.0, 0.007, 0.0),))
edge_on_leftface3 = PlateInstance.edges.findAt(((0.0, 0.015, 0.0),))
edge_on_leftface4 = PlateInstance.edges.findAt(((0.0, 0.021, 0.0),))
edge_on_leftface5 = PlateInstance.edges.findAt(((0.0, 0.04, 0.0),))

leftface_region1 = regionToolset.Region(edges=edge_on_leftface1)
leftface_region2 = regionToolset.Region(edges=edge_on_leftface2)
leftface_region3 = regionToolset.Region(edges=edge_on_leftface3)
leftface_region4 = regionToolset.Region(edges=edge_on_leftface4)
leftface_region5 = regionToolset.Region(edges=edge_on_leftface5)

# After the defintion of regions, we wil use the DisplacementBC() to define the constraints that replicate the symmetry
# condition.

holeModel.XsymmBC(name='Left Edge X_Symmetry1', createStepName='Initial', region=leftface_region1, localCsys=None)
holeModel.XsymmBC(name='Left Edge X_Symmetry2', createStepName='Initial', region=leftface_region2, localCsys=None)
holeModel.XsymmBC(name='Left Edge X_Symmetry3', createStepName='Initial', region=leftface_region3, localCsys=None)
holeModel.XsymmBC(name='Left Edge X_Symmetry4', createStepName='Initial', region=leftface_region4, localCsys=None)
holeModel.XsymmBC(name='Left Edge X_Symmetry5', createStepName='Initial', region=leftface_region5, localCsys=None)
holeModel.YsymmBC(name='Bottom Edge Y_Symmetry1', createStepName='Initial', region=bottomface_region1, localCsys=None)
holeModel.YsymmBC(name='Bottom Edge Y_Symmetry2', createStepName='Initial', region=bottomface_region2, localCsys=None)
holeModel.YsymmBC(name='Bottom Edge Y_Symmetry3', createStepName='Initial', region=bottomface_region3, localCsys=None)
holeModel.YsymmBC(name='Bottom Edge Y_Symmetry4', createStepName='Initial', region=bottomface_region4, localCsys=None)
holeModel.YsymmBC(name='Bottom Edge Y_Symmetry5', createStepName='Initial', region=bottomface_region5, localCsys=None)

# Application of load

# A load of 160N has to be applied at vertex (12.0, 0.0, 0.0). So we should identify it using the findAt() method.
# ConcentratedForce() method is used to apply the force of 160N at this vertex. Note that, we have referred the
# the step that we created sometime back.

"""
faces1 = holeAssembly.instances['Plate Instance'].faces.getSequenceFromMask(mask=('[#3f ]',), )
edges1 = holeAssembly.instances['Plate Instance'].edges.getSequenceFromMask(mask=('[#7ffff ]',), )
verts1 = holeAssembly.instances['Plate Instance'].vertices.getSequenceFromMask(mask=('[#3fff ]',), )
faces2 = holeAssembly.instances['Hole Instance'].faces.getSequenceFromMask(mask=('[#7 ]',), )
edges2 = holeAssembly.instances['Hole Instance'].edges.getSequenceFromMask(mask=('[#1ff ]',), )
verts2 = holeAssembly.instances['Hole Instance'].vertices.getSequenceFromMask(mask=('[#7f ]',), )
region_full = regionToolset.Region(vertices=verts1 + verts2, edges=edges1 + edges2,
                              faces=faces1 + faces2)
holeModel.Temperature(name='Predefined Field-1',
                                  createStepName='Initial', region=region_full, distributionType=UNIFORM,
                                  crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, magnitudes=(20.0,))
"""

faces1 = holeAssembly.instances['Plate Instance'].faces.getSequenceFromMask(mask=('[#3f ]',), )
region_plate_temp = regionToolset.Region(faces=faces1)
holeModel.Temperature(name='Predefined Field-1',
                                  createStepName='Initial', region=region_plate_temp, distributionType=UNIFORM,
                                  crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, magnitudes=(20.0, ))

faces2 = holeAssembly.instances['Hole Instance'].faces.getSequenceFromMask(mask=('[#7 ]',), )
region_hole_temp = regionToolset.Region(faces=faces2)
holeModel.Temperature(name='Predefined Field-2',
                                  createStepName='Initial', region=region_hole_temp, distributionType=UNIFORM,
                                  crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, magnitudes=(20.0, ))

holeModel.predefinedFields['Predefined Field-2'].setValuesInStep(stepName='Step-1', magnitudes=(120.0,))

# Mesh creation

# Get access to the mesh objects by using the import statement. We will use the predefined regions for element
# type definition. C3D8R elements are used in this simulation

import mesh

point_in_quad = (0.001, 0.001, 0.0)
point_in_circle = (0.003, 0.006, 0.0)
point_in_circle2 = (0.006, 0.003, 0.0)
point_in_square = (0.005, 0.015, 0.0)
point_in_square2 = (0.015, 0.005, 0.0)
point_in_tri = (0.01, 0.0225, 0.0)
point_in_other1 = (0.015, 0.04, 0.0)
point_in_other2 = (0.05, 0.02, 0.0)
point_in_other3 = (0.05, 0.04, 0.0)

face_in_quad = holeModel.parts['Holepart2'].faces.findAt(((0.001, 0.001, 0.0),))
face_in_circle = holeModel.parts['Holepart2'].faces.findAt(((0.003, 0.006, 0.0),))
face_in_circle2 = holeModel.parts['Holepart2'].faces.findAt(((0.006, 0.003, 0.0),))
face_in_square = holeModel.parts['Holepart'].faces.findAt(((0.005, 0.015, 0.0),))
face_in_square2 = holeModel.parts['Holepart'].faces.findAt(((0.015, 0.005, 0.0),))
face_in_tri = holeModel.parts['Holepart'].faces.findAt(((0.1, 0.0225, 0.0),))
face_in_other1 = holeModel.parts['Holepart'].faces.findAt(((0.015, 0.04, 0.0),))
face_in_other2 = holeModel.parts['Holepart'].faces.findAt(((0.05, 0.02, 0.0),))
face_in_other3 = holeModel.parts['Holepart'].faces.findAt(((0.05, 0.04, 0.0),))

        #   element shapes

pickedRegionsQuad_hole = holeModel.parts['Holepart2'].faces.findAt((point_in_quad,), (point_in_circle,),
                                                                   (point_in_circle2,))
pickedRegionsQuad_plate = holeModel.parts['Holepart'].faces.findAt((point_in_square,), (point_in_square2,),
                                                           (point_in_other1,),(point_in_other2,),(point_in_other3,))
pickedRegionsTri = holeModel.parts['Holepart'].faces.findAt((point_in_tri,))

holeModel.parts['Holepart'].setMeshControls(regions=pickedRegionsQuad_plate, elemShape=QUAD, technique=STRUCTURED)
holeModel.parts['Holepart2'].setMeshControls(regions=pickedRegionsQuad_hole, elemShape=QUAD, technique=STRUCTURED)
holeModel.parts['Holepart'].setMeshControls(regions=pickedRegionsTri,  elemShape=TRI, technique=FREE)

        #   element types

elemType1 = mesh.ElemType(elemCode=CPS4I, elemLibrary=STANDARD)
elemType2 = mesh.ElemType(elemCode=CPS3, elemLibrary=STANDARD)

pickedRegions = ((pickedRegionsQuad_hole),)
holeModel.parts['Holepart2'].setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

pickedRegions = ((pickedRegionsQuad_plate),)
holeModel.parts['Holepart'].setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

pickedRegions = ((pickedRegionsTri),)
holeModel.parts['Holepart'].setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

edge_in_circle1 = holeModel.parts['Holepart2'].edges.findAt(((0.0, 0.006, 0.0),))
edge_in_circle2 = holeModel.parts['Holepart2'].edges.findAt(((0.006, 0.0, 0.0),))
edge_in_circle3 = holeModel.parts['Holepart2'].edges.findAt(((0.00001, 0.009999, 0.0),))
edge_in_circle4 = holeModel.parts['Holepart2'].edges.findAt(((0.009999, 0.00001, 0.0),))
edge_in_circle5 = holeModel.parts['Holepart'].edges.findAt(((0.00001, 0.009999, 0.0),))
edge_in_circle6 = holeModel.parts['Holepart'].edges.findAt(((0.009999, 0.00001, 0.0),))

edge_in_square1 = holeModel.parts['Holepart'].edges.findAt(((0.0, 0.015, 0.0),))
edge_in_square2 = holeModel.parts['Holepart'].edges.findAt(((0.015, 0.015, 0.0),))
edge_in_square3 = holeModel.parts['Holepart'].edges.findAt(((0.015, 0.0, 0.0),))

holeModel.parts['Holepart2'].seedEdgeByNumber(edges=edge_in_circle1, number=20, constraint=FINER)
holeModel.parts['Holepart2'].seedEdgeByNumber(edges=edge_in_circle2, number=20, constraint=FINER)
holeModel.parts['Holepart2'].seedEdgeByNumber(edges=edge_in_circle3, number=20, constraint=FINER)
holeModel.parts['Holepart2'].seedEdgeByNumber(edges=edge_in_circle4, number=20, constraint=FINER)
holeModel.parts['Holepart'].seedEdgeByNumber(edges=edge_in_circle5, number=20, constraint=FINER)
holeModel.parts['Holepart'].seedEdgeByNumber(edges=edge_in_circle6, number=20, constraint=FINER)

holeModel.parts['Holepart2'].seedEdgeByBias(biasMethod=SINGLE, end2Edges=edge_in_square1, ratio=5.0, number=20, constraint=FINER)
holeModel.parts['Holepart2'].seedEdgeByBias(biasMethod=SINGLE, end2Edges=edge_in_square2, ratio=5.0, number=20, constraint=FINER)
holeModel.parts['Holepart2'].seedEdgeByBias(biasMethod=SINGLE, end1Edges=edge_in_square3, ratio=5.0, number=20, constraint=FINER)

holeModel.parts['Holepart'].seedPart(size=0.002,  deviationFactor=0.1)
holeModel.parts['Holepart2'].seedPart(size=0.002,  deviationFactor=0.1)

holeModel.parts['Holepart'].generateMesh()
holeModel.parts['Holepart2'].generateMesh()

# Job creation
# Get access to the job objects by using the import statement. The job() method is used to create a job. Make sure
# that you enter the correct name of the model. Most of the arguments entered here are not mandatory. You can edit the
# values beased on your requirements.

from job import *

mdb.Job(name='PlateWithHoleJob', model='Model-1', type=ANALYSIS, explicitPrecision=SINGLE,
        nodalOutputPrecision=SINGLE, description='Job simulates the pressure loading of a plate with the hole',
        parallelizationMethodExplicit=DOMAIN, multiprocessingMode=DEFAULT, numDomains=1, userSubroutine='',
        numCpus=1, memory=50, memoryUnits=PERCENTAGE, scratch='', echoPrint=OFF, modelPrint=OFF, contactPrint=OFF,
        historyPrint=OFF)

# The submit() method is use for submitting the job for analysis. The waitForCompletion() makes ABAQUS wait till
# the job is fully executed.

mdb.jobs['PlateWithHoleJob'].submit(consistencyChecking=OFF)
mdb.jobs['PlateWithHoleJob'].waitForCompletion()
