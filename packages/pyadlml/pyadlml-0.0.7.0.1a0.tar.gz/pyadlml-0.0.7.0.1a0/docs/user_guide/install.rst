1. Installation
***************

Pyadlml can be installed with ``pip`` or from `source`_.

Pip
~~~

The setup is pretty straight forward. At the command line type

::

    $ python -m pip install pyadlml

This will install all dependencies that are required to use every functionality offered
by pyadlml. For this reason, it is the recommended way to get started for developers.
Since this installation method downloads a large number of packages, there are
other dependency sets for different subsets of functionality:

::

    $ python -m pip install "pyadlml[light]"    # dataloading, statistics, pipeline, preprocessing and feature_extraction
    $ python -m pip install "pyadlml[datavis]"  # light's functionality and visualization

The minimal installation option ``light`` includes dataset loading utilities (``pyadlml.dataset``),
statistics (``pyadlml.stats``), the pipeline (``pyadlml.pipeline``) as well as preprocessing
(``pyadlml.preprocessing``) and feature extraction functionalities (``pyadlml.feature_extraction``).

The ``datavis`` option includes everything but the models (``pyadlml.models``).


Github
~~~~~~
As the `pipy`_ repository may lag behind, the latest version can be installed directly from `github`_ with

::

    $ git clone https://github.com/tcsvn/pyadlml
    $ cd pyadlml
    $ pip install .



.. _source: https://github.com/tcsvn/pyadlml
.. _github: https://github.com/tcsvn/pyadlml
.. _pipy: https://pypi.python.org/pypi/pyadlml/
