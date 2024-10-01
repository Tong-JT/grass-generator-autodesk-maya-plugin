import random
from PySide2 import QtWidgets, QtGui, QtCore
import os
import sys
import maya.cmds as cmds

# Maya only reads files within approved paths. This ensures that the current directory can be read by Maya
relativePath = "/GrassGenerator"
for path in sys.path:
    isExist = os.path.exists(path + relativePath)
    if isExist:
        sys.path.append(path + relativePath)

from grass import *


# The UI class controls the graphical interface that the user interacts with, and the logic associated with the
# interface.
class GrassUI(QtWidgets.QDialog):

    def __init__(self):
        super(GrassUI, self).__init__()
        self.setWindowTitle("Generate grass")
        self.setMinimumWidth(300)
        self.createWidgets()

    def createWidgets(self):
        # Creates all GUI components using PyQt. Values are called when buttons are pressed.
        self.grassGroup = QtWidgets.QButtonGroup()
        grassTypeBox = QtWidgets.QVBoxLayout()
        grassExplain = QtWidgets.QLabel("Select grass length:")
        grassTypeBox.addWidget(grassExplain)
        grassList = ["Mowed", "Short", "Medium", "Long"]
        self.sliderLabelMap = {}
        self.rbSliderMap = {}
        grassSliderBox = QtWidgets.QGridLayout()

        for index, grass in enumerate(grassList):
            grassRB = QtWidgets.QRadioButton(grass)
            self.grassGroup.addButton(grassRB)

            grassSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            grassSlider.setMaximum(100)
            grassSlider.setMinimumWidth(300)
            grassSlider.setEnabled(False)

            label = QtWidgets.QLabel('    0%', self)
            label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

            grassSliderBox.addWidget(grassRB, index, 0)
            grassSliderBox.addWidget(grassSlider, index, 1)
            grassSliderBox.addWidget(label, index, 2)

            self.sliderLabelMap[grassSlider] = label
            self.rbSliderMap[grassRB] = grassSlider

            grassRB.toggled.connect(self.updateSliders)
            grassSlider.valueChanged[int].connect(self.slidersHundredPercent)

        grassTypeBox.addLayout(grassSliderBox)
        self.grassGroup.setExclusive(False)

        spacer = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        submitButtonBox = QtWidgets.QVBoxLayout()
        grassExplain = QtWidgets.QLabel("Number of grass blades:")

        bladeSelectionBox = QtWidgets.QHBoxLayout()
        self.densityButtonGroup = QtWidgets.QButtonGroup()
        bladeDensity = ["Absolute", "Density (global grid)", "Density (subdivision)"]
        
        for density in bladeDensity:
            densityRB = QtWidgets.QRadioButton(density)
            self.densityButtonGroup.addButton(densityRB)
            bladeSelectionBox.addWidget(densityRB)

        submitButtonBox.addItem(spacer) 
        submitButtonBox.addWidget(grassExplain)   
        submitButtonBox.addLayout(bladeSelectionBox)
        
        self.grassNumInput = QtWidgets.QLineEdit(self)
        self.grassNumInput.setValidator(QtGui.QIntValidator(0, 1000, self))

        submitButton = QtWidgets.QPushButton("Submit")
        submitButton.clicked.connect(self.grassChoice)
        
        submitButtonBox.addWidget(self.grassNumInput)
        submitButtonBox.addWidget(submitButton)

        spacer2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        postEditBox = QtWidgets.QVBoxLayout()
        postEditLabel = QtWidgets.QLabel("Post-generation tools")
        postEditBox.addWidget(postEditLabel)

        deleteBox = QtWidgets.QHBoxLayout()
        self.deleteGroup = QtWidgets.QButtonGroup()
        deleteOptions = ["Delete selected", "Delete all"]
        
        for delete in deleteOptions:
            deleteRB = QtWidgets.QRadioButton(delete)
            self.deleteGroup.addButton(deleteRB)
            deleteBox.addWidget(deleteRB)

        deleteButton = QtWidgets.QPushButton("Delete follicles")
        deleteButton.clicked.connect(self.deleteFollicles)
        postEditBox.addLayout(deleteBox)
        postEditBox.addWidget(deleteButton)

        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addLayout(grassTypeBox)
        mainLayout.addLayout(submitButtonBox)
        mainLayout.addItem(spacer2)
        mainLayout.addLayout(postEditBox)

    def updateSliders(self):
        # Updates sliders and labels which are currently selected.
        for rb, slider in self.rbSliderMap.items():
            slider.setEnabled(rb.isChecked())
        self.slidersHundredPercent()

    def slidersHundredPercent(self):
        # Ensures all active sliders add up to 100%.
        sliders = [slider for button, slider in self.rbSliderMap.items() if button.isChecked()]
        if not sliders:
            return

        totalValue = sum(slider.value() for slider in sliders)
        if totalValue == 0:
            for slider in sliders:
                slider.setValue(0)
                self.updateLabel(slider)
            return

        for slider in sliders:
            slider.blockSignals(True)
            percentageValue = (slider.value()/totalValue)*100
            slider.setValue(max(0, min(100, int(percentageValue))))
            slider.blockSignals(False)
            self.updateLabel(slider)

    def updateLabel(self, slider):
        # Update number beside the slider.
        if slider in self.sliderLabelMap:
            label = self.sliderLabelMap[slider]
            value = slider.value()
            label.setText(f'    {value:.0f}%')

    def getPlaneBoundaries(self, planeName):
        # Get width and height of the plane, based on the bounding box. (y is the vertical height, x and z are parallel
        # to the floor plane).

        if not cmds.objExists(planeName):
            raise ValueError(f"{planeName} does not exist.")

        boundingBox = cmds.exactWorldBoundingBox(planeName)
        xMin, yMin, zMin, xMax, yMax, zMax = boundingBox
        width = xMax - xMin
        height = zMax - zMin
        
        return (width, height)

    def grassChoice(self):
        # Determines number of grassblades to generate based on the number inputted by user, the chosen density
        # type and percentage of total grass per grass type.
        planeName = cmds.ls(selection=True)
        numberRun = self.getSelectedDensity(planeName)
        grassList = [button for button in self.grassGroup.buttons() if button.isChecked()]

        for selectedGrass in grassList:
            slider = self.rbSliderMap[selectedGrass]
            sliderValue = slider.value()
            typeDensity = round((numberRun*sliderValue) / 100)
            self.generateMultiple(selectedGrass.text(), typeDensity, planeName)

    def getSelectedDensity(self, planeName):
        # User enters a number, then chooses how density is calculated.
        numInput = int(self.grassNumInput.text()) if self.grassNumInput.text().isdigit() else 0
        if numInput == 0:
            return
        
        selectedRadioButton = self.densityButtonGroup.checkedButton()
        if not selectedRadioButton:
            return None

        # The number entered is the number of grass blades generated
        selectedDensityText = selectedRadioButton.text()
        if selectedDensityText == "Absolute":
            return numInput
        
        # The number entered is multiplied by the surface area of the plane
        elif selectedDensityText == "Density (global grid)":
            width, height = self.getPlaneBoundaries(planeName[0])
            surfaceArea = int(width*height)
            densityGlobal = numInput*surfaceArea
            return densityGlobal
        
        # The number entered is multiplied by number of faces on plane
        elif selectedDensityText == "Density (subdivision)":
            cmds.select(planeName)
            faces = cmds.polyListComponentConversion(toFace=True)
            faceCount = len(cmds.ls(faces, fl=True))
            densityFace = numInput*faceCount
            return densityFace

    def createGrass(self, choice):
        # Instantiate grass type.
        # Note: Switch-case not supported in Maya, as Maya uses Python 3.7, and switch case was not available
        # until Python 3.10. Switch case is available with MEL
        
        if choice == "Mowed":
            new = MowedGrass()
        elif choice == "Short":
            new = ShortGrass()
        elif choice == "Medium":
            new = MedGrass()
        elif choice == "Long":
            new = LongGrass()   
            
        return new

    def createFollicle(self, surface):
        # Creates a follicle on surface. Sets up connections between follicle and surface to enable it to
        # follow surface's deformations.
        surfaceName = surface[0]    
        folShape = cmds.createNode("follicle")
        fol = cmds.listRelatives(folShape, f=True, parent=True)[0]

        cmds.connectAttr(f"{surfaceName}.outMesh", f"{folShape}.inputMesh")
        cmds.connectAttr(f"{surfaceName}.worldMatrix[0]", f"{folShape}.inputWorldMatrix")
        cmds.connectAttr(f"{folShape}.outTranslate", f"{fol}.translate")
        cmds.connectAttr(f"{folShape}.outRotate", f"{fol}.rotate")
        cmds.setAttr(f"{folShape}.simulationMethod", 0)
        
        return (folShape, fol)

    def generateMultiple(self, grassType, num, planeName):
        # Creates multiple grassblades, connects them to follicles, then randomises distribution throughout
        # the plane.
        width, height = self.getPlaneBoundaries(planeName[0])
        surfaceArea = int(width*height)
        shader = self.createLambertShader()
        
        for i in range(num):
            grassIteration = self.createGrass(grassType)
            grass = grassIteration.makeGrassBlade()
            grassHeight = grassIteration.getBlade()

            cmds.select(grass[0])
            cmds.hyperShade(assign=shader)

            uvPosition = [random.uniform(0, 1), random.uniform(0, 1)]
            follicleShape, fol = self.createFollicle(planeName)

            cmds.setAttr(f"{follicleShape}.parameterU", uvPosition[0])
            cmds.setAttr(f"{follicleShape}.parameterV", uvPosition[1])
            
            cmds.matchTransform(grass[0], fol)
            cmds.rotate(-90, random.random() * 360, 0, grass[0], r=True)
            cmds.move(0, grassHeight/2, 0, grass[0], r=True)
            cmds.parent(grass[0], fol)

    def createLambertShader(self):
        # Creates shaders for the grass bladers, a light green lambert with a mild gradient.
        # Visual output of shaders must be manually enabled before or after running script.
        shader = cmds.shadingNode('lambert', asShader=True)
        cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=shader + '_SG')
        cmds.setAttr(shader + '.color', 0.45, 0.96, 0.42, type='double3')
        cmds.setAttr(shader + '.ambientColor', 0.229, 0.251, 0, type='double3')

        ramp = cmds.shadingNode('ramp', asShader=True)
        cmds.setAttr(ramp + '.interpolation', 1)
        cmds.setAttr(ramp + '.colorEntryList[0].color', 0.494, 1, 0.418, type='double3')
        cmds.setAttr(ramp + '.colorEntryList[0].position', 0.8)
        cmds.setAttr(ramp + '.colorEntryList[1].color', 0.031, 0.115, 0.033, type='double3')
        cmds.setAttr(ramp + '.colorEntryList[1].position', 0.5)

        cmds.connectAttr(ramp + '.outColor', shader + '.color', force=True)
        return shader

    def deleteFollicles(self):
        # Logic for follicle deletion. User may manually select follicles to delete or delete all at once.
        selectedDeleteButton = self.deleteGroup.checkedButton()

        if selectedDeleteButton is None:
            print("No delete option selected.")
            return

        selectedDeleteText = selectedDeleteButton.text()
        if selectedDeleteText == "Delete selected":
            # Of selected objects, the object type 'follicle' is selected for deletion.
            selectedObjects = cmds.ls(selection=True)
            follicles = []
            for obj in selectedObjects:
                node_type = cmds.nodeType(obj)
                if node_type == 'follicle':
                    follicles.append(obj)
                else:
                    children = cmds.listRelatives(obj, children=True, fullPath=True) or []
                    for child in children:
                        if cmds.nodeType(child) == 'follicle':
                            follicles.append(child)

        elif selectedDeleteText == "Delete all":
            # All 'follicle' types in scene are selected.
            follicles = cmds.ls(type='follicle')
        
        for follicleShape in follicles:
            # For-in deletes the selected follicles, regardless of whether some or all were selected.
            follicleTransform = cmds.listRelatives(follicleShape, parent=True)[0]
            children = cmds.listRelatives(follicleTransform, children=True) or []
            for child in children:
                if cmds.nodeType(child) == 'transform':
                    cmds.parent(child, world=True)
                else:
                    continue
            cmds.delete(follicleTransform)

if __name__ == "__main__":
    menu = GrassUI()
    menu.show()
