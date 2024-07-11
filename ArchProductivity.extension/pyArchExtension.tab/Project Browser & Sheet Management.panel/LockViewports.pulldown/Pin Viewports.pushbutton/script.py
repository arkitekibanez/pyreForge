__title__ = "Pin Viewports"
__doc__ = """Version = 1.0
Date    = 05.04.2024
_____________________________________________________________________
Description:
Pin all viewports.
_____________________________________________________________________
How-to:
-> Just click on the button
_____________________________________________________________________
Last update:
- [05.04.2024] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- 
_____________________________________________________________________
Author: Luis Ibanez"""

# Import the necessary Revit API classes
import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons, TaskDialogResult

# Get the current Revit document
doc = __revit__.ActiveUIDocument.Document

# Show a warning prompt before proceeding
warning_dialog = TaskDialog("Warning")
warning_dialog.MainContent = "This operation will pin all viewports. Do you want to proceed?"
warning_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
warning_dialog.DefaultButton = TaskDialogResult.Yes

result = warning_dialog.Show()

if result == TaskDialogResult.Yes:
    # Define a function to pin all viewports in the document
    def pin_all_viewports(doc):
        # Start a transaction
        t = Transaction(doc, "Pin All Viewports")
        t.Start()

        # Get all the viewports in the document
        collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Viewports)

        # Iterate through viewports and pin them
        for viewport in collector:
            viewport.Pinned = True

        # Commit the transaction
        t.Commit()
        t.Dispose()

    # Call the function to pin all viewports
    pin_all_viewports(doc)

    # Show a smaller pop-up dialogue box when successful
    task_dialog = TaskDialog("Success")
    task_dialog.MainContent = "All viewports have been pinned successfully!"
    task_dialog.Show()
else:
    # Show a popup dialog when operation is cancelled
    cancelled_dialog = TaskDialog("Cancelled")
    cancelled_dialog.MainContent = "Operation cancelled."
    cancelled_dialog.Show()