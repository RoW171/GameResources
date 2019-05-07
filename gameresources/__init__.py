__author__ = "Robin 'r0w' Weiland"
__date__ = "2019-05-06"
__version__ = "0.0.0"

from pathlib import Path
from os.path import split
from os import walk, remove
from shutil import rmtree
from warnings import warn

RESIGNORE = 'resignore'  # file name for the ignore file


class Base:
    _path = None
    _parent = None

    def __repr__(self): return str(self.path)

    __str__ = __repr__

    def __getattribute__(self, item):
        try: return super().__getattribute__(item)
        except(AttributeError,): raise Exception(f"'{item}' was not found in '{self.path}'")

    __getitem__ = __getattribute__

    def __bool__(self): return self.path.exists()

    def remove(self):
        if self.path.is_dir() and rmtree(str(self.path)) != -1: raise Exception(f"Deleting '{self.path}' failed")
        elif remove(str(self.path)) != -1: raise Exception(f"Deleting '{self.path}' failed")
        del self.parent.__dict__[self.path.stem]
        
    @property
    def path(self): return self.path
    
    @path.setter
    def path(self, nPath): self.path = nPath

    @property
    def parent(self):
        return self.parent

    @parent.setter
    def parent(self, nParent):
        self.parent = nParent
        
    @property
    def resBase(self):
        parent = self.parent
        while parent.parent is not None: parent = parent.parent
        return parent


class Directory(Base):
    def __init__(self, name, path, parent):
        self.path = Path(path).resolve() / name
        self.parent = parent

    def __len__(self): return len(self.__dict__) - 2  # -2 because of path and parent

    def get(self):
        d = self.__dict__.copy()
        del d['_path'], d['_parent']
        return d

    @property
    def size(self): return sum([item.size for item in self.get().values()])

    def loadIgnore(self):
        if RESIGNORE in self.__dict__:
            with self.__dict__[RESIGNORE].open() as ignore:
                for line in ignore.readlines():
                    del self.__dict__[Path(line.strip()).stem]
            del self.__dict__[RESIGNORE]

    def createFile(self, name, ignoreExists=False):
        path = self.path / name
        path.touch(exist_ok=ignoreExists)
        self.__dict__[Path(name).stem] = File('', path, self)

    def createDirectory(self, name, ignoreExists=False):
        path = self.path / name
        if not ignoreExists and path.is_dir(): raise IsADirectoryError()
        path.mkdir()
        self.__dict__[name] = Directory('', path, self)


class File(Base):
    def __init__(self, name, path, parent):
        self.path = Path(path).resolve() / name
        self.parent = parent

    @property
    def size(self): return self.path.stat().st_size

    def get(self): return self

    def open(self, mode='r', **kwargs): return self.path.open(mode, **kwargs)


class Resources(Directory):
    FILE = File
    DIR = Directory
    
    def __init__(self, path):
        path = Path(path).resolve()
        super(Resources, self).__init__(path.stem, path, self)
        self.path = path
        self.parent = None
        
    def load(self, pathlist, name, root, cls):
        obj = self
        while pathlist: obj = obj.__dict__[pathlist.pop(0)]
        obj.__dict__[Path(name).stem] = cls(name, root, obj)
    
    def traverse(self):
        for root, dirs, files, in walk(str(self.path)):
            for directory in dirs:
                pathlist = [elem for elem in split(Path(root).relative_to(self.path)) if elem not in ('', '.')]
                self.load(pathlist, directory, root, Resources.DIR)
            for file in files:
                pathlist = [elem for elem in split(Path(root).relative_to(self.path)) if elem not in ('', '.')]
                self.load(pathlist, file, root, Resources.FILE)
    
    def remove(self): warn('Resourses base directory cannot be deleted')


if __name__ == '__main__': pass
