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

holeSketch = holeModel.ConstrainedSketch(name='Plate Sketch', sheetSize=25.0)
holeSketch.Line(point1=(0.01, 0.0), point2=(0.12, 0.0))
holeSketch.Line(point1=(0.12, 0.0), point2=(0.12, 0.05))
holeSketch.Line(point1=(0.12, 0.05), point2=(0.0, 0.05))
holeSketch.Line(point1=(0.0, 0.05), point2=(0.0, 0.01))
holeSketch.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 0.01), point2=(0.01, 0.0), direction=CLOCKWISE)

# Using the sketch created above, create a part by extrusion using the BaseSolidExtrude() method.

holePart = holeModel.Part(name='Holepart', dimensionality=THREE_D, type=DEFORMABLE_BODY)
holePart.BaseSolidExtrude(sketch=holeSketch, depth=0.01)

# Material creation

# First get access to objects relating to materials by using the import statement. Define the name of the material,
# which would be used further in the script. The Density() and Elastic() objects are used to specify the density
# and elastic properties as the name suggests. The input arguments to Density() looks so as it is actually a table
# with respect to temperature. Here we don't need that. So we use blank spaces. The same logic applies to Elastic()
# where it is a table with Young's modulus values with respect to Poisson's ratio

from material import *

holeMaterial = holeModel.Material(name='Steel')
holeMaterial.Elastic(table=((1.9e11, 0.31),   ))
holeMaterial.Density(table=((7915, ),   ))
holeMaterial.SpecificHeat(table=((465, ),  ))
holeMaterial.Conductivity(table=((54, ),  ))
#holeMaterial.Expansion(table=((0.0000012, ),  ))

# Section creation and assignment

# Get access to the section objects by using the import statement. Then create a solid section by using the
# HomogenousSolidSection() method. You can see that we have refered to the material we created in the last step.

from section import *
holeSection = holeModel.HomogeneousSolidSection(name='Plate Section', material='Steel')
hole_region = (holePart.cells,)
holePart.SectionAssignment(region=hole_region, sectionName='Plate Section')

# Assembly creation

# Get access to the assembly objects by using the import statement. The rootAssembly is an assembly object which
# is a member of the Model object. Create an instance of the part by using the Instance() method. By default, the
# 'dependent' parameter is set to OFF. Set this to ON. We have already defined the part name as 'steadyPart'.
# We will refer to that now.

from assembly import *
holeAssembly = holeModel.rootAssembly
holeInstance = holeAssembly.Instance(name='Plate Instance', part=holePart, dependent=ON)

"""
f = holePart.faces
d = holePart.datums

holePart.DatumPlaneByOffset(plane=f[3], flip=SIDE2, offset=0.025)
holePart.DatumPlaneByOffset(plane=f[0], flip=SIDE2, offset=0.025)

pickedFaces = f.getSequenceFromMask(mask=('[#20 ]',), )
holePart.PartitionFaceByDatumPlane(datumPlane=d[4], faces=pickedFaces)

pickedFaces = f.getSequenceFromMask(mask=('[#41 ]',), )
holePart.PartitionFaceByDatumPlane(datumPlane=d[3], faces=pickedFaces)

f = holePart.faces
e = holePart.edges
d = holePart.datums
t = holePart.MakeSketchTransform(sketchPlane=f[1], sketchUpEdge=e[1],
                          sketchPlaneSide=SIDE1, origin=(0.0, 0.0, 0.0))
s = holeModel.ConstrainedSketch(name='__profile__', sheetSize=0.059, gridSpacing=0.001, transform=t)

    # square
s.Line(point1=(0.0, 0.02), point2=(0.02, 0.02))
s.Line(point1=(0.02, 0.02), point2=(0.02, 0.0))

    # inner contour
s.Line(point1=(0.0, 0.017), point2=(0.015, 0.015))
s.Line(point1=(0.015, 0.015), point2=(0.017, 0.0))

    # outer contour
s.Line(point1=(0.0, 0.013), point2=(0.01, 0.01))
s.Line(point1=(0.01, 0.01), point2=(0.013, 0.0))

pickedFaces = f.getSequenceFromMask(mask=('[#2 ]',), )

holePart.PartitionFaceBySketch(sketchUpEdge=e[1], faces=pickedFaces, sketch=s)
"""
holeAssembly.regenerate()
# Step creation

# Get access to the step objects by using the import statement. The StaticStep() method is used to create a
# static step which could be used for loading. This is the step next to 'Initial' step created by dafault. Enter the
# initial increment and maximum increment as shown below.

from step import *
holeModel.HeatTransferStep(name='Step-1', previous='Initial',
                                       timePeriod=15000.0, initialInc=1.0, minInc=0.15, maxInc=15000.0,
                                       deltmx=100.0)

# Field output and history output request left at default.

# Application of boudnary conditions -
# Fix Y for bottom edge and x for left edge -
# For doing this, we will first identify the point and use the findAT() method to find the top face and then redefine
# the face and then define the region.

point_on_bottom = (0.015, 0.0, 0.005)

bottomface = holeInstance.faces.findAt((point_on_bottom,))
bottomface_region = regionToolset.Region(faces=bottomface)

point_on_left1 = (0.0, 0.015, 0.005)

leftface = holeInstance.faces.findAt((point_on_left1,))
leftface_region = regionToolset.Region(faces=leftface)

# After the defintion of regions, we wil use the DisplacementBC() to define the constraints that replicate the symmetry
# condition.

holeModel.XsymmBC(name='X_Axis_Symmetry', createStepName='Initial', region=leftface_region, localCsys=None)
holeModel.ZsymmBC(name='Z_Axis_Symmetry', createStepName='Initial', region=bottomface_region, localCsys=None)

# Application of load
# Find the load face by a point and then apply the Pressure load

cells1 = holeInstance.cells.getSequenceFromMask(mask=('[#1 ]',), )
faces1 = holeInstance.faces.getSequenceFromMask(mask=('[#7f ]',), )
edges1 = holeInstance.edges.getSequenceFromMask(mask=('[#7fff ]',), )
verts1 = holeInstance.vertices.getSequenceFromMask(mask=('[#3ff  ]',), )
region1 = regionToolset.Region(vertices=verts1, edges=edges1, faces=faces1,
                              cells=cells1)
holeModel.Temperature(name='Predefined Field-1',
                                  createStepName='Initial', region=region1, distributionType=UNIFORM,
                                  crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, magnitudes=(20.0,))

side1Faces1 = holeInstance.faces.getSequenceFromMask(mask=('[#10 ]',), )
region = holeAssembly.Surface(side1Faces=side1Faces1, name='Surf-1')
holeModel.FilmCondition(name='Int-1', createStepName='Step-1',
                                    surface=region, definition=EMBEDDED_COEFF, filmCoeff=750.0,
                                    filmCoeffAmplitude='', sinkTemperature=0.0, sinkAmplitude='',
                                    sinkDistributionType=UNIFORM, sinkFieldName='')

faces2 = holeInstance.faces.getSequenceFromMask(mask=('[#10 ]',), )
region2 = regionToolset.Region(faces=faces2)
holeModel.TemperatureBC(name='BC-6', createStepName='Step-1',
                                    region=region2, fixed=OFF, distributionType=UNIFORM, fieldName='',
                                    magnitude=125.0, amplitude=UNSET)

# Mesh creation

# Get access to the mesh objects by using the import statement. We will use the predefined regions for element
# type definition. C3D8R elements are used in this simulation

import mesh

elemType_formesh = mesh.ElemType(elemCode=DC3D20, elemLibrary=STANDARD, kinematicSplit=AVERAGE_STRAIN,
                                      secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
interior_point = (0.03, 0.015, 0.005)
holeCells = holePart.cells
allCells = holeCells.findAt((interior_point))
partRegion = (allCells,)
holePart.setElementType(regions=partRegion, elemTypes=(elemType_formesh,))
pickedRegions = holePart.cells.getSequenceFromMask(mask=('[#1 ]', ), )
holePart.setMeshControls(regions=pickedRegions, elemShape=HEX, technique=STRUCTURED)

holePart.seedPart(size=0.001, deviationFactor=0.03)
holePart.generateMesh()

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

