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

bearingSketch = bearingModel.ConstrainedSketch(name='bearing Sketch', sheetSize=20.0)
bearingSketch.Line(point1=(0.0, 0.0), point2=(10.0, 0.0))
bearingSketch.Line(point1=(10.0, 0.0), point2=(10.0, 20.0))
bearingSketch.Line(point1=(10.0, 20.0), point2=(0.0, 20.0))
bearingSketch.Line(point1=(0.0, 20.0), point2=(0.0, 0.0))

# Using the sketch created above, create a part by extrusion using the BaseSolidExtrude() method.

bearingPart = bearingModel.Part(name='bearingPart', dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
bearingPart.BaseShell(sketch=bearingSketch)

from material import *

bearingMaterial = bearingModel.Material(name='Soil')
bearingMaterial.Elastic(table=((30E6, 0.3),   ))
bearingMaterial.Density(table=((2000, ),   ))
bearingMaterial.MohrCoulombPlasticity(table=((10, 1),  ))
bearingMaterial.mohrCoulombPlasticity.MohrCoulombHardening(table=((100.0, 0.0),))

# Section creation and assignment

# Get access to the section objects by using the import statement. Then create a solid section by using the
# HomogenousSolidSection() method. You can see that we have refered to the material we created in the last step.

from section import *

bearingSection = bearingModel.HomogeneousSolidSection(name='Soil layer', material='Soil', thickness=0.1)
point_on_soil = (5, 10.0, 0.0)
face_on_soil = bearingPart.faces.findAt((point_on_soil,))
soil_region = (face_on_soil,)
bearingPart.SectionAssignment(region=soil_region, sectionName='Soil layer')

# Assembly creation

# Get access to the assembly objects by using the import statement. The rootAssembly is an assembly object which
# is a member of the Model object. Create an instance of the part by using the Instance() method. By default, the
# 'dependent' parameter is set to OFF. Set this to ON. We have already defined the part name as 'steadyPart'.
# We will refer to that now.

from assembly import *

bearingAssembly = bearingModel.rootAssembly
bearingInstance = bearingAssembly.Instance(name='Bearing Instance', part=bearingPart, dependent=ON)

# Partitions

sketchTransform = bearingPart.MakeSketchTransform(sketchPlane=face_on_soil[0], sketchPlaneSide=SIDE1,
                                                         origin=(0.0, 0.0, 0.0))
bearingSketch.Line(point1=(0.0, 19.8), point2=(2.0, 19.8))
bearingSketch.Line(point1=(1.0, 20.0), point2=(1.0, 0.0))
bearingSketch.Line(point1=(2.0, 20.0), point2=(2.0, 0.0))
bearingSketch.Line(point1=(6.0, 20.0), point2=(6.0, 0.0))
bearingSketch.Line(point1=(0.8, 0.0), point2=(0.8, 20.0))
bearingSketch.Line(point1=(1.2, 0.0), point2=(1.2, 20.0))

bearingPart.PartitionFaceBySketch(faces=face_on_soil, sketch=bearingSketch)
bearingAssembly.regenerate()

# Step creation

# Get access to the step objects by using the import statement. The StaticStep() method is used to create a
# static step which could be used for loading. This is the step next to 'Initial' step created by dafault. Enter the
# initial increment and maximum increment as shown below.

from step import *

bearingModel.StaticStep(name='Load Step', previous='Initial', description='Loads is applied now')

# Field output: (only the S22 value is required).

# bearingModel.fieldOutputRequests['F-Output-1'].setValues(variables=('S',))

# History output request left at default.

# Application of boundary conditions -

# Vertical allowance of movement (roller) on left edge

# For doing this, we will first identify the point and use the findAT() method to find the left face and then redefine
# the face and then define the region.

edge_on_leftface = bearingInstance.edges.findAt(((0.0, 10.0, 0.0),))
leftface_region = regionToolset.Region(edges=edge_on_leftface)
edge_on_leftface2 = bearingInstance.edges.findAt(((0.0, 19.9, 0.0),))
leftface_region2 = regionToolset.Region(edges=edge_on_leftface2)

edge_on_rightface = bearingInstance.edges.findAt(((10.0, 10.0, 0.0),))
rightface_region = regionToolset.Region(edges=edge_on_rightface)

edge_on_bottomface1 = bearingInstance.edges.findAt(((0.5, 0.0, 0.0),))
bottomface_region1 = regionToolset.Region(edges=edge_on_bottomface1)
edge_on_bottomface2 = bearingInstance.edges.findAt(((1.5, 0.0, 0.0),))
bottomface_region2 = regionToolset.Region(edges=edge_on_bottomface2)
edge_on_bottomface3 = bearingInstance.edges.findAt(((4.0, 0.0, 0.0),))
bottomface_region3 = regionToolset.Region(edges=edge_on_bottomface3)
edge_on_bottomface4 = bearingInstance.edges.findAt(((8.0, 0.0, 0.0),))
bottomface_region4 = regionToolset.Region(edges=edge_on_bottomface4)
edge_on_bottomface5 = bearingInstance.edges.findAt(((0.9, 0.0, 0.0),))
bottomface_region5 = regionToolset.Region(edges=edge_on_bottomface5)
edge_on_bottomface6 = bearingInstance.edges.findAt(((1.1, 0.0, 0.0),))
bottomface_region6 = regionToolset.Region(edges=edge_on_bottomface6)


# After the defintion of regions, we wil use the DisplacementBC() to define the constraints that replicate the symmetry
# condition.

bearingModel.XsymmBC(name='Left Edge X_Symmetry1', createStepName='Initial', region=leftface_region, localCsys=None)
bearingModel.XsymmBC(name='Left Edge X_Symmetry2', createStepName='Initial', region=leftface_region2, localCsys=None)


bearingModel.DisplacementBC(name='Right Edge Free Vertical1', createStepName='Initial', region=rightface_region,
                     u1=SET, u2=SET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='',
                              localCsys=None)

bearingModel.DisplacementBC(name='Bottom Edge Pin1', createStepName='Initial', region=bottomface_region1,
                     u1=SET, u2=SET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
bearingModel.DisplacementBC(name='Bottom Edge Pin2', createStepName='Initial', region=bottomface_region2,
                     u1=SET, u2=SET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
bearingModel.DisplacementBC(name='Bottom Edge Pin3', createStepName='Initial', region=bottomface_region3,
                     u1=SET, u2=SET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
bearingModel.DisplacementBC(name='Bottom Edge Pin4', createStepName='Initial', region=bottomface_region4,
                     u1=SET, u2=SET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
bearingModel.DisplacementBC(name='Bottom Edge Pin5', createStepName='Initial', region=bottomface_region5,
                     u1=SET, u2=SET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
bearingModel.DisplacementBC(name='Bottom Edge Pin6', createStepName='Initial', region=bottomface_region6,
                     u1=SET, u2=SET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)


# Application of load

# A load of 1000N has to be applied at vertex (0.0, 20.0, 0.0). So we should identify it using the findAt() method.
# ConcentratedForce() method is used to apply the force of 1000N at this vertex. Note that, we have referred the
# the step that we created sometime back.

edge_on_bearingface1 = bearingInstance.edges.findAt(((0.5, 20.0, 0.0),))
edge_on_bearingface2 = bearingInstance.edges.findAt(((0.9, 20.0, 0.0),))

bearingface_region1 = regionToolset.Region(edges=edge_on_bearingface1)
bearingface_region2 = regionToolset.Region(edges=edge_on_bearingface2)

bearingModel.DisplacementBC(name='Bearing analytical settlement1', createStepName='Load Step', region=bearingface_region1,
                     u1=UNSET, u2=-0.001, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='',
                        localCsys=None)

bearingModel.DisplacementBC(name='Bearing analytical settlement2', createStepName='Load Step', region=bearingface_region2,
                     u1=UNSET, u2=-0.001, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='',
                        localCsys=None)

# Mesh creation

# Get access to the mesh objects by using the import statement. We will use the predefined regions for element
# type definition. C3D8R elements are used in this simulation

import mesh

        #Bodies within the soil

point_on_soil_Left = (0.5, 5.0, 0.0)
point_on_soil_under1 = (0.9, 5.0, 0.0)
point_on_soil_under2 = (1.1, 5.0, 0.0)
point_on_soil_mid = (1.5, 5.0, 0.0)
point_on_soil_mid2 = (4.0, 5.0, 0.0)
point_on_soil_Right = (7.0, 5.0, 0.0)

point_on_top1 = (0.5, 19.9, 0.0)
point_on_top2 = (1.5, 19.9, 0.0)

point_in_square1 = (0.9, 19.9, 0.0)
point_in_square2 = (1.1, 19.9, 0.0)

        # Assinging body to a face

face_on_soil_Left = bearingPart.faces.findAt((point_on_soil_Left,))
face_on_soil_under1 = bearingPart.faces.findAt((point_on_soil_under1,))
face_on_soil_under2 = bearingPart.faces.findAt((point_on_soil_under2,))
face_on_soil_mid = bearingPart.faces.findAt((point_on_soil_mid,))
face_on_soil_mid2 = bearingPart.faces.findAt((point_on_soil_mid2,))
face_on_soil_Right = bearingPart.faces.findAt((point_on_soil_Right,))

face_on_top1 = bearingPart.faces.findAt((point_on_top1,))
face_on_top2 = bearingPart.faces.findAt((point_on_top2,))

face_on_square1 = bearingPart.faces.findAt((point_in_square1,))
face_on_square2 = bearingPart.faces.findAt((point_in_square2,))

        # Assigning the element type to the faces in the soil

soil_region = (face_on_soil_Left, face_on_soil_mid, face_on_soil_mid2, face_on_soil_Right, face_on_top1,
               face_on_top2, face_on_square1, face_on_square2, face_on_soil_under1, face_on_soil_under2)
mesh_region = soil_region
mesh_elem_type = mesh.ElemType(elemCode=CPE4, elemLibrary=STANDARD)
bearingPart.setElementType(regions=mesh_region, elemTypes=(mesh_elem_type, ))

        # Element shapes

pickedRegionsQuad = bearingPart.faces.findAt((point_on_soil_Left,), (point_on_soil_under1,), (point_on_soil_under2,),
                                             (point_on_soil_mid,), (point_on_soil_Right,), (point_on_top1,),
                                             (point_on_top2,))
bearingPart.setMeshControls(regions=pickedRegionsQuad, elemShape=QUAD, technique=STRUCTURED)

pickedRegionsTri = bearingPart.faces.findAt((point_in_square1,), (point_in_square2,), (point_on_soil_mid2,))
bearingPart.setMeshControls(regions=pickedRegionsTri, elemShape=TRI, technique=FREE)

        # Seeding the edges

edge_on_left = bearingInstance.edges.findAt(((0.0, 10.0, 0.0),))

edge_under1 = bearingInstance.edges.findAt(((0.8, 10.0, 0.0),))
edge_under2 = bearingInstance.edges.findAt(((1.0, 10.0, 0.0),))
edge_under3 = bearingInstance.edges.findAt(((1.2, 10.0, 0.0),))

edge_on_middle1 = bearingInstance.edges.findAt(((2.0, 10.0, 0.0),))
edge_on_middle2 = bearingInstance.edges.findAt(((6.0, 10.0, 0.0),))

edge_on_top1 = bearingInstance.edges.findAt(((0.5, 20.0, 0.0),))
edge_on_top2 = bearingInstance.edges.findAt(((1.5, 20.0, 0.0),))
edge_on_top3 = bearingInstance.edges.findAt(((0.9, 20.0, 0.0),))
edge_on_top4 = bearingInstance.edges.findAt(((1.1, 20.0, 0.0),))
edge_on_top5 = bearingInstance.edges.findAt(((4.0, 20.0, 0.0),))

edge_in_square = bearingInstance.edges.findAt(((1.0, 19.9, 0.0),))

bearingPart.seedEdgeByNumber(edges=edge_on_left, number=250, constraint=FINER)

bearingPart.seedEdgeByNumber(edges=edge_on_top1, number=50, constraint=FINER)
bearingPart.seedEdgeByNumber(edges=edge_on_top2, number=50, constraint=FINER)
bearingPart.seedEdgeByNumber(edges=edge_on_top5, number=20, constraint=FINER)

bearingPart.seedEdgeByBias(biasMethod=SINGLE, end1Edges=edge_in_square, ratio=20.0,
                      number=60, constraint=FINER)
bearingPart.seedEdgeByBias(biasMethod=SINGLE, end1Edges=edge_on_top3, ratio=20.0,
                      number=60, constraint=FINER)
bearingPart.seedEdgeByBias(biasMethod=SINGLE, end2Edges=edge_on_top4, ratio=20.0,
                      number=60, constraint=FINER)

bearingPart.seedPart(size=2, deviationFactor=0.03)
bearingPart.generateMesh()


# Job creation
# Get access to the job objects by using the import statement. The job() method is used to create a job. Make sure
# that you enter the correct name of the model. Most of the arguments entered here are not mandatory. You can edit the
# values beased on your requirements.

from job import *

mdb.Job(name='bearingJob2D', model='Model-1', type=ANALYSIS, explicitPrecision=SINGLE,
        nodalOutputPrecision=SINGLE, description='Job simulates the pressure loading of a bearing',
        parallelizationMethodExplicit=DOMAIN, multiprocessingMode=DEFAULT, numDomains=1, userSubroutine='',
        numCpus=1, memory=50, memoryUnits=PERCENTAGE, scratch='', echoPrint=OFF, modelPrint=OFF, contactPrint=OFF,
        historyPrint=OFF)

mdb.jobs['bearingJob2D'].submit(consistencyChecking=OFF)
mdb.jobs['bearingJob2D'].waitForCompletion()
