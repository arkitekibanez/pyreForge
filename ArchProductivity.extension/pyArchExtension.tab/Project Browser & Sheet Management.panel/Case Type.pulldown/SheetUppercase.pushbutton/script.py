# -*- coding: utf-8 -*-
__title__ = "Sheets>Uppercase"
__doc__ = """Version = 1.0
Date    = 05.04.2024
__________________________________________________________________
Description:
Set all sheet titles to UPPERCASE
__________________________________________________________________
How-to:
-> Just click on the button
__________________________________________________________________
Last update:
- [05.04.2024] - v1.0.0 Initial release
__________________________________________________________________
To-Do:
- 
__________________________________________________________________
Author: Luis Ibanez"""

# Import the necessary Revit API classes
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons, TaskDialogResult

# Get the active document
doc = __revit__.ActiveUIDocument.Document

# Show a warning prompt before proceeding
warning_dialog = TaskDialog("Warning")
warning_dialog.MainContent = "This operation will change all sheet titles to UPPERCASE. Do you want to proceed?"
warning_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
warning_dialog.DefaultButton = TaskDialogResult.Yes

result = warning_dialog.Show()

if result == TaskDialogResult.Yes:
    # Get all sheets in the document
    sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()

    # Loop through each sheet and update its name
    with Transaction(doc, 'Update Sheet Titles') as t:
        t.Start()
        for sheet in sheets:
            sheet_name = sheet.Name
            updated_sheet_name = sheet_name.upper()
            if sheet_name != updated_sheet_name:
                sheet.Name = updated_sheet_name
        t.Commit()

    # Show a smaller pop-up dialogue box when successful
    task_dialog = TaskDialog("Success")
    task_dialog.MainContent = "All Drawing title changed to Uppercase Succesfully"
    task_dialog.Show()
else:
    # Show a popup dialog when operation is cancelled
    cancelled_dialog = TaskDialog("Cancelled")
    cancelled_dialog.MainContent = "Operation cancelled."
    cancelled_dialog.Show()