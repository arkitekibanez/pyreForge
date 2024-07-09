# -*- coding: utf-8 -*-
__title__ = "Highlight Ceilings"
__doc__ = """Version = 1.0
Date    = 26.06.2024
__________________________________________________________________
Description:
This code  allows users to select all the ceiling in active view.
__________________________________________________________________
How-to:
-> Just click on the button
__________________________________________________________________
Last update:
- [26.06.2024] - 1.0 RELEASE
__________________________________________________________________
To-Do:
- Update to override the color per ceiling height.
__________________________________________________________________
Author: Luis Ibanez"""

# Import necessary Revit API classes
from Autodesk.Revit.UI import TaskDialog, TaskDialogResult, TaskDialogCommonButtons
from Autodesk.Revit.DB import *
from System.Collections.Generic import List

# Get the active document and selection
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
selection = uidoc.Selection

# Get the active view
active_view = doc.ActiveView

# Function to select all ceiling elements in the active view
def select_all_ceilings():
    # Filter for ceilings in the active view
    ceilings_collector = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Ceilings).WhereElementIsNotElementType()

    # Select all ceiling elements
    ceiling_elements = [ceiling.Id for ceiling in ceilings_collector]
    element_ids = List[ElementId](ceiling_elements)  # Convert list to ICollection[ElementId]
    selection.SetElementIds(element_ids)

# Show a warning prompt before proceeding
warning_dialog = TaskDialog("Warning")
warning_dialog.MainInstruction = "This will select all ceiling elements in the active view. Do you want to proceed?"
warning_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
warning_dialog.DefaultButton = TaskDialogResult.Yes

result = warning_dialog.Show()

if result == TaskDialogResult.Yes:
    select_all_ceilings()
    TaskDialog.Show("Ceiling Selection", "All ceiling elements in the active view have been selected.")
else:
    TaskDialog.Show("Operation Cancelled", "The operation was cancelled by the user.")
