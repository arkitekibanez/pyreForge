import clr

clr.AddReference('RevitAPI')
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
from Autodesk.Revit.DB import *
from System.Windows.Forms import Form, CheckBox, Button, Label
from System.Drawing import Point, Size

# Title and documentation strings
__title__ = "Grid Bubbles \nVisibility"
__doc__ = """Version: 1.0
Date: 15.07.2024
__________________________________________________________________
Description:
This script automates the process of managing grid bubble visibility in a Revit project view. 
It provides an interface to toggle the visibility of grid bubbles based on their orientation 
and position (Top, Bottom, Left, Right). The user can choose to hide or show bubbles 
for selected orientations through a user-friendly form.
__________________________________________________________________
How-to:
1. Run the script to open the Grid Bubble Visibility form.
2. Use the checkboxes to select which grid bubbles to hide or show:
   - **Top**: Toggle visibility of the top bubble.
   - **Bottom**: Toggle visibility of the bottom bubble.
   - **Left**: Toggle visibility of the left bubble.
   - **Right**: Toggle visibility of the right bubble.
   - **All**: Select all orientations.
   - **None**: Deselect all orientations.
3. Click **Hide** to hide the selected grid bubbles.
4. Click **Show** to show the selected grid bubbles.
__________________________________________________________________
Last update:
- [19.07.2024] - v1.0.0 interchanged Left and Right functionality, added Show button)
__________________________________________________________________
Author: Luis Ibanez"""


class MyForm(Form):
    def __init__(self, grids, view):
        self.Text = 'Grid Bubble Visibility'
        self.Size = Size(400, 300)  # Increase the size to ensure all items are visible
        self.grids = grids
        self.view = view

        # Warning Label
        self.warning_label = Label()
        self.warning_label.Text = 'Instruction: \nUse the checkboxes to select which side of grid bubbles to hide or show.'
        self.warning_label.AutoSize = True
        self.warning_label.Location = Point(10, 10)
        self.Controls.Add(self.warning_label)

        # Initialize CheckBoxes
        self.top_checkbox = CheckBox()
        self.top_checkbox.Text = 'Top'
        self.top_checkbox.Location = Point(10, 40)
        self.Controls.Add(self.top_checkbox)

        self.bottom_checkbox = CheckBox()
        self.bottom_checkbox.Text = 'Bottom'
        self.bottom_checkbox.Location = Point(10, 70)
        self.Controls.Add(self.bottom_checkbox)

        self.left_checkbox = CheckBox()
        self.left_checkbox.Text = 'Left'
        self.left_checkbox.Location = Point(10, 100)
        self.Controls.Add(self.left_checkbox)

        self.right_checkbox = CheckBox()
        self.right_checkbox.Text = 'Right'
        self.right_checkbox.Location = Point(10, 130)
        self.Controls.Add(self.right_checkbox)

        self.all_checkbox = CheckBox()
        self.all_checkbox.Text = 'All'
        self.all_checkbox.Location = Point(10, 160)
        self.all_checkbox.CheckedChanged += self.all_checkbox_checked_changed
        self.Controls.Add(self.all_checkbox)

        self.none_checkbox = CheckBox()
        self.none_checkbox.Text = 'None'
        self.none_checkbox.Location = Point(10, 190)
        self.none_checkbox.CheckedChanged += self.none_checkbox_checked_changed
        self.Controls.Add(self.none_checkbox)

        # Initialize Buttons
        self.hide_button = Button()
        self.hide_button.Text = 'Hide'
        self.hide_button.Location = Point(50, 220)
        self.hide_button.Click += self.hide_button_clicked
        self.Controls.Add(self.hide_button)

        self.show_button = Button()
        self.show_button.Text = 'Show'
        self.show_button.Location = Point(150, 220)  # Adjusted to add space between buttons
        self.show_button.Click += self.show_button_clicked
        self.Controls.Add(self.show_button)

        # Remove AcceptButton and CancelButton settings to prevent dialog from closing
        # self.AcceptButton = self.hide_button
        # self.CancelButton = self.show_button

    def all_checkbox_checked_changed(self, sender, args):
        if self.all_checkbox.Checked:
            self.top_checkbox.Checked = True
            self.bottom_checkbox.Checked = True
            self.left_checkbox.Checked = True
            self.right_checkbox.Checked = True
            self.none_checkbox.Checked = False

    def none_checkbox_checked_changed(self, sender, args):
        if self.none_checkbox.Checked:
            self.top_checkbox.Checked = False
            self.bottom_checkbox.Checked = False
            self.left_checkbox.Checked = False
            self.right_checkbox.Checked = False
            self.all_checkbox.Checked = False

    def hide_button_clicked(self, sender, args):
        self.toggle_bubbles(False)

    def show_button_clicked(self, sender, args):
        self.toggle_bubbles(True)

    def toggle_bubbles(self, show):
        # Start a new transaction
        t = Transaction(doc, 'Toggle Grid Bubbles')
        t.Start()

        # Get the checkboxes state
        show_top = self.top_checkbox.Checked
        show_bottom = self.bottom_checkbox.Checked
        show_left = self.left_checkbox.Checked
        show_right = self.right_checkbox.Checked

        # Hide/Show bubbles for each grid based on selected checkboxes
        for grid in self.grids:
            # Get the curve of the grid
            curve = grid.Curve
            if isinstance(curve, Line):
                # Transform the curve to the view's coordinate system
                transform = Transform.Identity
                transform.BasisX = self.view.RightDirection
                transform.BasisY = self.view.UpDirection
                transform.BasisZ = XYZ.BasisZ
                ep0 = transform.Inverse.OfPoint(curve.GetEndPoint(0))
                ep1 = transform.Inverse.OfPoint(curve.GetEndPoint(1))

                # Determine which end to hide/show based on the curve's direction
                if abs(ep0.X - ep1.X) > abs(ep0.Y - ep1.Y):
                    # More horizontal than vertical
                    if ep0.X > ep1.X:
                        # Grid is horizontal, start point is on the left
                        if show_right:
                            (grid.ShowBubbleInView if show else grid.HideBubbleInView)(DatumEnds.End0, self.view)
                        if show_left:
                            (grid.ShowBubbleInView if show else grid.HideBubbleInView)(DatumEnds.End1, self.view)
                    else:
                        # Grid is horizontal, end point is on the left
                        if show_left:
                            (grid.ShowBubbleInView if show else grid.HideBubbleInView)(DatumEnds.End1, self.view)
                        if show_right:
                            (grid.ShowBubbleInView if show else grid.HideBubbleInView)(DatumEnds.End0, self.view)
                else:
                    # More vertical than horizontal
                    if ep0.Y > ep1.Y:
                        # Grid is vertical, start point is at the bottom
                        if show_bottom:
                            (grid.ShowBubbleInView if show else grid.HideBubbleInView)(DatumEnds.End0, self.view)
                        if show_top:
                            (grid.ShowBubbleInView if show else grid.HideBubbleInView)(DatumEnds.End1, self.view)
                    else:
                        # Grid is vertical, end point is at the bottom
                        if show_top:
                            (grid.ShowBubbleInView if show else grid.HideBubbleInView)(DatumEnds.End1, self.view)
                        if show_bottom:
                            (grid.ShowBubbleInView if show else grid.HideBubbleInView)(DatumEnds.End0, self.view)

        # Commit the transaction
        t.Commit()


# Example usage
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
grids = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_Grids).ToElements()
form = MyForm(grids, view)
form.ShowDialog()
