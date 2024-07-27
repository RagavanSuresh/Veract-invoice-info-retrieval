from ultralytics import YOLO
import cv2
import numpy as np
import os

# Load the YOLOv8 model
model = YOLO('best.pt')

# Load an image
image_path = 'WhatsApp Image 2024-07-12 at 17.30.22(2).jpeg'
image = cv2.imread(image_path)

# Perform detection
results = model(image)

# Create a directory to save cropped images
output_dir = 'cropped_columns'
os.makedirs(output_dir, exist_ok=True)

# Crop and save detected columns
column_count = 0
for result in results:
    boxes = result.boxes.xyxy.cpu().numpy()  # Bounding boxes
    class_ids = result.boxes.cls.cpu().numpy()  # Class IDs
    
    print(f"Total detections: {len(boxes)}")
    
    for box, class_id in zip(boxes, class_ids):
        # Invert the class_id interpretation
        class_name = 'column' if class_id == 0 else 'Invoice-table'
        print(f"Detected class: {class_name}")
        
        if class_name == 'column':
            x_min, y_min, x_max, y_max = map(int, box)
            
            # Crop the column
            cropped_column = image[y_min:y_max, x_min:x_max]
            
            # Save the cropped column
            column_count += 1
            output_path = os.path.join(output_dir, f'column_{column_count}.jpg')
            cv2.imwrite(output_path, cropped_column)
            print(f"Saved column {column_count} with dimensions {cropped_column.shape}")

print(f"Saved {column_count} cropped columns in the '{output_dir}' directory.")

# Visualize all detections
for result in results:
    boxes = result.boxes.xyxy.cpu().numpy()
    class_ids = result.boxes.cls.cpu().numpy()
    for box, class_id in zip(boxes, class_ids):
        # Invert the class_id interpretation
        class_name = 'column' if class_id == 0 else 'Invoice-table'
        color = (0, 255, 0) if class_name == 'column' else (0, 0, 255)
        x_min, y_min, x_max, y_max = map(int, box)
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
        cv2.putText(image, class_name, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

cv2.imwrite('all_detections.jpg', image)
print("Saved visualization of all detections as 'all_detections.jpg'")
