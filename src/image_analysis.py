import cv2
import numpy as np
import pandas as pd
from skimage.measure import label, regionprops
from skimage.segmentation import watershed
from skimage.feature import peak_local_max

def analyze_image(image_path, min_seed_area, max_seed_area, save_binary_image=False):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise Exception(f"无法读取图像: {image_path}")

    _, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    distance = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    local_max = peak_local_max(distance, min_distance=50, labels=thresh, exclude_border=False)

    markers = np.zeros_like(image, dtype=np.int32)
    for idx, (r, c) in enumerate(local_max, 1):
        markers[r, c] = idx

    labels_ws = watershed(-distance, markers, mask=thresh)
    traits = extract_traits(image, labels_ws, min_seed_area, max_seed_area)

    if save_binary_image:
        cv2.imwrite(f"{image_path}_binary.jpg", thresh)
    
    return traits

def extract_traits(image, labels_ws, min_seed_area, max_seed_area):
    traits = []
    for i, r in enumerate(regionprops(labels_ws), 1):
        if r.area < min_seed_area or r.area > max_seed_area:
            continue
        # 特征提取逻辑...
        # 将提取的特征添加到 traits 列表中
    return traits