import carla
from typing import Tuple, List, Dict
import time 
import math 

# init the car's parameters such as torque and stuff if needed
def init_car(car: carla.Vehicle) -> None:
    
    # Create Wheels Physics Control
    front_left_wheel  = carla.WheelPhysicsControl(tire_friction=2.0, damping_rate=1.5, max_steer_angle=70.0, long_stiff_value=1000)
    front_right_wheel = carla.WheelPhysicsControl(tire_friction=2.0, damping_rate=1.5, max_steer_angle=70.0, long_stiff_value=1000)
    rear_left_wheel   = carla.WheelPhysicsControl(tire_friction=3.0, damping_rate=1.5, max_steer_angle=0.0,  long_stiff_value=1000)
    rear_right_wheel  = carla.WheelPhysicsControl(tire_friction=3.0, damping_rate=1.5, max_steer_angle=0.0,  long_stiff_value=1000)

    wheels = [front_left_wheel, front_right_wheel, rear_left_wheel, rear_right_wheel]

    # Change Vehicle Physics Control parameters of the vehicle
    physics_control = car.get_physics_control()

    physics_control.torque_curve = [carla.Vector2D(x=0, y=400), carla.Vector2D(x=1300, y=600)]
    physics_control.max_rpm = 10000
    physics_control.moi = 1.0
    physics_control.damping_rate_full_throttle = 0.0
    physics_control.use_gear_autobox = True
    physics_control.gear_switch_time = 0.5
    physics_control.clutch_strength = 10
    physics_control.mass = 10000
    physics_control.drag_coefficient = 0.25
    physics_control.steering_curve = [carla.Vector2D(x=0, y=1), carla.Vector2D(x=100, y=1), carla.Vector2D(x=300, y=1)]
    physics_control.use_sweep_wheel_collision = True
    physics_control.wheels = wheels

    # Apply Vehicle Physics Control for the vehicle
    car.apply_physics_control(physics_control)
    print(physics_control)

# def get_A_star_parameters(car: carla.Vehicle) -> Dict[str, float]:

#     physics_control = car.get_physics_control()
#     vehicle_transform = car.get_transform()
#     vehicle_bbox = car.bounding_box

#     # Get the position (center of the bounding box)
#     vehicle_location = vehicle_transform.location
#     wheels = physics_control.wheels
#     wheel_FL = wheels[0]
#     wheel_FR = wheels[1]
#     wheels_RL = wheels[2]
#     wheels_RR = wheels[3]
#     length = vehicle_bbox.extent.x * 2
#     width = vehicle_bbox.extent.y * 2
#     height = vehicle_bbox.extent.z * 2

#     vehicle_location = vehicle_transform.location

#     # Get the vehicle's forward direction (unit vector along the vehicle's front)
#     vehicle_forward = vehicle_transform.get_forward_vector()

#     # To get the front position (by moving the vehicle's location in the forward direction)
#     # You can scale the forward vector by a certain distance (e.g., half of the vehicle's length or the wheelbase)
#     distance_to_front = vehicle_bbox.extent.x  # Distance from the center to the front (half of vehicle length)
#     front_location = vehicle_location + vehicle_forward * distance_to_front
#     rear_location = vehicle_location - vehicle_forward * distance_to_front


#     # Dimensions of the bounding box (length, width, height)


#     RF = front_location.distance(wheel_FL)  # distance from rear to vehicle front end of vehicle

#     # 2. Distance from the rear to the back end of the vehicle (length of the vehicle from the rear to the back)
#     RB = rear_location.distance()  # Bounding box length (front-to-rear)

#     # 3. Distance between the left and right wheels (left-right distance)
#     left_right_distance = wheel_FL_position.distance(wheel_FR_position)

#     # 4. Wheelbase (distance between front and rear axles)
#     wheelbase = wheel_FL_position.distance(wheel_RL_position)

#     # Extracting the parameters
# RF = sy - length / 2 -  wheels_RL.position.y / 100
#     # 
    # RF = 3.655  # [m] distance from rear to vehicle front end of vehicle
    # RB = 0.8577  # [m] distance from rear to vehicle back end of vehicle
    # W = width  # [m] width of vehicle
#     WD = 1.529 * W  # [m] distance between left-right wheels
#     WB = 2.8191  # [m] Wheel base
#     # Assuming all tires have the same width and radius... duh
#     TR = physics_control.wheels[0].radius  # [m] Tyre radius
#     TW = 0.2  # [m] Tyre width
#     MAX_STEER = 0.6  # [rad] maximum steering angle

def stop_car(car: carla.Vehicle) -> None:
    control = car.get_control()
    control.throttle = 0
    control.brake = 1  
    control.steer = 0  
    control.hand_brake = True
    car.apply_control(control)

# move car forward or backward
def move_car(car: carla.Vehicle, reverse: bool = False, steer : float = 0, speed: float = 1.0) -> None:
    control = car.get_control()
    control.hand_brake = False
    control.throttle = speed  
    control.reverse = reverse  
    control.brake = 0        
    control.steer = steer        
    car.apply_control(control)

# Turn the car (left or right)
def turn_car(car: carla.Vehicle, direction: str, intensity: float = 1.0) -> None:
    control = car.get_control()
    if direction == 'left':
        control.steer = -intensity  # Turn left
    elif direction == 'right':
        control.steer = intensity  # Turn right
    car.apply_control(control)

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
def follow_path(car: carla.Vehicle, path: list, offset_x : float = 0, offset_y: float = 0, tolerance: float = 0.5, tolerance_angle: float = 0.1):
    """
    Moves the car along a series of waypoints (path).
    
    :param car: The car object.
    :param path: List of (x, y) waypoints the car needs to follow.
    :param offset_x: The amount of offset in the x direction
    :param offset_y: The amount of offset in the y direction
    :param tolerance: Distance tolerance to consider the car has reached the waypoint.
    """
    # first teleport the vehicle to the starting point 
    """
    In carla 
    North = 2pi 
    East = pi
    South = -pi
    West = pi
    """
    transform = carla.Transform(
        carla.Location(x=path.x[0] - offset_x, y=path.y[0] - offset_y, z=1),
        carla.Rotation(yaw=path.yaw[0] - 90)
    )
    car.set_transform(transform)
    time.sleep(1)

    prev_yaw = None
    for idx in range(len(path.x)):
        x, y, yaw, dir = path.x[idx] - offset_x, path.y[idx] - offset_y, path.yaw[idx], path.direction[idx]
        dir = False if dir == 1 else True 
        # -3.141592653589793 = north -> -1 
        # -pi/2 = east 
        # 0 = south 
        
        yaw += math.pi / 2
        # yaw *= -1 # carla's yaw angle is reversed 
        yaw /= math.pi / 2  # carla expect angles to be in [-1, 1]
        
        # current_yaw = math.radians(car.get_transform().rotation.yaw)
        # if idx < len(path.yaw) - 1 and -current_yaw == path.yaw[idx + 1]:
        #     steer_intensity = 0
        # else:
        #     steer_intensity = yaw
        print(f"Moving towards waypoint {idx+1}: ({x}, {y}, {yaw})")
        # move_car(car, dir, steer_intensity, 0.2)
        
        # Move the car towards the waypoint
        while True:
            # Get car's current position
            current_transform = car.get_transform()
            car_x, car_y = current_transform.location.x, current_transform.location.y
            current_yaw = math.radians(current_transform.rotation.yaw)

            # car_y += 0.4 # adjust for car's length
            # Calculate distance to the waypoint
            distance_to_target = distance((car_x, car_y), (x, y)) 
            
            desired_yaw = math.atan2(y - car_y, x - car_x)
            # Compute the yaw error and normalize it between -pi and pi
            yaw_error = desired_yaw - current_yaw
            yaw_error = math.atan2(math.sin(yaw_error), math.cos(yaw_error))
            
            # Use a simple proportional controller for the steering intensity
            if abs(yaw_error) < tolerance_angle:
                steer_intensity = 0  # reset steering when aligned
            else:
                gain = 1.0  # tune this gain for smoother turning
                steer_intensity = max(min(gain * yaw_error, 1), -1)

            move_car(car, dir, steer=steer_intensity, speed=0.4)

            if distance_to_target < tolerance:
                print(f"Arrived at waypoint {idx+1}")
                stop_car(car)
                break  # Break the loop once we reach the waypoint
            
            time.sleep(0.05)
    # Once all waypoints are completed, stop the car
    stop_car(car)
    print("Car has reached the destination.")
