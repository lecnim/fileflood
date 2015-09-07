.. all this good in only one file.


Hello Rucola!
=============

What is Rucola?
---------------

`Rucola` is a simple, pluggable static (not only) site generator for Python.
Its API is heavy influenced by `Metalsmith <http://metalsmith.io/>`_, but
generation process differs in some minor aspects.

You can use `Rucola` to build your blog or a web page, but the main idea
is about manipulating a directory of files using plugins. As a result this
framework you can build any project that is based on files.
The sky is the limit, probably.


What are plugins?
-----------------

Plugin is a python module that can be used by Rucola to
manipulate files. It is installed separately and mostly it name
is ``rucola-something``, for example ``rucola-markdown``, a plugin
used to render Markdown pages. List of available plugin is
`here <https://TODO>`_

.. todo::

   plugins list

What do I need?
---------------

Rucola requires a `Python <https://python.org/>`_, minimal version ``3.2``,
and has no other dependencies itself. Plugins has different dependencies,
but do not worry, they are installed automatically.


Installation
------------

Simplest way is to use `pip` command. If you want clean a installation of
Rucola, without any plugins use: ::

   $ pip install rucola

But plugins makes life easier, so it is recommended to install
Rucola with all suggested plugins: ::

   $ pip install rucola[plugins]

Rucola is only one file
~~~~~~~~~~~~~~~~~~~~~~~

As the title suggest - Rucola is only a ``rucola.py`` file, you can always
just copy that file and use it in your project. No problem. Maybe you
need to copy some plugins in the same way.


But how do I use it?
--------------------

TLDR
~~~~

There 3 working steps using Rucola:

1. Create a Rucola() object, it loads all files from a source directory.
2. Manipulate files using plugins or your own code.
3. Write result to output directory using ``build()`` method.


Meet the example directory
~~~~~~~~~~~~~~~~~~~~~~~~~~

Ok, lets create a example project with the given directory structure: ::

   project/
      build/
      src/
         index.html
         about.html
      build.py

``project/``
   It is called a `working directory`, it contains all project files.
``project/src/``
   Here are all source files that are manipulated by Rucola, it is
   called a `source directory`.
``project/build``
   Rucola writes manipulated files here, it is called an `output directory`.
``build.py``
   A python script that manipulates files from a `source directory`
   and writes them to an `output directory`.


First, we need to create the Rucola application, in a `build.py` file.
Remember that Rucola is called with a path to a ``working directory``,
not to a ``source`` one!

.. code-block:: python

   from rucola import Rucola

   app = Rucola('path/to/project')

A Rucola object has some interesting properties like:

.. code-block:: python

   app.path    # path to working directory: path/to/project
   app.source  # path to source directory: path/to/project/src
   app.output  # path to output directory: path/to/project/build

When you create a new Rucola object it will loads all files from
`source directory`. This files are available in ``app.files`` list
as a File instances, for example:

.. code-block:: python

   [File('index.htm'), File('about.html')]

Meet Files
~~~~~~~~~~

File is a simple dict-like object, with only two keys: ``path``
and ``content``:

.. code-block:: python

   file = File('fruit.txt', content='I am Banana!')

   file['path']     # 'fruit.txt'
   file['content']  # 'I am Banana!'

When Rucola builds a project it:

   1. Gets each File instance from ``app.files``.
   2. Write ``File['content']`` value into ``File['path']`` relative
      to `output directory`.

For example if ``app.files`` looks like:

.. code-block:: python

   [File('index.htm', 'Welcome'), File('about.html', 'I am Banana!')]

The `output directory` will look like: ::

   build/
      index.html
         Welcome
      about.html
         I am Banana!


Meet get() and find()
~~~~~~~~~~~~~~~~~~~~~

The simplest way of getting files from ``app.files`` is to
use :any:`get()` or :any:`find()` methods:

.. code-block:: python

   file = app.get('index.html')

   for file in app.find('*.html')
      pass

# glob support


Meet create()
~~~~~~~~~~~~~
TODO


Meet use()
~~~~~~~~~~
TODO


Meet build()
~~~~~~~~~~~~
TODO

Plugins
-------
TODO


Contents:



.. toctree::
   :maxdepth: 2

   api





Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

