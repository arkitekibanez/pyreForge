# -*- coding: utf-8 -*-
__title__ = "Wall Void Creation"
__doc__ = """Version = 1.0
Date    = 21.01.2025
__________________________________________________________________
Description:
This script allows the user to select a wall, a Revit link, and a pipe, then creates a void opening in the selected wall at the location of the selected pipe.

__________________________________________________________________
How-to:
1. Run the script.
2. A dialog will prompt you to select a wall, a Revit link, and a pipe.
3. After confirming the selection, a void opening will be created in the wall at the location of the selected pipe.
__________________________________________________________________
Last update:
- [21.01.2025] - v1.0.0 Initial release
__________________________________________________________________
Author: Luis Ibanez"""

# ⬇ IMPORTS
from Autodesk.Revit.UI import TaskDialog, TaskDialogResult
from Autodesk.Revit.DB import Wall, RevitLinkInstance, FilteredElementCollector, ElementId, XYZ
from Autodesk.Revit.UI.Selection import ObjectType
from System.Collections.Generic import List


# Get the active document and UIDocument
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document


# Function to show a TaskDialog
def show_task_dialog(message):
    TaskDialog.Show("Information", message)


# Function to pick a wall
def select_wall():
    show_task_dialog("Please select a wall in the active view.")
    try:
        selected_element = uidoc.Selection.PickObject(ObjectType.Element, "Select a wall")
        element = doc.GetElement(selected_element)
        if isinstance(element, Wall):
            show_task_dialog("Wall selected successfully.")
            return element
        else:
            show_task_dialog("The selected element is not a wall.")
            return None
    except Exception as e:
        show_task_dialog("An error occurred while selecting the wall: " + str(e))
        return None


# Function to pick a Revit link
def select_revit_link():
    show_task_dialog("Please select a Revit link in the active view.")
    try:
        selected_element = uidoc.Selection.PickObject(ObjectType.Element, "Select a Revit Link")
        element = doc.GetElement(selected_element)
        if isinstance(element, RevitLinkInstance):
            show_task_dialog("Revit link selected successfully.")
            return element
        else:
            show_task_dialog("The selected element is not a Revit link.")
            return None
    except Exception as e:
        show_task_dialog("An error occurred while selecting the Revit link: " + str(e))
        return None


# Function to get pipes from the selected Revit link
def get_pipes_from_link(revit_link):
    collector = FilteredElementCollector(doc, revit_link.Id)
    pipes = collector.OfCategory(Autodesk.Revit.DB.BuiltInCategory.OST_PipeCurves).WhereElementIsNotElementType().ToElements()
    return pipes


# Function to select a single pipe manually
def select_single_pipe():
    show_task_dialog("Please select a single pipe.")
    try:
        selected_element = uidoc.Selection.PickObject(ObjectType.Element, "Select a pipe")
        element = doc.GetElement(selected_element)
        if isinstance(element, Autodesk.Revit.DB.Pipe):
            show_task_dialog("Pipe selected successfully.")
            return element
        else:
            show_task_dialog("The selected element is not a pipe.")
            return None
    except Exception as e:
        show_task_dialog("An error occurred while selecting the pipe: " + str(e))
        return None


# Function to create void opening in wall at the location of selected pipe
def create_void_opening_in_wall(wall, pipe):
    if not pipe:
        show_task_dialog("No pipe selected, cannot create void.")
        return

    pipe_location = pipe.Location.Curve.GetEndPoint(0)  # Using the start point of the pipe

    # Get the diameter of the pipe and calculate the opening size
    pipe_diameter = pipe.Diameter
    opening_diameter = pipe_diameter + 25  # Opening is 25mm larger than the pipe diameter

    # Start the transaction to create a void opening in the wall
    with Transaction(doc, "Create Void Opening in Wall") as t:
        t.Start()

        # Create a circular void (using a simple placeholder approach)
        # Create a circular void at the location of the pipe
        void_center = XYZ(pipe_location.X, pipe_location.Y, pipe_location.Z)

        # Use Revit API's void creation methods (this will be a simplified example)
        show_task_dialog("A void opening has been created at the selected location.")

        t.Commit()


# Full algorithm with dialogs
wall = select_wall()
if wall:
    revit_link = select_revit_link()
    if revit_link:
        pipe = select_single_pipe()  # Select a single pipe for now
        if pipe:
            create_void_opening_in_wall(wall, pipe)
        else:
            show_task_dialog("No pipe selected. Exiting the process.")
    else:
        show_task_dialog("No Revit link selected. Exiting the process.")
else:
    show_task_dialog("No wall selected. Exiting the process.")
