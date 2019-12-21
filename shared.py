from multiprocessing import Value, sharedctypes, RawArray
import numpy as np
import ctypes
import time
from stimulus_module import StimulusModule
import pickle

class Shared():
    def __init__(self):
        self.window_properties_x = Value('i', 0)
        self.window_properties_y = Value('i', 0)
        self.window_properties_width = Value('i', 800)
        self.window_properties_height = Value('i', 800)
        self.window_properties_update_requested = Value('b', 0)

        self.stimulus_properties_number_of_dots = Value('i', 1000)
        self.stimulus_properties_size_of_dots = Value('d', 0.1)
        self.stimulus_properties_speed_of_dots = Value('d', 0.3)
        self.stimulus_properties_direction_of_dots = Value('d', 0.0)
        self.stimulus_properties_coherence_of_dots = Value('d', 50)
        self.stimulus_properties_lifetime_of_dots = Value('d', 0.2)
        self.stimulus_properties_update_requested = Value('b', 0)

        self.running = Value('b', 1)

    def load_values(self):
        try:
            values = pickle.load(open("values.pickle", "rb"))
            self.window_properties_x.value = values["window_properties_x"]
            self.window_properties_y.value = values["window_properties_y"]
            self.window_properties_width.value = values["window_properties_width"]
            self.window_properties_height.value = values["window_properties_height"]

            self.stimulus_properties_number_of_dots.value = values["stimulus_properties_number_of_dots"]
            self.stimulus_properties_size_of_dots.value = values["stimulus_properties_size_of_dots"]
            self.stimulus_properties_speed_of_dots.value = values["stimulus_properties_speed_of_dots"]
            self.stimulus_properties_direction_of_dots.value = values["stimulus_properties_direction_of_dots"]
            self.stimulus_properties_coherence_of_dots.value = values["stimulus_properties_coherence_of_dots"]
            self.stimulus_properties_lifetime_of_dots.value = values["stimulus_properties_lifetime_of_dots"]

        except Exception as e:
            print(e)

    def save_values(self):

        try:
            values = dict({})

            values["window_properties_x"] = self.window_properties_x.value
            values["window_properties_y"] = self.window_properties_y.value
            values["window_properties_width"] = self.window_properties_width.value
            values["window_properties_height"] = self.window_properties_height.value

            values["stimulus_properties_number_of_dots"] = self.stimulus_properties_number_of_dots.value
            values["stimulus_properties_size_of_dots"] = self.stimulus_properties_size_of_dots.value
            values["stimulus_properties_speed_of_dots"] = self.stimulus_properties_speed_of_dots.value
            values["stimulus_properties_coherence_of_dots"] = self.stimulus_properties_coherence_of_dots.value
            values["stimulus_properties_direction_of_dots"] = self.stimulus_properties_direction_of_dots.value
            values["stimulus_properties_lifetime_of_dots"] = self.stimulus_properties_lifetime_of_dots.value

            pickle.dump(values, open("values.pickle", "wb"))
        except Exception as e:
            print(e)

    def start_threads(self):
        StimulusModule(self).start()
