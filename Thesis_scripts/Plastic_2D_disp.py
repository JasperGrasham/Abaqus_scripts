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
bearingMaterial.Density(table=((2000, ),   ))
bearingMaterial.Elastic(table=((30E6, 0.3),   ))
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

    #   line

bearingSketch.Line(point1=(1.0, 0.0), point2=(1.0, 9.5))
bearingSketch.Line(point1=(1.0, 10.0), point2=(1.0, 17.5))
bearingSketch.Line(point1=(1.0, 18.0), point2=(1.0, 20.0))

    #   top square

bearingSketch.Line(point1=(0.0, 18.0), point2=(3.0, 18.0))
bearingSketch.Line(point1=(3.0, 18.0), point2=(3.0, 20.0))

    #   middle

bearingSketch.Line(point1=(0.0, 17.5), point2=(3.5, 17.5))
bearingSketch.Line(point1=(3.5, 17.5), point2=(3.5, 20.0))
bearingSketch.Line(point1=(3.5, 17.5), point2=(3.5, 10.0))
bearingSketch.Line(point1=(3.5, 17.5), point2=(6.0, 17.5))
bearingSketch.Line(point1=(0.0, 10.0), point2=(6.0, 10.0))
bearingSketch.Line(point1=(6.0, 10.0), point2=(6.0, 20.0))

    #   bottom

bearingSketch.Line(point1=(0.0, 9.5), point2=(6.5, 9.5))
bearingSketch.Line(point1=(6.5, 9.5), point2=(6.5, 20.0))
bearingSketch.Line(point1=(6.5, 9.5), point2=(10.0, 9.5))
bearingSketch.Line(point1=(6.5, 9.5), point2=(6.5, 0.0))

bearingPart.PartitionFaceBySketch(faces=face_on_soil, sketch=bearingSketch)
bearingAssembly.regenerate()

# Step creation

# Get access to the step objects by using the import statement. The StaticStep() method is used to create a
# static step which could be used for loading. This is the step next to 'Initial' step created by dafault. Enter the
# initial increment and maximum increment as shown below.

from step import *
bearingModel.StaticStep(name='Load Step', previous='Initial', timePeriod=1000.0, initialInc=100.0, minInc=0.00000001,
                        maxInc=100.0)

# Field output: (only the S22 value is required).

# bearingModel.fieldOutputRequests['F-Output-1'].setValues(variables=('S',))

# History output request left at default.

# Application of boundary conditions -

# Vertical allowance of movement (roller) on left edge

# For doing this, we will first identify the point and use the findAT() method to find the left face and then redefine
# the face and then define the region.

edge_on_leftface = bearingInstance.edges.findAt(((0.0, 5.0, 0.0),))
leftface_region = regionToolset.Region(edges=edge_on_leftface)
edge_on_leftface2 = bearingInstance.edges.findAt(((0.0, 9.75, 0.0),))
leftface_region2 = regionToolset.Region(edges=edge_on_leftface2)
edge_on_leftface3 = bearingInstance.edges.findAt(((0.0, 14.0, 0.0),))
leftface_region3 = regionToolset.Region(edges=edge_on_leftface3)
edge_on_leftface4 = bearingInstance.edges.findAt(((0.0, 17.75, 0.0),))
leftface_region4 = regionToolset.Region(edges=edge_on_leftface4)
edge_on_leftface5 = bearingInstance.edges.findAt(((0.0, 19.0, 0.0),))
leftface_region5 = regionToolset.Region(edges=edge_on_leftface5)

edge_on_rightface1 = bearingInstance.edges.findAt(((10.0, 10.0, 0.0),))
rightface_region1 = regionToolset.Region(edges=edge_on_rightface1)
edge_on_rightface2 = bearingInstance.edges.findAt(((10.0, 10.0, 0.0),))
rightface_region2 = regionToolset.Region(edges=edge_on_rightface2)

edge_on_bottomface1 = bearingInstance.edges.findAt(((1.0, 0.0, 0.0),))
bottomface_region1 = regionToolset.Region(edges=edge_on_bottomface1)
edge_on_bottomface2 = bearingInstance.edges.findAt(((5.0, 0.0, 0.0),))
bottomface_region2 = regionToolset.Region(edges=edge_on_bottomface2)
edge_on_bottomface3 = bearingInstance.edges.findAt(((9.0, 0.0, 0.0),))
bottomface_region3 = regionToolset.Region(edges=edge_on_bottomface3)


# After the defintion of regions, we wil use the DisplacementBC() to define the constraints that replicate the symmetry
# condition.

bearingModel.XsymmBC(name='Left Edge X_Symmetry1', createStepName='Initial', region=leftface_region, localCsys=None)
bearingModel.XsymmBC(name='Left Edge X_Symmetry2', createStepName='Initial', region=leftface_region2, localCsys=None)
bearingModel.XsymmBC(name='Left Edge X_Symmetry3', createStepName='Initial', region=leftface_region3, localCsys=None)
bearingModel.XsymmBC(name='Left Edge X_Symmetry4', createStepName='Initial', region=leftface_region4, localCsys=None)
bearingModel.XsymmBC(name='Left Edge X_Symmetry5', createStepName='Initial', region=leftface_region5, localCsys=None)

bearingModel.DisplacementBC(name='Right Edge Free Vertical1', createStepName='Initial', region=rightface_region1,
                     u1=SET, u2=SET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='',
                              localCsys=None)
bearingModel.DisplacementBC(name='Right Edge Free Vertical2', createStepName='Initial', region=rightface_region2,
                     u1=SET, u2=SET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='',
                              localCsys=None)

bearingModel.DisplacementBC(name='Bottom Edge Pin1', createStepName='Initial', region=bottomface_region1,
                     u1=SET, u2=SET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
bearingModel.DisplacementBC(name='Bottom Edge Pin2', createStepName='Initial', region=bottomface_region2,
                     u1=SET, u2=SET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
bearingModel.DisplacementBC(name='Bottom Edge Pin3', createStepName='Initial', region=bottomface_region3,
                     u1=SET, u2=SET, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)

# Application of load

# A load of 1000N has to be applied at vertex (0.0, 20.0, 0.0). So we should identify it using the findAt() method.
# ConcentratedForce() method is used to apply the force of 1000N at this vertex. Note that, we have referred the
# the step that we created sometime back.

edge_on_bearingface1 = bearingInstance.edges.findAt(((0.5, 20.0, 0.0),))

bearingface_region1 = regionToolset.Region(edges=edge_on_bearingface1)

bearingModel.DisplacementBC(name='Bearing analytical settlement1', createStepName='Load Step', region=bearingface_region1,
                     u1=UNSET, u2=-0.010525666666666668, ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='',
                        localCsys=None)

# Mesh creation

# Get access to the mesh objects by using the import statement. We will use the predefined regions for element
# type definition. C3D8R elements are used in this simulation

import mesh

        #Bodies within the soil

point_in_square1 = (0.5, 19.0, 0.0)
point_in_square2 = (2.0, 19.0, 0.0)

        # bodies within the soil 2

point_in_square3 = (0.5, 14.0, 0.0)
point_in_square4 = (2.0, 14.0, 0.0)
point_in_square5 = (5.0, 14.0, 0.0)
point_in_square6 = (5.0, 19.0, 0.0)

        #   bodies within the soil 3

point_in_square7 = (0.5, 5.0, 0.0)
point_in_square8 = (2.0, 5.0, 0.0)
point_in_square9 = (9.0, 5.0, 0.0)
point_in_square10 = (9.0, 15.0, 0.0)

        #   bodies within the triangles

point_in_tri1 = (0.5, 17.75, 0.0)
point_in_tri2 = (0.5, 9.75, 0.0)


        # Assinging body to a face

face_on_square1 = bearingPart.faces.findAt((point_in_square1,))
face_on_square2 = bearingPart.faces.findAt((point_in_square2,))
face_on_square3 = bearingPart.faces.findAt((point_in_square3,))
face_on_square4 = bearingPart.faces.findAt((point_in_square4,))
face_on_square5 = bearingPart.faces.findAt((point_in_square5,))
face_on_square6 = bearingPart.faces.findAt((point_in_square6,))
face_on_square7 = bearingPart.faces.findAt((point_in_square7,))
face_on_square8 = bearingPart.faces.findAt((point_in_square8,))
face_on_square9 = bearingPart.faces.findAt((point_in_square9,))
face_on_square10 = bearingPart.faces.findAt((point_in_square10,))
face_on_tri1 = bearingPart.faces.findAt((point_in_square1,))
face_on_tri2 = bearingPart.faces.findAt((point_in_square2,))

        # Assigning the element type to the faces in the soil

elemType1 = mesh.ElemType(elemCode=CPE4, elemLibrary=STANDARD)
elemType2 = mesh.ElemType(elemCode=CPE3, elemLibrary=STANDARD)

f = bearingPart.faces
faces = f.getSequenceFromMask(mask=('[#aff ]',), )
pickedRegions = (faces,)
bearingPart.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
elemType1 = mesh.ElemType(elemCode=CPE4, elemLibrary=STANDARD,
                          secondOrderAccuracy=OFF, hourglassControl=DEFAULT,
                          distortionControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=CPE3, elemLibrary=STANDARD,
                          secondOrderAccuracy=OFF, distortionControl=DEFAULT)

faces = f.getSequenceFromMask(mask=('[#500 ]',), )
pickedRegions = (faces,)
bearingPart.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

# Element shapes

pickedRegionsQuad = bearingPart.faces.findAt((point_in_square1,), (point_in_square2,), (point_in_square3,),
                                             (point_in_square4,), (point_in_square5,), (point_in_square6,),
                                             (point_in_square7,), (point_in_square8,), (point_in_square9,))
bearingPart.setMeshControls(regions=pickedRegionsQuad, elemShape=QUAD, technique=STRUCTURED)

pickedRegionsTri = bearingPart.faces.findAt((point_in_tri1,), (point_in_tri2,))
bearingPart.setMeshControls(regions=pickedRegionsTri, elemShape=TRI, technique=FREE)

        # Seeding the edges

edge_on_left1 = bearingInstance.edges.findAt(((0.0, 19.0, 0.0),))
edge_on_left2 = bearingInstance.edges.findAt(((0.0, 14.0, 0.0),))

edge_on_top1 = bearingInstance.edges.findAt(((0.5, 20.0, 0.0),))
edge_on_top2 = bearingInstance.edges.findAt(((2.0, 20.0, 0.0),))
edge_on_top3 = bearingInstance.edges.findAt(((5.0, 20.0, 0.0),))

edge_on_inner_top1 = bearingInstance.edges.findAt(((0.5, 17.5, 0.0),))
edge_on_inner_top2 = bearingInstance.edges.findAt(((2.0, 17.5, 0.0),))
edge_on_inner_rhs = bearingInstance.edges.findAt(((6.0, 19.0, 0.0),))

bearingPart.seedEdgeByNumber(edges=edge_on_left1, number=60, constraint=FINER)
bearingPart.seedEdgeByNumber(edges=edge_on_top1, number=30, constraint=FINER)
bearingPart.seedEdgeByNumber(edges=edge_on_top2, number=60, constraint=FINER)

bearingPart.seedEdgeByNumber(edges=edge_on_left2, number=60, constraint=FINER)

bearingPart.seedEdgeByNumber(edges=edge_on_top3, number=17, constraint=FINER)
bearingPart.seedEdgeByNumber(edges=edge_on_inner_top1, number=8, constraint=FINER)
bearingPart.seedEdgeByNumber(edges=edge_on_inner_top2, number=20, constraint=FINER)
bearingPart.seedEdgeByNumber(edges=edge_on_inner_rhs, number=20, constraint=FINER)

bearingPart.seedPart(size=0.4, deviationFactor=0.03)
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

#mdb.jobs['bearingJob2D'].submit(consistencyChecking=OFF)
#mdb.jobs['bearingJob2D'].waitForCompletion()
