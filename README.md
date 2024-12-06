## Grass Generator for Autodesk Maya
A tool for generating grass blades in a Maya scene. Allows users to customize grass length, density, and placement on selected surfaces using a graphical interface.

### Features
- Grass Length Selection: Choose from four grass types: Mowed, Short, Medium, and Long.
- Density Control: Adjust the number of grass blades based on different density calculations.
- Dynamic Sliders: Control grass percentages through sliders that adjust to ensure a total of 100%.
- Post-Generation Tools: Options to delete selected follicles or all follicles in the scene.
- Automatic generation of lambert shader

### Prerequisites
- Maya Autodesk 2023: This tool was built with Autodesk Maya 2023 and utilizes its Python API.
- Python 3.7: Maya' Python API utilises Python 3.7.
- PySide2 (Qt6): Ensure PySide2 is installed to create the graphical interface.

### Installation

Clone this repository
```
git clone https://github.com/Tong-JT/grass-generator-autodesk-maya-plugin.git
```

Add the GrassGenerator directory to your Maya Python path (script will automatically add relative path)
```
C:\Users\USERNAME\documents\maya\VERSION\scripts
```

Launch Maya and run the script
```
Go to Windows > General Editors > Script Editor.
Click on File > Open Script. Navigate to script, select it, and click Open.
Once the script is loaded in the editor, run it by pressing Ctrl + Enter or by clicking the Execute button.
```

Bookmark the script
```
Load script (as above).
Highlight the code in the Script Editor.
Drag and release the highlighted code into the shelf area, under the Custom tab.
Save script to shelf as type: 'Python'.
Customise popup and appearance as needed.

```

### Usage
- Select a Surface: First, select a plane in your scene where you want to generate grass.
- Open the Grass Generator: Run the script to display the Grass Generation UI.
- Choose Grass Type(s): Select your desired grass type(s) and adjust the proportion of grasses using the sliders.
- Set Density: Enter the number of grass blades you want to generate and choose how the density is calculated.
- Generate Grass: Click the "Submit" button to create the grass blades on the selected surface.
- Manage Follicles: Use the post-generation tools to delete follicles as needed.

### History
*Developed as a personal project - derived from a project in 'The MEL Companion: Maya Scripting for 3D Artists (2003) - David Stripinis'.*

- Created: 12th July 2024
- Completed: 18th August 2024
