import os
import cv2


def capture_debug_picture(picture, output_path):
    os.makedirs(output_path, exist_ok=True)
    cv2.imwrite(
        os.path.join(output_path, str(hash(str(picture))) + ".png"), picture,
    )
