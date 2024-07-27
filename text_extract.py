from paddleocr import PaddleOCR
import os
import cv2
from openpyxl import Workbook

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Directory containing the cropped column images
input_dir = 'cropped_columns'

# List to store extracted text from all images
all_extracted_text = []

# Iterate through all images in the input directory
for filename in sorted(os.listdir(input_dir)):
    if filename.endswith(('.png', '.jpg', '.jpeg')):  # Add more extensions if needed
        image_path = os.path.join(input_dir, filename)
        
        # Read the image
        img = cv2.imread(image_path)
        
        # Perform OCR
        result = ocr.ocr(img, cls=True)
        
        # Extract text from the result
        extracted_text = []
        for line in result:
            for word_info in line:
                extracted_text.append(word_info[1][0])  # Append the recognized text
        
        # Join all extracted text for this image
        full_text = '\n'.join(extracted_text)
        
        # Add the extracted text to the list
        all_extracted_text.append(full_text)
        
        print(f"Processed {filename}")

# Create a new workbook and select the active sheet
workbook = Workbook()
sheet = workbook.active

# Write the extracted text to the Excel file
for col_num, text in enumerate(all_extracted_text, 1):
    col_letter = sheet.cell(row=1, column=col_num).column_letter
    sheet[f"{col_letter}1"] = f"Column {col_num}"
    
    # Split the text by newlines and write each line to a separate cell
    for row_num, line in enumerate(text.split('\n'), 2):
        sheet.cell(row=row_num, column=col_num, value=line)

# Save the workbook
excel_filename = 'extracted_text.xlsx'
workbook.save(excel_filename)

print(f"Extracted text from {len(all_extracted_text)} images")
print(f"Extracted text has been saved to '{excel_filename}'")
