import json

# actors = world.get_actors()
# data = []

# for actor in actors:
#     transform = actor.get_transform()
#     blueprint = actor.type_id
#     data.append({
#         "type_id": blueprint,
#         "location": {
#             "x": transform.location.x,
#             "y": transform.location.y,
#             "z": transform.location.z
#         },
#         "rotation": {
#             "pitch": transform.rotation.pitch,
#             "yaw": transform.rotation.yaw,
#             "roll": transform.rotation.roll
#         }
#     })

with open("setup.json", "w") as f:
    json.dump(data, f, indent=4)

with open("setup.json", "r") as f:
    data = json.load(f)

blueprint_library = world.get_blueprint_library()

for actor_data in data:
    bp = blueprint_library.find(actor_data["type_id"])
    transform = carla.Transform(
        carla.Location(**actor_data["location"]),
        carla.Rotation(**actor_data["rotation"])
    )
    world.spawn_actor(bp, transform)

with open("weather.json", "r") as f:
    weather_data = json.load(f)

weather = world.get_weather()
weather.cloudiness = weather_data["cloudiness"]
weather.precipitation = weather_data["precipitation"]
weather.wind_intensity = weather_data["wind_intensity"]
world.set_weather(weather)
