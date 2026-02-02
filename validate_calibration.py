"""
CSC 8830- Computer Vision
Author: Dheeraj Kumar Narsani

Description:
    This script calculates the real-world dimensions of an object using 
    perspective projection equations. It includes a validation step to 
    calculate percentage error against a known ground truth.

Dependencies:
    opencv-python (pip install opencv-python)
    numpy (pip install numpy)
"""

import cv2
import math
import numpy as np
import os

# --- Global Variables ---
points = []
image = None
clone = None
window_name = "Dimension Calculator"

def click_event(event, x, y, flags, param):
    """
    Mouse callback function to capture point clicks.
    """
    global points, image, clone
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) >= 2:
            # Reset if already have 2 points
            points = []
            image = clone.copy()
            cv2.imshow(window_name, image)

        points.append((x, y))
        
        # Visual feedback: Draw a circle where clicked
        cv2.circle(image, (x, y), 5, (0, 0, 255), -1)
        
        if len(points) == 2:
            # Draw a line between the two points
            cv2.line(image, points[0], points[1], (0, 255, 0), 2)
            dist_px = math.sqrt((points[0][0] - points[1][0])**2 + (points[0][1] - points[1][1])**2)
            print(f"\n[INFO] Points selected: {points}")
            print(f"[INFO] Pixel Distance (w): {dist_px:.2f} pixels")
            process_measurement(dist_px)
            
        cv2.imshow(window_name, image)

def process_measurement(pixel_width):
    """
    Handles the logic for Calibration vs Measurement based on user input.
    """
    print("\n--- ACTION MENU ---")
    print("1. Calibrate (Calculate Focal Length)")
    print("2. Measure (Calculate Real Dimension)")
    print("Press any other key to cancel/re-select.")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == '1':
        try:
            real_width = float(input("Enter REAL width of the object (e.g., cm, in): "))
            distance = float(input("Enter DISTANCE from camera to object (same units as width): "))
            
            # Formula: f = (w * D) / W
            focal_length = (pixel_width * distance) / real_width
            print(f"\n[RESULT] Calculated Focal Length (f): {focal_length:.2f} pixels")
            print("KEEP THIS VALUE SAFE for measuring other objects at known distances!")
        except ValueError:
            print("[ERROR] Invalid numeric input.")
            
    elif choice == '2':
        try:
            focal_length = float(input("Enter known Focal Length (pixels): "))
            distance = float(input("Enter DISTANCE from camera to object: "))
            
            # Formula: W = (w * D) / f
            calculated_dim = (pixel_width * distance) / focal_length
            
            print(f"\n[RESULT] CALCULATED DIMENSION: {calculated_dim:.4f} units")
            
            # --- NEW: Validation Block ---
            validate = input("Do you know the ACTUAL dimension for validation? (y/n): ").lower()
            if validate == 'y':
                try:
                    actual_dim = float(input("Enter ACTUAL dimension: "))
                    
                    # Calculate Percentage Error
                    error = abs((calculated_dim - actual_dim) / actual_dim) * 100
                    
                    print(f"[VALIDATION] Actual: {actual_dim:.4f}")
                    print(f"[VALIDATION] Calculated: {calculated_dim:.4f}")
                    print(f"[VALIDATION] Percentage Error: {error:.2f}%")
                    
                    # Add error text to the image display
                    cv2.putText(image, f"Err: {error:.2f}%", 
                               (points[0][0], points[0][1] + 20), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    
                except ValueError:
                    print("[ERROR] Invalid input for actual dimension.")
            # -----------------------------
            
            # Draw result on image
            cv2.putText(image, f"{calculated_dim:.2f} units", 
                       (points[0][0], points[0][1] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow(window_name, image)
            
        except ValueError:
            print("[ERROR] Invalid numeric input.")
    else:
        print("[INFO] Action cancelled. Click new points to retry.")

def main():
    global image, clone
    
    print("=== Dimension Calculator Started ===")
    
    # 1. Load Image
    img_path = input("Enter image filename/path (e.g., test.jpg): ").strip()
    
    if not os.path.exists(img_path):
        print(f"[ERROR] File '{img_path}' not found.")
        return

    original_image = cv2.imread(img_path)
    if original_image is None:
        print("[ERROR] Could not decode image.")
        return

    # Resize for display if image is too massive
    height, width = original_image.shape[:2]
    max_height = 800
    if height > max_height:
        scale = max_height / height
        image = cv2.resize(original_image, (int(width * scale), int(height * scale)))
    else:
        image = original_image.copy()

    clone = image.copy()

    # 2. Setup Window and Mouse Callback
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, click_event)

    print("\n[INSTRUCTIONS]")
    print("- Click TWO points on the image to define the object width.")
    print("- Check the console for inputs after clicking.")
    print("- Press 'r' to clear lines.")
    print("- Press 'q' to exit.")

    while True:
        cv2.imshow(window_name, image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            image = clone.copy()
            global points
            points = []
            print("[INFO] Reset.")
        elif key == ord("q"):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()