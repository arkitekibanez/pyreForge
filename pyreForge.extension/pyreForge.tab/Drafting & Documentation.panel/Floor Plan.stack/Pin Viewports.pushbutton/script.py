__title__ = "Pin Viewports"
__doc__ = """Version = 1.1
Date    = 22.01.2025
_____________________________________________________________________
Description:
Pin or Unpin all viewports using a dialog with buttons.
_____________________________________________________________________
How-to:
-> Click the button and select whether to pin or unpin all viewports.
_____________________________________________________________________
Last update:
- [22.01.2025] - v1.1.0 Updated to use standard Yes/No buttons for Pin/Unpin options.
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

# Create a dialog with Pin and Unpin options using buttons
action_dialog = TaskDialog("Pin or Unpin Viewports")
action_dialog.MainContent = "Choose whether to pin or unpin all viewports."
action_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
action_dialog.MainInstruction = "Click Yes to Pin or No to Unpin the viewports."

# Show the dialog
result = action_dialog.Show()

# Define the function to pin or unpin viewports
def toggle_viewports(doc, pin=True):
    # Start a transaction
    t = Transaction(doc, "Toggle Viewports Pin")
    t.Start()

    # Get all the viewports in the document
    collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Viewports)

    # Iterate through viewports and either pin or unpin them
    for viewport in collector:
        viewport.Pinned = pin

    # Commit the transaction
    t.Commit()
    t.Dispose()

# Proceed based on user selection
if result == TaskDialogResult.Yes:  # "Pin" option
    toggle_viewports(doc, pin=True)
    # Show success dialog for pinning
    success_dialog = TaskDialog("Success")
    success_dialog.MainContent = "All viewports have been pinned successfully!"
    success_dialog.Show()

elif result == TaskDialogResult.No:  # "Unpin" option
    toggle_viewports(doc, pin=False)
    # Show success dialog for unpinning
    success_dialog = TaskDialog("Success")
    success_dialog.MainContent = "All viewports have been unpinned successfully!"
    success_dialog.Show()

# If the operation was canceled
else:
    cancelled_dialog = TaskDialog("Cancelled")
    cancelled_dialog.MainContent = "Operation cancelled."
    cancelled_dialog.Show()
