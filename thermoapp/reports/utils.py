# Models
from thermoapp.reports.models import Component

# Pyxl
from openpyxl import load_workbook

def excel_to_dict(path_to_file):
    """Handles data to excel
    from database.
    """
    excel_file=load_workbook(path_to_file)
    worksheet=excel_file['Sheet1']

    mp_arr = []
    i=0

    for row in worksheet.iter_rows():
        if i != 0:
            for j in range(len(row)):
                if j == 0:
                    monitoring_point=row[j].value
                elif j == 1:
                    velocity=row[j].value
                elif j == 2:
                    aceleration=row[j].value
                elif j == 3:
                    dem_odulada=row[j].value
                
            mp_arr.append({"monitoring_point": monitoring_point,
                           "velocity": velocity,
                           "aceleration": aceleration,
                           "dem_odulada": dem_odulada})
        else:
            i += 1
    
    return mp_arr

class VibrationsPoints():
    def __init__(self, component, monitoring_point, created, vel_prev, vel_last, ace_prev, ace_last, dem_prev, dem_last):
        self.component = component
        self.monitoring_point = monitoring_point
        self.created = created
        self.vel_prev = vel_prev 
        self.vel_last = vel_last
        self.ace_prev = ace_prev
        self.ace_last = ace_last
        self.dem_prev = dem_prev
        self.dem_last = dem_last
        self.outliers = []
        self.flag = False

    def find_outliers(self):
        """Find ouliers values
        on data.

        Args: 
        vel_last: last velocity read on db.
        ace_last: last acelaration read on db.
        dem_last: last demod frequency read on
        db.
        Return:
        A list with outliers value and its 
        monitoring points.
        """

        component = Component.objects.get(component=self.component)

        if component.vel_max < self.vel_last:
            self.outliers.append({'velocity': self.vel_last})
            self.flag = True
        
        if component.ace_max < self.ace_last:
            self.outliers.append({'acelaration': self.ace_last})
            self.flag = True

        if component.v_max < self.dem_last:
            self.outliers.append({'demod': self.dem_last})
            self.flag = True