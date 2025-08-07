import cv2
import numpy as np
import pandas as pd
from skimage.measure import regionprops
from skimage.segmentation import watershed
import os

def analyze_image(image_path, out_dir, base_name, min_area, max_area, max_length, save_binary):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    distance = cv2.distanceTransform(opened, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(distance, 0.0165 * distance.max(), 255, cv2.THRESH_BINARY)
    sure_fg = np.uint8(sure_fg)
    sure_bg = cv2.dilate(opened, kernel, iterations=2)
    unknown = cv2.subtract(sure_bg, sure_fg)
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    labels = watershed(-distance, markers, mask=thresh)
    vis = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    traits = []
    count = 0
    for r in regionprops(labels):
        if r.area < min_area or r.area > max_area or r.major_axis_length > max_length:
            continue
        count += 1
        coords = r.coords
        xy = coords[:, [1, 0]].astype(np.float32)
        mean = np.mean(xy, axis=0)
        centered = xy - mean
        _, vecs = np.linalg.eigh(np.cov(centered.T))
        main, perp = vecs[:, 1], vecs[:, 0]
        proj_main = centered @ main
        proj_perp = centered @ perp
        length = np.ptp(proj_main)
        width = np.ptp(proj_perp)
        angle = np.degrees(np.arctan2(main[1], main[0]))
        start = (mean + main * np.min(proj_main)).astype(int)
        end = (mean + main * np.max(proj_main)).astype(int)
        w1 = (mean - perp * width / 2).astype(int)
        w2 = (mean + perp * width / 2).astype(int)
        center = mean.astype(int)

        cv2.line(vis, tuple(start), tuple(end), (0, 0, 255), 2)
        cv2.line(vis, tuple(w1), tuple(w2), (255, 0, 0), 2)
        cv2.circle(vis, tuple(center), 3, (0, 255, 0), -1)
        cv2.putText(vis, str(count), (center[0] + 5, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

        traits.append({
            "ID": count,
            "Length_px": round(length, 2),
            "Width_px": round(width, 2),
            "L/W": round(length / width if width > 0 else 0, 3),
            "Angle_deg": round(angle, 2),
            "Centroid_X": center[0],
            "Centroid_Y": center[1],
            "Area_px": r.area,
            "Perimeter_px": round(r.perimeter, 2)
        })


    pd.DataFrame(traits).to_csv(os.path.join(out_dir, f"{base_name}_traits.csv"), index=False)
    cv2.imwrite(os.path.join(out_dir, f"{base_name}_vis.jpg"), vis)
    if save_binary:
        cv2.imwrite(os.path.join(out_dir, f"{base_name}_sure_fg.jpg"), sure_fg)
    return traits, count
