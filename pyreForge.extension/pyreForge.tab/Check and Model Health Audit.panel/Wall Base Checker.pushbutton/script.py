__title__ = "Wall Base \nOffset"
__doc__ = """Version = 1.0
Date    = 26.06.2024
__________________________________________________________________
Description:
This script highlights walls in the active Revit project where 
the base offset is not equal to zero. The walls with non-zero 
base offsets are selected for easy identification.
__________________________________________________________________
How-to:
1. Run the script by clicking the button.
2. The script will select walls whose base offset is not zero.
__________________________________________________________________
Last update:
- [26.06.2024] - v1.0.0 Initial release
__________________________________________________________________
Author: Luis Ibanez"""

# Import necessary modules
from Autodesk.Revit.DB import *
from System.Collections.Generic import List

# Get the active document and UI document
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Collect walls
walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

# Create a list of element IDs
element_ids = List[ElementId]()

for wall in walls:
    base_offset = wall.get_Parameter(BuiltInParameter.WALL_BASE_OFFSET)
    if base_offset:
        if base_offset.AsDouble()!= 0:
            element_ids.Add(wall.Id)

# Set the selection
uidoc.Selection.SetElementIds(element_ids)