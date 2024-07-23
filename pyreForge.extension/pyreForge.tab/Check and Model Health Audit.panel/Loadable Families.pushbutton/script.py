__title__ = "Loadable \nFamilies"
__doc__ = """Version = 1.2
Date    = 18.07.2024
__________________________________________________________________
Description:
This script retrieves the total number of loadable families loaded 
in the active Revit project and calculates their individual file 
sizes. It provides useful metrics for monitoring and optimizing 
Revit file sizes.
__________________________________________________________________
How-to:
1. Run the script by clicking the button.
2. A warning dialog will appear. Confirm to proceed.
3. The script will list all loadable families along with their file sizes in a TaskDialog.
4. If file sizes cannot be determined, 'Unknown size' will be shown.
__________________________________________________________________
Last update:
- [18.07.2024] - v1.0.1 Added file size calculation for each family and arranged output in specified format
- [15.07.2024] - v.0.0 Initial release
__________________________________________________________________
Author: Luis Ibanez"""

# -*- coding: utf-8 -*-

# Import the necessary Revit API classes
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons, TaskDialogResult
import os

# Show a warning prompt before proceeding
warning_dialog = TaskDialog("Warning")
warning_dialog.MainContent = "This operation will take some time to complete. Do you want to proceed?"
warning_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
warning_dialog.DefaultButton = TaskDialogResult.Yes

result = warning_dialog.Show()

if result == TaskDialogResult.Yes:
    # Get the active document
    doc = __revit__.ActiveUIDocument.Document

    # Get all family instances
    family_instances = FilteredElementCollector(doc).OfClass(FamilyInstance)

    # Initialize lists to store family names and their sizes
    family_names = []
    file_sizes = []

    # Iterate over the family instances
    for instance in family_instances:
        family = instance.Symbol.Family
        family_name = family.Name
        if family_name not in family_names:
            try:
                # Get the family file path
                family_document = doc.EditFamily(family)
                family_path = family_document.PathName
                family_document.Close(False)

                # Get the file size if the family has a valid path
                if os.path.exists(family_path):
                    file_size = os.path.getsize(family_path)
                    family_names.append(family_name)
                    file_sizes.append(file_size)
                else:
                    family_names.append(family_name)
                    file_sizes.append('Unknown size')
            except Exception as e:
                # Handle exceptions (including non-editable families)
                family_names.append(family_name)
                file_sizes.append('Unknown size')

    # Prepare the content for the TaskDialog
    content = "Loaded families and their file sizes:\n\n"
    for family, size in zip(family_names, file_sizes):
        if size == 'Unknown size':
            content += "{} | {}\n".format(family, size)
        else:
            size_str = "{} KB".format(size // 1024) if isinstance(size, int) else size
            content += "{} | {}\n".format(family, size_str)

    content += "\nTotal number of loaded families: {}".format(len(family_names))

    # Show a TaskDialog with the formatted content
    task_dialog = TaskDialog("Success")
    task_dialog.MainContent = content
    task_dialog.Show()
else:
    # User clicked No, do not proceed with the operation
    TaskDialog.Show("Information", "Operation canceled by user.")
