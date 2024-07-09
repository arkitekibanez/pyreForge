# -*- coding: utf-8 -*-
__title__ = "Mirrored \nElements"
__doc__ = """Version = 1.0
Date    = 05.04.2024
__________________________________________________________________
Description:
The BIM Interoperability tool report flags mirrored elements as 
not being part of best practice. This code will loop through and 
highlight the mirrored 3D elements in the active view
__________________________________________________________________
How-to:
-> Just click on the button
__________________________________________________________________
Last update:
- [05.04.2024] - 1.0 RELEASE
__________________________________________________________________
To-Do:
- 
__________________________________________________________________
Author: Luis Ibanez"""

import clr
clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import List

try:
    # Get the active Revit document and UI document
    doc = __revit__.ActiveUIDocument.Document
    uidoc = __revit__.ActiveUIDocument

    # Get all 3D elements in the active view
    elements = FilteredElementCollector(doc, uidoc.ActiveView.Id).WhereElementIsNotElementType().ToElements()

    # Filter out non-3D elements
    three_d_elements = []
    for element in elements:
        if element.Category and element.Category.CategoryType == CategoryType.Model:
            three_d_elements.append(element)

    # Clear the current selection
    uidoc.Selection.SetElementIds(List[ElementId]())

    # Iterate through elements and select mirrored elements
    element_ids = List[ElementId]()
    for element in three_d_elements:
        if hasattr(element, 'Mirrored') and element.Mirrored:
            element_ids.Add(element.Id)

    uidoc.Selection.SetElementIds(element_ids)

    # Show a message if no mirrored elements are found
    if len(element_ids) == 0:
        task_dialog = TaskDialog("No Mirrored Elements")
        task_dialog.MainContent = "No mirrored elements found in the active view."
        task_dialog.Show()

except AttributeError as e:
    print("Error: ", e)
    task_dialog = TaskDialog("Error")
    task_dialog.MainContent = "Error: " + str(e)
    task_dialog.Show()

except Exception as e:
    print("Error: ", e)
    task_dialog = TaskDialog("Error")
    task_dialog.MainContent = "An unexpected error occurred. Please try again."
    task_dialog.Show()