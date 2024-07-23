# -*- coding: utf-8 -*-
__title__ = "Toggle PointCloud"
__doc__ = """Version = 1.0
Date    = 11.07.2024
__________________________________________________________________
Description:
This script allows users to toggle the visibility of point cloud links in the active view.
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


# Function to toggle point cloud link visibility
def toggle_point_cloud_links():
    # Collect all point cloud links in the active view
    point_cloud_links_collector = FilteredElementCollector(doc, active_view.Id).OfClass(PointCloudInstance)

    # Start a transaction
    t = Transaction(doc, "Toggle Point Cloud Links")
    t.Start()

    try:
        for point_cloud in point_cloud_links_collector:
            # Get the current visibility setting
            current_visibility = active_view.GetElementOverrides(point_cloud.Id).IsCategoryHidden(
                BuiltInCategory.OST_PointClouds)

            # Toggle the visibility
            if current_visibility:
                active_view.SetCategoryHidden(BuiltInCategory.OST_PointClouds, False)
            else:
                active_view.SetCategoryHidden(BuiltInCategory.OST_PointClouds, True)

        t.Commit()
        TaskDialog.Show("Toggle Point Cloud Links", "Point cloud link visibility in the active view has been toggled.")
    except Exception as e:
        t.RollBack()
        TaskDialog.Show("Error", str(e))
        return


# Show a warning prompt before proceeding
warning_dialog = TaskDialog("Warning")
warning_dialog.MainInstruction = "This will toggle the visibility of point cloud links in the active view. Do you want to proceed?"
warning_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
warning_dialog.DefaultButton = TaskDialogResult.Yes

result = warning_dialog.Show()

if result == TaskDialogResult.Yes:
    toggle_point_cloud_links()
else:
    TaskDialog.Show("Operation Cancelled", "The operation was cancelled by the user.")
