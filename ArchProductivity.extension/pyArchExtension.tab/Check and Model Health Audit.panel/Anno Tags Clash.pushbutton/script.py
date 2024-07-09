__title__ = "Anno Tags \nClash Checker"
__doc__ = """Version = 1.1
Date    = 06.07.2024
__________________________________________________________________
Description:
This script detects and highlights specified tags in the active 
view that overlap with 3D elements such as walls, and columns. 
It is designed to help users identify and address clashes 
between annotation tags and 3D model elements within their 
Revit project.
__________________________________________________________________
How-to:
1. Ensure that the active view in your Revit project is the one 
you wish to analyze.
2. Run the script to begin the overlap detection process.
3. Tags that overlap with 3D elements will be highlighted in 
red in the active view.
4. Non-overlapping tags will revert to their default black color.
__________________________________________________________________
Last update:
- [06.07.2024] - 1.1 Updated to highlight specified tags when 
overlapping with 3D elements
__________________________________________________________________
To-Do:
- 
__________________________________________________________________
Author: Luis Ibanez"""

# Import necessary Revit API classes
from Autodesk.Revit.UI import Selection, TaskDialog, TaskDialogCommonButtons, TaskDialogResult
from Autodesk.Revit.DB import *
from System.Collections.Generic import List

# Get the active document and selection
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
selection = uidoc.Selection

# Get the active view
active_view = doc.ActiveView

# List of tag categories to check
tag_categories = [
    BuiltInCategory.OST_KeynoteTags,
    BuiltInCategory.OST_DetailComponentTags,
    BuiltInCategory.OST_MaterialTags,
    BuiltInCategory.OST_FloorTags,
    BuiltInCategory.OST_CurtaSystemTags,
    BuiltInCategory.OST_HostFinTags,
    BuiltInCategory.OST_StairsTags,
    BuiltInCategory.OST_MultiCategoryTags,
    BuiltInCategory.OST_AreaTags,
    BuiltInCategory.OST_StructuralColumnTags,
    BuiltInCategory.OST_ParkingTags,
    BuiltInCategory.OST_SiteTags,
    BuiltInCategory.OST_SpecialityEquipmentTags,
    BuiltInCategory.OST_GenericModelTags,
    BuiltInCategory.OST_CurtainWallPanelTags,
    BuiltInCategory.OST_WallTags,
    BuiltInCategory.OST_CeilingTags,
    BuiltInCategory.OST_CaseworkTags,
    BuiltInCategory.OST_FurnitureTags,
    BuiltInCategory.OST_RoomTags,
    BuiltInCategory.OST_DoorTags,
    BuiltInCategory.OST_WindowTags
]

# 3D elements categories to check against
element_categories = [
    BuiltInCategory.OST_Walls,
    BuiltInCategory.OST_Columns
]

# Function to check overlap between annotation and 3D element
def check_overlap_with_element(annotation, element):
    # Get the bounding box of the annotation
    annotation_bb = annotation.get_BoundingBox(active_view)

    if annotation_bb is None:
        return False

    # Get the bounding box of the 3D element
    element_bb = element.get_BoundingBox(active_view)

    if element_bb is None:
        return False

    # Check for overlap along X axis
    x_overlap = (annotation_bb.Min.X <= element_bb.Max.X) and (annotation_bb.Max.X >= element_bb.Min.X)

    # Check for overlap along Y axis
    y_overlap = (annotation_bb.Min.Y <= element_bb.Max.Y) and (annotation_bb.Max.Y >= element_bb.Min.Y)

    # Check for overlap along Z axis
    z_overlap = (annotation_bb.Min.Z <= element_bb.Max.Z) and (annotation_bb.Max.Z >= element_bb.Min.Z)

    # If overlaps along all axes, consider it as overlapping
    return x_overlap and y_overlap and z_overlap

# Function to set default color (black) for elements
def set_default_color(element, view):
    overrideSettings = OverrideGraphicSettings().SetProjectionLineColor(Color(0, 0, 0))  # Black color
    transaction = Transaction(view.Document, "Set Default Color")
    transaction.Start()
    view.SetElementOverrides(element.Id, overrideSettings)
    transaction.Commit()

# Function to highlight elements with red color
def highlight_element(element, view):
    overrideSettings = OverrideGraphicSettings().SetProjectionLineColor(Color(255, 0, 0))  # Red color for highlighting
    transaction = Transaction(view.Document, "Highlight Element")
    transaction.Start()
    view.SetElementOverrides(element.Id, overrideSettings)
    transaction.Commit()

# Function to revert colors of all tags back to black
def revert_tag_colors(tags, view):
    transaction = Transaction(view.Document, "Revert Tag Colors")
    transaction.Start()
    for tag_id in tags:
        element = doc.GetElement(tag_id)
        overrideSettings = OverrideGraphicSettings().SetProjectionLineColor(Color(0, 0, 0))  # Black color
        view.SetElementOverrides(element.Id, overrideSettings)
    transaction.Commit()

# Show a warning prompt before proceeding
warning_dialog = TaskDialog("Warning")
warning_dialog.MainInstruction = "This will highlight all tags clashing with 3D elements. Do you want to proceed?"
warning_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
warning_dialog.DefaultButton = TaskDialogResult.Yes

result = warning_dialog.Show()

if result == TaskDialogResult.Yes:
    # Get all tags in the active view
    tags = []
    for category in tag_categories:
        tags.extend(FilteredElementCollector(doc, active_view.Id).OfCategory(category).WhereElementIsNotElementType().ToElements())

    # List to store tags that overlap with 3D elements
    overlapping_tags = []

    # Collect all 3D elements in the model
    elements = []
    for category in element_categories:
        elements.extend(FilteredElementCollector(doc).OfCategory(category).WhereElementIsNotElementType().ToElements())

    # Iterate through tags and check for overlap with 3D elements
    for tag in tags:
        is_overlapping = False
        for element in elements:
            if check_overlap_with_element(tag, element):
                overlapping_tags.append(tag.Id)
                highlight_element(tag, active_view)
                is_overlapping = True
                break  # No need to check further if overlap detected
        if not is_overlapping:
            set_default_color(tag, active_view)

    # Inform the user about the number of overlapping tags found
    overlap_count = len(overlapping_tags)
    TaskDialog.Show("Overlap Detection with 3D Elements", "{} tags overlap with 3D elements.".format(overlap_count))

    # Show a prompt to revert colors
    revert_dialog = TaskDialog("Revert Colors")
    revert_dialog.MainInstruction = "Do you want to revert the colors of the highlighted tags to black?"
    revert_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
    revert_dialog.DefaultButton = TaskDialogResult.No

    revert_result = revert_dialog.Show()

    if revert_result == TaskDialogResult.Yes:
        revert_tag_colors(overlapping_tags, active_view)
        TaskDialog.Show("Colors Reverted", "The colors of the highlighted tags have been reverted to black.")
else:
    TaskDialog.Show("Operation Cancelled", "The operation was cancelled by the user.")
