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
git clone https://github.com/Tong-JT/GrassGenerator.git
```

Add the GrassGenerator directory to your Maya Python path
```
C:\Users\USERNAME\documents\maya\VERSION\scripts
```

### Usage
- Select a Surface: First, select the polygonal surface in your Maya scene where you want to generate grass.
- Open the Grass Generator: Run the script to display the Grass Generation UI.
- Choose Grass Type(s): Select your desired grass type and adjust the length using the sliders.
- Set Density: Enter the number of grass blades you want to generate and choose how the density is calculated.
- Generate Grass: Click the "Submit" button to create the grass blades on the selected surface.
- Manage Follicles: Use the post-generation tools to delete follicles as needed.
