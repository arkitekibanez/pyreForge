# -*- coding: utf-8 -*-
__title__ = "Erase Rooms"
__doc__ = """Version = 1.3
Date    = 09.07.2024
__________________________________________________________________
Description:
This script identifies and deletes unclosed or redundant rooms from the Revit model. 
It checks for rooms placed in the same location or with zero area, and provides 
confirmation dialogs to proceed with deletion or cancel the operation.
__________________________________________________________________
How-to:
1. Run the script from the Revit UI.
2. A dialog will display the list of rooms to be deleted.
3. Confirm the deletion by clicking 'Yes' or cancel the operation by clicking 'No'.
4. A success or cancellation message will be shown based on your choice.
__________________________________________________________________
Last update:
- [09.07.2024] - v1.0.1 DEBUG information added
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
    try:
        # Get the Revit application and document
        uiapp = __revit__.ActiveUIDocument
        doc = uiapp.Document

        # Identify rooms to be deleted
        rooms_to_delete = get_rooms_to_delete(doc)

        if rooms_to_delete:
            # Create a simple formatted string for the list of rooms
            room_info = []
            for room in rooms_to_delete:
                try:
                    room_id = room.Id.IntegerValue
                    room_name = room.LookupParameter("Name").AsString() if room.LookupParameter("Name") else "Unnamed"
                    room_area = room.Area
                    room_info.append("{0} - {1} (Area: {2})".format(room_id, room_name, room_area))
                except Exception as e:
                    print("Error accessing attributes for room: ", room.Id, e)
            room_list_str = "\n".join(room_info)

            # Show a simplified dialog with the list of rooms to be deleted
            room_list_dialog = TaskDialog("Rooms to be Deleted")
            room_list_dialog.MainContent = "The following rooms will be deleted:\n\n{0}".format(room_list_str)
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

    except Exception as e:
        # Print the error for debugging
        print("Error in main function: ", e)


# Function to get the list of unclosed and redundant rooms
def get_rooms_to_delete(doc):
    try:
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

    except Exception as e:
        # Print the error for debugging
        print("Error in get_rooms_to_delete function: ", e)
        return []


# Function to delete rooms
def delete_rooms(doc, rooms_to_delete):
    try:
        # Start a transaction
        t = Transaction(doc, "Delete Unclosed and Redundant Rooms")
        t.Start()

        # Delete the rooms
        for room in rooms_to_delete:
            doc.Delete(room.Id)

        # Commit the transaction
        t.Commit()

    except Exception as e:
        # Print the error for debugging
        print("Error in delete_rooms function: ", e)
        # Rollback the transaction if there's an error
        t.RollBack()


# Execute main function
if __name__ == "__main__":
    main()
