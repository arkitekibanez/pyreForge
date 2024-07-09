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
