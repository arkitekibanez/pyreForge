# -*- coding: utf-8 -*-
__title__ = "Modify Room Tag"
__doc__ = """Version = 1.2
Date    = 22.01.2025
__________________________________________________________________
Description:
Set all Room Tags to lowercase, uppercase, or sentence case.
__________________________________________________________________
How-to:
-> Click the button and select the desired case transformation.
__________________________________________________________________
Last update:
- [22.01.2025] - v1.2.0 Added logic to ensure only one case transformation option is selected at a time.
__________________________________________________________________
To-Do:
- 
__________________________________________________________________
Author: Luis Ibanez"""

import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")

import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from System.Windows.Forms import Form, Button, CheckBox, DialogResult, Application
from System.Drawing import Size, Point

# Form class for selecting case transformation
class CaseSelectionForm(Form):
    def __init__(self):
        self.Text = 'Select Case Transformation'
        self.Size = Size(300, 200)
        self.result = None

        # Create checkboxes
        self.lowercase_checkbox = CheckBox()
        self.lowercase_checkbox.Text = "Lowercase"
        self.lowercase_checkbox.Location = Point(10, 10)
        self.lowercase_checkbox.CheckedChanged += self.on_checkbox_changed

        self.uppercase_checkbox = CheckBox()
        self.uppercase_checkbox.Text = "Uppercase"
        self.uppercase_checkbox.Location = Point(10, 40)
        self.uppercase_checkbox.CheckedChanged += self.on_checkbox_changed

        self.sentencecase_checkbox = CheckBox()
        self.sentencecase_checkbox.Text = "Sentence Case"
        self.sentencecase_checkbox.Location = Point(10, 70)
        self.sentencecase_checkbox.CheckedChanged += self.on_checkbox_changed

        # Create OK button
        ok_button = Button()
        ok_button.Text = "OK"
        ok_button.DialogResult = DialogResult.OK
        ok_button.Location = Point(10, 100)

        # Add controls to the form
        self.Controls.Add(self.lowercase_checkbox)
        self.Controls.Add(self.uppercase_checkbox)
        self.Controls.Add(self.sentencecase_checkbox)
        self.Controls.Add(ok_button)

        # Set form's accept button
        self.AcceptButton = ok_button

    # Event handler to ensure only one checkbox is selected at a time
    def on_checkbox_changed(self, sender, args):
        if sender.Checked:
            if sender == self.lowercase_checkbox:
                self.uppercase_checkbox.Checked = False
                self.sentencecase_checkbox.Checked = False
            elif sender == self.uppercase_checkbox:
                self.lowercase_checkbox.Checked = False
                self.sentencecase_checkbox.Checked = False
            elif sender == self.sentencecase_checkbox:
                self.lowercase_checkbox.Checked = False
                self.uppercase_checkbox.Checked = False

# Function to change room text based on selected case
def change_room_text(doc, transform_func):
    rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType()

    with Transaction(doc, "Change Room Text") as t:
        t.Start()
        for room in rooms:
            room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()
            new_text = transform_func(room_name)
            room.get_Parameter(BuiltInParameter.ROOM_NAME).Set(new_text)
        t.Commit()

# Helper functions for case transformation
def to_sentence_case(s):
    return s.capitalize() if s else ""

# Main function
def main():
    app = __revit__.Application
    doc = __revit__.ActiveUIDocument.Document

    # Show the form and get the result
    form = CaseSelectionForm()
    if form.ShowDialog() == DialogResult.OK:
        if form.lowercase_checkbox.Checked:
            change_room_text(doc, str.lower)
            success_message = "All room tags have been changed to lowercase successfully!"
        elif form.uppercase_checkbox.Checked:
            change_room_text(doc, str.upper)
            success_message = "All room tags have been changed to uppercase successfully!"
        elif form.sentencecase_checkbox.Checked:
            change_room_text(doc, to_sentence_case)
            success_message = "All room tags have been changed to sentence case successfully!"
        else:
            success_message = "No option selected."

        if success_message:
            TaskDialog.Show("Success", success_message)
    else:
        TaskDialog.Show("Cancelled", "Operation cancelled.")

# Execute main function
if __name__ == "__main__":
    main()
