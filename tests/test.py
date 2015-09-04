import os.path

from fileflood import Flood, File, SOURCE_DIR, OUTPUT_DIR, pathmatch
from tests import BaseTest

join = os.path.join


class TestPathname(BaseTest):
    
    def test_basic(self):
    
        self.assertTrue(pathmatch('a', 'a'))
        self.assertTrue(not pathmatch('abc', 'bcd'))
        self.assertTrue(pathmatch('/a/b/c', '/a/b/c'))
        self.assertTrue(pathmatch('a/a/a', 'a/a/a'))
        self.assertTrue(pathmatch('a/b/c', 'a/b/c'))
        self.assertTrue(not pathmatch('a/b', 'a/b/c'))
        self.assertTrue(not pathmatch('a/b/c', 'a/b'))

        # Problems with / on begin and end of a path
        self.assertTrue(not pathmatch('/a/b/c', 'a/b/c'))
        self.assertTrue(not pathmatch('a/b/c', 'a/b/'))
        self.assertTrue(not pathmatch('a/b/c', 'a/b/c/'))

    def test_any_char(self):
        """?"""
        
        self.assertTrue(pathmatch('ab', 'a?'))
        self.assertTrue(not pathmatch('ba', 'a?'))

    def test_any_from_list(self):
        """[]"""
        
        self.assertTrue(pathmatch('a.a', 'a.[abc]'))
        self.assertTrue(pathmatch('a.b', 'a.[abc]'))
        self.assertTrue(pathmatch('a.c', 'a.[abc]'))
        self.assertTrue(pathmatch('/a/a/c', '/a/[ab]/c'))
        self.assertTrue(pathmatch('/a/b/c', '/a/[ab]/c'))
        self.assertTrue(not pathmatch('/a/ab/c', '/a/[ab]/c'))
        self.assertTrue(pathmatch('./1.gif', './[0-9].*'))
        self.assertTrue(pathmatch('./2.gif', './[0-9].*'))
        self.assertTrue(not pathmatch('./10.gif', './[0-9].*'))
        
    def test_not_from_list(self):
        """![]"""
        
        self.assertTrue(pathmatch('a.d', 'a.[!abc]'))
        self.assertTrue(not pathmatch('a.a', 'a.[!abc]'))
        self.assertTrue(not pathmatch('a.b', 'a.[!abc]'))
        self.assertTrue(not pathmatch('a.c', 'a.[!abc]'))
        
    def test_anything(self):
        """*"""
        
        self.assertTrue(pathmatch('abc', 'a*'))
        self.assertTrue(pathmatch('a.a', 'a.*'))
        self.assertTrue(pathmatch('a.', 'a.*'))
        self.assertTrue(pathmatch('a.bar', 'a.*'))
        self.assertTrue(not pathmatch('b.a', 'a.*'))
        self.assertTrue(not pathmatch('a.foo/b', 'a.*'))
        self.assertTrue(pathmatch('a/b/c', 'a/*/c'))
        self.assertTrue(pathmatch('a/b/c.jpg', 'a/b/*.jpg'))
        self.assertTrue(pathmatch('test/apple', 'test/a*'))
        self.assertTrue(not pathmatch('test/apple/blabla', 'test/a*'))

    def test_recursively(self):
        """**"""
        
        p = 'a/**'
        
        self.assertTrue(not pathmatch('a', p))
        self.assertTrue(pathmatch('a/a', p))
        self.assertTrue(pathmatch('a/b', p))
        self.assertTrue(pathmatch('a/b/c', p))
        self.assertTrue(pathmatch('a/a.py', p))
        self.assertTrue(pathmatch('a/bb', p))
        self.assertTrue(not pathmatch('b', p))
        
        self.assertTrue(pathmatch('a/b/c/d', 'a/**/d'))
        self.assertTrue(not pathmatch('a/b', '**/a/*'))
        self.assertTrue(pathmatch('a/b/c.jpg', '**/*.jpg'))
        self.assertTrue(not pathmatch('a/b/c.jpg', '*.jpg'))
        
        p = 'a*/**'
        
        self.assertTrue(pathmatch('a/', p))
        self.assertTrue(not pathmatch('a', p))
        self.assertTrue(pathmatch('a/b/', p))
        self.assertTrue(pathmatch('a/b', p))
        self.assertTrue(pathmatch('ab/', p))
        self.assertTrue(pathmatch('a/b/c', p))
        self.assertTrue(pathmatch('a/b/c/a.jpg', p))
        self.assertTrue(pathmatch('a/bb', p))
        
        p = '**/*.py'
        
        self.assertTrue(pathmatch('a/test.py', p))
        self.assertTrue(pathmatch('a/b/x.py', p))
        self.assertTrue(pathmatch('file.py', p))
        self.assertTrue(pathmatch('/file.py', p))
        self.assertTrue(not pathmatch('file.txt', p))
        self.assertTrue(not pathmatch('a/b/py', p))
        
        p = '**/*'
        
        self.assertTrue(pathmatch('a', p))
        self.assertTrue(pathmatch('a/a', p))
        self.assertTrue(pathmatch('a/b/c', p))
        self.assertTrue(pathmatch('x.py', p))
        self.assertTrue(pathmatch('a/b/x.py', p))
        self.assertTrue(pathmatch('/a', '**/*'))
        
        self.assertTrue(not pathmatch('a', '/**/*'))
        
        p = '**/'
        
        self.assertTrue(pathmatch('a/', p))
        self.assertTrue(pathmatch('a/b/', p))
        self.assertTrue(pathmatch('b/', p))
        self.assertTrue(not pathmatch('a', p))
        self.assertTrue(not pathmatch('file.txt', p))
        self.assertTrue(not pathmatch('a/bar.py', p))
        
        p = '../a/**/*.py'
        
        self.assertTrue(pathmatch('../a/bar.py', p))
        self.assertTrue(pathmatch('../a/foo/hello.py', p))
        self.assertTrue(not pathmatch('../a/foo/apple.txt', p))
        
        p = '**/bar.py'
        
        self.assertTrue(pathmatch('bar.py', p))
        self.assertTrue(pathmatch('a/bar.py', p))
        self.assertTrue(pathmatch('b/bar.py', p))
        self.assertTrue(not pathmatch('a/bar', p))
        
        p = '**'
        
        self.assertTrue(pathmatch('bar.py', p))
        self.assertTrue(pathmatch('foo', p))
        self.assertTrue(pathmatch('foo/hello.py', p))
        self.assertTrue(pathmatch('foo/world.txt', p))



class TestFile(BaseTest):
    """File"""

    def test_init(self):

        f = File('foo/bar', 'test')

        self.assertEqual(f.path, 'foo/bar')
        self.assertEqual(f.content, 'test')

    def test_attribs(self):

        f = File('foo')

        f.path = 'fruit.txt'
        f.content = 'banana'

        self.assertEqual(f.path, 'fruit.txt')
        self.assertEqual(f.content, 'banana')

    def test_set_data(self):

        f = File('foo')
        f['fruit'] = 'banana'

        self.assertDictEqual(f, {'path': 'foo',
                                 'content': '',
                                 'fruit': 'banana'})


class TestFlood(BaseTest):
    """Flood"""

    # helpers

    def example_app(self, **kwargs):
        self.create_dir('src')
        self.create_file('src/index.md', 'hello')
        self.create_dir('src/posts')
        self.create_file('src/posts/a.md', 'apple')
        self.create_file('src/posts/b.md', 'banana')

        if not kwargs:
            kwargs = {'source': 'src', 'output': 'build'}

        f = Flood('.', **kwargs)
        return f

    # basic tests

    def test_init_empty(self):
        """should accepts an empty source directory"""

        self.create_dir(SOURCE_DIR)

        f = Flood('.')

        self.assertEqual(f.path, os.path.abspath('.'))
        self.assertEqual(f.source, os.path.abspath(SOURCE_DIR))
        self.assertEqual(f.output, os.path.abspath(OUTPUT_DIR))
        self.assertListEqual(f.files, [])

    def test_init(self):

        self.create_dir('src')
        self.create_file('src/foo.txt')
        self.create_dir('src/a')
        self.create_file('src/a.txt')

        f = Flood('.', source='src', output='ready')

        self.assertEqual(f.path, os.path.abspath('.'))
        self.assertEqual(f.source, os.path.abspath('src'))
        self.assertEqual(f.output, os.path.abspath('ready'))

        x = [i.path for i in f.files]
        self.assertCountEqual(x, ['foo.txt', 'a.txt'])

    # TODO: ignore argument

    # def test_init_ignore(self):
    #
    #     f = self.example_app(ignore='index.md')
    #     self.assertIsNone(f.get('index.md'))
    #
    #     f = self.example_app(ignore=join('**', '*.md'))
    #     self.assertIsNone(f.get('index.md'))
    #     self.assertIsNone(f.get('posts/a.md'))
    #     self.assertIsNone(f.get('posts/b.md'))

    def test_source_not_found(self):

        # Missing main directory.
        self.assertRaises(OSError, Flood, 'project')

        # Missing source directory.
        self.create_dir('project')
        self.assertRaises(OSError, Flood, 'project')

    def test_build(self):
        """should build a file in the correct output"""

        self.create_dir(SOURCE_DIR)
        self.create_file(SOURCE_DIR + '/foo.html', 'test')
        Flood('.').build()
        self.assertEqual(self.read_file(OUTPUT_DIR + '/foo.html'), 'test')

    def test_output(self):

        self.create_dir(SOURCE_DIR)
        self.create_file(SOURCE_DIR + '/foo.txt', 'test')

        Flood('.', output='ready').build()

        self.assertEqual(self.read_file('ready/foo.txt'), 'test')

    # build()

    def test_build_path(self):

        self.example_app().build('index.md')

        self.assertEqual(self.read_file('build/index.md'), 'hello')

    def test_build_file(self):

        f = self.example_app()
        f.build(f.get('index.md'))

        self.assertEqual(self.read_file('build/index.md'), 'hello')

    def test_build_recursive(self):

        f = self.example_app()
        f.build('**/*.md')

        self.assertEqual(self.read_file('build/index.md'), 'hello')
        self.assertEqual(self.read_file('build/posts/a.md'), 'apple')
        self.assertEqual(self.read_file('build/posts/b.md'), 'banana')

    # get()

    def test_get(self):

        self.create_dir('src')
        self.create_file('src/fruit.txt', 'banana')

        f = Flood('.', source='src')
        i = f.get('fruit.txt')

        self.assertIsNotNone(i)
        self.assertEqual(i.content, 'banana')
        self.assertEqual(i.path, 'fruit.txt')

    def test_get_nothing(self):
        """get should returns None if a file is not found"""

        f = self.example_app()
        self.assertIsNone(f.get('not_found'))

    # find() # TODO:

    def test_find(self):
        # TODO: it returns iterator or list?

        self.create_dir('src')
        self.create_file('src/foo.txt', 'banana')
        self.create_file('src/bar.txt', 'apple')

        f = Flood('.', source='src')
        # TODO: detailed tests
        self.assertEqual(len([i for i in f.find('*.txt')]), 2)

    # create()

    def test_create(self):
        """create() should creates and returns a correct file"""

        self.create_dir(SOURCE_DIR)
        f = Flood('.', output='build')

        file = f.create('foo.html', 'bar')
        self.assertIsInstance(file, File)
        self.assertEqual(file['path'], 'foo.html')
        self.assertEqual(file['content'], 'bar')

        file = f.create('bar.html')
        self.assertEqual(file['content'], '')

    def test_create_utf_content(self):
        """create() should supports the utf content"""

        f = self.example_app()
        f.create('utf', 'ĄŚŹ当世')
        f.build('utf')

        self.assertEqual(self.read_file('build/utf'),'ĄŚŹ当世')

    # use()

    # TODO: Test order of plugins usage

    def test_use(self):

        def plugin(app):
            app.happy = True

        self.create_dir(SOURCE_DIR)
        f = Flood('.')
        f.happy = False
        f.use(plugin)

        self.assertTrue(f.happy)

    def test_use_many_plugins(self):

        def a(app):
            app.test += 'A'
        def b(app):
            app.test += 'B'

        self.create_dir(SOURCE_DIR)
        f = Flood('.')
        f.test = ''
        f.use(a, b)

        self.assertEqual('AB', f.test)

    # clear_output()

    def test_clear_output(self):

        f = self.example_app()
        f.build()

        self.assertTrue(f.clear_output())
        self.assertListEqual(os.listdir('build'), [])

    def test_cleat_empty_output(self):

        self.create_dir(SOURCE_DIR)
        self.create_dir(OUTPUT_DIR)
        f = Flood('.')
        f.clear_output()

        self.assertListEqual(os.listdir('build'), [])

    def test_clear_missing_output(self):

        self.assertFalse(self.example_app().clear_output())
