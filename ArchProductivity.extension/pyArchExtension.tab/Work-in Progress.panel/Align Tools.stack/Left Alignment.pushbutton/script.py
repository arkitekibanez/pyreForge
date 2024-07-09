# -*- coding: utf-8 -*-
__title__ = "Align Text Annotations"
__doc__ = """Version = 1.0
Date    = 05.04.2024
__________________________________________________________________
Description:
This script aligns the selected text annotation to the left.
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
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Collections.Generic import List

try:
    # Get the active Revit document and UI document
    doc = __revit__.ActiveUIDocument.Document
    uidoc = __revit__.ActiveUIDocument

    def align_text_annotation():
        try:
            # Get the selected elements
            selection = uidoc.Selection
            elements = selection.GetElementIds()

            # Align the selected text annotations to the left
            t = Transaction(doc, 'Align Text Annotations')
            t.Start()
            for element_id in elements:
                element = doc.GetElement(element_id)
                if element.Category.Name == "Text Annotations":
                    element.HorizontalAlignment = HorizontalAlignment.Left
            t.Commit()
            print("Text annotations aligned to the left.")
        except Autodesk.Revit.Exceptions.OperationCanceledException:
            print("Text annotation selection cancelled. Exiting script.")

    align_text_annotation()

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