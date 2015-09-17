import os.path
import types

from rucola import Rucola, File, SOURCE_DIR, OUTPUT_DIR, pathmatch, PYTHON32
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

    def test_content_call(self):

        def x():
            return 'banana'

        f = File('foo', content=x)
        self.assertEqual('banana', f.content)

    def test_global_metadata(self):

        g = {'fruit': 'banana',
             'animal': 'dog'}
        f = File('foo', global_metadata=g)
        f['animal'] = 'cat'

        self.assertEqual(f['fruit'], 'banana')
        self.assertEqual(f['animal'], 'cat')

    def test_metadata_not_found(self):

        f = File('foo')
        with self.assertRaises(KeyError):
            f['notfound']


class TestRucola(BaseTest):
    """Rucola"""

    # helpers

    def example_app(self, **kwargs):
        self.create_dir('src')
        self.create_file('src/index.md', 'hello')
        self.create_file('src/logo.jpg')
        self.create_dir('src/posts')
        self.create_file('src/posts/a.md', 'apple')
        self.create_file('src/posts/b.md', 'banana')
        self.create_file('src/posts/image.jpg')

        if not kwargs:
            kwargs = {'source': 'src', 'output': 'build'}

        r = Rucola('.', **kwargs)
        return r

    # basic tests

    def test_init_empty(self):
        """should accepts an empty source directory"""

        self.create_dir(SOURCE_DIR)

        r = Rucola('.')

        self.assertEqual(r.path, os.path.abspath('.'))
        self.assertEqual(r.source, os.path.abspath(SOURCE_DIR))
        self.assertEqual(r.output, os.path.abspath(OUTPUT_DIR))
        self.assertListEqual(r.files, [])

    def test_init(self):

        self.create_dir('src')
        self.create_file('src/foo.txt')
        self.create_dir('src/a')
        self.create_file('src/a.txt')

        r = Rucola('.', source='src', output='ready')

        self.assertEqual(r.path, os.path.abspath('.'))
        self.assertEqual(r.source, os.path.abspath('src'))
        self.assertEqual(r.output, os.path.abspath('ready'))

        x = [i.path for i in r.files]
        self.assertCountEqual(x, ['foo.txt', 'a.txt'])

    # TODO: ignore argument

    # def test_init_ignore(self):
    #
    #     r = self.example_app(ignore='index.md')
    #     self.assertIsNone(f.get('index.md'))
    #
    #     r = self.example_app(ignore=join('**', '*.md'))
    #     self.assertIsNone(f.get('index.md'))
    #     self.assertIsNone(f.get('posts/a.md'))
    #     self.assertIsNone(f.get('posts/b.md'))

    def test_source_not_found(self):

        exc = IOError if PYTHON32 else FileNotFoundError

        # Missing main directory.
        self.assertRaises(exc, Rucola, 'project')

        # Missing source directory.
        self.create_dir('project')
        self.assertRaises(exc, Rucola, 'project')

    def test_output(self):

        self.create_dir(SOURCE_DIR)
        self.create_file(SOURCE_DIR + '/foo.txt', 'test')

        Rucola('.', output='ready').build()

        self.assertEqual(self.read_file('ready/foo.txt'), 'test')

    # metadata

    def test_global_metadata(self):

        r = Rucola()
        r.metadata = {'foo': 'banana'}
        file = r.create('text.html')
        r.metadata = {'foo': 'apple'}

        self.assertEqual(file['foo'], 'apple')

    # build()

    def test_build(self):

        self.example_app().build()

        self.assertEqual(self.read_file('build/index.md'), 'hello')
        self.assertEqual(self.read_file('build/logo.jpg'), '')
        self.assertEqual(self.read_file('build/posts/a.md'), 'apple')
        self.assertEqual(self.read_file('build/posts/b.md'), 'banana')
        self.assertEqual(self.read_file('build/posts/image.jpg'), '')

    def test_build_path(self):

        f = self.example_app().build('index.md')

        self.assertEqual(self.read_file('build/index.md'), 'hello')
        self.assertIsInstance(f[0], File)

    def test_build_file(self):

        r = self.example_app()
        f = r.build(r.get('index.md'))

        self.assertEqual(self.read_file('build/index.md'), 'hello')
        self.assertIsInstance(f[0], File)

    def test_build_recursive(self):

        r = self.example_app()
        r.build('**/*.md')

        self.assertEqual(self.read_file('build/index.md'), 'hello')
        self.assertEqual(self.read_file('build/posts/a.md'), 'apple')
        self.assertEqual(self.read_file('build/posts/b.md'), 'banana')

    def test_build_return(self):

        r = self.example_app()
        files = r.build('posts/*.md')

        self.assertEqual(self.read_file('build/posts/a.md'), 'apple')
        self.assertEqual(self.read_file('build/posts/b.md'), 'banana')
        self.assertCountEqual(
            files, [r.get('posts/a.md'),
                    r.get('posts/b.md')]
        )

    def test_build_safe_delete(self):

        r = self.example_app()
        for i in r.build('posts/*.md'):
            r.files.remove(i)

        self.assertFalse(r.get('posts/a.md') in r.files)
        self.assertFalse(r.get('posts/b.md') in r.files)

    # get()

    def test_get(self):

        self.create_dir('src')
        self.create_file('src/fruit.txt', 'banana')

        r = Rucola('.', source='src')
        i = r.get('fruit.txt')

        self.assertIsNotNone(i)
        self.assertEqual(i.content, 'banana')
        self.assertEqual(i.path, 'fruit.txt')

    def test_get_nothing(self):
        """get should returns None if a file is not found"""

        r = self.example_app()
        self.assertIsNone(r.get('not_found'))

    # find()

    def test_find(self):

        r = self.example_app()
        files = r.find('**/*.jpg')

        self.assertCountEqual(
            files, [r.get('logo.jpg'),
                    r.get('posts/image.jpg')]
        )

    def test_find_nothing(self):
        self.assertFalse(self.example_app().find('404.html'))

    def test_find_multiple(self):

        r = self.example_app()
        files = r.find('*.jpg', 'posts/*.jpg')

        self.assertCountEqual(
            files, [r.get('logo.jpg'),
                    r.get('posts/image.jpg')]
        )

        # No multiple instances of one file in returned list
        files = r.find('*.jpg', '*.jpg')
        self.assertListEqual(files, [r.get('logo.jpg')])

    def test_find_multiple_recursively(self):

        r = self.example_app()
        files = r.find('posts/a.md', '**/*.md')

        self.assertCountEqual(
            files, [r.get('index.md'),
                    r.get('posts/a.md'),
                    r.get('posts/b.md')]
        )

    def test_find_safe_delete(self):

        r = self.example_app()

        for i in r.find('**/*.md'):
            r.files.remove(i)

        self.assertFalse(r.find('**/*.md'))

    def test_ifind(self):

        r = self.example_app()
        files = r.ifind('**/*.md')

        self.assertIsInstance(files, types.GeneratorType)
        files = [i for i in files]
        self.assertEqual(3, len(files))
        self.assertCountEqual(
            files, [r.get('index.md'),
                    r.get('posts/a.md'),
                    r.get('posts/b.md')]
        )

    # create()

    def test_create(self):
        """create() should creates and returns a correct file"""

        self.create_dir(SOURCE_DIR)
        r = Rucola('.', output='build')

        file = r.create('foo.html', content='bar')
        self.assertIsInstance(file, File)
        self.assertEqual(file['path'], 'foo.html')
        self.assertEqual(file['content'], 'bar')

        file = r.create('bar.html')
        self.assertEqual(file['content'], '')

    def test_create_utf_content(self):
        """create() should supports the utf content"""

        r = self.example_app()
        r.create('utf', content='ĄŚŹ当世')
        r.build('utf')

        self.assertEqual(self.read_file('build/utf'), 'ĄŚŹ当世')

    def test_create_bytes(self):

        r = self.example_app()
        r.create('bytes', content=b'1234')
        r.build()

        self.assertEqual(self.read_file('build/bytes'), '1234')


    # use()

    # TODO: Test order of plugins usage

    def test_use(self):

        def plugin(app):
            app.happy = True

        self.create_dir(SOURCE_DIR)
        r = Rucola('.')
        r.happy = False
        r.use(plugin)

        self.assertTrue(r.happy)

    def test_use_many_plugins(self):

        def a(app):
            app.test += 'A'
        def b(app):
            app.test += 'B'

        self.create_dir(SOURCE_DIR)
        r = Rucola('.')
        r.test = ''
        r.use(a, b)

        self.assertEqual('AB', r.test)

    # clear_output()

    def test_clear_output(self):

        r = self.example_app()
        r.build()

        self.assertTrue(r.clear_output())
        self.assertListEqual(os.listdir('build'), [])

    def test_cleat_empty_output(self):

        self.create_dir(SOURCE_DIR)
        self.create_dir(OUTPUT_DIR)
        r = Rucola('.')
        r.clear_output()

        self.assertListEqual(os.listdir('build'), [])

    def test_clear_missing_output(self):

        self.assertFalse(self.example_app().clear_output())
