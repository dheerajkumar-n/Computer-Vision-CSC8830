import numpy as np
import cv2
import glob

# --- CONFIGURATION ---
# Number of INTERNAL corners (Count: Squares minus 1)
# Looking at your images, it's 8 corners wide and 6 corners tall
CHECKERBOARD = (8, 6) 
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane

# Path to your new images
images = glob.glob('calibration_images/*.jpeg') # Ensure extension matches your files

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    if ret == True:
        objpoints.append(objp)
        # Refining pixel coordinates for better accuracy
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        print(f"✅ Checkerboard found in {fname}")
    else:
        print(f"❌ Could not find board in {fname}. Check lighting/corners.")

# Actual Calibration
if len(objpoints) > 0:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    print("\n--- YOUR INTRINSIC MATRIX (K) ---")
    print(mtx)
    
    # Save these for Step 2
    np.savez("camera_params.npz", mtx=mtx, dist=dist)
    print("\nCalibration successful! Parameters saved to camera_params.npz")
else:
    print("Error: No boards were detected in any images.")