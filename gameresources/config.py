__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-05-07"
__version__ = "0.0.0"

from configparser import ConfigParser
from io import StringIO, TextIOWrapper
from warnings import warn


class Section:
    _config = None
    _name = str()

    def __getattribute__(self, item): return super(Section, self).__getattribute__(item)

    __getitem__ = __getattribute__

    def __setattr__(self, key, value):
        try:
            if key not in ('_config', '_name'): self._config.saveEntry(self._name, key, value)
            super(Section, self).__setattr__(key, value)
        except (AttributeError,):
            raise NotImplemented('adding options will be possible in the future')  # TODO: add option into section here

    __setitem__ = __setattr__

    def __contains__(self, item): return item in self.__dict__


class Config(ConfigParser):
    def __init__(self, path, **kwargs):
        self._path = path
        super(Config, self).__init__(**kwargs)
        self(self._path)
        self.load()

    def __call__(self, nFile=None):
        if isinstance(nFile, (StringIO, TextIOWrapper,)):
            self.read_file(nFile)
            self._path = nFile.name
        if isinstance(nFile, str):
            self.read(nFile)
            self._path = nFile
        return self

    def __repr__(self): return str(self._path)

    __str__ = __repr__

    def __getattribute__(self, item): return super(Config, self).__getattribute__(item)

    __getitem__ = __getattribute__

    def __setattr__(self, key, value):
        try: super(Config, self).__setattr__(key, value)
        except (AttributeError,):
            raise NotImplemented('adding sections will be possible in the future')  # TODO: add sections here

    __setitem__ = __setattr__

    def __contains__(self, item): return item in self.__dict__

    def load(self):
        for section in self.sections():
            s = Section()
            s._config = self
            s._name = section
            for option in self.options(section):
                s.__dict__[option] = self.loadEntry(section, option)
            self.__dict__[section] = s

    def loadEntry(self, section, option, fallback=None, datatype=str, subdatatype=str, chunksize=None):
        try:
            loadedItem = self.get(section, option, fallback=fallback)
            if datatype == list or datatype == tuple:
                loadedItem = loadedItem.replace('(', '').replace(')', '')
                if loadedItem == '': return datatype([])
                loadedItem = datatype(map(subdatatype, loadedItem.split(', ')))
                if chunksize is not None: loadedItem = datatype((zip(*[iter(loadedItem)] * chunksize)))
            elif datatype == bool: loadedItem = bool(int(loadedItem))
            else: loadedItem = datatype(loadedItem)
            return loadedItem
        except (Exception,) as e:
            warn(f'failed loading {section}:{option}; returned fallback; {e.__name__}')
            return fallback

    def save(self):
        with open(self._path, 'w') as configfile: self.write(configfile)

    def saveEntry(self, section, option, value, saveToFile=True):
        if isinstance(value, (list, tuple,)): value = ', '.join(value)
        elif type(value) == bool: value = str(int(value))
        self.set(section, option, str(value))
        if saveToFile: self.save()


if __name__ == '__main__':
    from pathlib import Path
    c = Config(Path(r'C:\Users\robin\Documents\Private\Python\GameResources\testing\config.ini').open('r'))
    print(c.gameplay.player_speed)
    # c.gameplay['player-speed'] = 4
