__title__ = "PascalCase"
__doc__ = """Version = 1.0
Date    = 26.06.2024
__________________________________________________________________
Description:
Change the families names to PascalCase.
Note: system default will be ignored.
__________________________________________________________________
How-to:
-> Just click on the button
__________________________________________________________________
Last update:
- [26.06.2024] - 1.0 RELEASE
__________________________________________________________________
To-Do:
- 
__________________________________________________________________
Author: Luis Ibanez"""

# Import the necessary Revit API classes
from Autodesk.Revit.DB import FilteredElementCollector, FamilySymbol, Transaction
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons, TaskDialogResult

# Get the active document
doc = __revit__.ActiveUIDocument.Document

# Show a warning prompt before proceeding
warning_dialog = TaskDialog("Warning")
warning_dialog.MainContent = "This operation will take some time to complete. Do you want to proceed?"
warning_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
warning_dialog.DefaultButton = TaskDialogResult.Yes

result = warning_dialog.Show()

if result == TaskDialogResult.Yes:
    # Get all loaded families in the document
    loaded_families = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()

    # Debug: Print count of loaded families
    print("Found %d loaded families." % len(loaded_families))

    # Function to convert string to PascalCase
    def to_pascal_case(s):
        return ''.join(word.capitalize() for word in s.split())

    # Loop through each loaded family and update its name
    with Transaction(doc, 'Update Loaded Family Names') as t:
        t.Start()
        for family_symbol in loaded_families:
            family_name = family_symbol.Family.Name
            updated_family_name = to_pascal_case(family_name)  # Change to PascalCase

            # Check if the updated name is different
            if family_name!= updated_family_name:
                family_symbol.Family.Name = updated_family_name
                # Debug: Print updated family name
                print("Updated family name: %s" % updated_family_name)
        t.Commit()

    # Show a pop-up dialog when successful
    task_dialog = TaskDialog("Success")
    task_dialog.MainContent = "All Loaded Family names changed to PascalCase successfully"
    task_dialog.Show()
else:
    # Show a message if the user cancels
    task_dialog = TaskDialog("Cancelled")
    task_dialog.MainContent = "Operation cancelled."
    task_dialog.Show()