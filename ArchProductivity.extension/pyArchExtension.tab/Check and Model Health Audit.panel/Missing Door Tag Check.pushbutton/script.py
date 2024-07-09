__title__ = "Missing Door \nTag Checker"
__doc__ = """Version = 1.0
Date    = 26.06.2024
__________________________________________________________________
Description:
identifies and highlights doors in the active view that do not 
have associated door tags, aiding in quality control and 
documentation accuracy.
__________________________________________________________________
How-to:
1. Navigate to the view within your Revit project where you 
want to check for untagged doors.
2. Execute the script
3. Observe the highlighted doors in the active view, which 
indicates the doors without associated tags, and take necessary 
actions to tag them appropriately.
_________________________________________________________________
Last update:
- [26.06.2024] - 1.0 RELEASE
__________________________________________________________________
To-Do:
- 
__________________________________________________________________
Author: Luis Ibanez"""

# Import necessary Revit API classes
from Autodesk.Revit.UI import Selection, TaskDialog, UIApplication
from Autodesk.Revit.DB import *
from System.Collections.Generic import List

# Function to set default color (black) for elements
def set_default_color(element, view):
    overrideSettings = OverrideGraphicSettings().SetProjectionLineColor(Color(0, 0, 0))  # Black color
    transaction = Transaction(view.Document, "Set Default Color")
    transaction.Start()
    view.SetElementOverrides(element.Id, overrideSettings)
    transaction.Commit()

# Function to highlight elements with red color
def highlight_element(element, view):
    overrideSettings = OverrideGraphicSettings().SetProjectionLineColor(Color(255, 0, 0))  # Red color for highlighting
    transaction = Transaction(view.Document, "Highlight Element")
    transaction.Start()
    view.SetElementOverrides(element.Id, overrideSettings)
    transaction.Commit()

# Get the active document and selection
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Get the active view
active_view = doc.ActiveView

# Get all doors in the active view
doors = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()

# Get all door tags in the active view
door_tags = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_DoorTags).WhereElementIsNotElementType().ToElements()

# Create a set of door IDs that have tags
tagged_door_ids = set()
for door_tag in door_tags:
    tagged_element_ids = door_tag.GetTaggedLocalElementIds()
    for tagged_element_id in tagged_element_ids:
        if tagged_element_id != ElementId.InvalidElementId:
            tagged_door_ids.add(tagged_element_id)

# Find doors that do not have tags
unmarked_door_ids = [door.Id for door in doors if door.Id not in tagged_door_ids]

# Highlight the unmarked doors in red and set default color to others
for door in doors:
    if door.Id in unmarked_door_ids:
        highlight_element(door, active_view)
    else:
        set_default_color(door, active_view)

# Convert the list of unmarked door ids to a List of ElementId
unmarked_door_element_ids = List[ElementId](unmarked_door_ids)

# Highlight the unmarked doors in the UI selection
uidoc.Selection.SetElementIds(unmarked_door_element_ids)

# Determine the number of unmarked doors
num_unmarked_doors = len(unmarked_door_element_ids)

# Show a TaskDialog with the number of unmarked doors found or a message if none found
if num_unmarked_doors > 0:
    task_dialog = TaskDialog("Doors with Missing Tags")
    task_dialog.MainContent = "There are {} doors with missing tags found. Please fix them.".format(num_unmarked_doors)
    task_dialog.Show()
else:
    task_dialog = TaskDialog("No Doors Found")
    task_dialog.MainContent = "No doors with missing tags found in the active view."
    task_dialog.Show()
