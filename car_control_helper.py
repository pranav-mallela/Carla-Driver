import carla

# TODO: init the car's parameters such as torque and stuff 
def init_car(car: carla.Vehicle) -> None :
    pass 

def stop_car(car: carla.Vehicle) -> None:
    control = car.get_control()
    control.throttle = 0
    control.brake = 1  
    control.steer = 0  
    car.apply_control(control)

# move car forward or backward
def move_car(car: carla.Vehicle, reverse: bool = False, steer : float = 0, speed: float = 1.0) -> None:
    control = car.get_control()
    control.throttle = speed  
    control.reverse = reverse  
    control.brake = 0        
    control.steer = steer        
    car.apply_control(control)

