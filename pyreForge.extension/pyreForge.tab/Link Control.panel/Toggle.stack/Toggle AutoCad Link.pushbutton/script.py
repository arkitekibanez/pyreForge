# -*- coding: utf-8 -*-
__title__ = "Toggle CAD Links"
__doc__ = """Version = 1.0
Date    = 11.07.2024
__________________________________________________________________
Description:
Work in Progress!
This script allows users to toggle the visibility of AutoCAD links in the active view.
__________________________________________________________________
How-to:
1. Run the script by clicking on the button.
2. Confirm the operation in the prompted dialog.
__________________________________________________________________
Last update:
- [11.07.2024] - 1.0 RELEASE
__________________________________________________________________
To-Do:
Have some bugs, to be fixed on the next release.
__________________________________________________________________
Author: Luis Ibanez"""

# Import necessary Revit API classes
from Autodesk.Revit.UI import TaskDialog, TaskDialogResult, TaskDialogCommonButtons
from Autodesk.Revit.DB import *

# Get the active document and active view
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
active_view = doc.ActiveView

# Function to toggle AutoCAD link visibility
def toggle_autocad_links():
    # Collect all AutoCAD links in the active view
    autocad_links_collector = FilteredElementCollector(doc, active_view.Id).OfClass(ImportInstance)

    # Start a transaction
    t = Transaction(doc, "Toggle AutoCAD Links")
    t.Start()

    try:
        for autocad_link in autocad_links_collector:
            # Get the current visibility setting
            current_visibility = active_view.GetElementOverrides(autocad_link.Id).IsCategoryHidden(
                BuiltInCategory.OST_Imports)

            # Toggle the visibility
            if current_visibility:
                active_view.SetCategoryHidden(BuiltInCategory.OST_Imports, False)
            else:
                active_view.SetCategoryHidden(BuiltInCategory.OST_Imports, True)

        t.Commit()
        TaskDialog.Show("Toggle AutoCAD Links", "AutoCAD link visibility in the active view has been toggled.")
    except Exception as e:
        t.RollBack()
        TaskDialog.Show("Error", str(e))
        return

# Show a warning prompt before proceeding
warning_dialog = TaskDialog("Warning")
warning_dialog.MainInstruction = "This will toggle the visibility of AutoCAD links in the active view. Do you want to proceed?"
warning_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
warning_dialog.DefaultButton = TaskDialogResult.Yes

result = warning_dialog.Show()

if result == TaskDialogResult.Yes:
    toggle_autocad_links()
else:
    TaskDialog.Show("Operation Cancelled", "The operation was cancelled by the user.")
