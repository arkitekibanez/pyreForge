# -*- coding: utf-8 -*-
__title__ = "Color Ceilings \nby Height"
__doc__ = """Version = 1.0
Date    = 11.07.2024
__________________________________________________________________
Description:
This script allows users to highlight ceilings in the active view based on their height. 
Ceilings are colored according to predefined colors based on height ranges from 1.5 to 5 meters.
__________________________________________________________________
How-to:
1. Run the script by clicking on the button.
2. Confirm the operation in the prompted dialog.
__________________________________________________________________
Last update:
- [11.07.2024] - v1.0.0 Initial release
__________________________________________________________________
Author: Luis Ibanez"""

# Import necessary Revit API classes
from Autodesk.Revit.UI import TaskDialog, TaskDialogResult, TaskDialogCommonButtons
from Autodesk.Revit.DB import *
from System.Collections.Generic import List

# Get the active document and selection
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
selection = uidoc.Selection

# Get the active view
active_view = doc.ActiveView

# Function to get a color based on height
def get_color_by_height(height):
    base_height = 1.5  # Starting height in meters
    max_height = 5.0  # Maximum height in meters
    increment = 0.1  # Increment in meters (100mm)

    colors = [
        Color(255, 0, 0),  # Red
        Color(0, 255, 0),  # Green
        Color(0, 0, 255),  # Blue
        Color(255, 255, 0),  # Yellow
        Color(0, 255, 255),  # Cyan
        Color(255, 0, 255),  # Magenta
        Color(128, 0, 0),  # Maroon
        Color(0, 128, 0),  # Dark Green
        Color(0, 0, 128),  # Navy
        Color(128, 128, 0)  # Olive
    ]

    if height < base_height:
        return Color(255, 255, 255)  # White for heights below base_height
    elif height > max_height:
        return Color(0, 0, 0)  # Black for heights above max_height

    index = int((height - base_height) / increment)
    return colors[index % len(colors)]

# Function to get the solid fill pattern ID
def get_solid_fill_pattern_id(doc):
    solid_fill = None
    collector = FilteredElementCollector(doc).OfClass(FillPatternElement)
    for pattern in collector:
        if pattern.GetFillPattern().IsSolidFill:
            solid_fill = pattern.Id
            break
    return solid_fill

# Function to override graphics for ceilings based on their height
def override_ceilings_by_height():
    # Filter for ceilings in the active view
    ceilings_collector = FilteredElementCollector(doc, active_view.Id).OfCategory(
        BuiltInCategory.OST_Ceilings).WhereElementIsNotElementType()

    # Get the solid fill pattern ID
    solid_fill_id = get_solid_fill_pattern_id(doc)

    # Start a transaction
    t = Transaction(doc, "Override Ceilings by Height")
    t.Start()

    try:
        # Iterate through the ceilings and apply overrides
        for ceiling in ceilings_collector:
            height_param = ceiling.LookupParameter("Height Offset From Level")
            if height_param:
                height = height_param.AsDouble() * 0.3048  # Convert from feet to meters
                color = get_color_by_height(height)

                # Create OverrideGraphicSettings
                override_settings = OverrideGraphicSettings()
                override_settings.SetProjectionLineColor(color)
                override_settings.SetSurfaceForegroundPatternColor(color)

                # Set the surface foreground pattern to solid fill
                if solid_fill_id:
                    override_settings.SetSurfaceForegroundPatternId(solid_fill_id)

                active_view.SetElementOverrides(ceiling.Id, override_settings)

        t.Commit()
    except Exception as e:
        t.RollBack()
        TaskDialog.Show("Error", str(e))
        return

# Function to revert ceiling colors to original
def revert_ceilings_color():
    # Start a transaction
    t = Transaction(doc, "Revert Ceiling Colors")
    t.Start()

    try:
        # Filter for ceilings in the active view
        ceilings_collector = FilteredElementCollector(doc, active_view.Id).OfCategory(
            BuiltInCategory.OST_Ceilings).WhereElementIsNotElementType()

        # Iterate through the ceilings and revert overrides
        for ceiling in ceilings_collector:
            override_settings = OverrideGraphicSettings()

            # Set the surface foreground pattern and color to default (no override)
            override_settings.SetSurfaceForegroundPatternId(ElementId.InvalidElementId)
            override_settings.SetSurfaceForegroundPatternColor(Color(255, 255, 255))  # Default color (white)

            active_view.SetElementOverrides(ceiling.Id, override_settings)

        t.Commit()
        TaskDialog.Show("Ceiling Color Reverted", "Ceiling colors have been reverted to the original state.")
    except Exception as e:
        t.RollBack()
        TaskDialog.Show("Error", str(e))
        return

# Show a warning prompt before proceeding
warning_dialog = TaskDialog("Warning")
warning_dialog.MainInstruction = "This will highlight all ceiling elements in the active view by their height. Do you want to proceed?"
warning_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
warning_dialog.DefaultButton = TaskDialogResult.Yes

result = warning_dialog.Show()

if result == TaskDialogResult.Yes:
    override_ceilings_by_height()
    TaskDialog.Show("Ceiling Highlight", "Ceiling elements in the active view have been highlighted by height.")
else:
    TaskDialog.Show("Operation Cancelled", "The operation was cancelled by the user.")

# Option to revert colors
revert_dialog = TaskDialog("Revert Ceiling Colors")
revert_dialog.MainInstruction = "Do you want to revert the ceiling colors back to the original?"
revert_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
revert_dialog.DefaultButton = TaskDialogResult.No

revert_result = revert_dialog.Show()

if revert_result == TaskDialogResult.Yes:
    revert_ceilings_color()
