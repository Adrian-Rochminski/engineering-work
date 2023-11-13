import json

env_file = "environment.json"


def read_conf():
    with open(env_file, 'r') as f:
        config = json.load(f)
    return config
