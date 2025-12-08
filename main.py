import os
import cv2
import logging
from Models.AI_models import CCTVSystem

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Paths
    testing_images_dir = 'data/testing_images'
    output_images_dir = 'data/output_images'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_images_dir, exist_ok=True)
    
    # Initialize System
    system = CCTVSystem()
    
    # Process Images
    if not os.path.exists(testing_images_dir):
        logger.error(f"Testing images directory not found: {testing_images_dir}")
        return

    images = [f for f in os.listdir(testing_images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not images:
        logger.warning("No images found in testing directory.")
        return

    logger.info(f"Found {len(images)} images to process.")

    for image_name in images:
        image_path = os.path.join(testing_images_dir, image_name)
        logger.info(f"Processing {image_name}...")
        
        frame = cv2.imread(image_path)
        if frame is None:
            logger.error(f"Failed to read image: {image_path}")
            continue
            
        # Process the frame
        processed_frame = system.process_frame(frame)
        
        # Save result
        output_path = os.path.join(output_images_dir, f"processed_{image_name}")
        cv2.imwrite(output_path, processed_frame)
        logger.info(f"Saved processed image to {output_path}")

    logger.info("Processing complete.")

if __name__ == "__main__":
    main()
