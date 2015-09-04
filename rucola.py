"""
Rucola
A simple framework (not only) for static sites generation.

TODO: Add descripiton here

"""

# TODO: Logging msgs
# TODO: Clear code
# TODO: Clear output during init of Rucola() ?

import os
import sys
import fnmatch
import re
import posixpath
import shutil
from logging import debug, info, basicConfig

basicConfig(format='%(message)s', level=0)

__author__ = 'Kasper'
__version__ = '0.0.1.dev1'


# Minimum supported python: 3.2
if sys.hexversion < 0x030200F0:
    raise ImportError('Python < 3.2 not supported!')


SOURCE_DIR = 'source'
OUTPUT_DIR = 'build'


# Path match

SEP = '/'  # os.sep

magic_check = re.compile('([*?[])')
magic_check_bytes = re.compile(b'([*?[])')

def has_magic(s):
    if isinstance(s, bytes):
        match = magic_check_bytes.search(s)
    else:
        match = magic_check.search(s)
    return match is not None


def pathmatch(path, pattern):

    a, b = path.split(SEP), pattern.split(SEP)
    b_set = None

    while True:

        if not a and not b:
            return True

        if not a or (not b and not b_set == '**'):
            return False

        a_set = a.pop(0)

        if b_set != '**':
            b_set = b.pop(0)

        if b_set == '**' and b:

            a = a[-len(b):]
            b_set = b.pop(0)
            if a: a_set = a.pop(0)

        if has_magic(b_set):
            if not fnmatch.fnmatch(a_set, b_set):
                return False
        elif a_set != b_set:
            return False




class ContentReader:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path) as f:
            return f.read()


class File(dict):

    def __init__(self, path, content=None):
        super().__init__()

        self['path'] = path
        if content is None:
            content = ''
        self['content'] = content

    def __getitem__(self, key):

        if key == 'content':
            x = dict.__getitem__(self, key)
            if isinstance(x, ContentReader):
                return x.read()
        return dict.__getitem__(self, key)

    def has_buffer(self):
        x = dict.__getitem__(self, 'content')
        return isinstance(x, ContentReader)

    def get_buffer(self):
        return dict.__getitem__(self, 'content')


    # Shortcuts

    @property
    def path(self):
        return self['path']

    @path.setter
    def path(self, value):
        self['path'] = value

    @property
    def content(self):
        return self['content']

    @content.setter
    def content(self, value):
        self['content'] = value


class Rucola:

    def __init__(self, path, source=SOURCE_DIR, output=OUTPUT_DIR):

        info('\nLoading: ' + path)

        self.path = os.path.abspath(path)
        self._source = os.path.join(self.path, source)
        self._output = ''
        self.output = os.path.join(self.path, output)

        # TODO: Change this to a professional exception raising

        # Path not found
        os.stat(self.path)

        # Source not found
        os.stat(self.source)

        self._pathmatch = None



        # try:
        #     f = open(path)
        # except OSError as e:
        #     if e.errno == errno.ENOENT:
        #         # do your FileNotFoundError code here
        #     else:
        #         raise

        self.files = self._find_files()

    @property
    def source(self):
        return self._source

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, path):
        info('Output: ' + path)
        self._output = path


    def _find_files(self):

        result = []

        for path, dirs, files in os.walk(self.source):
            for f in files:

                # /home/source/foo/ + file.txt => foo/file.txt
                p = os.path.relpath(os.path.join(path, f), self.source)
                # convert \\ to /
                p = posixpath.join(*p.split(os.sep))

                debug(p)

                result.append(File(p, ContentReader(os.path.join(path, f))))

        return result

    def get(self, path):

        for file in self.files:
            if pathmatch(file.path, path):
                return file
        return None

    def _build_file(self, file):

        debug(file.path)

        os.makedirs(os.path.join(self.output, os.path.dirname(file.path)), exist_ok=True)

        if file.has_buffer():
            shutil.copy(file.get_buffer().path, os.path.join(self.output, file.path))
        else:

            mode = 'wb' if isinstance(file.content, bytes) else 'w'

            with open(os.path.join(self.output, file.path), mode) as f:
                f.write(file.content)

    def build(self, target='**/*'):
        """Builds files.

        Args:
            target: Accepts str or File object.
        """

        info('Building: ' + str(target))

        # Create missing output dir
        os.makedirs(self.output, exist_ok=True)

        if isinstance(target, File):
            self._build_file(target)
            return [target]

        else:
            result = []
            for file in self.find(target):
                self._build_file(file)
                result.append(file)
            return result

    def find(self, *patterns):
        """
        Returns list of all files that matches a given patterns.

        Order of paths is not changing the order of returned files.
        """

        return [i for i in self.ifind(*patterns)]


    def ifind(self, *patterns):
        """
        Not safe-remove in place.
        """

        for file in self.files:
            for p in patterns:
                if pathmatch(file.path, p):
                    yield file
                    break

    def clear_output(self):

        if os.path.exists(self.output):
            info('Clearing output directory')

            shutil.rmtree(self.output)
            os.mkdir(self.output)
            return True
        return False

    def create(self, path, content=''):

        info('Creating file: ' + path)

        f = File(path, content)
        self.files.append(f)
        return f

    def use(self, *plugins):

        for i in plugins:
            if callable(i):
                info('Using plugin: ' + repr(i))
                i(self)
        return self
