__title__ = "Dims & Text \nClash Checker"
__doc__ = """Version = 1.0
Date    = 26.06.2024
__________________________________________________________________
Description:
This script detects and selects annotations (dimensions and text 
notes) in the active view that overlap with wall elements.
__________________________________________________________________
How-to:
1.The script will analyze the active view, detecting any 
overlaps between annotations and wall elements.
2.Annotations that overlap with walls will be highlighted in 
the active view.
3. A message dialog will appear, informing you of the number 
of overlapping annotations detected.
__________________________________________________________________
Last update:
- [26.06.2024] - 1.0 RELEASE
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

# Function to check overlap between annotation and wall
def check_overlap_with_wall(annotation, wall):
    # Get the bounding box of the annotation
    annotation_bb = annotation.get_BoundingBox(active_view)

    if annotation_bb is None:
        return False

    # Get the bounding box of the wall
    wall_bb = wall.get_BoundingBox(active_view)

    if wall_bb is None:
        return False

    # Check for overlap along X axis
    x_overlap = (annotation_bb.Min.X <= wall_bb.Max.X) and (annotation_bb.Max.X >= wall_bb.Min.X)

    # Check for overlap along Y axis
    y_overlap = (annotation_bb.Min.Y <= wall_bb.Max.Y) and (annotation_bb.Max.Y >= wall_bb.Min.Y)

    # Check for overlap along Z axis
    z_overlap = (annotation_bb.Min.Z <= wall_bb.Max.Z) and (annotation_bb.Max.Z >= wall_bb.Min.Z)

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

# Function to revert colors of all annotations back to black
def revert_annotation_colors(annotations, view):
    transaction = Transaction(view.Document, "Revert Annotation Colors")
    transaction.Start()
    for annotation_id in annotations:
        element = doc.GetElement(annotation_id)
        overrideSettings = OverrideGraphicSettings().SetProjectionLineColor(Color(0, 0, 0))  # Black color
        view.SetElementOverrides(element.Id, overrideSettings)
    transaction.Commit()

# Show a warning prompt before proceeding
warning_dialog = TaskDialog("Warning")
warning_dialog.MainInstruction = "This will highlight all dimensions and text annotations clashing with walls. Do you want to proceed?"
warning_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
warning_dialog.DefaultButton = TaskDialogResult.Yes

result = warning_dialog.Show()

if result == TaskDialogResult.Yes:
    # Get all dimensions and text notes in the active view
    annotations = FilteredElementCollector(doc, active_view.Id).OfCategory(
        BuiltInCategory.OST_Dimensions).WhereElementIsNotElementType().ToElements()
    text_notes = FilteredElementCollector(doc, active_view.Id).OfCategory(
        BuiltInCategory.OST_TextNotes).WhereElementIsNotElementType().ToElements()

    # Combine dimensions and text notes into one list
    all_annotations = list(annotations) + list(text_notes)

    # List to store annotations that overlap with walls
    overlapping_annotations = []

    # Collect all walls in the model
    walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

    # Iterate through annotations and check for overlap with walls
    for annotation in all_annotations:
        is_overlapping = False
        for wall in walls:
            if check_overlap_with_wall(annotation, wall):
                overlapping_annotations.append(annotation.Id)
                highlight_element(annotation, active_view)
                is_overlapping = True
                break  # No need to check further if overlap detected
        if not is_overlapping:
            set_default_color(annotation, active_view)

    # Inform the user about the number of overlapping annotations found
    overlap_count = len(overlapping_annotations)
    TaskDialog.Show("Overlap Detection with Walls", "{} annotations overlap with walls.".format(overlap_count))

    # Show a prompt to revert colors
    revert_dialog = TaskDialog("Revert Colors")
    revert_dialog.MainInstruction = "Do you want to revert the colors of the highlighted annotations to black?"
    revert_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
    revert_dialog.DefaultButton = TaskDialogResult.No

    revert_result = revert_dialog.Show()

    if revert_result == TaskDialogResult.Yes:
        revert_annotation_colors(overlapping_annotations, active_view)
        TaskDialog.Show("Colors Reverted", "The colors of the highlighted annotations have been reverted to black.")
else:
    TaskDialog.Show("Operation Cancelled", "The operation was cancelled by the user.")
