__title__ = "Win Suffix"
__doc__ = """Version = 1.0
Date    = 05.04.2024
__________________________________________________________________
Description:
Change window tags into sequential tag by adding a text suffix, 
Note: Tag should contain "Mark" label instead of "Type Mark".
__________________________________________________________________
How-to:
-> Just click on the button
__________________________________________________________________
Last update:
- [05.04.2024] - 1.1 RELEASE (update tooltip)
- [05.04.2024] - 1.0 RELEASE (initial release)
__________________________________________________________________
To-Do:
- 
__________________________________________________________________
Author: Luis Ibanez"""


from Autodesk.Revit.DB import *


def set_window_tags(doc):
    # Start a transaction to make modifications
    t = Transaction(doc, "Set Window Tags")
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

                # Find all windows in the room
                windows_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows).WherePasses(
                    bb_filter).WhereElementIsNotElementType()

                # Initialize suffix with 'A' for each room
                suffix = 'A'

                for window in windows_collector:
                    # Set the window tag as room number with suffix
                    window_tag_number = "{}{}".format(room_number, suffix)
                    window.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).Set(window_tag_number)

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
set_window_tags(doc)
