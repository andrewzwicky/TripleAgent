import os
import hashlib

import cv2


def capture_debug_picture(output_path, picture, filename=None):
    os.makedirs(output_path, exist_ok=True)
    if filename is None:
        cv2.imwrite(
            os.path.join(
                output_path, hashlib.md5(picture.tobytes()).hexdigest() + ".png"
            ),
            picture,
        )
    else:
        cv2.imwrite(
            os.path.join(output_path, filename + ".png"),
            picture,
        )
