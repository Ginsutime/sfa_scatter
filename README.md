sfa_scatter
-------------
**Name:** Brett Austin  
  **Directory Structure:** `sfa_scatter/src/scatter.py` contains the entirety of the code sample\
  **Explanation of Code Sample:**
  - A) Allows user to launch the scatter tool from a custom button on the Maya tool shelf
  - B) GUI is implemented with PySide2 and is called from the shelf icon once the button is clicked
  - C) Allows user to select an object to scatter with and a destination to scatter to
  - D) When the scatter button on the tool is clicked, it scatters the object onto selected vertices by:
      - Creating an instance or instances of the object being scattered
      - Moving the instance(s) to vertices on the scatter destination object
  - E) Ability to scatter object onto vertices of an object if only the object is selected instead of specific vertices
  - F) Ability to specify XYZ rotation minimums and maximums with built in ranges limiting responses to between 0 and 360
  - G) Ability to specify XYZ scale minimums and maximums with built in ranges limiting responses between 0.1 and 10
  - H) Ability to specify a percentage of selected target object vertices to scatter onto
  - I) Allows user to scatter objects that align to the normals of the target surface by enabling an option checkbox
  - J) Allows user to specify position offset that dictates how much to embed scattered objects under the target surface
  - K) Allows user to press reset button in order to return all fields to their defaults
  - L) Will log a warning message to the user and do nothing else if:
      - Object being scattered or scatter destination object fields are empty
      - Select button on object being scattered or scatter destination object is clicked with no objects selected in scene
      - Minimum values of XYZ rotation or scale are higher than the maximum values
      - Percentage of selected target object vertices to scatter onto is set to 0, meaning none would be scattered\
      
**Date When Code Was Written:**\
First Commit: April 4, 2021\
Final Commit: April 29, 2021
