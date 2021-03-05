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