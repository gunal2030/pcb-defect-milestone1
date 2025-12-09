import cv2
import numpy as np


def read_images(template_path, test_path):
    """Read template and test images from disk."""
    template = cv2.imread(template_path)
    test = cv2.imread(test_path)

    if template is None:
        raise FileNotFoundError(f"Template image not found: {template_path}")
    if test is None:
        raise FileNotFoundError(f"Test image not found: {test_path}")

    return template, test


def to_gray_and_align(template, test):
    """Convert to grayscale and resize test image to match template size."""
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    test_gray = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)

    th, tw = template_gray.shape
    test_gray_resized = cv2.resize(test_gray, (tw, th))

    return template_gray, test_gray_resized


def compute_difference(template_gray, test_gray_resized):
    """Pixel-wise absolute difference between template and test."""
    diff = cv2.absdiff(template_gray, test_gray_resized)
    return diff


def threshold_otsu(diff):
    """Apply Otsu thresholding to get a binary mask of defects."""
    _, mask = cv2.threshold(
        diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return mask
