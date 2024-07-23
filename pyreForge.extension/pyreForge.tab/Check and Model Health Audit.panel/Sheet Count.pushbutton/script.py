# -*- coding: utf-8 -*-
__title__ = "Sheet \nCount"
__doc__ = """Version = 1.0
Date    = 05.04.2024
__________________________________________________________________
Description:
This script counts the total number of sheets in the active Revit project and categorizes them into two groups:
1. Active sheets with views.
2. Placeholder sheets with no views.
The script then displays this information in a TaskDialog.
__________________________________________________________________
How-to:
1. Run the script by clicking the button.
2. A TaskDialog will appear showing the total number of sheets, 
the count of sheets with views, and the count of placeholder sheets.
__________________________________________________________________
Last update:
- [05.04.2024] - 1.0.0 Initial Release
__________________________________________________________________
Author: Luis Ibanez"""

# Import the necessary Revit API classes
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog

# Get the active document
doc = __revit__.ActiveUIDocument.Document

# Get all sheets in the document
sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()

# Initialize counters
total_sheets = 0
sheets_with_views = 0
placeholder_sheets = 0

# Loop through each sheet and count
for sheet in sheets:
    total_sheets += 1
    if sheet.GetAllPlacedViews().Count > 0:
        sheets_with_views += 1
    else:
        placeholder_sheets += 1

# Show a TaskDialog with the count of sheets
task_dialog = TaskDialog("Success")
task_dialog.MainContent = "Total sheets: {}\nActive sheets with views: {}\nPlaceholder sheets: {}".format(total_sheets, sheets_with_views, placeholder_sheets)
task_dialog.Show()
