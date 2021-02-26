# utils
import os

# OCR
import easyocr

# Utils
from pathlib import Path

# Settings
from django.conf import settings

# Machine learning
from thermoapp.reports.ml import *


def temp_and_ocr(thermo_photo):
    """Validate content of thermo photo"""

    thermo = settings.MEDIA_ROOT + str(Path(thermo_photo.thermo_picture.url[6:]).parent)
    temp = []
    
    res = calculate_temp_bbox(thermo) 
    
    for i in range(len(res)):
        probe_img = cv2.imread(settings.MEDIA_ROOT + str(Path(thermo_photo.thermo_picture.url[6:])))
        probe_img = probe_img[res[i]['y1']:res[i]['y2'],
                                  res[i]['x1']:res[i]['x2']]

        reader = easyocr.Reader(['th','en'])
        bounds = reader.readtext(probe_img)

        try:
            temp.append(float(bounds[0][1]))
        except:
            return

    thermo_photo.RTMax = max(temp)
    thermo_photo.RTMin = min(temp)
    thermo_photo.RTMean = ((max(temp) + min(temp)) / 2)
    thermo_photo.is_valid = True
    thermo_photo.save()
    
