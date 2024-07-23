# -*- coding: utf-8 -*-
__title__ = "Room Tag: SentenceCase"
__doc__ = """Version = 1.0
Date    = 05.04.2024
__________________________________________________________________
Description:
Set all Room Tags to SentenceCase
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

    # Show a warning prompt before proceeding
    warning_dialog = TaskDialog("Warning")
    warning_dialog.MainContent = "This operation will change all room tags to Sentencecase. Do you want to proceed?"
    warning_dialog.CommonButtons = TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No
    warning_dialog.DefaultButton = TaskDialogResult.Yes

    # Show the warning dialog
    result = warning_dialog.Show()

    if result == TaskDialogResult.Yes:
        # Call the function to change room text to sentence case
        change_room_text_sentence_case(doc)

        # Show a smaller pop-up dialogue box when successful
        task_dialog = TaskDialog("Success")
        task_dialog.MainContent = "All room tags have been changed to sentence case successfully!"
        task_dialog.Show()
    else:
        # Show a popup dialog when operation is cancelled
        cancelled_dialog = TaskDialog("Cancelled")
        cancelled_dialog.MainContent = "Operation cancelled."
        cancelled_dialog.Show()


# Function to change room text to sentence case
def change_room_text_sentence_case(doc):
    # Get all room elements
    collector = FilteredElementCollector(doc)
    rooms = collector.OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType()

    # Start a transaction
    t = Transaction(doc, "Change Room Text to Sentence Case")
    t.Start()

    # Iterate through each room
    for room in rooms:
        # Get the current room name
        room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsString()

        # Apply sentence case transformation
        new_text = room_name.capitalize()

        # Set the new room name
        room.get_Parameter(BuiltInParameter.ROOM_NAME).Set(new_text)

    # Commit the transaction
    t.Commit()


# Execute main function
if __name__ == "__main__":
    main()