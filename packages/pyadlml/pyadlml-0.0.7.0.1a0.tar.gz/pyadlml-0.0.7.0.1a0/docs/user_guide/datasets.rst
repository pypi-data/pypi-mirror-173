.. _Dataset user guide:

2. Datasets
***********

.. image:: ../_static/images/datasets.svg
   :height: 200px
   :width: 500 px
   :scale: 100 %
   :alt: alternate text
   :align: center

.. _activity_dataframe:

Usually a dataset is composed of two dataframes, the logged activities and the recorded device readings.
An activity dataframes entry consists of the *start_time*, the *end_time*  and the *activity*
that is being performed.

.. csv-table:: df_activities
   :header: "start_time", "end_time", "activity"
   :widths: 30, 30, 10

    27-12-2020 16:35:13.936,27-12-2020 17:35:23.397,eating
    27-12-2020 17:35:24.021,28-12-2020 03:35:29.806,going_to_bed
    28-12-2020 03:35:32.808,28-12-2020 03:40:36.057,waking_up
    ...

.. _device_dataframe:

A device dataframe entry consists of the *time* a certain *device* reported a
specific *val*\ue. The most common Smart Home devices produce are binary. In addition, pyadlml supports
categorical or numerical device values.

.. csv-table:: df_devices
   :header: "time", "device", "value"
   :widths: 30, 20, 10

    2020-12-27 15:35:08.124228,light.bathroom, False
    2020-12-27 15:45:10.470072,switch bedroom, True
    2020-12-27 17:35:11.961696,temp.sensor 3,13.84
    ...

.. Note::
    Pyadlml supports 8 datasets so far. If you happen to come by a dataset, not included in this `list`_
    feel free to open an issue on github and I am going to add the dataset to the library.


Getting the data
================

A dataset can be loaded by using a function following the schema

.. py:function:: pyadlml.dataset.fetch_datasetname(cache=True, keep_original=False, retain_corrections=False)

   Returns a data object with attributes *df_activities* and *df_devices*


The data object serves as a container for relevant dataset attributes, that may differ
for each dataset. For an exhaustive list and detailed dataset information visit :ref:`datasets <Dataset View>`.
The example below shows the :ref:`amsterdam <amsterdam>` dataset being loaded

.. code:: python

    >>> from pyadlml.dataset import fetch_amsterdam

    >>> data = fetch_amsterdam()
    >>> dir(data)
    [..., df_activities, df_devices, ...]

    >>> print(data.df_devices)
                        time             device  value
    0    2008-02-25 00:20:14  Hall-Bedroom door   True
    1    2008-02-25 00:22:57  Hall-Bedroom door  False
    ...
    2619 2008-03-23 19:04:47          Frontdoor  False
    [2620 rows x 3 columns]

    >>> print(data.df_activities)
                     start_time            end_time        activity
    0   2008-02-25 19:40:26.000 2008-02-25 20:22:58  prepare Dinner
    1   2008-02-25 20:23:12.000 2008-02-25 20:23:35       get drink
    ...
    262 2008-03-21 19:10:36.000 2008-03-23 19:04:58     leave house
    [263 rows x 3 columns]

.. attention::
    Some researchers record activities for multiple inhabitants living in the same Smart Home. The resulting activity dataframes can not be accessed
    through the standard attribute name. Thus, if ``data.df_activities`` returns ``None`` make sure to check the other
    attributes with ``dir(data)``.

    .. code:: python

        from pyadlml.dataset import fetch_aras

        data = fetch_aras()
        dir(data)
        >>> [..., df_activities_subject1, df_activities_subject2, df_devices, ...]

.. _storage_and_cache:

Storage and cache
=================

By default, datasets are stored in the folder where python is executed. Many datasets originally use
different formats to represent device readings and activities. As a result, pyadlml has to transform
these datasets beforehand which may take some time.
By setting the ``fetch_dataset``\s parameter ``cache=True`` the processed dataset is stored as binary file
after an initial fetch and used for all successive loads.
The folder where the data is saved can be selected with

.. code:: python

    from pyadlml.dataset import fetch_aras, set_data_home

    # Set the save-folder to '/path/to/folder' for this session
    set_data_home('/path/to/folder/')

    # The original aras dataset will be saved to '/path/to/folder/aras'
    # The cached version will be saved to '/path/to/folder/somehash'
    data = fetch_aras(cache=True, keep_original=True)


For more methods utilising the data home directory refer to the :ref:`api <todo>`

Coming from activity-assistant
==============================
If you collected your own data using `Activity Assistant`_, the dataset can be loaded
by extracting the ``dataset_name.zip`` file

::

    $ cd /path/to/
    $ unzip dataset_name.zip
    $ ls /path/to/dataset_name
      devices.csv
      device_mapping.csv
      activities_chris.csv
      activity_mapping.csv


and pointing pyadlml to the folder containing the zip's content:

.. code:: python

    from pyadlml.dataset import load_act_assist

    data = load_act_assist('/path/to/dataset_name/', subjects=['chris'])

.. note::
    Activity Assistant creates an activity file using the naming convention ``activities_[subject_name].csv``.
    Pyadlml loads the activity dataframe into the attribute ``data.df_activities_[subject_name]``.

.. _error_correction:

Data cleaning
=============


Automatic correction
~~~~~~~~~~~~~~~~~~~~

In order to correctly compute all summary statistics or data transformations, pyadlml places some
constraints on how an activity and device dataframe ought to look like. For example activity intervals are not
allowed to overlap, devices should not trigger at exactly the same moment and directly succeeding binary device
triggers have to differ. Since some datasets are in a rather desolate state, the ``fetch_dataset`` method already
cleans the data beforehand. To offer transparency on what values are altered, passing
the parameter ``retain_correction=True`` to the ``fetch_dataset`` method, stores activity- as well
as device-corrections in the ``data`` objects attributes.

Activity correction
^^^^^^^^^^^^^^^^^^^

Altered activity entries can be accessed by the attribute ``data.correction_activities``.
The list contains tuples, where the first item is a list of affected activities before
and the second item after the correction.

.. code:: python

    >>> from pyadlml.dataset import fetch_uci_adl_binary
    >>> data = fetch_uci_adl_binary(subject='OrdonezB', retain_corrections=True)
    >>> dir(data)
    [..., correction_activities_OrdonezB, ...]

    >>> print(len(data.data.correction_activities_OrdonezB))
    23

    >>> # Overlapping activities before correction
    >>> print(data.correction_activities_OrdonezB[0][0])
                start_time            end_time   activity
    69 2012-11-14 00:28:00 2012-11-14 00:29:59  Toileting
    70 2012-11-14 00:29:00 2012-11-14 05:12:59   Sleeping

    >>> # Corrected activities as present in the data.df_activities
    >>> print(data.correction_activities_OrdonezB[0][1])
                   start_time            end_time   activity
    0 2012-11-14 00:28:00.000 2012-11-14 00:29:00  Toileting
    1 2012-11-14 00:29:00.001 2012-11-14 05:12:59   Sleeping


Device correction
^^^^^^^^^^^^^^^^^

Devices are corrected by dropping duplicate entries, altering entries where the timestamps
coincide and disregarding equal pairwise succeeding values of binary devices.
When timestamps of two entries are the same, one of the two entries is randomly chosen
and a small offset is added onto the timestamp. Device entries with altered timestamps
can be accessed by the attribute ``data.correction_devices_duplicate_timestamp``.
When a binary device, reports the same value in direct succession, the redundant entry is
dropped. The disregarded rows can be accessed with the attribute ``data.correction_devices_on_off_inconsistency``.

.. code:: python

    >>> # print the dropped entries where binary device activation was inconsistent
    >>> print(data.correction_devices_on_off_inconsistency)
                            time           device  value
    274  2012-11-12 22:34:27.000  Living Door PIR  False
    302  2012-11-12 23:45:08.000  Living Door PIR  False
    1732 2012-11-19 15:52:33.000  Living Door PIR   True
    4668 2012-11-12 22:34:27.010  Living Door PIR  False
    4669 2012-11-12 23:45:08.010  Living Door PIR  False
    4670 2012-11-19 15:52:33.010  Living Door PIR   True

    >>> # print the entries where the timestamps were altered
    >>> print(data.correction_devices_duplicate_timestamp)
                        time                device  value
    4027 2012-11-30 12:56:27  Living Seat Pressure   True
    4129 2012-12-01 00:04:58  Living Seat Pressure  False


Datasets
~~~~~~~~

Although the automatic correction applies heuristics to correct the most impactful inconsistencies, some dataset
require additional cleaning. Recording correct and meaningful data is `hard`_. For example, if one device
event is neglected a wrong state for that device may be assumed for days. In addition, days without
the inhabitant recording any activities may occur. Many or long gaps between recordings are not an issue
if the dataset is used for unsupervised or semi-supervised learning.
However, as the package's described goal is supervised learning a reduced activity coverage is undesirable.
For these reasons, each ``fetch_dataset`` method comes with the parameter ``load_cleaned`` that,
if set, downloads a cleaned version of the dataset. Since the cleaning process is opinionated
the steps are recorded for reproduction and transparency in jupyter. Be sure to take a look at the `notebooks`_.
All evaluations and model rankings reported in this `project`_ are based on the cleaned datasets.
When training and evaluating supervised models, the cleaned datasets are the recommended way to start:


.. code:: python

    >>> from pyadlml.dataset import fetch_casas_aruba
    >>> data = fetch_casas_aruba(load_cleaned=True)


Tools
~~~~~

To aid the data cleaning process, pyadlml ships a few methods that ease wrangling. For example,
to select a specific timespan type

.. code:: python

    >>> from pyadlml.dataset.utils import select_timespan
    >>> df_dev, df_act = select_timespan(data.df_devices, data.df_activities,\
    >>> start_time='28.90.1298', end_time='28.90.1298')

The ``remove_days`` method can be used to exclude days and correctly shift succeeding activities and device readings
to close the gaps:

.. code:: python

    >>> from pyadlml.dataset.utils import remove_days

    >>> # removes the given days and shifts all succeeding activities and events by one day
    >>> # in order to close the emerging gaps
    >>> df_dev, df_act = remove_days(data.df_devices, data.df_activities, days=['28.90.1298', '28.90.1298'])


.. _list: https://todo_link_to_datasets
.. _notebooks: https://github.com/tcsvn/pyadlml/notebooks/
.. _Activity Assistant: https://github.com/tcsvn/activity-assistant
.. _project: https://TODO
.. _hard: https://github.com/tscvn/pyadlml/notebooks/tuebingen_2019.ipynb