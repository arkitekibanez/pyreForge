"""
Script Name: Create Scope Box from Enclosed 2D Line
Version: 1.3
Date: 23.01.2025
Description: This script allows users to create a Scope Box in the active view by interactively selecting an enclosed set of 2D model lines.
How-to:
1. Run the script in RevitPythonShell or as a pyRevit tool.
2. Confirm the initial dialog to proceed.
3. Select a set of ModelLine elements forming a closed loop when prompted.
4. Review the debug dialog for details about the process.
5. The script will create a scope box around the selected lines.
Last Update: [23.01.2025] - v1.3 Improved selection mechanism and debugging information.
Author: Luis Ibanez
"""

# Import Revit API libraries
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import ISelectionFilter  # Import ISelectionFilter

# Import System exceptions
from System import InvalidOperationException

# Get the current document and active view
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
view = doc.ActiveView

# Selection filter for ModelLines
class ModelLineSelectionFilter(ISelectionFilter):
    def AllowElement(self, element):
        # Allow only ModelLines in the current selection
        return isinstance(element, ModelLine)
    def AllowReference(self, reference, point):
        return False  # Disallow picking by reference

# Function to create a scope box
def create_scope_box_from_2d_line():
    debug_message = "Debug Information:\n"  # Initialize debug information

    # Step 1: Confirm initial dialog
    dialog_result = TaskDialog.Show(
        "Create Scope Box",
        "This tool allows you to create a Scope Box from an enclosed set of 2D lines. "
        "Confirm to proceed to the selection step.",
        TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
    )

    if dialog_result != TaskDialogResult.Yes:
        TaskDialog.Show("Cancelled", "Operation cancelled by user.")
        return

    debug_message += "User confirmed to proceed.\n"

    try:
        # Step 2: Prompt user to select model lines
        TaskDialog.Show(
            "Step 2: Select Lines",
            "Please select the 2D lines forming a closed loop.\nUse Ctrl to select multiple lines."
        )

        selection_filter = ModelLineSelectionFilter()
        selected_refs = uidoc.Selection.PickObjects(
            ObjectType.Element, selection_filter, "Select enclosed lines to create a scope box"
        )

        # Convert references to ModelLine elements
        model_lines = [doc.GetElement(ref) for ref in selected_refs]
        debug_message += "Number of selected lines: " + str(len(model_lines)) + "\n"

        if not model_lines:
            TaskDialog.Show("Error", "No lines were selected.")
            return

        # Collect curve geometry from the selected lines
        curves = [line.GeometryCurve for line in model_lines]
        debug_message += "Collected curves:\n"
        for curve in curves:
            debug_message += str(curve) + "\n"

        # Validate that the curves form a closed loop
        if not CurveLoop.AreCurvesJoined(curves):
            TaskDialog.Show("Error", "Selected lines do not form a closed loop.")
            return

        curve_loop = CurveLoop.Create(curves)

        # Compute bounding box for the closed loop
        bounding_box = curve_loop.GetBoundingBox()
        debug_message += "Bounding box dimensions:\n"
        debug_message += "Min: " + str(bounding_box.Min) + "\n"
        debug_message += "Max: " + str(bounding_box.Max) + "\n"

        # Step 3: Create a new scope box
        with Transaction(doc, "Create Scope Box") as t:
            t.Start()
            scope_box = doc.Create.NewScopeBox(view)
            scope_box.Name = "Scope Box from 2D Lines"

            # Set the scope box dimensions
            scope_box.Min = bounding_box.Min
            scope_box.Max = bounding_box.Max
            t.Commit()

        debug_message += "Scope box created successfully!\n"
        TaskDialog.Show("Debug Information", debug_message)
        TaskDialog.Show("Success", "Scope box created successfully!")

    except InvalidOperationException as ex:
        TaskDialog.Show("Error", "Operation canceled or invalid selection.\n" + str(ex))
    except Exception as e:
        debug_message += "Error occurred: " + str(e) + "\n"
        TaskDialog.Show("Debug Information", debug_message)
        TaskDialog.Show("Error", str(e))

# Run the function
create_scope_box_from_2d_line()
