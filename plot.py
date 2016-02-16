from TecData import TecData
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

    def getboolean_or_else(self, section, option, or_else):
        try:
            return self.json[section][option]
        except:
            return or_else

    def get(self, section, option):
        val = self.json[section][option]
        return val


class PlotItem(dict):
    def __init__(self, config, **kwargs):
        super(PlotItem, self).__init__(**kwargs)
        self['contour'] = self.contour
        self['roche_lobe'] = self.roche_lobe

    def contour(self, _data, axes, _item_config):
        _data.plot_contour(axes, _item_config)

    def roche_lobe(self, _data, axes, _item_config):
        _data.plot_roche_lobe(axes, _item_config)


config = Configuration("plot.json")

folder = config.get_or_else("data", "folder", "")
pattern = config.get_or_else("data", "pattern", "*")
target = folder + config.get_or_else("data", "target", "target")

is_create_target = config.getboolean_or_else("data", "create_target_dir", True)

if is_create_target:
    import os

    if not os.path.exists(target):
        os.makedirs(target)

import glob

files = glob.glob(folder + pattern)

total_files = int(files.__len__())

start_from = int(config.get_or_else("data", "start", 0))

if start_from < 0 or start_from > total_files:
    start_from = 0

till_to = int(config.get_or_else("data", "end", total_files))

if till_to < 0 or till_to < start_from or till_to > total_files:
    till_to = total_files

files = files[start_from: till_to]

plot_items = PlotItem(config)


def process_figures(file_index):
    _file = files[file_index]
    _data = TecData(_file)

    figures = config.json['figures']

    for figure in figures:
        items_on_figure = figure['items']
        is_save_figure = figure['save']
        fig, ax = plt.subplots()
        fig.suptitle(str(figure['title']) + str(_data.sub_title()))
        for item in items_on_figure:
            item_config = config.json['types'][item]
            plot_items[item](_data, ax, item_config)
        if is_save_figure:
            plt.savefig(target + figure['out_name'] + _data.get_name() + ".png")
        else:
            plt.show()
        plt.close(fig)


nodes = config.json['execution']['nodes']

import multiprocessing

pool = multiprocessing.Pool(nodes)
try:
    pool.map(process_figures, range(0, files.__len__()))
finally:
    pool.close()
