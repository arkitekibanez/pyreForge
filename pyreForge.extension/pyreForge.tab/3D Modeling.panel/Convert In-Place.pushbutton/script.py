# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
import clr
import os

# Add reference to System.Windows.Forms
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import OpenFileDialog, DialogResult

uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document

__title__ = "Convert\nIn-Place"
__doc__ = """Version=1.0
Date=05.04.2024
__________________________________________________________________
Description:
Work in Progress, current script creates a duplicate of the selected
in-place family.
__________________________________________________________________
How-to:
-> Follow the step-by-step dialog.
__________________________________________________________________
Last update:
-[05.04.2024]-v1.0.5 Debugging Transaction Rollback.
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


def browse_for_template():
    dialog = OpenFileDialog()
    dialog.Filter = "Revit Family Templates (*.rft)|*.rft"
    dialog.Title = "Select the Family Template"
    if dialog.ShowDialog() == DialogResult.OK:
        return dialog.FileName
    return None


def create_loadable_generic_family(template_path):
    try:
        # Check if the template file exists
        if not os.path.exists(template_path):
            TaskDialog.Show("Error", "Template file does not exist: " + template_path)
            return None
        else:
            TaskDialog.Show("Debug", "Template Path: " + template_path)

        # Create a new family document from the selected template
        app = __revit__.Application
        family_doc = app.NewFamilyDocument(template_path)
        if family_doc:
            TaskDialog.Show("Debug", "Family document created successfully.")  # Debug check
            transaction = Transaction(family_doc, "Create Loadable Generic Family")
            transaction.Start()

            try:
                # Attempting very basic geometry to isolate issue
                TaskDialog.Show("Debug", "Attempting simple reference plane creation.")  # Debug check
                # Create a simple reference plane (instead of extrusion)
                ref_plane = family_doc.FamilyCreate.NewReferencePlane(XYZ.Zero, XYZ.BasisX, XYZ.BasisY,
                                                                      family_doc.ActiveView)

                TaskDialog.Show("Debug", "Reference Plane created.")  # Debug check

                # Commit the transaction
                transaction.Commit()

                # Save the family document to a temporary location
                temp_path = os.path.join(os.getenv('TEMP'), 'TemporaryFamily.rfa')
                family_doc.SaveAs(temp_path)
                family_doc.Close(False)

                # Load the family into the current project
                transaction = Transaction(doc, "Load Family")
                transaction.Start()

                loaded_family = doc.LoadFamily(temp_path)

                transaction.Commit()

                # Delete the temporary family file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

                return loaded_family
            except Exception as ex:
                TaskDialog.Show("Error", "Failed to create loadable generic family: " + str(ex))
                transaction.RollBack()  # Rollback the transaction if it fails
                return None
        else:
            TaskDialog.Show("Error", "Failed to create family document.")
            return None
    except Exception as ex:
        TaskDialog.Show("Error", "Failed to create loadable generic family: " + str(ex))
        return None


def main():
    try:
        # Step 1: Select Model-In-Place Family
        TaskDialog.Show("Step 1", "Please select a model-in-place family instance.")
        element = select_model_in_place_family()
        if not element:
            return  # Cancelled by user

        # Step 2: Select Template
        TaskDialog.Show("Step 2", "Select the template file for the new loadable family.")
        template_path = browse_for_template()
        if not template_path:
            TaskDialog.Show("Cancelled", "No template selected. Operation cancelled.")
            return

        # Step 3: Validate Category
        if element.Category.Name != "Generic Models":
            TaskDialog.Show("Error", "Selected element is not a generic model-in-place family.")
            return

        # Step 4: Create and Load Family
        loaded_family = create_loadable_generic_family(template_path)
        if loaded_family:
            TaskDialog.Show("Success", "Loadable generic family created and loaded successfully.")
        else:
            TaskDialog.Show("Error", "Failed to create or load the loadable family.")
    except Exception as ex:
        TaskDialog.Show("Critical Error", "Unexpected error occurred: " + str(ex))


if __name__ == '__main__':
    main()
