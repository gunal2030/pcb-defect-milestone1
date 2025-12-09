import os
import cv2

from src.processing import (
    read_images,
    to_gray_and_align,
    compute_difference,
    threshold_otsu,
)


def run_missing_hole_demo():
    """Simple demo for one PCB pair (Missing Hole example)."""
    os.makedirs("img", exist_ok=True)

    template_path = "img/Missing_hole_Demonstration_1_Template.jpg"
    test_path = "img/Missing_hole_Demonstration_2_Test.jpg"

    template, test = read_images(template_path, test_path)

    template_gray, test_gray_resized = to_gray_and_align(template, test)
    diff = compute_difference(template_gray, test_gray_resized)
    mask = threshold_otsu(diff)

    cv2.imwrite("img/template_gray.png", template_gray)
    cv2.imwrite("img/test_gray_resized.png", test_gray_resized)
    cv2.imwrite("img/diff_map.png", diff)
    cv2.imwrite("img/binary_mask.png", mask)


if __name__ == "__main__":
    run_missing_hole_demo()
