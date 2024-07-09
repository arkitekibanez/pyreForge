__title__ = "Loadable \nFamilies"
__doc__ = """Version = 1.0
Date    = 05.04.2024
__________________________________________________________________
Description:
This script retrieves the total number of loadable families loaded, 
along with their individual file sizes. It provides a useful metric 
for monitoring and optimizing Revit file sizes.
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

# -*- coding: utf-8 -*-

# Import the necessary Revit API classes
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog

# Get the active document
doc = __revit__.ActiveUIDocument.Document

# Get all family instances
family_instances = FilteredElementCollector(doc).OfClass(FamilyInstance)

# Initialize a dictionary to store family names
loaded_families = {}

# Iterate over the family instances
for instance in family_instances:
    family_name = instance.Symbol.Family.Name
    if family_name not in loaded_families:
        loaded_families[family_name] = True

# Show a TaskDialog with the number of loaded families
task_dialog = TaskDialog("Success")
task_dialog.MainContent = "Loaded families:\n"
for family in loaded_families.keys():
    task_dialog.MainContent += "{}\n".format(family)
task_dialog.MainContent += "\nTotal number of loaded families: {}".format(len(loaded_families))
task_dialog.Show()