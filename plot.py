import multiprocessing
import time
from TecData import TecData
from FileData import FileData
from NurgushBinData import NurgushBinData
import matplotlib.pyplot as plt
import json


class Configuration:
    def __init__(self, config_name):
        json_data_file = open('plot.json')
        self.json = json.load(json_data_file)
        json_data_file.close()

    def get_or_else(self, section, option, or_else):
        try:
            return self.get(section, option)
        except:
            return or_else
            return or_else

    def getboolean_or_else(self, section, option, or_else):
        try:
            return self.json[section][option]
        except:
            return or_else

    def get(self, section, option):
        val = self.json[section][option]
        return val


class PlotItem(dict):
    def __init__(self, initial_file, **kwargs):
        super(PlotItem, self).__init__(**kwargs)
        self['contour'] = self.contour
        self['roche_lobe'] = self.roche_lobe
        self['velocity_filed'] = self.plot_velocity_filed
        self['slice_y'] = self.plot_slice_y
        self['plot_magnetic'] = self.plot_magnetic

    def contour(self, _data, axes, _item_config):
        _data.plot_contour(axes, _item_config)

    def roche_lobe(self, _data, axes, _item_config):
        _data.plot_roche_lobe(axes, _item_config)

    def plot_velocity_filed(self, _data, axes, _item_config):
        _data.plot_velocity_filed(axes, _item_config)

    def plot_slice_y(self, _data, axes, _item_config):
        _data.slice_y(axes, _item_config, initial_file)

    def plot_magnetic(self, _data, axes, _item_config):
        _data.plot_magnetic(axes, _item_config)


config = Configuration("plot.json")

folder = config.get_or_else("data", "folder", "")
pattern = config.get_or_else("data", "pattern", "*")


def get_target_dir():
    target_from_config = str(config.get_or_else("data", "target", "target"))
    if target_from_config.startswith("/"):
        return target_from_config
    else:
        return folder + target_from_config


is_create_target = config.getboolean_or_else("data", "create_target_dir", True)

target = get_target_dir()

if is_create_target:
    import os

    if not os.path.exists(target):
        print "Create directories."
        os.makedirs(target)

data_type = config.get_or_else("data", "data_type", "tec")


def read_data(filename):
    print "read data"
    return {
        "tec": lambda name: TecData(name),
        "idl": lambda name: FileData(name),
        "nurgushbin": lambda name: NurgushBinData(name)
    }.get(data_type)(filename)


import glob

files = glob.glob(folder + pattern)

total_files = int(files.__len__())

initial_index = config.get_or_else("data", "initial_index", None)

initial_file = None

if initial_index is not None and 0 <= initial_index < files.__len__():
    initial_file_name = files.pop(initial_index)
    print "Build initial file....."
    initial_file = read_data(initial_file_name)
    total_files = int(files.__len__())

start_from = int(config.get_or_else("data", "start", 0))

if start_from < 0 or start_from > total_files:
    start_from = 0

take = int(config.get_or_else("data", "take", total_files - start_from))

if take < 0 or take > total_files - start_from:
    take = 0

files = files[start_from: start_from + take]

total_files = int(files.__len__())

exact_name = config.get_or_else("data", "exact_name", None)

if exact_name is not None:
    files = [folder + str(exact_name)]
    total_files = 1

plot_items = PlotItem(initial_file)


def process_figures(file_index):
    _file = files[file_index]
    print "Progress  (" + "{0:.2f}".format(file_index / float(total_files) * 100.0) + "%) " + str(_file)

    figures = config.json['figures']

    for figure in figures:
        _is_skip_figure = figure['skip']
        if not _is_skip_figure:
            _data = read_data(_file)
            items_on_figure = figure['items']
            is_save_figure = figure['save']
            fig, ax = plt.subplots()
            fig.suptitle(str(figure['title']) + str(_data.sub_title()))
            fig.set_size_inches(15.5, 14.5)
            for item in items_on_figure:
                print item
                item_config = config.json['types'][item]
                plot_items[item](_data, ax, item_config)
            if is_save_figure:
                plt.savefig(target + figure['out_name'] + _data.get_name() + ".png")
            else:
                plt.show()
            plt.close(fig)


nodes = config.json['execution']['nodes']

process_figures(0)
# pool = multiprocessing.Pool(nodes)
# try:
#     pool.map(process_figures, range(0, total_files))
# finally:
#     pool.close()
