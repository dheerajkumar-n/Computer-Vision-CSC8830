import cv2
import os

# --- CHANGE THIS TO YOUR ACTUAL FILENAME ---
# Make sure to include .jpg or .png correctly!
image_name = "validateobject.jpeg"
if not os.path.exists(image_name):
    print(f"❌ Error: The file '{image_name}' was not found in this folder.")
    print("Available files:", os.listdir("."))
    exit()

img = cv2.imread(image_name)
points = []

def get_pixels(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(img, (x, y), 8, (0, 255, 0), -1)
        cv2.imshow("Pixel Selector", img)
        
        if len(points) == 2:
            width_px = abs(points[1][0] - points[0][0])
            height_px = abs(points[1][1] - points[0][1])
            print(f"\n✅ PIXEL DATA CAPTURED")
            print(f"Point 1 (Top-Left): {points[0]}")
            print(f"Point 2 (Bottom-Right): {points[1]}")
            print(f"Width: {width_px} pixels")
            print(f"Height: {height_px} pixels")
            print("\nYou can now close this window and copy these numbers to Part 3.")

cv2.imshow("Pixel Selector", img)
cv2.setMouseCallback("Pixel Selector", get_pixels)
print("INSTRUCTIONS: Click the top-left corner, then the bottom-right corner of your object.")
cv2.waitKey(0)
cv2.destroyAllWindows()