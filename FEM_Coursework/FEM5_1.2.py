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
holeSketch.Line(point1=(0.0, -0.01), point2=(0.0, -0.05))
holeSketch.Line(point1=(0.0, -0.05), point2=(0.12, -0.05))
holeSketch.Line(point1=(0.12, -0.05), point2=(0.12, -0.035))
holeSketch.Line(point1=(0.12, -0.035), point2=(0.12, 0.0))
holeSketch.Line(point1=(0.12, 0.0), point2=(0.12, 0.035))
holeSketch.Line(point1=(0.12, 0.035), point2=(0.12, 0.05))
holeSketch.Line(point1=(0.12, 0.05), point2=(0.0, 0.05))
holeSketch.Line(point1=(0.0, 0.05), point2=(0.0, 0.01))
holeSketch.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, 0.01), point2=(0.0, -0.01), direction=CLOCKWISE)

# Using the sketch created above, create a part by extrusion using the BaseSolidExtrude() method.

holePart = holeModel.Part(name='holePart', dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
holePart.BaseShell(sketch=holeSketch)
ReferencePoint1 = holePart.ReferencePoint(point=(0.12, 0.0, 0.0))

# Material creation

# First get access to objects relating to materials by using the import statement. Define the name of the material,
# which would be used further in the script. The Density() and Elastic() objects are used to specify the density
# and elastic properties as the name suggests. The input arguments to Density() looks so as it is actually a table
# with respect to temperature. Here we don't need that. So we use blank spaces. The same logic applies to Elastic()
# where it is a table with Young's modulus values with respect to Poisson's ratio

from material import *

holeMaterial = holeModel.Material(name='Steel')
holeMaterial.Elastic(table=((1.9e11, 0.31),   ))

# Section creation and assignment

# Get access to the section objects by using the import statement. Then create a solid section by using the
# HomogenousSolidSection() method. You can see that we have refered to the material we created in the last step.

from section import *

holeSection = holeModel.HomogeneousSolidSection(name='Plate Section', material='Steel', thickness=0.01)
point_on_plate = (0.06, 0.0, 0.0)
face_on_plate = holePart.faces.findAt((point_on_plate,))
plate_region = (face_on_plate,)
holePart.SectionAssignment(region=plate_region, sectionName='Plate Section')

# Assembly creation

# Get access to the assembly objects by using the import statement. The rootAssembly is an assembly object which
# is a member of the Model object. Create an instance of the part by using the Instance() method. By default, the
# 'dependent' parameter is set to OFF. Set this to ON. We have already defined the part name as 'steadyPart'.
# We will refer to that now.

from assembly import *
holeAssembly = holeModel.rootAssembly
holeInstance = holeAssembly.Instance(name='Plate Instance', part=holePart, dependent=ON)

# Partitions

sketchTransform = holePart.MakeSketchTransform(sketchPlane=face_on_plate[0], sketchPlaneSide=SIDE1,
                                                         origin=(0.0, 0.0, 0.0))
    # square around circle

holeSketch.Line(point1=(0.0, 0.02), point2=(0.02, 0.02))
holeSketch.Line(point1=(0.02, 0.02), point2=(0.02, -0.02))
holeSketch.Line(point1=(0.02, -0.02), point2=(0.0, -0.02))
holeSketch.Line(point1=(0.004, 0.004), point2=(0.02, 0.02))
holeSketch.Line(point1=(0.004, -0.004), point2=(0.02, -0.02))
    # other

holeSketch.Line(point1=(0.0, 0.025), point2=(0.12, 0.025))
holeSketch.Line(point1=(0.0, -0.025), point2=(0.12, -0.025))
holeSketch.Line(point1=(0.025, -0.05), point2=(0.025, 0.5))

holePart.PartitionFaceBySketch(faces=face_on_plate, sketch=holeSketch)
holeAssembly.regenerate()

# Step creation

# Get access to the step objects by using the import statement. The StaticStep() method is used to create a
# static step which could be used for loading. This is the step next to 'Initial' step created by dafault. Enter the
# initial increment and maximum increment as shown below.

from step import *
holeModel.StaticStep(name='Load Step', previous='Initial', description='Loads is applied now')

# Field output and history output request left at default.

# Application of boundary conditions -

# Vertical allowance of movement (roller) on left edge

# For doing this, we will first identify the point and use the findAT() method to find the left face and then redefine
# the face and then define the region.

edge_on_leftface1 = holeInstance.edges.findAt(((0.0, 0.04, 0.0),))
edge_on_leftface2 = holeInstance.edges.findAt(((0.0, 0.021, 0.0),))
edge_on_leftface3 = holeInstance.edges.findAt(((0.0, 0.015, 0.0),))
edge_on_leftface4 = holeInstance.edges.findAt(((0.0, -0.04, 0.0),))
edge_on_leftface5 = holeInstance.edges.findAt(((0.0, -0.021, 0.0),))
edge_on_leftface6 = holeInstance.edges.findAt(((0.0, -0.015, 0.0),))
leftface_region1 = regionToolset.Region(edges=edge_on_leftface1)
leftface_region2 = regionToolset.Region(edges=edge_on_leftface2)
leftface_region3 = regionToolset.Region(edges=edge_on_leftface3)
leftface_region4 = regionToolset.Region(edges=edge_on_leftface4)
leftface_region5 = regionToolset.Region(edges=edge_on_leftface5)
leftface_region6 = regionToolset.Region(edges=edge_on_leftface6)

# After the defintion of regions, we wil use the DisplacementBC() to define the constraints that replicate the symmetry
# condition.

holeModel.XsymmBC(name='Left Edge X_Symmetry1', createStepName='Initial', region=leftface_region1, localCsys=None)
holeModel.XsymmBC(name='Left Edge X_Symmetry2', createStepName='Initial', region=leftface_region2, localCsys=None)
holeModel.XsymmBC(name='Left Edge X_Symmetry3', createStepName='Initial', region=leftface_region3, localCsys=None)
holeModel.XsymmBC(name='Left Edge X_Symmetry4', createStepName='Initial', region=leftface_region4, localCsys=None)
holeModel.XsymmBC(name='Left Edge X_Symmetry5', createStepName='Initial', region=leftface_region5, localCsys=None)
holeModel.XsymmBC(name='Left Edge X_Symmetry6', createStepName='Initial', region=leftface_region6, localCsys=None)

# Application of moment load

from interaction import *

side1Edges1 = holeAssembly.instances['Plate Instance'].edges.getSequenceFromMask(mask=('[#3c030000 ]',), )

r1 = holeAssembly.instances['Plate Instance'].referencePoints
refPoints1 = (r1[2],)

region = regionToolset.Region(referencePoints=refPoints1)
region2 = regionToolset.Region(side1Edges=side1Edges1)

holeModel.Coupling(name='Constraint-1', controlPoint=region,
                               surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC,
                               localCsys=None, u1=ON, u2=OFF, ur3=ON)

holeModel.Moment(name='Load-1', createStepName='Load Step',
                             region=region, cm3=5200000.0, distributionType=UNIFORM, field='',
                             localCsys=None)

# Mesh creation

# Get access to the mesh objects by using the import statement. We will use the predefined regions for element
# type definition. C3D8R elements are used in this simulation

import mesh

point_in_square = (0.005, 0.015, 0.0)
point_in_square2 = (0.015, 0.005, 0.0)
point_in_square3 = (0.005, -0.015, 0.0)
point_in_tri = (0.0, 0.0225, 0.0)
point_in_other1 = (0.015, 0.04, 0.0)
point_in_other2 = (0.015, -0.04, 0.0)
point_in_other3 = (0.05, 0.02, 0.0)
point_in_other4 = (0.05, 0.04, 0.0)
point_in_other5 = (0.05, -0.04, 0.0)

face_in_square = holePart.faces.findAt((point_in_square,))
face_in_square2 = holePart.faces.findAt((point_in_square2,))
face_in_square3 = holePart.faces.findAt((point_in_square3,))
face_in_tri = holePart.faces.findAt((point_in_tri,))
face_in_other1 = holePart.faces.findAt((point_in_other1,))
face_in_other2 = holePart.faces.findAt((point_in_other2,))
face_in_other3 = holePart.faces.findAt((point_in_other3,))
face_in_other4 = holePart.faces.findAt((point_in_other4,))
face_in_other5 = holePart.faces.findAt((point_in_other5,))

plate_region = (face_in_square, face_in_square2, face_in_square3, face_in_tri, face_in_other1, face_in_other2,
                face_in_other3, face_in_other4, face_in_other5)
mesh_region = plate_region
mesh_elem_type = mesh.ElemType(elemCode=CPS4, elemLibrary=STANDARD)
holePart.setElementType(regions=mesh_region, elemTypes=(mesh_elem_type, ))
pickedRegionsQuad = holePart.faces.findAt((point_in_square,), (point_in_square2,), (point_in_square3,),
                                          (point_in_other1,), (point_in_other2,), (point_in_other3,),
                                          (point_in_other4,), (point_in_other5,))
holePart.setMeshControls(regions=pickedRegionsQuad, elemShape=QUAD, technique=STRUCTURED)

pickedRegionsTri = holePart.faces.findAt((point_in_tri,))
holePart.setMeshControls(regions=pickedRegionsTri, elemShape=TRI, technique=FREE)

edge_in_circle1 = holeInstance.edges.findAt(((0.00001, 0.009999, 0.0),))
edge_in_circle2 = holeInstance.edges.findAt(((0.009999, 0.00001, 0.0),))
edge_in_circle3 = holeInstance.edges.findAt(((0.00001, -0.009999, 0.0),))

edge_in_square1 = holeInstance.edges.findAt(((0.0, 0.015, 0.0),))
edge_in_square2 = holeInstance.edges.findAt(((0.015, 0.015, 0.0),))
edge_in_square3 = holeInstance.edges.findAt(((0.015, -0.015, 0.0),))
edge_in_square4 = holeInstance.edges.findAt(((0.0, -0.015, 0.0),))

holePart.seedEdgeByNumber(edges=edge_in_circle1, number=40, constraint=FINER)
holePart.seedEdgeByNumber(edges=edge_in_circle2, number=80, constraint=FINER)
holePart.seedEdgeByNumber(edges=edge_in_circle3, number=40, constraint=FINER)

holePart.seedEdgeByBias(biasMethod=SINGLE, end2Edges=edge_in_square1, ratio=5.0, number=40, constraint=FINER)
holePart.seedEdgeByBias(biasMethod=SINGLE, end1Edges=edge_in_square2, ratio=5.0, number=40, constraint=FINER)
holePart.seedEdgeByBias(biasMethod=SINGLE, end2Edges=edge_in_square3, ratio=5.0, number=40, constraint=FINER)
holePart.seedEdgeByBias(biasMethod=SINGLE, end1Edges=edge_in_square4, ratio=5.0, number=40, constraint=FINER)

holePart.seedPart(size=0.0015,  deviationFactor=0.1)
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
