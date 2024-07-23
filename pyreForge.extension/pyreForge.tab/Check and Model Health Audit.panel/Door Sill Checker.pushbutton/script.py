__title__ = "Door Sill \nChecker"
__doc__ = """Version = 1.0
Date    = 26.06.2024
__________________________________________________________________
Description:
Highlight the door is sill height is not equal to zero. 
__________________________________________________________________
How-to:
1. Click on the button to execute.
2. Execute the command again to update the color once the level has been set to zero.
3. Doors that are part of a curtain wall will be false highlighted, 
to change the color,select all door, then change the graphic 
override to 'no graphics override'.
__________________________________________________________________
Last update:
- [26.06.2024] - v1.0.0 Initial release
__________________________________________________________________
To-Do:
- 
__________________________________________________________________
Author: Luis Ibanez"""

import clr
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

# Function to set default color (black) for elements
def set_default_color(element):
    overrideSettings = OverrideGraphicSettings().SetProjectionLineColor(Color(0, 0, 0))  # Black color
    uidoc.ActiveView.SetElementOverrides(element.Id, overrideSettings)

# Function to highlight elements with non-zero sill height
def highlight_element(element):
    overrideSettings = OverrideGraphicSettings().SetProjectionLineColor(Color(255, 0, 0))  # Red color for highlighting
    uidoc.ActiveView.SetElementOverrides(element.Id, overrideSettings)

# Get the active Revit document and UI document
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Get all doors in the document
doors = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()

# Create Transaction to make changes in the project.
with Transaction(doc, "Highlight Doors with Non-Zero Sill Height") as t:
    t.Start()

    for door in doors:
        sill_height_param = door.get_Parameter(BuiltInParameter.INSTANCE_SILL_HEIGHT_PARAM)
        if sill_height_param:
            sill_height = sill_height_param.AsDouble()
            if sill_height != 0:
                highlight_element(door)
            else:
                set_default_color(door)

    t.Commit()
