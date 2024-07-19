__title__ = "Room Sequence"
__doc__ = """Version = 1.0
Date    = 05.04.2024
__________________________________________________________________
Description:
Change the room tags from left to right sequence.
__________________________________________________________________
How-to:
-> Just click on the button
__________________________________________________________________
Last update:
- [05.04.2024] - v1.0.0 Initial release
__________________________________________________________________
To-Do:
- 
__________________________________________________________________
Author: Luis Ibanez"""

from Autodesk.Revit.DB import *
import re

def set_room_numbers(doc):
    # Start a transaction to make modifications
    t = Transaction(doc, "Set Room Numbers")
    t.Start()

    try:
        # Get all levels in the document
        levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType()

        # Create a dictionary to store room numbers by level
        room_numbers = {}
        for level in levels:
            level_name = level.Name
            match = re.search(r'\d+', level_name)  # Search for one or more digits in the level name
            if match:
                level_number = int(match.group())  # Extract the numeric part
            else:
                level_number = 0  # Default to level 0 if no numeric part is found
            if level_number == 0:
                room_numbers[level_number] = 1  # Initialize room number for level 0
            else:
                room_numbers[level_number] = level_number * 100 + 1  # Initialize room number for other levels

        # Get all rooms in the document
        rooms_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType()

        # Sort rooms by their X-coordinate (left to right)
        rooms = sorted(rooms_collector, key=lambda room: room.Location.Point.X)

        for room in rooms:
            # Get the room's level
            room_level_id = room.LevelId
            room_level = doc.GetElement(room_level_id)
            level_name = room_level.Name
            match = re.search(r'\d+', level_name)  # Search for one or more digits in the level name
            if match:
                level_number = int(match.group())  # Extract the numeric part
            else:
                level_number = 0  # Default to level 0 if no numeric part is found

            # Get the next available room number for this level
            room_number = room_numbers[level_number]

            # Update the room number
            if level_number == 0:
                room.get_Parameter(BuiltInParameter.ROOM_NUMBER).Set(str(room_number).zfill(3))  # Pad with leading zeros
            else:
                room.get_Parameter(BuiltInParameter.ROOM_NUMBER).Set(str(room_number))

            # Increment the room number for this level
            room_numbers[level_number] += 1

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
set_room_numbers(doc)