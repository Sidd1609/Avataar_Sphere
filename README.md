# Avataar: 3D Spheres Rendering Application

## Overview

This repository contains the codebase for a simple application in OpenGL written in Python. The following features are available in this application.

### Completed Deliverables
**Sphere Rendering Application:**
1. **Initial Setup:**
    - [✅] Create a windowed application that renders 36 spheres in a 6x6 grid-like pattern.
2. **Shading:**
    - [✅]  Applied a shading model to the spheres.
    - [✅] Used an orthographic camera for consistent visibility.

3. **Parameter Variation:**
    - [✅] Choose diffuse and spectral parameters of the shading model and change these parameters linearly over the two axes (left to right, and top to bottom).

4. **Interactive Color Change:**
    - [✅] Register mouse-click events that trigger a color change of the clicked sphere to the normal color at that point colorized.

5. **Deselection and Exit:**
    - [✅] Register mouse-click to deselect the previous change on the sphere and return to normal when a click event occurs outside any sphere.
    - [✅] Trigger application exit by pressing the ESC key.
  
## Getting Started
### Prerequisites
- Python==3.8.18
- pygame==2.5.2
- pyopengl==3.1.6
- pyopengl-accelerate==3.1.7
- glfw==2.6.4

### Installation

**Clone the Repository:**
   ```bash
   git clone https://github.com/Sidd1609/Avataar_Sphere.git
   cd Avataar_Sphere

   #Install the requirements
   pip install -r requirements.txt

   #Execute the Windowed Application by running the script
   python3 6Spheres_main.py
   ```

## Result

<p align="center">
  <img src="Main_Result.gif" alt="Your GIF" width="600" height="600">
</p>

<!--![Result GIF](Main_Result.gif)-->

## Contributors
- Sri Siddarth Chakaravarthy

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


