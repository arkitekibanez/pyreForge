# -*- coding: utf-8 -*-
__title__ = "Views Case"
__doc__ = """Version = 1.1
Date    = 22.01.2025
_____________________________________________________________________
Description:
Change all view titles to lowercase, uppercase, or Pascal case.
_____________________________________________________________________
How-to:
-> Click the button and select the desired case transformation.
_____________________________________________________________________
Last update:
- [22.01.2025] - v1.1.0 Added custom form with checkboxes for case transformation.
_____________________________________________________________________
To-Do:
- 
_____________________________________________________________________
Author: Luis Ibanez"""

# Import necessary Revit API classes
import clr
clr.AddReference("RevitAPI")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction, ViewType
from Autodesk.Revit.UI import TaskDialog
from System.Windows.Forms import Form, Button, CheckBox, Label, DialogResult, Application
from System.Drawing import Size, Point

class CaseSelectionForm(Form):
    def __init__(self):
        self.Text = 'Select Case Transformation'
        self.Size = Size(400, 250)
        self.result = None

        # Create checkboxes
        self.lowercase_checkbox = CheckBox()
        self.lowercase_checkbox.Text = "Lowercase"
        self.lowercase_checkbox.Location = Point(10, 10)
        self.lowercase_checkbox.CheckedChanged += self.checkbox_changed

        self.uppercase_checkbox = CheckBox()
        self.uppercase_checkbox.Text = "Uppercase"
        self.uppercase_checkbox.Location = Point(10, 40)
        self.uppercase_checkbox.CheckedChanged += self.checkbox_changed

        self.pascalcase_checkbox = CheckBox()
        self.pascalcase_checkbox.Text = "Pascal Case"
        self.pascalcase_checkbox.Location = Point(10, 70)
        self.pascalcase_checkbox.CheckedChanged += self.checkbox_changed

        # Create a label for description
        self.label_description = Label()
        self.label_description.Text = "Select a transformation for view titles"
        self.label_description.Location = Point(10, 120)
        self.label_description.Size = Size(350, 40)

        # Create OK button
        ok_button = Button()
        ok_button.Text = "OK"
        ok_button.DialogResult = DialogResult.OK
        ok_button.Location = Point(10, 170)

        # Add controls to the form
        self.Controls.Add(self.lowercase_checkbox)
        self.Controls.Add(self.uppercase_checkbox)
        self.Controls.Add(self.pascalcase_checkbox)
        self.Controls.Add(self.label_description)
        self.Controls.Add(ok_button)

        # Set form's accept button
        self.AcceptButton = ok_button

    def checkbox_changed(self, sender, event):
        if sender.Checked:
            # Disable other checkboxes when one is selected
            if sender == self.lowercase_checkbox:
                self.uppercase_checkbox.Enabled = False
                self.pascalcase_checkbox.Enabled = False
            elif sender == self.uppercase_checkbox:
                self.lowercase_checkbox.Enabled = False
                self.pascalcase_checkbox.Enabled = False
            elif sender == self.pascalcase_checkbox:
                self.lowercase_checkbox.Enabled = False
                self.uppercase_checkbox.Enabled = False
        else:
            # Re-enable all checkboxes when none is selected
            self.lowercase_checkbox.Enabled = True
            self.uppercase_checkbox.Enabled = True
            self.pascalcase_checkbox.Enabled = True

def to_pascal_case(s):
    return ' '.join(word.capitalize() for word in s.split())

def transform_view_names(doc, transform_func):
    views = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
    with Transaction(doc, 'Update View Names') as t:
        t.Start()
        for view in views:
            if view.ViewType in [
                ViewType.FloorPlan, ViewType.Elevation, ViewType.Section, ViewType.Detail,
                ViewType.ThreeD, ViewType.Legend, ViewType.Schedule, ViewType.CeilingPlan]:
                view_name = view.Name
                updated_view_name = transform_func(view_name)
                if view_name != updated_view_name:
                    view.Name = updated_view_name
        t.Commit()

# Get the active document
doc = __revit__.ActiveUIDocument.Document

# Show the form and get the result
form = CaseSelectionForm()
if form.ShowDialog() == DialogResult.OK:
    if form.lowercase_checkbox.Checked:
        transform_view_names(doc, str.lower)
        success_message = "All view titles have been changed to lowercase successfully."
    elif form.uppercase_checkbox.Checked:
        transform_view_names(doc, str.upper)
        success_message = "All view titles have been changed to uppercase successfully."
    elif form.pascalcase_checkbox.Checked:
        transform_view_names(doc, to_pascal_case)
        success_message = "All view titles have been changed to Pascal case successfully."
    else:
        success_message = "No option selected."

    if success_message:
        TaskDialog.Show("Success", success_message)
else:
    TaskDialog.Show("Cancelled", "Operation cancelled.")
