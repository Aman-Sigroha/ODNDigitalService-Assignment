# ODN Digital Service - Border Detection and Removal

This project automatically detects and removes borders from images in the `input/` directory, saving the cropped results to the `output/` directory. It works robustly for borders of any color (white, off-white, gray, etc.) using an adaptive corner-color scanning method.

## Features
- Detects and removes borders/frames from images.
- Preserves the background and main content.
- Generates a CSV report (`border_report.csv`) with border sizes for each image.
- Works for images with white, off-white, gray, or colored borders.

## Setup Instructions

1. **Clone or download the repository.**
2. **Ensure you have Python 3.7+ installed.**
3. **Create and activate a virtual environment (recommended):**
   ```sh
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
4. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
5. **Place your images in the `input/` directory.**

## Usage Instructions

1. **Run the script:**
   ```sh
   python border_detection_and_removal.py
   ```
2. **Results:**
   - Cropped images will be saved in the `output/` directory with the same filenames.
   - A CSV report (`border_report.csv`) will be generated in the project root, detailing the border sizes detected and removed for each image.

## Parameters
- You can adjust the sensitivity of border detection by editing the `color_thresh` and `line_consistency` parameters in the script if needed.

## Notes
- The script is fully automatic and does not require manual cropping or annotation.
- Works best for images where the border color is consistent along each edge.

---

If you have any questions or need further customization, feel free to ask!