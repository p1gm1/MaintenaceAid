# Models
from thermoapp.reports.models import Component

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