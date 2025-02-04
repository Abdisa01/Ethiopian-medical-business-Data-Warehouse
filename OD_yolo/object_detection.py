import os
import logging
import torch
import pandas as pd
import cv2
from sqlalchemy import create_engine
from ultralytics import YOLO

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load YOLO model
yolo_model = YOLO('yolov5s.pt')
logging.info("YOLO model loaded.")

# Define image directory
image_dir = 'photos/'
output_csv = 'detection_results.csv'

# Ensure output directory exists
if not os.path.exists(image_dir):
    logging.error("Image directory not found.")
    exit()

# Process images
detections = []
for img_name in os.listdir(image_dir):
    img_path = os.path.join(image_dir, img_name)
    image = cv2.imread(img_path)
    
    if image is None:
        logging.warning(f"Could not read image: {img_name}")
        continue
    
    results = yolo_model(img_path)
    for result in results:
        for box in result.boxes:
            detections.append([
                img_name, 
                int(box.xyxy[0][0]), int(box.xyxy[0][1]), int(box.xyxy[0][2]), int(box.xyxy[0][3]), 
                float(box.conf[0]), int(box.cls[0])
            ])

# Save results to CSV
columns = ['Image', 'X_min', 'Y_min', 'X_max', 'Y_max', 'Confidence', 'Class']
df = pd.DataFrame(detections, columns=columns)
df.to_csv(output_csv, index=False)
logging.info("Detection results saved to CSV.")

# Store in PostgreSQL
db_url = 'postgresql://username:password@localhost:5432/medical_db'
engine = create_engine(db_url)
df.to_sql('object_detections', engine, if_exists='replace', index=False)
logging.info("Detection results stored in PostgreSQL.")

print("Object detection completed successfully!")
