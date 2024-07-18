__title__ = "Family>Pascal or Sentence Case with Types"
__doc__ = """Version = 1.0
Date    = 26.06.2024
__________________________________________________________________
Description:
Change the family names and their types to Sentence Case or Pascal Case including the its subtypes.
Important Note: system default will be ignored.
__________________________________________________________________
How-to:
-> Just click on the button
__________________________________________________________________
Last update:
- [26.06.2024] - 1.1 RELEASE (added fuction to support subtypes conversion)
- [26.06.2024] - 1.0 RELEASE
__________________________________________________________________
To-Do:
- 
__________________________________________________________________
Author: Luis Ibanez"""

# Import the necessary Revit API classes
from Autodesk.Revit.DB import FilteredElementCollector, FamilySymbol, Transaction
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons, TaskDialogResult
import re

# Function to convert to Pascal Case with word boundary detection
def to_pascal_case(text):
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', text).split()
    return ''.join(word.capitalize() for word in words)

# Function to convert to Sentence Case with word boundary detection
def to_sentence_case(text):
    words = re.sub(r'([a-z])([A-Z])', r'\1 \2', text).split()
    if len(words) > 0:
        words[0] = words[0].capitalize()
    return ' '.join(words).lower()

# Get the active document
doc = __revit__.ActiveUIDocument.Document

# Show a warning prompt before proceeding
warning_dialog = TaskDialog("Warning")
warning_dialog.MainContent = "This operation will take some time to complete. Do you want to proceed?"
warning_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
warning_dialog.DefaultButton = TaskDialogResult.Yes

result = warning_dialog.Show()

if result == TaskDialogResult.Yes:
    # Get all loaded family symbols in the document
    loaded_families = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()

    # Debug: Print count of loaded families
    print("Found %d loaded family symbols." % len(loaded_families))

    # Use a set to keep track of families we've already renamed
    renamed_families = set()

    # Loop through each loaded family symbol and update its name and type names
    with Transaction(doc, 'Update Loaded Family Names and Types') as t:
        t.Start()
        for family_symbol in loaded_families:
            family = family_symbol.Family
            family_name = family.Name

            # Convert the family name if it hasn't been renamed yet
            if family.Id not in renamed_families:
                updated_family_name = to_pascal_case(family_name)  # Change to Pascal Case
                # updated_family_name = to_sentence_case(family_name)  # Uncomment to change to Sentence Case

                # Check if the updated family name is different
                if family_name != updated_family_name:
                    family.Name = updated_family_name
                    # Debug: Print updated family name
                    print("Updated family name: %s" % updated_family_name)
                    renamed_families.add(family.Id)

            # Convert the family type name
            family_type_name = family_symbol.Name
            updated_family_type_name = to_pascal_case(family_type_name)  # Change to Pascal Case
            # updated_family_type_name = to_sentence_case(family_type_name)  # Uncomment to change to Sentence Case

            # Check if the updated family type name is different
            if family_type_name != updated_family_type_name:
                family_symbol.Name = updated_family_type_name
                # Debug: Print updated family type name
                print("Updated family type name: %s" % updated_family_type_name)
        t.Commit()

    # Show a pop-up dialog when successful
    task_dialog = TaskDialog("Success")
    task_dialog.MainContent = "All Loaded Family names and types changed successfully"
    task_dialog.Show()
else:
    # Show a message if the user cancels
    task_dialog = TaskDialog("Cancelled")
    task_dialog.MainContent = "Operation cancelled."
    task_dialog.Show()
