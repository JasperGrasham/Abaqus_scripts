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

bearingModel = mdb.models['Model-1']

# Part creation

# These two statements will provide access to all the objects related to sketch and part. Including this is not
# mandatory, but it is good practice.

from sketch import *
from part import *

# In this set of set of statements, we would define a sketch by using the ConstrainedSketch() method. This method in
# turn has Line() method which can be used to draw the lines that we want in the sketch. Enter a value for
# 'sheetSize' based on your overall problem size.

bearingSketch = bearingModel.ConstrainedSketch(name='Plate Sketch', sheetSize=25.0)
bearingSketch.Line(point1=(0.0, 0.0), point2=(10.0, 0.0))
bearingSketch.Line(point1=(10.0, 0.0), point2=(10.0, 20.0))
bearingSketch.Line(point1=(10.0, 20.0), point2=(0.0, 20.0))
bearingSketch.Line(point1=(0.0, 20.0), point2=(0.0, 0.0))

# Using the sketch created above, create a part by extrusion using the BaseSolidExtrude() method.

bearingPart = bearingModel.Part(name='Bearingpart', dimensionality=THREE_D, type=DEFORMABLE_BODY)
bearingPart.BaseSolidExtrude(sketch=bearingSketch, depth=10.0)

from material import *

bearingMaterial = bearingModel.Material(name='Soil')
bearingMaterial.Density(table=((2000, ),   ))
bearingMaterial.Elastic(table=((30E6, 0.3),   ))
#bearingMaterial.MohrCoulombPlasticity(table=((10, 1),  ))
#bearingMaterial.mohrCoulombPlasticity.MohrCoulombHardening(table=((100.0, 0.0),))

# Section creation and assignment

# Get access to the section objects by using the import statement. Then create a solid section by using the
# HomogenousSolidSection() method. You can see that we have refered to the material we created in the last step.

from section import *

bearingSection = bearingModel.HomogeneousSolidSection(name='Soil Section', material='Soil')
bearing_region = (bearingPart.cells,)
bearingPart.SectionAssignment(region=bearing_region, sectionName='Soil Section')

# Assembly creation

# Get access to the assembly objects by using the import statement. The rootAssembly is an assembly object which
# is a member of the Model object. Create an instance of the part by using the Instance() method. By default, the
# 'dependent' parameter is set to OFF. Set this to ON. We have already defined the part name as 'steadyPart'.
# We will refer to that now.

from assembly import *

bearingAssembly = bearingModel.rootAssembly
bearingInstance = bearingAssembly.Instance(name='Bearing Instance', part=bearingPart, dependent=ON)

f = bearingPart.faces
bearingPart.DatumPlaneByOffset(plane=f[5], flip=SIDE2, offset=1.0)
bearingPart.DatumPlaneByOffset(plane=f[3], flip=SIDE2, offset=1.0)

pickedFaces = f.getSequenceFromMask(mask=('[#1 ]',), )
d = bearingPart.datums
bearingPart.PartitionFaceByDatumPlane(datumPlane=d[3], faces=pickedFaces)
bearingPart.PartitionFaceByDatumPlane(datumPlane=d[4], faces=pickedFaces)

pickedFaces = f.getSequenceFromMask(mask=('[#4 ]',), )
d = bearingPart.datums
bearingPart.PartitionFaceByDatumPlane(datumPlane=d[4], faces=pickedFaces)

pickedFaces = f.getSequenceFromMask(mask=('[#80 ]',), )
d = bearingPart.datums
bearingPart.PartitionFaceByDatumPlane(datumPlane=d[4], faces=pickedFaces)

pickedFaces = f.getSequenceFromMask(mask=('[#40 ]',), )
d = bearingPart.datums
bearingPart.PartitionFaceByDatumPlane(datumPlane=d[4], faces=pickedFaces)

pickedFaces = f.getSequenceFromMask(mask=('[#400 ]',), )
d = bearingPart.datums
bearingPart.PartitionFaceByDatumPlane(datumPlane=d[4], faces=pickedFaces)

pickedFaces = f.getSequenceFromMask(mask=('[#200 ]',), )
d = bearingPart.datums
bearingPart.PartitionFaceByDatumPlane(datumPlane=d[3], faces=pickedFaces)

pickedFaces = f.getSequenceFromMask(mask=('[#100 ]',), )
d = bearingPart.datums
bearingPart.PartitionFaceByDatumPlane(datumPlane=d[3], faces=pickedFaces)

pickedFaces = f.getSequenceFromMask(mask=('[#400 ]',), )
d = bearingPart.datums
bearingPart.PartitionFaceByDatumPlane(datumPlane=d[3], faces=pickedFaces)

pickedFaces = f.getSequenceFromMask(mask=('[#10 ]',), )
d = bearingPart.datums
bearingPart.PartitionFaceByDatumPlane(datumPlane=d[3], faces=pickedFaces)

bearingAssembly.regenerate()

# Step creation

# Get access to the step objects by using the import statement. The StaticStep() method is used to create a
# static step which could be used for loading. This is the step next to 'Initial' step created by dafault. Enter the
# initial increment and maximum increment as shown below.

from step import *

bearingModel.StaticStep(name='Load Step', previous='Initial', description='Loads is applied now')

# Field output and history output request left at default.

# Application of boundary conditions -

# Vertical allowance of movement (roller) on left edge

# For doing this, we will first identify the point and use the findAT() method to find the left face and then redefine
# the face and then define the region.

X_SYM_plane_point1 = (0.0, 10.0, 0.5)
X_SYM_plane_point2 = (0.0, 10.0, 5.0)
X_SYM_plane_face1 = bearingInstance.faces.findAt((X_SYM_plane_point1,))
X_SYM_plane_face2 = bearingInstance.faces.findAt((X_SYM_plane_point2,))
X_SYM_plane_face_region1 = regionToolset.Region(faces=X_SYM_plane_face1)
X_SYM_plane_face_region2 = regionToolset.Region(faces=X_SYM_plane_face2)

bearingModel.XsymmBC(name='X_Axis_Symmetry1', createStepName='Initial', region=X_SYM_plane_face_region1,
                     localCsys=None)
bearingModel.XsymmBC(name='X_Axis_Symmetry2', createStepName='Initial', region=X_SYM_plane_face_region2,
                     localCsys=None)

Z_SYM_plane_point1 = (0.5, 10.0, 0.0)
Z_SYM_plane_point2 = (5.0, 10.0, 0.0)
Z_SYM_plane_face1 = bearingInstance.faces.findAt((Z_SYM_plane_point1,))
Z_SYM_plane_face2 = bearingInstance.faces.findAt((Z_SYM_plane_point2,))
Z_SYM_plane_face_region1 = regionToolset.Region(faces=Z_SYM_plane_face1)
Z_SYM_plane_face_region2 = regionToolset.Region(faces=Z_SYM_plane_face2)

bearingModel.ZsymmBC(name='Z_Axis_Symmetry1', createStepName='Initial', region=Z_SYM_plane_face_region1,
                     localCsys=None)
bearingModel.ZsymmBC(name='Z_Axis_Symmetry2', createStepName='Initial', region=Z_SYM_plane_face_region2,
                     localCsys=None)

bottom_face_point1 = (0.5, 0.0, 0.5)
bottom_face_point2 = (0.5, 0.0, 5.0)
bottom_face_point3 = (5.0, 0.0, 0.5)
bottom_face_point4 = (5.0, 0.0, 5.0)

bottom_face1 = bearingInstance.faces.findAt((bottom_face_point1,))
bottom_face2 = bearingInstance.faces.findAt((bottom_face_point2,))
bottom_face3 = bearingInstance.faces.findAt((bottom_face_point3,))
bottom_face4 = bearingInstance.faces.findAt((bottom_face_point4,))

bottom_face_region1 = regionToolset.Region(faces=bottom_face1)
bottom_face_region2 = regionToolset.Region(faces=bottom_face2)
bottom_face_region3 = regionToolset.Region(faces=bottom_face3)
bottom_face_region4 = regionToolset.Region(faces=bottom_face4)

bearingModel.DisplacementBC(name='Bottom Edge pin1', createStepName='Initial', region=bottom_face_region1, u1=SET,
                            u2=SET, u3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
bearingModel.DisplacementBC(name='Bottom Edge pin2', createStepName='Initial', region=bottom_face_region2, u1=SET,
                            u2=SET, u3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
bearingModel.DisplacementBC(name='Bottom Edge pin3', createStepName='Initial', region=bottom_face_region3, u1=SET,
                            u2=SET, u3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
bearingModel.DisplacementBC(name='Bottom Edge pin4', createStepName='Initial', region=bottom_face_region4, u1=SET,
                            u2=SET, u3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

right_edge_point = (10.0, 5.0, 5.0)

right_face = bearingInstance.faces.findAt((right_edge_point,))

right_face_region = regionToolset.Region(faces=right_face)

bearingModel.DisplacementBC(name='Right edge pin', createStepName='Initial', region=right_face_region, u1=UNSET,
                            u2=SET, u3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

outside_near_point = (5.0, 5.0, 10.0)

outside_near_face = bearingInstance.faces.findAt((outside_near_point,))

outside_near_face_region = regionToolset.Region(faces=outside_near_face)

bearingModel.DisplacementBC(name='Outside near edge pin', createStepName='Initial', region=outside_near_face_region, u1=UNSET,
                            u2=SET, u3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

# Application of load

# A load of 1000N has to be applied at vertex (0.0, 20.0, 0.0). So we should identify it using the findAt() method.
# ConcentratedForce() method is used to apply the force of 1000N at this vertex. Note that, we have referred the
# the step that we created sometime back.

faces1 = bearingAssembly.instances['Bearing Instance'].faces.getSequenceFromMask(mask=('[#100 ]',), )
region = regionToolset.Region(faces=faces1)
mdb.models['Model-1'].DisplacementBC(name='BC-13', createStepName='Load Step',
                                     region=region, u1=UNSET, u2=-0.0024873333333333336, u3=UNSET, ur1=UNSET, ur2=UNSET,
                                     ur3=UNSET, amplitude=UNSET, fixed=OFF, distributionType=UNIFORM,
                                     fieldName='', localCsys=None)

# Mesh creation

# Get access to the mesh objects by using the import statement. We will use the predefined regions for element
# type definition. C3D8R elements are used in this simulation

import mesh

elemType_formesh = mesh.ElemType(elemCode=C3D20R, elemLibrary=STANDARD, kinematicSplit=AVERAGE_STRAIN,
                                      secondOrderAccuracy=OFF, hourglassControl=DEFAULT, distortionControl=DEFAULT)
interior_point = (5.0, 5.0, 5.0)
bearingCells = bearingPart.cells
allCells = bearingCells.findAt((interior_point))
partRegion = (allCells,)
bearingPart.setElementType(regions=partRegion, elemTypes=(elemType_formesh,))

bearingPart.seedPart(size=0.5, deviationFactor=0.01)

bearingPart.generateMesh()

# Job creation
# Get access to the job objects by using the import statement. The job() method is used to create a job. Make sure
# that you enter the correct name of the model. Most of the arguments entered here are not mandatory. You can edit the
# values beased on your requirements.

from job import *

mdb.Job(name='bearingJob3D', model='Model-1', type=ANALYSIS, explicitPrecision=SINGLE,
        nodalOutputPrecision=SINGLE, description='Job simulates the pressure loading of a bearing',
        parallelizationMethodExplicit=DOMAIN, multiprocessingMode=DEFAULT, numDomains=1, userSubroutine='',
        numCpus=1, memory=50, memoryUnits=PERCENTAGE, scratch='', echoPrint=OFF, modelPrint=OFF, contactPrint=OFF,
        historyPrint=OFF)

# The submit() method is use for submitting the job for analysis. The waitForCompletion() makes ABAQUS wait till
# the job is fully executed.

# mdb.jobs['bearingJob3D'].submit(consistencyChecking=OFF)
# mdb.jobs['bearingJob3D'].waitForCompletion()

