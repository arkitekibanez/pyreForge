__title__ = "BG Sepia"
__doc__ = """Version: 1.1
Date: 05.04.2024
_____________________________________________________________________
Description:
Change Revit background color to Sepia.
_____________________________________________________________________
How-to:
- Just click on the button to change the background color.
_____________________________________________________________________
Last update:
- [05.04.2024] - 1.1 RELEASE
_____________________________________________________________________
Author: Luis Ibanez
Note: TO edit the script, hold shoft and click"""

from Autodesk.Revit.DB import Color
from Autodesk.Revit.UI import TaskDialog

# Initialize current_color_index
current_color_index = 0


# Function to convert RGB to sepia tone
def rgb_to_sepia(rgb):
    r, g, b = rgb
    sepia_r = min(255, int((r * 0.393) + (g * 0.769) + (b * 0.189)))
    sepia_g = min(255, int((r * 0.349) + (g * 0.686) + (b * 0.168)))
    sepia_b = min(255, int((r * 0.272) + (g * 0.534) + (b * 0.131)))
    return Color(sepia_r, sepia_g, sepia_b)


# Function to convert RGB to dark gray
def rgb_to_dark_gray(rgb):
    return Color(25, 24, 24)  # Dark gray color


# Function to convert RGB to white
def rgb_to_white(rgb):
    return Color(255, 255, 255)  # White color


# Main function
def main():
    global current_color_index

    # List of colors: sepia, dark gray, white
    colors = [rgb_to_sepia((220, 193, 167)), rgb_to_dark_gray((220, 193, 167)), rgb_to_white((220, 193, 167))]

    # Get the current color
    current_color = colors[current_color_index]

    # Set the background color to the next color in the list
    __revit__.Application.BackgroundColor = current_color

    # Update the current color index for the next iteration
    current_color_index = (current_color_index + 1) % len(colors)


# Run the main function
if __name__ == '__main__':
    main()

# Show a smaller pop-up dialogue box when successful
task_dialog = TaskDialog("Success")
task_dialog.MainContent = "Background has been changed to sepia!"
task_dialog.Show()
