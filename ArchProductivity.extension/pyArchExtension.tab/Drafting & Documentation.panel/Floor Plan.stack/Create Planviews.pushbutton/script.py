# -*- coding: utf-8 -*-
__title__ = "Create Plans"
__doc__ = """Version = 1.0
Date    = 26.06.2024
__________________________________________________________________
Description:
This code  allows users to select one or more levels and create 
corresponding floor plans, area plans, structural plans, or 
ceiling plans.
__________________________________________________________________
How-to:
-> Just click on the button
__________________________________________________________________
Last update:
- [26.06.2024] - v1.0.0 Initial release
__________________________________________________________________
To-Do:
- 
__________________________________________________________________
Author: Luis Ibanez"""

# -*- coding: utf-8 -*-
# ⬇ IMPORTS
from Autodesk.Revit.DB import *
import clr

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Windows.Forms import Form, CheckBox, Button, DialogResult, MessageBoxButtons, MessageBoxIcon, ComboBox, \
    ListBox, CheckedListBox, Label
from System.Drawing import Point, Size
from Autodesk.Revit.UI import TaskDialog


class CreatePlanForm(Form):
    def __init__(self):
        self.Text = "Create Plan"
        self.Width = 300
        self.Height = 450

        self.level_note_label = Label()
        self.level_note_label.Text = "Please select one or more levels to proceed:"
        self.level_note_label.Location = Point(10, 10)
        self.level_note_label.Width = 250
        self.Controls.Add(self.level_note_label)

        self.level_listbox = CheckedListBox()
        self.level_listbox.Location = Point(10, 30)
        self.level_listbox.Width = 150
        self.level_listbox.Height = 150
        self.Controls.Add(self.level_listbox)

        self.plan_checkboxes = []
        plan_types = ["Floor Plan", "Area Plan", "Structural Plan", "Ceiling Plan"]
        for i, plan_type in enumerate(plan_types):
            checkbox = CheckBox()
            checkbox.Text = plan_type
            checkbox.Location = Point(10, 190 + i * 30)
            checkbox.Width = 150
            self.Controls.Add(checkbox)
            self.plan_checkboxes.append(checkbox)

        self.ok_button = Button()
        self.ok_button.Text = "OK"
        self.ok_button.Location = Point(10, 350)
        self.ok_button.Width = 75
        self.ok_button.DialogResult = DialogResult.OK
        self.AcceptButton = self.ok_button
        self.Controls.Add(self.ok_button)

        self.cancel_button = Button()
        self.cancel_button.Text = "Cancel"
        self.cancel_button.Location = Point(100, 350)
        self.cancel_button.Width = 75
        self.cancel_button.DialogResult = DialogResult.Cancel
        self.CancelButton = self.cancel_button
        self.Controls.Add(self.cancel_button)

        self.load_levels()

    def load_levels(self):
        doc = __revit__.ActiveUIDocument.Document
        levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
        for level in levels:
            self.level_listbox.Items.Add(level.Name)
            self.level_listbox.SetItemChecked(self.level_listbox.Items.Count - 1, False)

    def create_plans(self):
        global view_family
        doc = __revit__.ActiveUIDocument.Document
        selected_levels = [self.level_listbox.Items[i] for i in range(self.level_listbox.Items.Count) if
                           self.level_listbox.GetItemChecked(i)]
        view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()

        for level_name in selected_levels:
            level = None
            for l in FilteredElementCollector(doc).OfClass(Level).ToElements():
                if l.Name == level_name:
                    level = l
                    break

            for i, checkbox in enumerate(self.plan_checkboxes):
                if checkbox.Checked:
                    plan_type = checkbox.Text
                    if plan_type == "Floor Plan":
                        view_family = ViewFamily.FloorPlan
                    elif plan_type == "Area Plan":
                        view_family = ViewFamily.AreaPlan
                    elif plan_type == "Structural Plan":
                        view_family = ViewFamily.StructuralPlan
                    elif plan_type == "Ceiling Plan":
                        view_family = ViewFamily.CeilingPlan

                    view_types_plans = [vt for vt in view_types if vt.ViewFamily == view_family]
                    plan_type = view_types_plans[0]
                    with Transaction(doc, "Create {} Plan".format(plan_type)) as t:
                        t.Start()
                        view = ViewPlan.Create(doc, plan_type.Id, level.Id)
                        t.Commit()
                    print("{} plan created for level {}".format(plan_type, level_name))

        # Show a pop-up dialog when successful
        task_dialog = TaskDialog("Success")
        task_dialog.MainContent = "Plans created successfully!"
        task_dialog.Show()


form = CreatePlanForm()
if form.ShowDialog() == DialogResult.OK:
    form.create_plans()
