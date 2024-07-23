# -*- coding: utf-8 -*-
__title__ = "Get RVT \nFile Size"
__doc__ = """Version = 1.0
Date    = 05.04.2024
__________________________________________________________________
Description:
Get the total file size of the Revit document (saved in local)
Caveat: This will measure only the local file size, since not
every user has credentials to access ACC or BIM 360 API.
__________________________________________________________________
How-to:
1. Open the Revit model.
2. Run this script to get the file size.
3. If the model is located in the cloud, a message will be 
displayed indicating this.
__________________________________________________________________
Last update:
- [18.07.2024] - v1.0.1 Removed the floating value from the output display
- [05.04.2024] - v1.0.0 Initial release
__________________________________________________________________
To-Do:
- 
__________________________________________________________________
Author: Luis Ibanez"""

# Import the necessary Revit API classes
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog
import System.IO

# Get the active document
doc = __revit__.ActiveUIDocument.Document

# Get the file path of the Revit document
file_path = doc.PathName

# Check if the file path is empty (indicating the model is located in the cloud)
if not file_path:
    task_dialog = TaskDialog("Information")
    task_dialog.MainContent = "The model is located in the cloud and/or the local file path is not available."
    task_dialog.Show()
else:
    # Get the file size using FileInfo
    file_info = System.IO.FileInfo(file_path)
    total_file_size = file_info.Length

    # Convert the total file size to megabytes
    total_file_size_mb = total_file_size / (1024 * 1024)

    # Show a TaskDialog with the total file size
    task_dialog = TaskDialog("Success")
    task_dialog.MainContent = ("Total file size: {} MB.\n"
                               "Note: Revit file size should not exceed 150-200MB. "
                               "Consider splitting models and linking files if it's within this file size range.").format(total_file_size_mb)
    task_dialog.Show()
