import maya.cmds as cmds
import random

class Grass:
    def __init__(self):
        self.bladeHeight
        self.grassBend
        self.curveHeight
        self.bladeWidth = random.uniform(0.02,0.04)
        self.randomRotation = random.uniform(0,360)
        

    # Generate individual grass blade
    def makeGrassBlade(self):
        # Create blade
        self.blade = cmds.polyCone(radius = self.bladeWidth, height = self.bladeHeight, subdivisionsX = 3, subdivisionsY = 8)
        cmds.constructionHistory( tgl=False )

        # Make thin
        cmds.setAttr(self.blade[0] + '.scaleX', 0.35)

        # Randomise position and rotate
        cmds.xform(self.blade[0], translation = [0, self.bladeHeight/2, 0])
        cmds.polySoftEdge(angle=120)

        # Bend deformer
        cmds.nonLinear(type='bend', lowBound = 0, highBound = 2, curvature = self.grassBend*-1)
        bendHandle = cmds.ls(selection=True)
        cmds.setAttr(bendHandle[0] + '.translateY', self.curveHeight)

        cmds.select(self.blade)
        cmds.select(bendHandle, add=True)
        cmds.delete(constructionHistory=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False)

        return self.blade

    def getBlade(self):
        return self.bladeHeight
    


class MowedGrass(Grass):    
    def __init__(self):
        self.bladeHeight = random.uniform(0.5,0.7)
        self.grassBend = random.uniform(8,10)
        self.curveHeight = 0.15
        Grass.__init__(self)
        

class ShortGrass(Grass):
    def __init__(self):
        self.bladeHeight = random.uniform(0.7,1)
        self.grassBend = random.uniform(10,25)
        self.curveHeight = 0.15
        Grass.__init__(self)

class MedGrass(Grass):
    def __init__(self):
        self.bladeHeight = random.uniform(1,1.3)
        self.grassBend = random.uniform(25,40)
        self.curveHeight = random.uniform(0.15, 0.25)
        Grass.__init__(self)

class LongGrass(Grass):
    def __init__(self):
        self.bladeHeight = random.uniform(1.3,1.6)
        self.grassBend = random.uniform(25,50)
        self.curveHeight = random.uniform(0.15, 0.25)
        Grass.__init__(self)
