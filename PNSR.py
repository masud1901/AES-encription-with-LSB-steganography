import math
import numpy as np
from scipy import signal
import cv2


class Compare:
    def correlation(self, img1, img2):
        return signal.correlate2d(img1, img2)

    def meanSquareError(self, img1, img2):
        error = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
        error /= float(img1.shape[0] * img1.shape[1])
        return error

    def psnr(self, img1, img2):
        mse = self.meanSquareError(img1, img2)
        if mse == 0:
            return 100
        PIXEL_MAX = 255.0
        return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

    def addPadd(self, img, row, col):
        img = cv2.resize(img, (col + (8 - col % 8), row + (8 - row % 8)))
        return img


def main():
    a = Compare()

    # Read the original and the stego images
    img1_path = "./Images/Apple.png"
    img2_path = "./output/encrypted.png"

    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    # Ensure images are read properly
    if img1 is None or img2 is None:
        print("Error: One or both image paths are incorrect.")
        return

    # Get the dimensions of the images
    row1, col1 = img1.shape[:2]
    row2, col2 = img2.shape[:2]

    # Add padding to both images to make their dimensions compatible for comparison
    img1 = a.addPadd(img1, row1, col1)
    img2 = a.addPadd(img2, row2, col2)

    # Calculate PSNR
    psnr_value = a.psnr(img1, img2)
    print(f"PSNR value: {psnr_value}")


if __name__ == "__main__":
    main()
