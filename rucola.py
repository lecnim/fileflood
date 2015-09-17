"""
Rucola
A simple framework (not only) for static sites generation.

Use the :any:`Rucola` class and :any:`File` instances to
create an application that generate a static site.
See the :any:`Rucola` methods for more details, especially look at
:any:`Rucola.find()`, :any:`Rucola.use()` and :any:`Rucola.build()`.
Good luck!

"""

# TODO: Logging msgs
# TODO: Clear code
# TODO: Clear output during init of Rucola() ?
# TODO: Drop python 3.2 support

import os
import sys
import fnmatch
import re
import posixpath
import shutil
import logging
import filecmp

__author__ = 'Kasper Minciel'
__version__ = '0.0.1.dev2'
__license__ = 'MIT'

# Minimum supported python: 3.2
if sys.hexversion < 0x030200F0:
    raise ImportError('Python < 3.2 not supported!')

PYTHON32 = True if sys.hexversion < 0x030300F0 else False

SOURCE_DIR = 'src'
OUTPUT_DIR = 'build'

# Logging

log = logging.getLogger(__name__)
info = log.info
debug = lambda x: log.debug('  ' + x)



# Utils

def compare_dirs(a, b):
    """Returns True if a content of directory `a` is same as a content of `b`."""

    def compare(x, a, b):

        if x.diff_files or x.funny_files:
            return False

        for i in x.same_files:
            if not filecmp.cmp(os.path.join(a, i), os.path.join(b, i), shallow=False):
                return False

        for i in x.subdirs:
            compare(i, a, b)

        return True

    dc = filecmp.dircmp(a, b)
    return compare(dc, a, b)

def split_path(path):
    """Split a path using the system-depended separator slash.

    >>> split_path(os.path.join('a', 'b', 'c'))
    ['a', 'b', 'c']
    """

    if not os.path.basename(path):
        path = os.path.dirname(path)

    folders = []
    while 1:
        path, folder = os.path.split(path)

        if folder != '':
            folders.append(folder)
        else:
            if path != '':
                folders.append(path)
            break

    folders.reverse()
    return folders

# Path match

SEP = '/'  # os.sep

magic_check = re.compile('([*?[])')
magic_check_bytes = re.compile(b'([*?[])')

def has_magic(s):
    """Returns True if a path uses a glob syntax characters."""

    if isinstance(s, bytes):
        match = magic_check_bytes.search(s)
    else:
        match = magic_check.search(s)
    return match is not None


def pathmatch(path, pattern):
    """Returns `True` if `path` matches a pattern, else `False`.
    Supports a glob syntax. I don't remember how does it works,
    it splits `path` and `pattern` and compare elements using
    the python `fnmatch` module.

    Example:

    >>> pathmatch('a/b/c', 'a/b/*')
    True
    >>> pathmatch('a/foo/bar', 'a/**/*')
    True
    >>> pathmatch('b/c/d', 'a/b/c')
    False

    """

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

# Main classes


class ContentReader:
    """When called it opens a `self.path` file and reads it. That is all.
    It is used by :any:`File` instances to save memory. Without it all
    instances store their contents directly in a ``content`` key, even when
    they are not used. Using this class, a content is read and returned only
    when needed.
    """
    def __init__(self, path):
        self.path = path

    def __call__(self, *args, **kwargs):
        with open(self.path) as f:
            return f.read()


class File(dict):
    """Dict-like class that represent a file. Used by :any:`Rucola` to
    generate representation of `source` directory. In most situations
    you do not use this class, use :any:`Rucola.create()` instead.

    Example:

    >>> app = Rucola()
    >>> file = File('cat.txt', content='meow')
    File('cat.txt')
    >>> app.build(file)

    Initialization parameters:

        `path`
            Path where `content` will be written during building.

        `content`
            File content.

        `global_metadata`
            If a key is not found, look for it in this dict. For example used
            to get access to global ``Rucola.metadata``.

    """

    def __init__(self, path, content=None, global_metadata=None):
        super().__init__()

        self.globals = global_metadata

        self['path'] = path
        if content is None:
            content = ''
        self['content'] = content

    def __getitem__(self, key):

        if key == 'content':
            x = dict.__getitem__(self, key)
            if callable(x):
                return x()
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            if self.globals and key in self.globals:
                return self.globals[key]
            raise

    #

    def has_buffer(self):
        """Returns `True` if a `content` is not set and it is dynamically
        read from filesystem.
        """
        x = dict.__getitem__(self, 'content')
        return isinstance(x, ContentReader)

    def get_buffer(self):
        """Returns object that is used to read `content` from a filesystem."""
        return dict.__getitem__(self, 'content')

    # Shortcuts

    @property
    def path(self):
        """Same as a `self['path']`"""
        return self['path']

    @path.setter
    def path(self, value):
        self['path'] = value

    @property
    def content(self):
        """Mostly a `content` property do not store a real file data, because
        of memory saving. It stores a :any:`ContentReader` object that reads
        a real file data only when `content` property is used.
        Same as a `self['content']`"""
        return self['content']

    @content.setter
    def content(self, value):
        self['content'] = value


class Rucola:
    """Rucola static site generator.

    Initialization parameters:

        `path`
            A working directory. This directory should contains
            `source` and `output` directories. If `None`, skip
            the files loading process, `self.files` will be an empty list.
            If path is not found, Rucola raises an exception.

        `source (default: 'src')`
            A directory relative to a `path` working directory.
            All files are loaded from here. If path is not found,
            Rucola raises an exception.

        `output (default: 'build')`
            A directory relative to a `path` working directory.
            All built files are written here.

        `pathmatcher`
            Object used to test if a path matches a pattern.

    """

    def __init__(self, path=None, source=SOURCE_DIR, output=OUTPUT_DIR,
                 pathmatcher=pathmatch):

        self._pathmatch = pathmatcher

        self._metadata = {}

        if path is None:

            self.path = None
            self._source = None
            self._output = os.path.abspath(output)
            self.files = []

        else:

            info('\nLoading: ' + path)

            self.path = os.path.abspath(path)
            self._source = os.path.join(self.path, source)
            self._output = ''
            self.output = os.path.join(self.path, output)

            if not os.path.exists(self.path) or not os.path.exists(self.source):
                msg = 'Directory not found, please create it first: ' + path
                if PYTHON32:
                    raise IOError(msg)
                else:
                    raise FileNotFoundError(msg)

            self.files = self._find_files()

    @property
    def source(self):
        """Absolute path to source directory. It cannot be changed!"""
        return self._source

    @property
    def output(self):
        """Absolute path to output directory"""
        return self._output

    @output.setter
    def output(self, path):
        info('Output: ' + path)
        self._output = path

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        for f in self.files:
            f.globals = value
        self._metadata = value

    def _find_files(self):
        """Returns list with :any:`File` instances, loaded from
        `self.source` directory"""

        result = []

        for path, dirs, files in os.walk(self.source, followlinks=True):
            for f in files:

                # /home/source/foo/ + file.txt => foo/file.txt
                p = os.path.relpath(os.path.join(path, f), self.source)
                # convert \\ to /
                p = posixpath.join(*p.split(os.sep))

                debug(p)

                result.append(
                    File(p,
                         content=ContentReader(os.path.join(path, f)),
                         global_metadata=self.metadata)
                )

        return result

    #

    def _build_file(self, file):
        """Write `content` of :any:`File` instance to
        `self.output` directory."""

        debug(file.path)

        os.makedirs(os.path.join(self.output, os.path.dirname(file.path)), exist_ok=True)

        if file.has_buffer():
            shutil.copy(file.get_buffer().path, os.path.join(self.output, file.path))
        else:

            if isinstance(file.content, bytes):
                mode, encoding = 'wb', None
            else:
                mode, encoding = 'w', 'utf-8'

            with open(os.path.join(self.output, file.path), mode, encoding=encoding) as f:
                f.write(file.content)

    def build(self, target='**/*'):
        """Find all :any:`File` instances that matches a `target` pattern and write their
        `content` to `self.output` directory. Returns list of built :any:`File` instances.
        Pattern supports glob syntax, just like :any:`find()` method.

        Also parameter `target` can be a :any:`File` instance:

        >>> app = Rucola()
        >>> file = app.get('foo.html')
        >>> app.build(file)
        File('foo.html')

        It is possible to remove already built :any:`File` instances from a
        :any:`Rucola` app. For example build all `html` files and remove them
        from an app.

        >>> for file in app.build('**/*.html'):
        >>>     app.files.remove(file)

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

    def get(self, path):
        """Returns a :any:`File` instance that matches a given `path` or
        `None` if not found.

        Example:

        >>> app = Rucola()
        >>> file = app.get('path/to/file')
        """

        for file in self.files:
            if self._pathmatch(file.path, path):
                return file
        return None

    def find(self, *patterns):
        """Returns list of all :any:`File` instances that matches a given `patterns`.
        The order of patterns arguments do not change the order of returned instances.

        Pattern supports glob syntax:

        >>> '*.html'       # Matches all html files in a current directory
        >>> '**/*.html'    # Matches all html files in all directories
        >>> '?.html'       # Matches <any-char>.html like a.html, b.html etc.

        It is possible to remove files from a :any:`Rucola` app in a loop:

        >>> app = Rucola()
        >>> for file in app.find('*.html'):
        >>>     app.files.remove(file)


        """

        return [i for i in self.ifind(*patterns)]


    def ifind(self, *patterns):
        """Iterate :any:`File` instances that matches a given patterns.
        Same as a :any:`find()` method but not safe to remove files
        from a :any:`Rucola` app in a loop.
        """

        for file in self.files:
            for p in patterns:
                if self._pathmatch(file.path, p):
                    yield file
                    break

    def clear_output(self):
        """Removes all files in a `self.output` directory. Returns a `True` if
        the operation was successful or a `False` if a `output` directory
        do not exists."""

        if os.path.exists(self.output):
            info('Clearing output directory')

            shutil.rmtree(self.output)
            os.mkdir(self.output)
            return True
        return False

    def create(self, path, content=''):
        """Returns a new :any:`File` instance with given `path` and `content`.
        It is added to `self.files` list. If the :any:`File` with a given `path`
        already exists, returns `None` and do not create anything.

        Example:

        >>> app = Rucola()
        >>> file = app.create('path/to/banana.txt', content='I am banana!')
        File('path/to/banana.txt')
        """

        # TODO: Remove content parameter, use metadata instead

        if self.get(path):
            return None

        info('Creating file: ' + path)

        f = File(path, content, global_metadata=self.metadata)
        self.files.append(f)
        return f

    def use(self, *plugins):
        """Call each `plugin` with `self` as a argument. Returns `self`.

        A plugin is just a callable object, can be a function or a class
        or anything:

        >>> def foo(x):
        >>>     x.output = 'new/output'
        >>> app = Rucola()
        >>> app.use(foo)
        >>> app.output
        'new/output'
        """

        for i in plugins:
            if callable(i):
                info('Using plugin: ' + repr(i))
                i(self)
        return self
