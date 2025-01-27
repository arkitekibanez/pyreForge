__title__ = "Lock RVT Links"
__doc__ = """Version = 1.3
Date    = 24.01.2025
__________________________________________________________________
Description:
Pin or Unpin all Revit links using a dialog with Yes/No buttons.
__________________________________________________________________
How-to:
-> Click the button and select whether to pin or unpin all Revit links.
__________________________________________________________________
Last update:
- [24.01.2025] - v1.3.0 Updated to use Yes/No buttons for Pin/Unpin options.
__________________________________________________________________
Author: Luis Ibanez"""

# Import the necessary Revit API classes
import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons, TaskDialogResult

# Get the current Revit document
doc = __revit__.ActiveUIDocument.Document

# Create a dialog with Pin and Unpin options using Yes/No buttons
action_dialog = TaskDialog("Pin or Unpin Revit Links")
action_dialog.MainContent = "Choose whether to pin or unpin all Revit links."
action_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
action_dialog.MainInstruction = "Click Yes to Pin or No to Unpin the Revit links."

# Show the dialog
result = action_dialog.Show()

# Define the function to pin or unpin Revit links
def toggle_links(doc, pin=True):
    # Start a transaction
    t = Transaction(doc, "Toggle Revit Links Pin")
    t.Start()

    # Get all the Revit links in the document
    collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks)

    # Iterate through the Revit links and either pin or unpin them
    for link in collector:
        link.Pinned = pin

    # Commit the transaction
    t.Commit()
    t.Dispose()

# Proceed based on user selection
if result == TaskDialogResult.Yes:  # "Pin" option
    toggle_links(doc, pin=True)
    # Show success dialog for pinning
    success_dialog = TaskDialog("Success")
    success_dialog.MainContent = "All Revit links have been pinned successfully!"
    success_dialog.Show()

elif result == TaskDialogResult.No:  # "Unpin" option
    toggle_links(doc, pin=False)
    # Show success dialog for unpinning
    success_dialog = TaskDialog("Success")
    success_dialog.MainContent = "All Revit links have been unpinned successfully!"
    success_dialog.Show()

# If the operation was canceled
else:
    cancelled_dialog = TaskDialog("Cancelled")
    cancelled_dialog.MainContent = "Operation cancelled."
    cancelled_dialog.Show()
