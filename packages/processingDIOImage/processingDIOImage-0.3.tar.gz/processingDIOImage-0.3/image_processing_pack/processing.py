from locale import normalize
import re
import numpy as np
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from skimage.metrics import structural_similarity
from skimage.transform import resize


def find_differencer(image1, image2):
    assert image1.shape == image2.shape, "Specify 2 images with de same shape"
    gray_image1 = rgb2gray(image1)
    gray_image2 = rgb2gray(image2)
    (score, difference_image) = structural_similarity(
        gray_image1, gray_image2, full=True)
    print("Similarity of the images:", score)
    normalize_difference_image = (difference_image.np.min(
        difference_image))/(np.max(difference_image)-np.min(difference_image))
    return normalize_difference_image


def transfer_histogram(image1, image2):
    matched_image = match_histograms(image1, image2, multichannel=True)
    return matched_image


def resize_image(image, proportion):
    assert 0 <= proportion <= 1, "Specify a valid proportion between 0 and 1."
    height = round(image.shape[0] * proportion)
    width = round(image.shape[1] * proportion)
    image_resized = resize(image, (height, width), anti_aliasing=True)
    return image_resized
