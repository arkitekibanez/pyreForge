# -*- coding: utf-8 -*-
__title__ = "Overkill \nDimensions"
__doc__ = """Version = 1.1
Date    = 22.01.2025
__________________________________________________________________
Description:
This script identifies and deletes overlapping dimensions in the active view of Autodesk Revit.
It compares the bounding boxes of all dimensions and retains one copy of each overlapping set, 
deleting the others. The remaining dimensions are selected and displayed for the user.
__________________________________________________________________
How-to:
1. Run the script.
2. The script will check for overlapping dimensions in the active view.
3. The first occurrence of each overlapping set will be retained, and others will be deleted.
4. A success message will confirm the number of dimensions retained.
__________________________________________________________________
Last update:
- [22.01.2025] - v1.1.0 Added orientation check to prevent overlapping of vertical and horizontal dimensions
- [14.01.2025] - v1.0.0 Initial release
__________________________________________________________________
Author: Luis Ibanez"""

# ⬇ IMPORTS
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog
from System.Collections.Generic import List

import clr
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from System.Windows.Forms import Form, Label, Button, CheckBox, DialogResult
from System.Drawing import Point, Size


# Get the active document
doc = __revit__.ActiveUIDocument.Document

# Create a filter for dimensions
dimension_filter = ElementCategoryFilter(BuiltInCategory.OST_Dimensions)

# Collect all dimensions in the active view
collector = FilteredElementCollector(doc, doc.ActiveView.Id).WherePasses(dimension_filter)

# Function to check if two dimensions are overlapping based on their bounding box
def are_dimensions_overlapping(dim1, dim2):
    bbox1 = dim1.get_BoundingBox(doc.ActiveView)
    bbox2 = dim2.get_BoundingBox(doc.ActiveView)

    if bbox1 and bbox2:
        # Check if bounding boxes intersect
        return bbox1.Min.X < bbox2.Max.X and bbox1.Max.X > bbox2.Min.X and \
            bbox1.Min.Y < bbox2.Max.Y and bbox1.Max.Y > bbox2.Min.Y
    return False

# Function to check if the dimension is vertical
def is_vertical_dimension(dim):
    line = dim.Curve
    return abs(line.Direction.X) < abs(line.Direction.Y)

# Check if dimensions were found
if collector.GetElementCount() > 0:
    # Convert the collected dimensions to a list
    dimensions = list(collector)
    to_delete = []

    # Iterate through dimensions and compare for overlaps
    for i, dim1 in enumerate(dimensions):
        for j, dim2 in enumerate(dimensions):
            if i < j and are_dimensions_overlapping(dim1, dim2):
                # Only consider overlap if both dimensions are the same orientation (both vertical or both horizontal)
                if is_vertical_dimension(dim1) == is_vertical_dimension(dim2):
                    # Add overlapping dimension to delete list
                    to_delete.append(dim2)

    # Retain only one copy (keep the first dimension)
    to_delete = list(set(to_delete))  # Remove duplicates

    # Delete overlapping dimensions
    with Transaction(doc, "Delete overlapping dimensions") as t:
        t.Start()
        for dim in to_delete:
            doc.Delete(dim.Id)
        t.Commit()

    # Update the selection to only the remaining dimension
    remaining_dimensions = list(set(dimensions) - set(to_delete))
    selected_elements = List[ElementId]([ElementId(dim.Id.IntegerValue) for dim in remaining_dimensions])
    __revit__.ActiveUIDocument.Selection.SetElementIds(selected_elements)
    TaskDialog.Show("Success", "Retained " + str(len(remaining_dimensions)) + " dimension(s).")
else:
    TaskDialog.Show("No Dimensions", "No dimensions found in the active view.")
