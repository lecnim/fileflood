import unittest
import tempfile
import shutil
import os
from rucola import OUTPUT_DIR


class BaseTest(unittest.TestCase):

    def setUp(self):

        # Path pointing to current working directory.
        self.cwd = os.getcwd()
        # Path to commands test directory.
        self.path = os.path.dirname(__file__)
        # Path to temporary directory with sites.
        self.temp_path = tempfile.mkdtemp()
        # Set current working directory to temporary directory with sites.
        os.chdir(self.temp_path)

    def tearDown(self):
        # Go to previous working directory and clear files.
        os.chdir(self.cwd)
        shutil.rmtree(self.temp_path)

    # File system shortcuts.

    def read_file(self, path):
        """Returns data from given path. Use '/' as a path separator,
        path must be relative to current temp path."""

        if os.path.isabs(path):
            raise ValueError('path must be relative!')

        fp = os.path.join(self.temp_path, *path.split('/'))
        self.assertTrue(os.path.exists(fp),
                        msg='path not found: ' + fp)

        with open(fp) as file:
            return file.read()

    def create_file(self, path, content=''):
        """Creates a new file with a data. Use '/' as a path separator,
        path must be relative to temp."""

        if os.path.isabs(path):
            raise ValueError('path must be relative!')

        path = os.path.join(self.temp_path, *path.split('/'))
        dir_path = os.path.dirname(path)

        # Create missing dirs.
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(path, 'w') as file:
            file.write(content)

    def create_dir(self, path):
        """Creates a new directory. Use '/' as a path separator,
        path must be relative to temp."""

        if os.path.isabs(path):
            raise ValueError('path must be relative!')

        path = os.path.join(self.temp_path, *path.split('/'))
        os.makedirs(path)

    def remove_file(self, path):
        """BE CAREFUL! Removes given file. Use '/' as a path separator,
        path must be relative to temp."""

        if os.path.isabs(path):
            raise ValueError('path must be relative!')
        os.remove(os.path.join(self.temp_path, *path.split('/')))

    def remove_dir(self, path):
        """BE CAREFUL! Removes directory recursively. Use '/' as a path
        separator, path must be relative to temp."""

        if os.path.isabs(path):
            raise ValueError('path must be relative!')

        p = os.path.join(self.temp_path, *path.split('/'))
        shutil.rmtree(p)


import inspect



class FunctionalTest(unittest.TestCase):

    def setUp(self):

        # Clear build directory
        self.test_dir = os.path.dirname(inspect.getfile(self.__class__))
        output = os.path.join(self.test_dir, OUTPUT_DIR)
        if os.path.exists(output):
            shutil.rmtree(output)


    # Comparing outputs.

    def get_files(self, path):
        """Returns all files in tree."""

        paths = []
        for i in os.walk(path):
            for file in i[2]:
                paths.append(os.path.join(os.path.relpath(i[0], path), file))
        return paths

    def compare(self, app):
        """Checks if files in test/output directory are same as generated in
        site output. Argument path is patch relative to output directory."""

        expected = os.path.join(self.test_dir, 'expected')

        for path, dirs, files in os.walk(expected):
            for f in files:

                exp_file = os.path.join(path, f)
                rel_file = os.path.relpath(exp_file, expected)
                build_file = os.path.join(app.output, rel_file)

                # Check if file was created in output directory.
                self.assertTrue(os.path.exists(build_file),
                                msg='File not found in build directory: ' + rel_file)

                # Compare file contents.
                with open(build_file) as a:
                    with open(exp_file) as b:
                        self.assertEqual(a.read(), b.read(),
                                         msg='Files contents do not match!')

        # Compares directory tree.

        expected_files = self.get_files(expected)
        build_files = self.get_files(app.output)
        self.assertCountEqual(expected_files, build_files)


class PluginTest(FunctionalTest):
    pass