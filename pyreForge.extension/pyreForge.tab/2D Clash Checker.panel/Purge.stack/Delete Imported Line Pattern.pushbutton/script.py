__title__ = "Delete Imported Line Pattern"
__doc__ = """Version = 1.2
Date    = 18.07.2024
__________________________________________________________________
Description:
Delete imported line pattern
__________________________________________________________________
How-to:

__________________________________________________________________
Last update:
- [22.11.2024] - v1.0.0 Updated to ignore leaders when checking 
for overlaps with 3D elements.
__________________________________________________________________
To-Do:
- 
__________________________________________________________________
Author: Luis Ibanez"""

# Import necessary Revit API classes
from Autodesk.Revit.DB import FilteredElementCollector, FillPatternElement, Transaction, BuiltInCategory, ElementId, \
    Element
from Autodesk.Revit.UI import TaskDialog

# Get the current document
doc = __revit__.ActiveUIDocument.Document


# Function to delete unused filled patterns
def delete_unused_filled_patterns(document):
    # Collect all FillPatternElement objects
    fill_patterns = FilteredElementCollector(document).OfClass(FillPatternElement).ToElements()

    # Initialize lists for unused patterns and their IDs
    unused_patterns = []
    unused_ids = []

    # Check each fill pattern to see if it is in use
    for pattern in fill_patterns:
        # Collect all elements that might use the fill pattern
        is_used = False
        for category in [BuiltInCategory.OST_Floors, BuiltInCategory.OST_Ceilings, BuiltInCategory.OST_Walls,
                         BuiltInCategory.OST_Roofs, BuiltInCategory.OST_Materials]:
            elements = FilteredElementCollector(document).OfCategory(category).ToElements()
            for element in elements:
                if hasattr(element, "GetMaterialIds"):
                    material_ids = element.GetMaterialIds(False)
                    for mat_id in material_ids:
                        material = document.GetElement(mat_id)
                        if material and material.SurfaceForegroundPatternId == pattern.Id:
                            is_used = True
                            break
                if is_used:
                    break
            if is_used:
                break

        # Add unused patterns to the list
        if not is_used:
            unused_patterns.append(pattern)
            unused_ids.append(pattern.Id)

    # Begin a transaction to delete the unused fill patterns
    with Transaction(document, "Delete Unused Filled Patterns") as trans:
        trans.Start()

        # Delete each unused fill pattern
        for pattern_id in unused_ids:
            document.Delete(pattern_id)

        trans.Commit()

    # Display a confirmation message
    TaskDialog.Show("Delete Unused Filled Patterns", "{} unused filled patterns were deleted.".format(len(unused_patterns)))


# Run the function to delete unused filled patterns
delete_unused_filled_patterns(doc)
