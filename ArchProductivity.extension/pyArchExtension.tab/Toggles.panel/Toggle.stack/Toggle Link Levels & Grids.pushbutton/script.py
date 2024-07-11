# -*- coding: utf-8 -*-
__title__ = "Toggle Link \nLevels & Grids"
__doc__ = """Version = 1.0
Date    = 11.07.2024
__________________________________________________________________
Description:
This script allows users to toggle the visibility of levels and grids within Revit links in the active view.
__________________________________________________________________
How-to:
1. Run the script by clicking on the button.
2. Confirm the operation in the prompted dialog.
__________________________________________________________________
Last update:
- [11.07.2024] - 1.0 RELEASE
__________________________________________________________________
Author: Luis Ibanez"""

# Import necessary Revit API classes
from Autodesk.Revit.UI import TaskDialog, TaskDialogResult, TaskDialogCommonButtons
from Autodesk.Revit.DB import *

# Get the active document and active view
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
active_view = doc.ActiveView


# Function to toggle visibility of levels and grids within Revit links
def toggle_link_levels_grids():
    # Define the categories to toggle
    categories_to_toggle = [
        BuiltInCategory.OST_Levels,
        BuiltInCategory.OST_Grids
    ]

    # Start a transaction
    t = Transaction(doc, "Toggle Link Levels & Grids")
    t.Start()

    try:
        # Collect all Revit link instances in the active view
        link_instances = FilteredElementCollector(doc, active_view.Id).OfCategory(
            BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType()

        for link_instance in link_instances:
            link_doc = link_instance.GetLinkDocument()
            if link_doc:
                for category in categories_to_toggle:
                    # Get the visibility settings for the category in the link instance
                    cat = link_doc.Settings.Categories.get_Item(category)
                    if cat:
                        current_visibility = active_view.GetCategoryHidden(cat.Id)

                        # Toggle the visibility state
                        new_visibility = not current_visibility
                        active_view.SetCategoryHidden(cat.Id, new_visibility)

        t.Commit()
        TaskDialog.Show("Toggle Visibility",
                        "The visibility of levels and grids within Revit links in the active view has been toggled.")
    except Exception as e:
        t.RollBack()
        TaskDialog.Show("Error", str(e))


# Show a warning prompt before proceeding
warning_dialog = TaskDialog("Warning")
warning_dialog.MainInstruction = "This will toggle the visibility of levels and grids within Revit links in the active view. Do you want to proceed?"
warning_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
warning_dialog.DefaultButton = TaskDialogResult.Yes

result = warning_dialog.Show()

if result == TaskDialogResult.Yes:
    toggle_link_levels_grids()
else:
    TaskDialog.Show("Operation Cancelled", "The operation was cancelled by the user.")
