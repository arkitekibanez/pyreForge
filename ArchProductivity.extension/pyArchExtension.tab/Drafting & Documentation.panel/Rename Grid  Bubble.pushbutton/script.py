# Title and documentation strings
__title__ = "Auto Rename \nGrid Bubbles"
__doc__ = """Version: 1.1
Date: = 05.04.2024
__________________________________________________________________
Description:
This script automates the process of updating grid numbering in a Revit project view. 
It categorizes grids into vertical and horizontal based on their orientation. 
Vertical grids are numbered sequentially starting from 1 upwards, while horizontal 
grids are labeled alphabetically (A, B, C, etc.). 
__________________________________________________________________
How-to:
1. The script identifies and sorts grids into vertical and horizontal orientations.
2. Vertical grids are numbered sequentially starting from 1 upwards.
3. Horizontal grids are labeled alphabetically (A, B, C, etc.) starting from the topmost grid.
__________________________________________________________________
Author: Luis Ibanez"""

# Import necessary Revit API classes
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons, TaskDialogResult
from Autodesk.Revit.DB import *
from System.Collections.Generic import List
from System.Windows.Forms import Form, Label, TextBox, Button, DialogResult
from System.Drawing import Point

# Define the input form for prefix and suffix
class PrefixSuffixForm(Form):
    def __init__(self):
        self.Text = "Enter Prefix and Suffix"
        self.Width = 300
        self.Height = 200

        # Prefix label and textbox
        self.prefix_label = Label()
        self.prefix_label.Text = "Prefix:"
        self.prefix_label.Location = Point(10, 20)
        self.Controls.Add(self.prefix_label)

        self.prefix_textbox = TextBox()
        self.prefix_textbox.Location = Point(self.prefix_label.Right + 10, self.prefix_label.Top)
        self.prefix_textbox.Width = 100  # Adjust width as needed
        self.Controls.Add(self.prefix_textbox)

        # Suffix label and textbox
        self.suffix_label = Label()
        self.suffix_label.Text = "Suffix:"
        self.suffix_label.Location = Point(10, self.prefix_label.Bottom + 20)
        self.Controls.Add(self.suffix_label)

        self.suffix_textbox = TextBox()
        self.suffix_textbox.Location = Point(self.suffix_label.Right + 10, self.suffix_label.Top)
        self.suffix_textbox.Width = 100  # Adjust width as needed
        self.Controls.Add(self.suffix_textbox)

        # OK button
        self.ok_button = Button()
        self.ok_button.Text = "OK"
        self.ok_button.Location = Point(10, self.suffix_label.Bottom + 20)
        self.ok_button.DialogResult = DialogResult.OK
        self.AcceptButton = self.ok_button
        self.Controls.Add(self.ok_button)

        # Cancel button
        self.cancel_button = Button()
        self.cancel_button.Text = "Cancel"
        self.cancel_button.Location = Point(self.ok_button.Right + 10, self.suffix_label.Bottom + 20)
        self.cancel_button.DialogResult = DialogResult.Cancel
        self.CancelButton = self.cancel_button
        self.Controls.Add(self.cancel_button)

# Function to get prefix and suffix input from the user
def get_prefix_suffix():
    form = PrefixSuffixForm()
    result = form.ShowDialog()
    if result == DialogResult.OK:
        prefix = form.prefix_textbox.Text
        suffix = form.suffix_textbox.Text
        form.Dispose()  # Dispose the form after use
        return prefix, suffix
    else:
        form.Dispose()  # Dispose the form after use
        return None, None

# Function to update grid names based on prefix and suffix
def update_grid_with_prefix_suffix(prefix, suffix):
    # Get active document and view
    doc = __revit__.ActiveUIDocument.Document
    active_view = doc.ActiveView

    # Function to determine if a grid is vertical
    def is_vertical(grid):
        direction = grid.Curve.Direction
        return abs(direction.X) < 0.01 and abs(direction.Y) > 0.99

    # Function to determine if a grid is horizontal
    def is_horizontal(grid):
        direction = grid.Curve.Direction
        return abs(direction.X) > 0.99 and abs(direction.Y) < 0.01

    # Function to generate a unique temporary grid name
    def generate_temp_name(base_name, existing_names):
        return base_name + "_temp"

    # Function to generate a unique final grid name for vertical grids (1 to 100)
    def generate_vertical_name(number):
        return "{}{}{}".format(prefix, number, suffix)

    # Function to generate a unique final grid name for horizontal grids (A to Z)
    def generate_horizontal_name(letter):
        return "{}{}{}".format(prefix, letter, suffix)

    # Get all grids in the active view
    grids = FilteredElementCollector(doc, active_view.Id).OfCategory(
        BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElements()

    # Sort grids based on their position
    def sort_grids(grids):
        vertical_grids = [grid for grid in grids if is_vertical(grid)]
        horizontal_grids = [grid for grid in grids if is_horizontal(grid)]

        # Sort vertically from left to right
        sorted_vertical_grids = sorted(vertical_grids, key=lambda g: g.Curve.GetEndPoint(0).X)
        # Sort horizontally from top to bottom
        sorted_horizontal_grids = sorted(horizontal_grids, key=lambda g: g.Curve.GetEndPoint(0).Y, reverse=True)

        return sorted_vertical_grids + sorted_horizontal_grids

    sorted_grids = sort_grids(grids)

    if not sorted_grids:
        TaskDialog.Show("Error", "No grids found in the active view.")
        return

    # Collect existing grid names to ensure uniqueness
    existing_names = set(grid.Name for grid in grids)

    # Start a transaction to modify the grids
    transaction = Transaction(doc, "Update Grid Numbering")

    try:
        if transaction.HasStarted():
            transaction.RollBack()

        transaction.Start()

        # Assign temporary unique names to all grids
        for grid in sorted_grids:
            temp_name = generate_temp_name(grid.Name, existing_names)
            grid.Name = temp_name
            existing_names.add(temp_name)

        # Reassign final names based on orientation
        last_number_vertical = 1
        last_letter_horizontal = 'A'

        for grid in sorted_grids:
            if is_vertical(grid):
                new_name = generate_vertical_name(last_number_vertical)
                last_number_vertical += 1
            elif is_horizontal(grid):
                new_name = generate_horizontal_name(last_letter_horizontal)
                last_letter_horizontal = chr(ord(last_letter_horizontal) + 1)

            grid.Name = new_name
            existing_names.add(new_name)

        transaction.Commit()

        # Inform the user about the number of grids updated
        grid_count = len(sorted_grids)
        TaskDialog.Show("Grid Numbering Update", "{} grids have been renumbered.".format(grid_count))

    except Exception as ex:
        # Roll back transaction if an error occurs
        if transaction.HasStarted():
            transaction.RollBack()
        TaskDialog.Show("Error", "Failed to update grid numbering: {}".format(ex))

    finally:
        # Dispose of transaction resources
        if transaction.HasStarted():
            transaction.Dispose()

# Main execution flow
if __name__ == "__main__":
    # Show prefix and suffix input form
    prefix, suffix = get_prefix_suffix()

    # If prefix and suffix are provided, update grids
    if prefix is not None and suffix is not None:
        update_grid_with_prefix_suffix(prefix, suffix)
    else:
        TaskDialog.Show("Cancelled", "Operation cancelled by user.")

