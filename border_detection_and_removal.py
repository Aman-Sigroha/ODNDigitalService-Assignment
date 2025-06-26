import os
import csv
from PIL import Image
import numpy as np
import cv2

def is_similar(pixel1, pixel2, color_thresh=25):
    """Checks if two pixels are similar based on Euclidean distance in RGB."""
    dist = np.linalg.norm(np.array(pixel1) - np.array(pixel2))
    return dist < color_thresh

def adaptive_border_scan(image, color_thresh=25, line_consistency=0.9):
    """
    Scans inward from each edge, comparing pixels to the corner color.
    Stops when a line is no longer consistent with the corner color.
    """
    arr = np.array(image.convert('RGB'))
    h, w, _ = arr.shape

    # Sample corner colors
    top_left_corner = arr[0, 0]
    top_right_corner = arr[0, w-1]
    bottom_left_corner = arr[h-1, 0]

    # --- Top Border ---
    top = 0
    for i in range(h):
        consistent_pixels = sum(1 for pixel in arr[i, :] if is_similar(pixel, top_left_corner, color_thresh))
        if consistent_pixels / w < line_consistency:
            break
        top += 1

    # --- Bottom Border ---
    bottom = 0
    for i in range(h - 1, -1, -1):
        consistent_pixels = sum(1 for pixel in arr[i, :] if is_similar(pixel, bottom_left_corner, color_thresh))
        if consistent_pixels / w < line_consistency:
            break
        bottom += 1

    # --- Left Border ---
    left = 0
    for i in range(w):
        consistent_pixels = sum(1 for pixel in arr[:, i] if is_similar(pixel, top_left_corner, color_thresh))
        if consistent_pixels / h < line_consistency:
            break
        left += 1

    # --- Right Border ---
    right = 0
    for i in range(w - 1, -1, -1):
        consistent_pixels = sum(1 for pixel in arr[:, i] if is_similar(pixel, top_right_corner, color_thresh))
        if consistent_pixels / h < line_consistency:
            break
        right += 1

    # Prevent over-cropping if the whole image is one color
    if top + bottom >= h: top, bottom = 0, 0
    if left + right >= w: left, right = 0, 0
        
    cropped = arr[top:h-bottom, left:w-right]
    return left, top, w - left - right, h - top - bottom, cropped

def main():
    input_dir = 'input'
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    images = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Found {len(images)} images in '{input_dir}': {images}")
    
    csv_rows = []
    for img_name in images:
        img_path = os.path.join(input_dir, img_name)
        try:
            print(f"Processing {img_name}... (Adaptive border scan)")
            image = Image.open(img_path)
            
            x, y, w, h, cropped = adaptive_border_scan(image)
            
            # Ensure the cropped image is not empty
            if cropped.shape[0] > 0 and cropped.shape[1] > 0:
                cropped_path = os.path.join(output_dir, img_name)
                cv2.imwrite(cropped_path, cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR))
                print(f"Saved cropped image to {cropped_path}")
            else:
                print(f"Skipped saving empty crop for {img_name}")

            img_h_orig, img_w_orig, _ = cv2.imread(img_path).shape
            top_border = y
            left_border = x
            bottom_border = img_h_orig - (y + h)
            right_border = img_w_orig - (x + w)

            sides = []
            if top_border > 0: sides.append('top')
            if bottom_border > 0: sides.append('bottom')
            if left_border > 0: sides.append('left')
            if right_border > 0: sides.append('right')

            csv_rows.append({
                'filename': img_name,
                'border_top': top_border,
                'border_bottom': bottom_border,
                'border_left': left_border,
                'border_right': right_border,
                'sides_with_border': ','.join(sides)
            })
        except Exception as e:
            print(f"Error processing {img_name}: {e}")
            
    if csv_rows:
        try:
            with open('border_report.csv', 'w', newline='') as csvfile:
                fieldnames = ['filename', 'border_top', 'border_bottom', 'border_left', 'border_right', 'sides_with_border']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_rows)
            print("CSV report 'border_report.csv' generated.")
        except Exception as e:
            print(f"Error writing CSV report: {e}")
    else:
        print("No images processed, CSV report not generated.")

if __name__ == '__main__':
    main()
