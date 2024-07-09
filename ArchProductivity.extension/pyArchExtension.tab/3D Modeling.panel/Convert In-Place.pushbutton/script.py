# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.Structure import StructuralType  # Import StructuralType explicitly
import clr
import os

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

__title__ = "Convert \nIn-Place \n(WIP)"
__doc__ = """Version = 1.0
Date    = 05.04.2024
__________________________________________________________________
Description:
Work in progress, this script attempt to convert in-place families to
loadable families.
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


def select_model_in_place_family():
    try:
        # Prompt user to select a model-in-place family instance
        picked_element = uidoc.Selection.PickObject(Selection.ObjectType.Element,
                                                    "Select a model-in-place family instance")
        if picked_element:
            return doc.GetElement(picked_element.ElementId)
        else:
            return None
    except Autodesk.Revit.Exceptions.OperationCanceledException:
        TaskDialog.Show("Selection Cancelled", "Model-in-place family selection cancelled.")
        return None


def create_loadable_generic_family(template_path):
    try:
        # Check if the template file exists
        if not os.path.exists(template_path):
            TaskDialog.Show("Error", "Template file does not exist: " + template_path)
            return None

        # Create a new family document from the template
        app = __revit__.Application
        family_doc = app.NewFamilyDocument(template_path)
        if family_doc:
            transaction = Transaction(family_doc, "Create Loadable Generic Family")
            transaction.Start()

            try:
                # Perform operations to create geometry or other necessary settings
                # For example, you can create a simple extrusion here
                profile_plane = Plane.CreateByNormalAndOrigin(XYZ.BasisZ, XYZ.Zero)
                sketch_plane = SketchPlane.Create(family_doc, profile_plane)
                profile = Line.CreateBound(XYZ.Zero, XYZ.BasisX * 10)
                extrusion = family_doc.FamilyCreate.NewExtrusion(True, [profile], sketch_plane, 10, False)

                transaction.Commit()

                # Save the family document to a temporary location
                temp_path = os.path.join(os.getenv('TEMP'), 'TemporaryFamily.rfa')
                family_doc.SaveAs(temp_path)
                family_doc.Close(False)

                # Load the family from the temporary location into the current project
                transaction = Transaction(doc, "Load Family")
                transaction.Start()

                loaded_family = doc.LoadFamily(temp_path)

                transaction.Commit()

                # Delete the temporary family file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

                return loaded_family
            except Exception as ex:
                transaction.RollBack()
                TaskDialog.Show("Error", "Failed to create loadable generic family: " + str(ex))
                return None
        else:
            TaskDialog.Show("Error", "Failed to create family document.")
            return None
    except Exception as ex:
        TaskDialog.Show("Error", "Failed to create loadable generic family: " + str(ex))
        return None


def main():
    # Show a warning dialog and prompt the user to select a model-in-place family
    task_dialog = TaskDialog("Select Model-in-Place Family")
    task_dialog.MainContent = "Please select a model-in-place family instance."
    task_dialog.CommonButtons = TaskDialogCommonButtons.Ok | TaskDialogCommonButtons.Cancel

    result = task_dialog.Show()
    if result == TaskDialogResult.Ok:
        element = select_model_in_place_family()
        if element and element.Category.Name == "Generic Models" and element.StructuralType == StructuralType.NonStructural:
            template_path = r"C:\Users\ibanezl3110\AppData\Roaming\CustomRevitExtension\ArchProductivity.extension\CustomControl.tab\Modeling.panel\Convert In-Place.pushbutton\Generic Model.rft"
            loaded_family = create_loadable_generic_family(template_path)
            if loaded_family:
                TaskDialog.Show("Success", "Loadable generic family created and loaded successfully.")
        else:
            TaskDialog.Show("Error",
                            "No valid model-in-place family selected or selected element is not a generic model in-place.")
    else:
        TaskDialog.Show("Info", "Operation cancelled by user.")


if __name__ == '__main__':
    main()
