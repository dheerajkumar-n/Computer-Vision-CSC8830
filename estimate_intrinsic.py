import cv2
import numpy as np
import glob
import os
import sys

print("\n==============================")
print(" CAMERA CALIBRATION (FINAL) ")
print("==============================\n")

# -------------------------------------------------
# CONFIGURATION — MATCHES YOUR CHECKERBOARD
# -------------------------------------------------

# Inner corners visible in your photos:
# (count squares and subtract 1)
CHECKERBOARD = (7, 7)      # columns, rows
SQUARE_SIZE_MM = 25        # physical size (used for scale)
IMAGE_DIR = "board_photos"
MIN_VIEWS = 6

# -------------------------------------------------
# LOAD IMAGES
# -------------------------------------------------

image_files = sorted(glob.glob(os.path.join(IMAGE_DIR, "*.jpeg")))

if len(image_files) == 0:
    print("❌ No calibration images found.")
    print("Expected images in:", IMAGE_DIR)
    sys.exit(1)

print(f"Found {len(image_files)} images.\n")

# -------------------------------------------------
# PREPARE WORLD POINTS
# -------------------------------------------------

objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[
    0:CHECKERBOARD[0],
    0:CHECKERBOARD[1]
].T.reshape(-1, 2)

objp *= SQUARE_SIZE_MM

objpoints = []  # 3D points
imgpoints = []  # 2D points

# -------------------------------------------------
# DETECT CORNERS (SCREEN-FRIENDLY METHOD)
# -------------------------------------------------

print("Detecting checkerboard corners...\n")

for fname in image_files:
    img = cv2.imread(fname)
    if img is None:
        print(f"[SKIP] Cannot read {fname}")
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # IMPORTANT: SB method works best for iPad / screen boards
    found, corners = cv2.findChessboardCornersSB(
        gray,
        CHECKERBOARD,
        cv2.CALIB_CB_NORMALIZE_IMAGE
    )

    if not found:
        print(f"[FAIL] No corners detected: {os.path.basename(fname)}")
        continue

    objpoints.append(objp)
    imgpoints.append(corners)

    print(f"[OK] Corners detected: {os.path.basename(fname)}")

# -------------------------------------------------
# VALIDATION CHECK
# -------------------------------------------------

valid_views = len(objpoints)

print("\n==============================")
print(" CALIBRATION SUMMARY ")
print("==============================")
print(f"Total images     : {len(image_files)}")
print(f"Valid detections : {valid_views}")

if valid_views < MIN_VIEWS:
    print("\n❌ Calibration aborted.")
    print("Reason: insufficient valid checkerboard views.")
    print("Fix: capture more tilted images or reduce glare.")
    sys.exit(1)

# -------------------------------------------------
# RUN CAMERA CALIBRATION
# -------------------------------------------------

print("\nRunning camera calibration...\n")

ret, camera_matrix, distortion, rvecs, tvecs = cv2.calibrateCamera(
    objpoints,
    imgpoints,
    gray.shape[::-1],
    None,
    None
)

# -------------------------------------------------
# SAVE RESULTS
# -------------------------------------------------

os.makedirs("outputs", exist_ok=True)
np.savez(
    "outputs/intrinsics.npz",
    K=camera_matrix,
    distortion=distortion
)

# -------------------------------------------------
# FINAL OUTPUT
# -------------------------------------------------

print("CALIBRATION SUCCESSFUL\n")
print("Camera Intrinsic Matrix (K):")
print(camera_matrix)

print("\nDistortion Coefficients:")
print(distortion.ravel())

print("\nFocal length (pixels):", round(camera_matrix[0, 0], 2))
print("\nSaved to: outputs/intrinsics.npz")

print("\n==============================")
print(" DONE ")
print("==============================\n")