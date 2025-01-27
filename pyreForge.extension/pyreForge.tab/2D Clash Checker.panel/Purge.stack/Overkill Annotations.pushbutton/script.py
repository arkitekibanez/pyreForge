# -*- coding: utf-8 -*-
__title__ = "Overkill \nAnnotations"
__doc__ = """Version = 1.5
Date    = 14.01.2025
__________________________________________________________________
Description:
This script identifies and deletes overlapping text notes, room tags, window tags, door tags, and wall tags in the active view of Autodesk Revit.
The user can select which types of annotations to purge via a dialog box. The script retains one copy of each overlapping set and deletes the others. 
The remaining elements are selected and displayed for the user.
__________________________________________________________________
How-to:
1. Run the script.
2. A dialog will appear allowing you to select which annotations to purge.
3. The script will check for overlapping annotations in the active view based on your selection.
4. The first occurrence of each overlapping set will be retained, and others will be deleted.
5. A success message will confirm the number of elements retained.
__________________________________________________________________
Last update:
- [14.01.2025] - v1.5.0 Added user selection for annotation types
__________________________________________________________________
To-Do:
- Optimize bounding box comparison.
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

# Function to create a dialog for user selection
def create_selection_dialog():
    form = Form()
    form.Text = "Select Annotations to Purge"
    form.Size = Size(300, 300)

    lbl = Label(Text="Select the types of annotations to purge:")
    lbl.Location = Point(10, 10)
    form.Controls.Add(lbl)

    chk_textnotes = CheckBox(Text="Text Notes", Location=Point(10, 40))
    chk_roomtags = CheckBox(Text="Room Tags", Location=Point(10, 70))
    chk_windowtags = CheckBox(Text="Window Tags", Location=Point(10, 100))
    chk_doortags = CheckBox(Text="Door Tags", Location=Point(10, 130))
    chk_walltags = CheckBox(Text="Wall Tags", Location=Point(10, 160))

    form.Controls.Add(chk_textnotes)
    form.Controls.Add(chk_roomtags)
    form.Controls.Add(chk_windowtags)
    form.Controls.Add(chk_doortags)
    form.Controls.Add(chk_walltags)

    btn_ok = Button(Text="OK", Location=Point(50, 200))
    btn_cancel = Button(Text="Cancel", Location=Point(150, 200))

    btn_ok.Click += lambda sender, e: setattr(form, "DialogResult", DialogResult.OK)
    btn_cancel.Click += lambda sender, e: setattr(form, "DialogResult", DialogResult.Cancel)

    form.Controls.Add(btn_ok)
    form.Controls.Add(btn_cancel)

    result = form.ShowDialog()

    return {
        "textnotes": chk_textnotes.Checked,
        "roomtags": chk_roomtags.Checked,
        "windowtags": chk_windowtags.Checked,
        "doortags": chk_doortags.Checked,
        "walltags": chk_walltags.Checked,
        "result": result
    }

# Function to check if two elements are overlapping based on their bounding boxes
def are_elements_overlapping(el1, el2):
    bbox1 = el1.get_BoundingBox(doc.ActiveView)
    bbox2 = el2.get_BoundingBox(doc.ActiveView)

    if bbox1 and bbox2:
        return bbox1.Min.X < bbox2.Max.X and bbox1.Max.X > bbox2.Min.X and \
            bbox1.Min.Y < bbox2.Max.Y and bbox1.Max.Y > bbox2.Min.Y
    return False

# Process and delete overlapping elements
def process_and_delete_overlapping_elements(collector, element_type):
    if collector.GetElementCount() > 0:
        elements = list(collector)
        to_delete = []

        for i, el1 in enumerate(elements):
            for j, el2 in enumerate(elements):
                if i < j and are_elements_overlapping(el1, el2):
                    to_delete.append(el2)

        to_delete = list(set(to_delete))

        with Transaction(doc, "Delete overlapping " + element_type) as t:
            t.Start()
            for el in to_delete:
                doc.Delete(el.Id)
            t.Commit()

        return list(set(elements) - set(to_delete))
    return []

# Show the selection dialog
selection = create_selection_dialog()
if selection["result"] == DialogResult.OK:
    remaining_elements = []

    if selection["textnotes"]:
        collector = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_TextNotes)
        remaining_elements.extend(process_and_delete_overlapping_elements(collector, "text notes"))

    if selection["roomtags"]:
        collector = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_RoomTags)
        remaining_elements.extend(process_and_delete_overlapping_elements(collector, "room tags"))

    if selection["windowtags"]:
        collector = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_WindowTags)
        remaining_elements.extend(process_and_delete_overlapping_elements(collector, "window tags"))

    if selection["doortags"]:
        collector = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_DoorTags)
        remaining_elements.extend(process_and_delete_overlapping_elements(collector, "door tags"))

    if selection["walltags"]:
        collector = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(BuiltInCategory.OST_WallTags)
        remaining_elements.extend(process_and_delete_overlapping_elements(collector, "wall tags"))

    if remaining_elements:
        selected_elements = List[ElementId]([ElementId(el.Id.IntegerValue) for el in remaining_elements])
        __revit__.ActiveUIDocument.Selection.SetElementIds(selected_elements)
        TaskDialog.Show("Success", "Retained " + str(len(remaining_elements)) + " element(s).")
    else:
        TaskDialog.Show("No Elements", "No overlapping elements found for the selected types in the active view.")
else:
    TaskDialog.Show("Cancelled", "The operation was cancelled.")
