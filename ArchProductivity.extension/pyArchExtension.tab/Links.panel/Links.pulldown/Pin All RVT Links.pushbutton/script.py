__title__ = 'Pin All RVT Links'
__doc__ = """Version = 1.0
Date    = 05.04.2024
__________________________________________________________________
Description:
Pin all links
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
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction

# Get the current Revit application and document
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

def pin_all_links():
    # Start a transaction
    t = Transaction(doc, "Pin All Links")
    t.Start()

    # Get all linked models
    collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks)
    links = collector.ToElements()

    # Pin each linked model
    for link in links:
        if not link.Pinned:
            link.Pinned = True

    # Commit the transaction
    t.Commit()

# Call the function to pin all links
pin_all_links()
