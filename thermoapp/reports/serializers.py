# django rest
from rest_framework import serializers

# utils
import os
from pathlib import Path

# OCR
import easyocr

# Machine learning
from thermoapp.reports.ml import *

class ReportSerializer(serializers.Serializer):
    """Create report form class."""

    def validate(self, data):
        """Validate content of thermo photo"""

        ROOT_DIR = str(Path(__file__).resolve(strict=True).parent.parent)

        thermo = ROOT_DIR+'/media/thermo_photo/' # Valor desde base de datos, url de foto termica

        temp = [0.0,0.0] # Valor hardcodeado, en la practica debe tomarse de la base de datos, lista con los valores máx y mín del modelo reporte 
        temp_idx = sum(temp)/len(temp) # Promedio de temperaturas, si da cero tiene los valores default
        
        if temp_idx == 0.0:
            image_ids = os.listdir(thermo)
            res = calculate_temp_bbox(thermo) # Determina los valores de temperatura en la foto, importación de ml.py
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
                        print('The located temperature is: '+bounds[0][1]) # Cambia los valores de temp mín y temp máx en el modelo, se debe cambiar por el print.
                    except:
                        raise serializers.ValidationError('Thermo photo was taken incorrectly')
            
            data['temp']=temp

        else:
            data['temp']=temp

        return data
            
            

        
        
