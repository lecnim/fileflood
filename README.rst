Rucola
======


Rucola is a simple, pluggable static site generator for Python.


(influenced by `Metalsmith <http://metalsmith.io/>`_)


Example of power plugins!
-------------------------

Project structure: ::

   src/
      index.md
      about.md
   build.py

Content of ``build.py`` file:

.. code-block:: python

   from rucola import Rucola
   from rucola_markdown import Markdown
   from rucola_permalinks import Permalinks

   app = Rucola('path/to/dir')
   app.use(
      Markdown(),
      Permalinks(':path/:title')
   )
   app.build()

Result: ::

   build/
      about/
         index.html
      index.html
   src/
      index.md
      about.md
   build.py



`More examples here! <https://github.com/lecnim/rucola/tree/master/examples/>`_.


Installation
------------

Just use pip, moreover it will install all available plugins::

   $ pip install rucola[plugins]



But how does it works?
----------------------

Rucola works the same steps as Metalsmith:

1. Load all files from source directory.
2. Manipulate files (for example by plugins or user functions)
3. Write result to output directory.


1. Loading
~~~~~~~~~~

First, Rucola loads all files from ``src`` directory:

.. code-block:: python

   app = Rucola('path/to/dir')

All that files are stored in ``app.files`` list:

.. code-block:: python

   [
      File('index.md'),
      File('something.jpg')
   ]


2. Modifying
~~~~~~~~~~~~

Plugins are manipulating the loaded files:

.. code-block:: python

   app.use(
      Markdown()
   )

It is a simple mechanism, plugin is just a simple class:

.. code-block:: python

   class Plugin:
      def __call__(app):
         # do something with Rucola app here!

----

Also you can manipulate files with your own hands.
Use a ``get`` method to get a file that you want:

.. code-block:: python

   file = app.get('index.md')

Or get many files using a ``find`` method with a glob-like syntax:

.. code-block:: python

   for file in app.find('**/*.html'):
      pass

Files are dict-like objects with two default keys:

.. code-block:: python

   file['path']     # Path to a file, relative to a source directory.
   file['content']  # Content of a file.

So if you want to change the file content, change it, that's all:

.. code-block:: python

   file['path'] = 'foo/bar.html'
   file['content'] = 'My new happy content!'


3. Writing
~~~~~~~~~~

Write all manipulated files to a output directory:

.. code-block:: python

   app.build()

Or write only chosen ones:

.. code-block:: python

   app.build('foo/bar.html')
   app.build('posts/*.md')    # build md files in a `posts` directory
   app.build('**/*.md')       # build every md file



Plugins
-------

TODO