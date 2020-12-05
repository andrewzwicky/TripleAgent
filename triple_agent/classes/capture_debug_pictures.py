import os
import cv2


def capture_debug_picture(picture, output_path, filename=None):
    os.makedirs(output_path, exist_ok=True)

    if filename is None:
        cv2.imwrite(
            os.path.join(output_path, str(hash(str(picture))) + ".png"),
            picture,
        )
    else:
        cv2.imwrite(
            os.path.join(output_path, filename + ".png"),
            picture,
        )
