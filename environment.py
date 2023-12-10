import json

import environment_data_load


class EnvironmentSimulator:
    def __init__(self):
        self.average_temp = 20
        self.temp_loss_gain_in_night_day_circle = 10
        self.day_night_circle_ticks_ratio = 100
        self.energy_usage_factor = 1.0
        self.current_tick = 0
        self.light_intensity = 0
        self.water_in_field = 0
        self.nutrients_in_field = 0
        self.current_temp = self.average_temp

    def load_from_json(self):
        data = environment_data_load.read_conf()
        self.average_temp = data['average_temp']
        self.temp_loss_gain_in_night_day_circle = data['temp_loss_gain_in_night_day_circle']
        self.day_night_circle_ticks_ratio = data['day_night_circle_ticks_ratio']
        self.light_intensity = data['light_intensity']
        self.water_in_field = data['water_in_field']
        self.nutrients_in_field = data['nutrients_in_field']

    def is_daytime(self):
        return self.current_tick % (2 * self.day_night_circle_ticks_ratio) < self.day_night_circle_ticks_ratio

    def actual_temperature(self):
        if self.is_daytime():
            return self.current_temp + self.temp_loss_gain_in_night_day_circle / self.day_night_circle_ticks_ratio
        else:
            return self.current_temp - self.temp_loss_gain_in_night_day_circle / self.day_night_circle_ticks_ratio

    def energy_consumption(self, mass, temperature):
        if temperature > self.average_temp:
            return mass * temperature * self.energy_usage_factor
        else:
            return mass / temperature * self.energy_usage_factor

    def update_tick(self):
        self.current_tick += 1

    def environment_change(self):
        self.update_tick()
        temp = self.actual_temperature()
        self.current_temp = temp
        # self.energy_consumption()
        return temp
