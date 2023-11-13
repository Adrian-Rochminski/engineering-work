import environment_data_load

environment_data = {}


def set_environment():
    global environment_data
    environment_data = environment_data_load.read_conf()
