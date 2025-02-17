import carla

def draw_line(world, start_coords, end_coords, color=carla.Color(255, 0, 0), thickness=0.5):
    """
    Draws a line in the CARLA world between two points.

    :param world: The CARLA world object
    :param start_coords: A tuple (x, y, z) for the start point of the line
    :param end_coords: A tuple (x, y, z) for the end point of the line
    :param color: The color of the line, default is red (255, 0, 0)
    :param thickness: The thickness of the line, default is 0.5
    """
    # Convert the coordinates into carla.Vector3D
    start = carla.Vector3D(*start_coords)
    end = carla.Vector3D(*end_coords)

    # Draw the line
    world.debug.draw_line(start, end, color=color, thickness=thickness)


# Example usage
if __name__ == "__main__":
    # Connect to CARLA and get the world
    client = carla.Client('localhost', 2000)
    world = client.get_world()

    # Define start and end coordinates (x, y, z)
    start_coords = (0, 0, 0)
    end_coords = (10, 10, 0)

    # Call the helper function to draw the line
    draw_line(world, start_coords, end_coords)