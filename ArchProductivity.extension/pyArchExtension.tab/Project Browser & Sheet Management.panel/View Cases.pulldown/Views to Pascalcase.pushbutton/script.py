__title__ = "AllViewsToPascalCase"
__doc__ = """Version = 1.0
Date    = 05.04.2024
_____________________________________________________________________
Description:
Change all view titles to pascal case.
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

# Import necessary Revit API classes
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons, TaskDialogResult
from Autodesk.Revit.DB import *

# Get the active document
doc = __revit__.ActiveUIDocument.Document

# Show a warning prompt before proceeding
warning_dialog = TaskDialog("Warning")
warning_dialog.MainContent = "This operation will change all view titles to pascal case. Do you want to proceed?"
warning_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
warning_dialog.DefaultButton = TaskDialogResult.Yes

result = warning_dialog.Show()

if result == TaskDialogResult.Yes:
    # Get all views in the document (including system family views, detail views, legends, and schedules)
    views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()

    # Define a function to check if the name contains prohibited characters
    def is_valid_name(name):
        prohibited_characters = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '{', '}']
        return all(char not in name for char in prohibited_characters)

    # Start a transaction to update view names
    with Transaction(doc, 'Update View Names') as t:
        t.Start()

        # Loop through each view and update its name to pascal case
        for view in views:
            # Check if the view is a system family view, detail view, legend, or schedule
            if view.ViewType in [ViewType.FloorPlan, ViewType.Elevation, ViewType.Section, ViewType.Detail, ViewType.ThreeD,
                                 ViewType.Legend, ViewType.Schedule, ViewType.CeilingPlan]:
                view_name = view.Name
                words = view_name.split()
                updated_view_name = ''.join(word.capitalize() for word in words)  # Change to pascal case

                # Check if the updated name is valid
                if is_valid_name(updated_view_name):
                    if view_name != updated_view_name:
                        view.Name = updated_view_name
                else:
                    # Handle the case where the updated name is not valid
                    task_dialog = TaskDialog("Error")
                    task_dialog.MainContent = "Skipping view '{0}' due to prohibited characters in the name.\nUpdated name: '{1}'".format(
                        view_name, updated_view_name)
                    task_dialog.Show()

        # Commit the transaction
        t.Commit()

    # Show a success message
    task_dialog = TaskDialog("Success")
    task_dialog.MainContent = "All View names changed to pascal case successfully"
    task_dialog.Show()
else:
    # Show a popup dialog when operation is cancelled
    cancelled_dialog = TaskDialog("Cancelled")
    cancelled_dialog.MainContent = "Operation cancelled."
    cancelled_dialog.Show()