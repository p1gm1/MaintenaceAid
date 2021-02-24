# utils
import os

# OCR
import easyocr

#Model Thermophoto
from thermoapp.reports.models import ThermoPhoto

# Machine learning
from thermoapp.reports.ml import *


def temp_and_ocr(thermo_photo):
    """Validate content of thermo photo"""

    thermo = thermo_photo.picture.url 
    temp = []
    image_ids = os.listdir(thermo)
    res = calculate_temp_bbox(thermo) 
    for j in range(len(image_ids)):
        image_id = image_ids[j].split('.')[0]
        for i in range(len(res)):
            probe_img = cv2.imread(f'{thermo}/{image_id}.jpg')
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
    thermo_photo.RTMean = ((max(temp) - min(temp)) / 2)
    thermo_photo.is_valid = True
    thermo_photo.save()
    
