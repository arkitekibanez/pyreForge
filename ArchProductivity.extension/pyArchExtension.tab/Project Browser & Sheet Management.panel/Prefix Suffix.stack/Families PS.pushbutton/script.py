import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from Autodesk.Revit.UI import TaskDialog, TaskDialogResult
from Autodesk.Revit.DB import *
from System.Collections.Generic import List
from System.Windows.Forms import Form, Label, TextBox, Button, DialogResult
from System.Drawing import Point, Size

__title__ = "Add Prefix/Suffix to Families"
__doc__ = """Version = 1.0
Date    = 05.04.2024
_____________________________________________________________________
Description:
Add a Family Prefix and Suffix per user input.
_____________________________________________________________________
How-to:
-> Just click on the button
_____________________________________________________________________
Last update:
- [05.04.2024] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- 
_____________________________________________________________________
Author: Luis Ibanez"""

# Get the active document
doc = __revit__.ActiveUIDocument.Document

# Get all loaded families in the document
loaded_families = FilteredElementCollector(doc).OfClass(FamilySymbol).ToElements()

# Function to generate a unique name
def generate_unique_name(base_name):
    existing_names = [fam.Family.Name for fam in loaded_families]
    unique_name = base_name
    count = 1
    while unique_name in existing_names:
        unique_name = "{}_{}".format(base_name, count)
        count += 1
    return unique_name

# Define the input form for prefix and suffix
class PrefixSuffixForm(Form):
    def __init__(self):
        self.Text = "Enter Family Prefix and Suffix"
        self.Width = 550
        self.Height = 200

        # Prefix label and textbox
        self.prefix_label = Label()
        self.prefix_label.Text = "Prefix:"
        self.prefix_label.Location = Point(20, 20)
        self.Controls.Add(self.prefix_label)

        self.prefix_textbox = TextBox()
        self.prefix_textbox.Location = Point(self.prefix_label.Right + 10, self.prefix_label.Top)
        self.prefix_textbox.Size = Size(150, 20)
        self.Controls.Add(self.prefix_textbox)

        # Suffix label and textbox
        self.suffix_label = Label()
        self.suffix_label.Text = "Suffix:"
        self.suffix_label.Location = Point(20, self.prefix_label.Bottom + 20)
        self.Controls.Add(self.suffix_label)

        self.suffix_textbox = TextBox()
        self.suffix_textbox.Location = Point(self.suffix_label.Right + 10, self.suffix_label.Top)
        self.suffix_textbox.Size = Size(150, 20)
        self.Controls.Add(self.suffix_textbox)

        # Add Prefix or Suffix button
        self.add_button = Button()
        self.add_button.Text = "Add Prefix or Suffix"
        self.add_button.Location = Point(20, self.suffix_label.Bottom + 20)
        self.add_button.Size = Size(150, 30)
        self.add_button.DialogResult = DialogResult.OK
        self.AcceptButton = self.add_button
        self.Controls.Add(self.add_button)

        # Remove Prefix/Suffix button
        self.remove_button = Button()
        self.remove_button.Text = "Remove Prefix/Suffix"
        self.remove_button.Location = Point(self.add_button.Right + 20, self.suffix_label.Bottom + 20)
        self.remove_button.Size = Size(150, 30)
        self.remove_button.Click += self.remove_prefix_suffix
        self.Controls.Add(self.remove_button)

        # Cancel button
        self.cancel_button = Button()
        self.cancel_button.Text = "Cancel"
        self.cancel_button.Location = Point(self.remove_button.Right + 20, self.suffix_label.Bottom + 20)
        self.cancel_button.Size = Size(150, 30)
        self.cancel_button.DialogResult = DialogResult.Cancel
        self.CancelButton = self.cancel_button
        self.Controls.Add(self.cancel_button)

    def remove_prefix_suffix(self, sender, event):
        prefix_to_remove = self.prefix_textbox.Text.strip()
        suffix_to_remove = self.suffix_textbox.Text.strip()

        if prefix_to_remove or suffix_to_remove:
            with Transaction(doc, 'Remove Prefix/Suffix from Family Names') as t:
                t.Start()
                for family_symbol in loaded_families:
                    family_name = family_symbol.Family.Name

                    # Remove prefix if present
                    if prefix_to_remove and family_name.startswith(prefix_to_remove):
                        family_name = family_name[len(prefix_to_remove):]

                    # Remove suffix if present
                    if suffix_to_remove and family_name.endswith(suffix_to_remove):
                        family_name = family_name[:-len(suffix_to_remove)]

                    family_symbol.Family.Name = generate_unique_name(family_name)
                t.Commit()

                # Show a pop-up dialog when successful
                task_dialog = TaskDialog("Success")
                task_dialog.MainContent = "Prefix and/or Suffix removed from Family names successfully."
                task_dialog.Show()
        else:
            # Show a message if neither prefix nor suffix is provided
            task_dialog = TaskDialog("Error")
            task_dialog.MainContent = "Please provide either a prefix or suffix to remove."
            task_dialog.Show()

# Instantiate the form and show it
form = PrefixSuffixForm()
result = form.ShowDialog()

if result == DialogResult.OK:
    prefix = form.prefix_textbox.Text.strip()
    suffix = form.suffix_textbox.Text.strip()

    if prefix or suffix:
        with Transaction(doc, 'Update Loaded Family Names') as t:
            t.Start()
            for family_symbol in loaded_families:
                family_name = family_symbol.Family.Name
                new_family_name = family_name

                # Apply prefix if family name doesn't already start with it
                if prefix and not family_name.startswith(prefix):
                    new_family_name = prefix + new_family_name

                # Apply suffix if provided and family name doesn't already end with it
                if suffix and not family_name.endswith(suffix):
                    new_family_name += suffix

                new_family_name = generate_unique_name(new_family_name)

                if family_name != new_family_name:
                    family_symbol.Family.Name = new_family_name
                    print("Updated family name: %s" % new_family_name)
            t.Commit()

        # Show a pop-up dialog when successful
        task_dialog = TaskDialog("Success")
        task_dialog.MainContent = "All Loaded Family names modified successfully with prefix and suffix."
        task_dialog.Show()
    else:
        # Show a message if neither prefix nor suffix is provided
        task_dialog = TaskDialog("Error")
        task_dialog.MainContent = "Please provide either a prefix or suffix."
        task_dialog.Show()
else:
    # Show a message if the user cancels
    task_dialog = TaskDialog("Cancelled")
    task_dialog.MainContent = "Operation cancelled."
    task_dialog.Show()
