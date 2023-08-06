import os, sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.normpath(os.path.join(current_path, './')))
sys.path.append(os.path.normpath(os.path.join(current_path, 'protobuf')))

import time
import random
from protobuf.morai_simulation_pb2 import WEATHER_TYPE_RAINY
import protobuf.morai_actor_pb2
import protobuf.morai_type_pb2

DEFAULT_MORAI_SIM_ADDR = '127.0.0.1'
DEFAULT_MORAI_SIM_PORT = 7789
DEFAULT_VEHICLE_MODEL_NAME = '2016_Hyundai_Ioniq'


def spawn_vehicle(adapter, transform, velocity, vehicle_model_name, pause):
    spawn_actor_params = protobuf.morai_actor_pb2.SpawnActorParams()

    param = protobuf.morai_actor_pb2.SpawnActorParam()
    param.actor_info.actor_id = '-1'
    param.actor_info.actor_type = protobuf.morai_actor_pb2.ACTOR_TYPE_VEHICLE
    param.transform.CopyFrom(transform)
    param.vehicle.velocity = velocity
    param.vehicle.vehicle_model_name = vehicle_model_name
    param.vehicle.pause = pause

    spawn_actor_params.params.append(param)
    actor_responses = adapter.spawn_actor(spawn_actor_params)

    param.actor_info.actor_id = extract_actor_id(actor_responses)    
    return param.actor_info


def spawn_pedestrian(adapter, transform, velocity, active_dist, move_dist, pedestrian_name, start_action):
    spawn_actor_params = protobuf.morai_actor_pb2.SpawnActorParams()

    param = protobuf.morai_actor_pb2.SpawnActorParam()
    param.actor_info.actor_id = '-1'
    param.actor_info.actor_type = protobuf.morai_actor_pb2.ACTOR_TYPE_PEDESTRIAN
    param.transform.CopyFrom(transform)    
    param.pedestrian.velocity = velocity
    param.pedestrian.active_dist = active_dist
    param.pedestrian.move_dist = move_dist
    param.pedestrian.pedestrian_name = pedestrian_name
    param.pedestrian.start_action = start_action

    spawn_actor_params.params.append(param)
    actor_responses = adapter.spawn_actor(spawn_actor_params)
    
    param.actor_info.actor_id = extract_actor_id(actor_responses)    
    return param.actor_info


def spawn_obstacle(adapter, transform, scale = None, obstacle_name = 'WoodBox'):
    spawn_actor_params = protobuf.morai_actor_pb2.SpawnActorParams()

    param = protobuf.morai_actor_pb2.SpawnActorParam()        
    param.actor_info.actor_id = '-1'
    param.actor_info.actor_type = protobuf.morai_actor_pb2.ACTOR_TYPE_OBSTACLE
    param.transform.CopyFrom(transform)
    
    if scale is None:
        scale = protobuf.morai_type_pb2.Vector3()
        scale.x = 1
        scale.y = 1
        scale.z = 1
    param.obstacle.obstacle_name = obstacle_name
    param.obstacle.scale.CopyFrom(scale)

    spawn_actor_params.params.append(param)
    actor_responses = adapter.spawn_actor(spawn_actor_params)
    
    param.actor_info.actor_id = extract_actor_id(actor_responses)    
    return param.actor_info


def extract_actor_id(actor_responses):
    actor_id = ''
    if actor_responses == None or actor_responses.values[0].result == False:
        print('spawn actor error')
    else:
        actor_id = actor_responses.values[0].display_name
    
    return actor_id


def spawn_actors(adapter):
    actors = []
    transform = protobuf.morai_type_pb2.Transform()
    transform.location.x = 5
    transform.rotation.z = 0
    actors.append(spawn_vehicle(adapter, transform, 10, DEFAULT_VEHICLE_MODEL_NAME, False))

    transform.location.x += 5
    transform.rotation.z = 5
    actors.append(spawn_vehicle(adapter, transform, 20, DEFAULT_VEHICLE_MODEL_NAME, False))

    transform.location.x += 5
    actors.append(spawn_pedestrian(adapter, transform, 10, 10, 20, 'Man1', True))

    transform.location.x += 4
    actors.append(spawn_obstacle(adapter, transform))
    
    return actors

adapter = None

def example_main():
    global adapter

    # Create adapter
    adapter = SimAdapter()

    # Connect
    adapter.connect(DEFAULT_MORAI_SIM_ADDR, DEFAULT_MORAI_SIM_PORT)

    # Initialize
    adapter.initialize()

    # API Test    
    simulator_version = adapter.get_simulator_version()
    print(f'sim version {simulator_version}')

    available_maps = adapter.get_available_maps()
    print(f'available maps : {available_maps}')

    map_name = available_maps[random.randrange(0, len(available_maps)-1)]
    print(f'load world : {map_name}, {DEFAULT_VEHICLE_MODEL_NAME}')
    try:
        adapter.load_world(map_name, DEFAULT_VEHICLE_MODEL_NAME)
    except BaseException as e:
        pass
    
    mgeo_data = adapter.get_mgeo(map_name)
    adapter.start_actor_state_receiver(print_actor_states)

    data_path = adapter.get_data_path()
    print(f'data path : {data_path}')

    actors = spawn_actors(adapter)

    time.sleep(100)

    adapter.destroy_all_actors()

    # Disconnect
    adapter.disconnect()

def print_actor_states():    
    global adapter

    actor_states = adapter.get_actor_states()
    for actor_state in actor_states.states:
        print(actor_state)
        print('-------------------------------------')


if __name__ == '__main__':
    example_main()
