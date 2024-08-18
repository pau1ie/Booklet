
Installation
==================

HPBooklet provides executable files for Windows and Linux(Ubuntu).
All the resources are fully independent to the OS, therefore it should
run fine on OSX, however, the developer does not have any Apple devices,
so cannot build it.
If you are OSX user you can build project yourself see the 
:ref:`From Source <from_source>` section below.


Executable Bunldle
--------------------

Download executable file from `Sourceforge <https://sourceforge.net/projects/hornpenguinbooklet/>`_.

.. raw:: html

    <a href="https://sourceforge.net/projects/hornpenguinbooklet/files/latest/download"><img alt="Download HornPenguin Booklet" src="https://a.fsdn.com/con/app/sf-download-button" width=276 height=48 srcset="https://a.fsdn.com/con/app/sf-download-button?button_size=2x 2x"></a>

The repository provides two types of program one file version and one directory bundle.
The directory bundle version of each OS is presented with compressed file, :code:`zip` and :code:`tgz` which are common compressed file format in each OS. 

Windows
^^^^^^^^^^^^^^^^

.. code-block:: 

    booklet.exe # one file version
    booklet_Windows.zip # one directory bundle

Linux
^^^^^^^^^^^^^^^^

.. code-block:: 

    booklet # one file version
    booklet_Linux.tgz # one directory bundle

OSX
^^^^^

Please build yourself or directly execute from sources. 
See the below section.

.. warning:: 

    Python is compatible with the major three OSs, however, the
    implementation of tkinter in those OSs have minor differences.
    For example, :code:`iconbitmap` had an issue in Linux. Tkiner Label
    and Button do not work properly in OSX.
    The developer identified those bugs and fixed them as best he could:
    (the `tkmacosx <https://github.com/Saadmairaj/tkmacosx>`_ module was
    useful), but there could be more bugs in Linux and Mac environments.
    Please create an issue in gitbub if you notice any additional bugs.


From source
--------------------

.. _from_source:

This section explains how to aquire, run and build the project from
source.

Get the project
^^^^^^^^^^^^^^^^^^^

You can download the project with git. 

.. code-block::

    git clone https://github.com/HornPenguin/Booklet.git # github 
    git clone https://git.code.sf.net/p/hornpenguinbooklet/code hornpenguinbooklet-code # sourceforge

or download with zipped file from project `source repository <https://github.com/HornPenguin/Booklet>`_
..

    **Directory**

    - :code:`booklet`: Python source code.
    - :code:`dist`: Standalone executable files for OSs.
    - :code:`documents`: Sphinx rst document source (i.e. source of this documentation)
    - :code:`images`: Miscellaneous images, in working images or original :code:`.odg` files.
    - :code:`resources`: Essential resources for program: sound, images, logo, ... . 
    - :code:`test`: Contains some jupyter notebook tests.

    **File**

    - :code:`.readthedocs.yaml`: Readthedocs setting file.
    - :code:`build.py`: Build script for Pyinstaller and Sphinx.
    - :code:`Makefile, make.bat`: Sphinx build script.

Dependencies
^^^^^^^^^^^^^^

* `PyPDF2 <https://pypdf2.readthedocs.io/>`_
* `reportlab <https://www.reportlab.com/>`_
* `Pillow <https://pillow.readthedocs.io/en/stable/>`_
* `simpleaudio <https://simpleaudio.readthedocs.io/en/latest/>`_
* `fonttools <https://github.com/fonttools/fonttools>`_
* `tkmacosc <https://pypi.org/project/tkmacosx/>`_: OSX specific dependency

Install the above dependencies with the following command. 

.. code-block:: 

    pip install -r requirements.txt

:code:`simpleaudio` in Ubuntu, requires compilers, build tools, and a
prerequisite library, :code:`libasound2-dev`, to be installed. 
If you are using Ubuntu, you can install :code:`build-essential` from
the Ubuntu repository and install :code:`libasound2-dev` with the
following command.

.. code-block:: 
    
    sudo apt install build-essential libasound2-dev

In Mac, these prerequisites are automatically installed.


Execution with python 
^^^^^^^^^^^^^^^^^^^^^^^^

From the root of project directory,

Command Line Interface
""""""""""""""""""""""""

.. code-block:: 

    python ./booklet/main.py --console {INPUT} {OUTPUTPAHT} {options}

See :ref:`usage <usage_label>` for more detail about thge command line
options.

GUI
""""""""""""""""""

.. code-block:: 

    python ./booklet/main.py 

Building
^^^^^^^^^^^^^^^^^^^^^^^^

This project uses `PyInstaller <https://pyinstaller.org/en/stable/>`_ as
a build tool to generate a standalone executable bundle.
In the root of the project directory, there is a :code:`build.py` file. 
It is a simple python script to initiate the proejct and document build
process with pyinstaller and sphinx.
Install Pyinstaller, before starting the build.

.. code-block::

    pip install requirements_build.txt

Some settings are preconfigured in `build.py`. additional pyinstaller
arguments can be used. See the PyInstaller
`documentation <https://pyinstaller.org/en/stable/>`_.

.. code-block:: 

    python build.py --onefile # one file bundle
    python build.py --onedir # one directory bundle

Build with graphic user interface *with splash image*.

.. code-block:: 

    python build.py --onefile --splash=resources\\splash.png
     

The :code:`--onedir` option add platform name to its directory name.

Add the :code:`--sphinx` option to :code:`build.py` to automatically
build project documentation with sphinx.

.. code-block:: 

    python build.py --onedir --sphinx=html