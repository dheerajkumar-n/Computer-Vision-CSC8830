# Values taken directly from your successful calibration screenshot
fx = 1160.39054
fy = 1161.54557

def get_real_size(px, dist_mm, focal):
    # Real Size = (Pixel Length * Z) / Focal Length
    return (px * dist_mm) / focal

# --- YOUR DATA FROM THE LATEST SCREENSHOT ---
distance_z = 2000    #  measured distance in mm 
width_pixels = 5     # From your latest redo
height_pixels = 115  # From your latest redo

# Final Calculations
calc_width_mm = get_real_size(width_pixels, distance_z, fx)
calc_height_mm = get_real_size(height_pixels, distance_z, fy)

print(f"--- ASSIGNMENT VALIDATION RESULTS ---")
print(f"Distance to Object: {distance_z} mm")
print(f"Calculated Real Width: {calc_width_mm:.2f} mm")
print(f"Calculated Real Height: {calc_height_mm:.2f} mm ({calc_height_mm/10:.2f} cm)")