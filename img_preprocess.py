import cv2
import numpy as np
import os

def preprocess_cropped_images(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    def binarize(image):
        _, binarized_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binarized_image

    def remove_noise(image):
        return cv2.fastNlMeansDenoising(image, None, 30, 7, 21)

    def adjust_brightness_contrast(image, brightness=0, contrast=0):
        image = image.astype(np.int32)
        image = np.clip(image * (1 + contrast / 127) - contrast + brightness, 0, 255)
        return image.astype(np.uint8)

    def sharpen(image):
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        return cv2.filter2D(image, -1, kernel)

    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_dir, filename)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            # Apply preprocessing steps
            image = binarize(image)
            image = remove_noise(image)
            image = adjust_brightness_contrast(image, brightness=30, contrast=30)
            image = sharpen(image)

            # Save the preprocessed image
            output_path = os.path.join(output_dir, filename)
            cv2.imwrite(output_path, image)
            print(f"Processed and saved: {output_path}")

# Example usage
input_cropped_columns_dir = 'cropped_columns'
output_preprocessed_dir = 'preprocessed_cropped_columns'
preprocess_cropped_images(input_cropped_columns_dir, output_preprocessed_dir)
