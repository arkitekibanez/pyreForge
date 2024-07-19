__title__ = 'Pin/Unpin CAD Links'
__doc__ = """Version = 1.0
Date    = 11.07.2024
__________________________________________________________________
Description:
Work-in Progress!
Toggle pin and unpin all CAD links. 
__________________________________________________________________
How-to:
-> Just click on the button
__________________________________________________________________
Last update:
- [11.07.2024] - v1.0.0 Initial release
__________________________________________________________________
To-Do:
Have some bugs, to be fixed on the next release.
__________________________________________________________________
Author: Luis Ibanez"""

import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction, CADLinkType

# Get the current Revit application and document
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

def toggle_pin_cad_links():
    # Start a transaction
    t = Transaction(doc, "Toggle Pin/Unpin CAD Links")
    t.Start()

    # Get all CAD links
    collector = FilteredElementCollector(doc).OfClass(CADLinkType)
    cad_links = collector.ToElements()

    # Toggle pin/unpin for each CAD link
    for link in cad_links:
        link.Pinned = not link.Pinned

    # Commit the transaction
    t.Commit()

# Call the function to toggle pin/unpin all CAD links
toggle_pin_cad_links()
