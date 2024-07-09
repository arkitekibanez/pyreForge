__title__ = 'Pin All CAD Links'
__doc__ = """Version = 1.0
Date    = 05.04.2024
__________________________________________________________________
Description:
Pin all CAD links
__________________________________________________________________
How-to:
-> Just click on the button
__________________________________________________________________
Last update:
- [05.04.2024] - 1.0 RELEASE
__________________________________________________________________
To-Do:
- 
__________________________________________________________________
Author: Luis Ibanez"""

import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction, CADLinkType

# Get the current Revit application and document
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document


def pin_all_cad_links():
    # Start a transaction
    t = Transaction(doc, "Pin All CAD Links")
    t.Start()

    # Get all CAD links
    collector = FilteredElementCollector(doc).OfClass(CADLinkType)
    cad_links = collector.ToElements()

    # Pin each CAD link
    for link in cad_links:
        if not link.Pinned:
            link.Pinned = True

    # Commit the transaction
    t.Commit()


# Call the function to pin all CAD links
pin_all_cad_links()
