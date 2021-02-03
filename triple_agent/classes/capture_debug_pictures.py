import os
import hashlib
from pathlib import Path

import numpy as np
import cv2


def capture_debug_picture(output_path: Path, picture: np.ndarray, filename: str = None):
    os.makedirs(output_path, exist_ok=True)
    if filename is None:
        cv2.imwrite(
            # cv2 does not accept Path objects yet: https://github.com/opencv/opencv/issues/15731
            str(
                output_path.joinpath(
                    hashlib.md5(picture.tobytes()).hexdigest() + ".png"
                ).resolve()
            ),
            picture,
        )
    else:
        cv2.imwrite(
            str(output_path.joinpath(filename + ".png").resolve()),
            picture,
        )
