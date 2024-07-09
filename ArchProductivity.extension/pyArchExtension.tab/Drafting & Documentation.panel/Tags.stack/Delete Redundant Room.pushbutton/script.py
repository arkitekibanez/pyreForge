# -*- coding: utf-8 -*-
__title__ = "Delete \nRedundant Rooms"
__doc__ = """Version = 1.3
Date    = 09.07.2024
__________________________________________________________________
Description:
Delete unclosed and redundant rooms
__________________________________________________________________
How-to:
-> Just click on the button
__________________________________________________________________
Last update:
- [09.07.2024] - 1.3 DEBUG information added
__________________________________________________________________
Author: Luis Ibanez"""

import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *


# Main function
def main():
    # Get the Revit application and document
    app = __revit__.Application
    doc = __revit__.ActiveUIDocument.Document

    # Identify rooms to be deleted
    rooms_to_delete = get_rooms_to_delete(doc)

    if rooms_to_delete:
        room_info = ["{0} - {1} (Area: {2})".format(room.Id, room.Name, room.Area) for room in rooms_to_delete]
        room_list_str = "\n".join(room_info)

        # Show a dialog with the list of rooms to be deleted
        room_list_dialog = TaskDialog("Rooms to be Deleted")
        room_list_dialog.MainContent = "The following rooms will be deleted:\n{0}".format(room_list_str)
        room_list_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
        room_list_dialog.DefaultButton = TaskDialogResult.Yes
        result = room_list_dialog.Show()

        if result == TaskDialogResult.Yes:
            # Call the function to delete the rooms
            delete_rooms(doc, rooms_to_delete)

            # Show a smaller pop-up dialogue box when successful
            task_dialog = TaskDialog("Success")
            task_dialog.MainContent = "Unclosed and redundant rooms have been deleted successfully!"
            task_dialog.Show()
        else:
            # Show a popup dialog when operation is cancelled
            cancelled_dialog = TaskDialog("Cancelled")
            cancelled_dialog.MainContent = "Operation cancelled."
            cancelled_dialog.Show()
    else:
        no_rooms_dialog = TaskDialog("No Rooms to Delete")
        no_rooms_dialog.MainContent = "There are no unclosed or redundant rooms to delete."
        no_rooms_dialog.Show()


# Function to get the list of unclosed and redundant rooms
def get_rooms_to_delete(doc):
    # Get all room elements
    collector = FilteredElementCollector(doc)
    rooms = collector.OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()

    rooms_to_delete = []
    checked_locations = {}

    # Iterate through each room
    for room in rooms:
        # Check if the room is redundant (placed in the same location as another room)
        room_location = room.Location
        if isinstance(room_location, LocationPoint):
            room_point = room_location.Point
            room_area = room.Area

            if (room_point, room_area) in checked_locations:
                rooms_to_delete.append(room)
            else:
                checked_locations[(room_point, room_area)] = room

            if room_area == 0:
                rooms_to_delete.append(room)

    return rooms_to_delete


# Function to delete rooms
def delete_rooms(doc, rooms_to_delete):
    # Start a transaction
    t = Transaction(doc, "Delete Unclosed and Redundant Rooms")
    t.Start()

    # Delete the rooms
    for room in rooms_to_delete:
        doc.Delete(room.Id)

    # Commit the transaction
    t.Commit()


# Execute main function
if __name__ == "__main__":
    main()
