__title__ = "Door Suffix"
__doc__ = """Version: 1.0
Date: 05.04.2024
__________________________________________________________________
Description:
Change door tags into sequential tags by adding number suffixes. 
Door tags will follow room numbers.
Note: Tags should contain the Mark Label.
__________________________________________________________________
How-to:
- Just click on the button to execute the script.
__________________________________________________________________
Last update:
- [05.04.2024] - v1.0.0 Initial release
__________________________________________________________________
Author: Luis Ibanez"""

from Autodesk.Revit.DB import *


def set_door_numbers(doc):
    # Start a transaction to make modifications
    t = Transaction(doc, "Set Door Numbers")
    t.Start()

    try:
        # Get all rooms in the document
        rooms_collector = FilteredElementCollector(doc).OfCategory(
            BuiltInCategory.OST_Rooms).WhereElementIsNotElementType()

        for room in rooms_collector:
            # Get the room number
            room_number = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString()

            if room_number:
                # Get the bounding box of the room
                bb = room.get_BoundingBox(None)
                outline = Outline(bb.Min, bb.Max)
                bb_filter = BoundingBoxIntersectsFilter(outline)

                # Find all doors in the room
                doors_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WherePasses(
                    bb_filter).WhereElementIsNotElementType()

                # Initialize suffix with 'A' for each room
                suffix = 'A'

                for door in doors_collector:
                    # Set the door number as room number with suffix
                    door_number = "{}{}".format(room_number, suffix)
                    door.get_Parameter(BuiltInParameter.DOOR_NUMBER).Set(door_number)

                    # Increment suffix to next letter
                    suffix = chr(ord(suffix) + 1)

        # Commit the transaction
        t.Commit()
    except Exception as ex:
        # Rollback the transaction if an exception occurs
        t.RollBack()
        print("An error occurred: {}".format(ex))


# Usage:
doc = __revit__.ActiveUIDocument.Document
set_door_numbers(doc)
