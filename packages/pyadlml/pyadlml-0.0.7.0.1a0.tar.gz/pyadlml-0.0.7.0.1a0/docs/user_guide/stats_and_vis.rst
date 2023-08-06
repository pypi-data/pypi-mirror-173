3. Statistics and Visualization
*******************************

.. image:: ../_static/images/statistics.svg
   :height: 80px
   :width: 300 px
   :scale: 200 %
   :alt: alternate text
   :align: center

Understanding a datasets structure and assessing its quality is necessary for the successful
adaption of machine learning models. Pyadlml supports various methods for the calculation
and visualization of dataset statistics. Since most graphs correspond to a particular statistic,
the following sections lists them jointly. In addition, some visualizations have a corresponding
interactive version, that are indicated. Finally, a dashboard provides the means for
efficient and interactive data exploration.

Methods for calculating statistics can be imported from
the ``pyadlml.stats``, generating plots from the ``pyadlml.plot`` and interactive plots
from ``pyadlml.plotly`` module. The dashboard is located in the example folder of the
github repo. The :ref:`amsterdam <Amsterdam>` dataset is used for all
the following examples.

.. code:: python

    >>> from pyadlml.dataset import fetch_amsterdam
    >>> data = fetch_amsterdam()


Activities
==========

Count
~~~~~

Get the total count a person performed a specific activity with

.. code:: python

    >>> from pyadlml.stats import activity_count
    >>> activity_count(data.df_activities)
                activity  occurrence
    0          get drink         19
    1          go to bed         47
    2        leave house         33
    3  prepare Breakfast         19
    4     prepare Dinner         12
    5        take shower         22
    6         use toilet        111

    >>> from pyadlml.plot import plot_activity_bar_count
    >>> plot_activity_bar_count(data.df_activities, idle=True);

.. image:: ../_static/images/plots/act_bar_cnt.png
   :height: 300px
   :width: 500 px
   :scale: 90 %
   :alt: alternate text
   :align: center


.. Note::
    In almost every dataset gaps exist between activities where device readings are
    recorded but a corresponding activity label is missing. In order to retain a cohesive
    sequence the *idle* activity can be used to fill the activity gaps [#f1]_. To include
    the *idle* activity in the statistics pass the parameter ``idle=True`` to the respective method.

Duration
~~~~~~~~

Compute the total time an inhabitant spent performing an activity with:

.. code:: python

    >>> from pyadlml.stats import activity_duration
    >>> activity_duration(data.df_activities)
                activity       minutes
    0          get drink     16.700000
    1          go to bed  11070.166267
    2        leave house  22169.883333
    3  prepare Breakfast     63.500000
    4     prepare Dinner    338.899967
    5        take shower    209.566667
    6         use toilet    195.249567

    >>> from pyadlml.plots import plot_activity_bar_duration
    >>> plot_activity_bar_duration(data.df_activities)

.. image:: ../_static/images/plots/act_bar_dur.png
   :height: 300px
   :width: 500 px
   :scale: 90 %
   :alt: alternate text
   :align: center

or use a boxplot to obtain information about the activities distribution

.. code:: python

    from pyadlml.plots import plot_devices_bp_duration

    plot_devices_bp_duration(data.df_activities)

.. image:: ../_static/images/plots/act_bp.png
   :height: 300px
   :width: 500 px
   :scale: 90 %
   :alt: alternate text
   :align: center

Note, the inhabitant seems to sleep on average :math:`3` hours. This activity duration appears to be rather short.
However, the transition matrix below reveals the activity *going to bed* is often followed by *using toilet*
and vice versa. Consequently the mistery is solved.

Transition
~~~~~~~~~~

Compute a transition matrix that displays how often one activity is followed
by another

.. code:: python

    >>> from pyadlml.stats import activity_transition

    >>> activity_transition(data.df_activities)
    act_after          get drink  go to bed  ...  use toilet
    activity
    get drink                  3          0  ...          15
    go to bed                  0          0  ...          43
    leave house                3          1  ...          22
    prepare Breakfast          1          0  ...           8
    prepare Dinner             7          0  ...           4
    take shower                0          0  ...           1
    use toilet                 5         46  ...          18

A matrices entry :math:`c_{ij}` represents how often activity :math:`i` is followed
by activity :math:`j`.
In the above example the inhabitant visits the toilet 43 times after he goes to bed.
The matrix can also be visualized as a heatmap:

.. code:: python

    from pyadlml.plots import plot_activity_hm_transitions

    plot_activity_hm_transitions(data.df_activities)

.. image:: ../_static/images/plots/act_hm_trans.png
   :height: 300px
   :width: 500 px
   :scale: 90 %
   :alt: alternate text
   :align: center


Density
~~~~~~~

Different activities are more probable during certain times of the day. For example the
activity *breakfast* is more likely to be performed in the morning whereas the activity *going
to bed* usually occurs in the evening. Pyadlml offers a way to approximate the activity density
over one day with monte-carlo sampling:

.. code:: python

    >>> from pyadlml.stats import activities_dist
    >>> activities_dist(data.df_activities, n=1000)
             prepare Dinner           get drink ...         leave house
    0   1990-01-01 18:12:39 1990-01-01 21:14:07 ... 1990-01-01 13:30:33
    1   1990-01-01 20:15:14 1990-01-01 20:23:31 ... 1990-01-01 12:03:13
    ..                      ...                 ...                 ...
    999 1990-01-01 18:16:27 1990-01-01 08:49:38 ... 1990-01-01 16:18:25

    >>> from pyadlml.plots import plot_activity_ridgeline
    >>> plot_activity_ridgeline(data.df_activities)

.. image:: ../_static/images/plots/act_ridge_line.png
   :height: 300px
   :width: 500 px
   :scale: 90 %
   :alt: alternate text
   :align: center


Devices
=======

There are two perspectives on the devices recordings in a Smart Home environment.
First, you can look at the states of the binary, categorical and numerical devices
for a fixed point in time.
Second, by taking only a look at when devices activations happen. The devices jointly
produce an event stream. In neuroscience the related concept of spike trains is studied.
Pyadlml borrows a few techniques from spike train analysis to provide insights on events from
Smart Home devices.


States
~~~~~~

To get an overview over all device states over the period of an experiment use

.. code:: python

    >>> from pyadlml.plots import plot_device_states
    >>> plot_device_states(data.df_devices)

.. image:: ../_static/images/plots/dev_states.png
   :height: 800px
   :width: 2000 px
   :scale: 50 %
   :alt: alternate text
   :align: center

.. warning::
    Matplotlib renders the vertical bars representing the device states at a certain resolution.
    If a device adopts a state for a timespan lesser than the smallest depictable step,
    that state will not appear in the plot. Consequently, a plot not showing certain device states
    does not imply the device never to adopt these states (e.g ``Plates cupboard`` , ``ToiletFlush``, ...
    in the above plot).
    Therefore, it is recommended to look at other plots/statistics in addition to get a
    graps of what is happening. By selecting a smaller time-frame these activations may show up:

    .. code:: python

        >>> plot_device_states(data.df_devices, selected_timespan=['12.08.2008', '13.08.2008'])



Fraction
^^^^^^^^

Compute the time and fraction a device is in a certain state. Binary devices are divided
into *on* and *off* states. For categorical devices the respective categories are computed

.. code:: python

    >>> from pyadlml.stats import device_fractions
    >>> device_fractions(data.df_devices)
                    device                  td_on                  td_off   frac_on  frac_off
    0        Cups cupboard 0 days 00:10:13.010000 27 days 18:34:19.990000  0.000255  0.999745
    1           Dishwasher        0 days 00:55:02        27 days 17:49:31  0.001376  0.998624
    ...                ...                    ...                     ...        ...      ...
    13      Washingmachine        0 days 00:08:08        27 days 18:36:25  0.000203  0.999797

    >>> from pyadlml.plots import plot_device_state_fraction
    >>> plot_device_state_fraction(data.df_devices)

.. image:: ../_static/images/plots/dev_on_off.png
   :height: 300px
   :width: 500 px
   :scale: 100 %
   :alt: alternate text
   :align: center

The distribution for each state can be visualized using a boxplot and passing the respective state as parameter

.. code:: python

    from pyadlml.plots import plot_device_state_dist

    plot_device_state_dist(data.df_devices, binary_state='on', categorical_state=[('device', 'cat1')])

.. image:: ../_static/images/plots/dev_bp_dur.png
   :height: 300px
   :width: 500 px
   :scale: 90 %
   :alt: alternate text
   :align: center

State Cross-Correlation
^^^^^^^^^^^^^^^^^^^^^^^

Similarity between devices states may offer insights in how useful some devices are, since uncorrelated device states provide a more robust basis for machine learning algorithms. To
get an intuition how much a devices state :math:`g` resembles another :math:`f`
over time, the cross correlation can be computed with


.. math::
    C_{f,g}(\tau) = \frac{1}{T}\int g(t)\cdot f(t-\tau)dt  \text{ with } \tau=0, f(t),g(t)\in \{-1,1\}\\
    \text{and } f,g \text{ is Boolean } : \text{off} \rightarrow -1, \text{on} \rightarrow 1\\
    \text{and } f,g \text{ is Categorical } : \text{cat not present} \rightarrow -1, \text{cat present} \rightarrow 1


The equation above shows the cross-correlation being a function of :math:`\tau`. By evaluating the function for a
range of :math:`\tau`, properties such as periodic similarity can be discovered.
However, the following statistic's target is to compare signals only at their unshifted state. Therefore,
the time-lag is set to :math:`\tau = 0` resulting in a single reported value for each device
combination. A binary device will map the state "on":math:`\rightarrow 1` and "off":math:`\rightarrow -1`.
Categorical devices are split into their categories, where each category maps to the value 1 if present or -1 if not.
Consequently, two devices having an identical device activation yield a correlation of :math:`1` and
one being the inverse of the other a :math:`-1`. Devices that TODO and neutral :math:`0`.


.. code:: python

    >>> from pyadlml.stats import device_duration_corr
    >>> device_duration_corr(data.df_devices)
    device              Cups cupboard  Dishwasher  ...  Washingmachine
    device                                         ...
    Cups cupboard            1.000000    0.997571  ...        0.999083
    Dishwasher               0.997571    1.000000  ...        0.996842
    ...
    Washingmachine           0.999083    0.996842  ...        1.000000
    [14 rows x 14 columns]

    >>> from pyadlml.plots import plot_device_cross_correlation_states
    >>> plot_device_cross_correlation_states(data.df_devices)

.. image:: ../_static/images/plots/dev_hm_dur_cor.png
   :height: 400px
   :width: 500 px
   :scale: 90 %
   :alt: alternate text
   :align: center

.. note::

    Note that categories for a categorical device with more than two categories will always be somehow similar to each other
    as only one category can be present at a moment in time. Therefore it makes only sense to relate other devices
    to the categorical device and not the categories within a device.

The heatmap above shows most devices are in the same state at the same time. This is not
surprising as most devices are *off* the whole time (TODO link). Note this does not apply to the *Microwave*,
that seems to be *on* a long time when other devices are *off*. However this is unlikely as a *Microwave* usually
is *on* only for a small amount of time. This artefact hints at a mistake in the data collection process.
The *Microwave* erroneous state is corrected in the data cleaning notebook (link). More on cleaned datasets
can be read in the (TODO link to section). This example illustrates that it is important to sanity-check the data to
quickly identify if something went wrong during the collection process.


Events
~~~~~~

.. image:: ../_static/images/event_train.svg
   :height: 100px
   :width: 300 px
   :scale: 90 %
   :alt: alternate text
   :align: center

A useful way to look at device data is in form of event trains. Hereby only the time of the event and the
causing device are considered whereas the value produced at that event is neglected. The following
plot visualizes all events over the whole duration of the experiment:

.. code:: python

    >>> from pyadlml.plot import plot_device_event_raster
    >>> plot_device_event_raster(data.df_devices)

.. image:: ../_static/images/plots/dev_raster.png
   :height: 300px
   :width: 500 px
   :scale: 90 %
   :alt: alternate text
   :align: center


Event counts
^^^^^^^^^^^^
Compute the total amount of events produced per device

.. code:: python

    >>> from pyadlml.stats import device_trigger_count
    >>> device_trigger_count(data.df_devices)
                    device  trigger_count
    0        Cups cupboard             98
    1           Dishwasher             42
    ..                 ...            ...
    13      Washingmachine             34

    >>> from pyadlml.plots import plot_device_bar_count
    >>> plot_device_bar_count(data.df_devices)

.. image:: ../_static/images/plots/dev_bar_trigger.png
   :height: 300px
   :width: 500 px
   :scale: 90 %
   :alt: alternate text
   :align: center

Inter-event-Intervals
^^^^^^^^^^^^^^^^^^^^^
An inter-event interval is defined as the time passed between a pair of succeeding events.
To compute the inter-event distribution in seconds use

.. code:: python

    >>> from pyadlml.stats import device_time_diff

    >>> device_time_diff(data.df_devices)
    array([1.63000e+02, 3.30440e+04, 1.00000e+00, ..., 4.00000e+00,
           1.72412e+05, 1.00000e+00])

    >>> from pyadlml.plot import plot_device_iei

    >>> plot_device_iei(data.df_devices, todo=['3s', '10s'])


.. image:: ../_static/images/plots/dev_hist_trigger_td.png
   :height: 300px
   :width: 500 px
   :scale: 100 %
   :alt: alternate text
   :align: center

.. note::
    In the illustration above some events fall into the ~ :math:`5ms` bin. This may be an artefact
    as the automatic device correction offsets an event by that amount of time, if both events originally happen exactly at the same time.


Event density
^^^^^^^^^^^^^

Since activities are thought of as the generating process behind events and
certain activities are more probable during certain times of the day,
plotting the event density over the course of one day may offer useful insights.
A day can be discretized into bins of length :math:`dt` with

.. code:: python

    >>> from pyadlml.stats import device_event_density_one_day
    >>> device_trigger_one_day(data.df_devices, dt='1h')

    device    Cups cupboard  Dishwasher   ...  Washingmachine
    time                                  ...
    00:00:00            0.0         0.0   ...             0.0
    01:00:00           16.0         0.0   ...             0.0
    ...
    23:00:00            6.0         8.0   ...             2.0

    >>> from pyadlml.plots import plot_device_event_density
    >>> plot_device_event_density(data.df_devices, dt='1h')

.. image:: ../_static/images/plots/dev_hm_trigger_one_day.png
   :height: 300px
   :width: 500 px
   :scale: 100 %
   :alt: alternate text
   :align: center

Cross-correlogram
^^^^^^^^^^^^^^^^^

To relate events to each other one event is fixed and the number of succeeding events that fall
into a certain time-lag are counted. These events are called coincidence events.
Devices are represented as time-dependent functions :math:`\#g(t)` and :math:`f(t)`
the Cross-correlogram is thus defined as


.. math::
    C(\tau) = \frac{1}{\#g()}\sum_{t=-\infty}^{\infty} g(t+\tau)f(t)


Peaks in the correlogram are typically interpreted as evidence of event timing synchronization.
As the time-scales for device events may vastly vary as some devices may fire with a frequency
of days and some in the millisecond range a time span of interest has to be given as parameter ``lag_range``

.. code:: python

    >>> from pyadlml.stats import device_event_cross_correlogram
    >>> from pyadlml.plot import plot_device_event_cross_correlogram

    # only select a subset in order to present an uncluttered plot
    >>> df_devs_sub = df_devs[df_devs[DEVICE].isin(['Hall-Bedroom door', 'Hall-Toilet door', 'Hall-Bathroom door', 'ToiletFlush' 'Plates cupboard', 'Fridge', 'Microwave', 'Groceries Cupboard'])]

    # returns an array of #devices #devices #bins and the bins
    >>> cc, bins = device_event_cross_correlogram(df_devs_sub, binsize='2s', max_lag='2min')
    >>> print(cc.shape, bins.shape)
    (6,6,120), (120,)

    >>> plot_device_event_cross_correlogram(df_devs_sub, binsize='2s', max_lag='2min')

.. image:: ../_static/images/plots/dev_event_cc.png
   :height: 400px
   :width: 500 px
   :scale: 90 %
   :alt: alternate text
   :align: center


To get solely the crosscorrelation for a certain time-lag :math:`\tau` the following plot can be utilized.
The plot is a slice through the correlogram above where :math:`\tau` controls the time-lag.

.. code:: python

    >>> from pyadlml.plot import plot_device_event_cross_correlogram_slice
    >>> plot_device_event_cross_correlogram_slice(data.df_devices, tau='2s')

.. image:: ../_static/images/plots/dev_hm_trigger_sw.png
   :height: 400px
   :width: 500 px
   :scale: 90 %
   :alt: alternate text
   :align: center

.. note:: Grey fields should be are indicator of negative infinity when using the ``z_scale=log`` and are
    presented as having no value for better visual bla.

Activites and devices
=====================

The co-occurrence of device events and activities is off particular interest as models are trying
to learn exactly this relationship. The section is divided into plots relating the device states or the events with activities.


State
~~~~~

To get an view over all states use

.. code:: python

    >>> from pyadlml.plots import plot_act_and_dev_states
    >>> plot_act_and_dev_states(data.df_devices, grid=True)

.. image:: ../_static/images/plots/states.png
   :height: 800px
   :width: 2000 px
   :scale: 50 %
   :alt: alternate text
   :align: center


States ~ Activities
^^^^^^^^^^^^^^^^^^^

To show what state a device is usually in during an activity type

.. code:: python

    >>> from pyadlml.stats import contingency_states
        >>> from pyadlml.plot import plot_contingency_states

        >>> contingency_states(data.df_devices, data.df_activities)
        activity                     get drink ...             use toilet
        Hall-Bedroom door Off  0 days 00:01:54 ... 0 days 00:12:24.990000
        Hall-Bedroom door On   0 days 00:14:48 ... 0 days 03:02:49.984000
        ...                                ...
        Washingmachine On      0 days 00:00:00 ...        0 days 00:00:00
        [28 rows x 7 columns]

        >>> contingency_states(data.df_devices, data.df_activities)
        >>> from pyadlml.plot import plot_contingency_states

        >>> contingency_states(data.df_devices, data.df_activities)
        activity                     get drink ...             use toilet
        Hall-Bedroom door Off  0 days 00:01:54 ... 0 days 00:12:24.990000
        Hall-Bedroom door On   0 days 00:14:48 ... 0 days 03:02:49.984000
        ...                                ...
        Washingmachine On      0 days 00:00:00 ...        0 days 00:00:00
        [28 rows x 7 columns]

        >>> contingency_states(data.df_devices, data.df_activities)
    >>> from pyadlml.plot import plot_contingency_states

    >>> contingency_states(data.df_devices, data.df_activities)
    activity                     get drink ...             use toilet
    Hall-Bedroom door Off  0 days 00:01:54 ... 0 days 00:12:24.990000
    Hall-Bedroom door On   0 days 00:14:48 ... 0 days 03:02:49.984000
    ...                                ...
    Washingmachine On      0 days 00:00:00 ...        0 days 00:00:00
    [28 rows x 7 columns]

    >>> plot_contingency_states(data.df_devices, data.df_activities)

.. image:: ../_static/images/plots/cont_hm_duration.png
   :height: 300px
   :width: 800 px
   :scale: 90 %
   :alt: alternate text
   :align: center

Events
~~~~~~

To assess the dataset with one glance plot the events and activities over time with

.. code:: python

    >>> from pyadlml.plot import plot_activities_vs_devices

    >>> plot_activities_vs_devices(data.df_devices, data.df_activities)

.. image:: ../_static/images/plots/raster.png
   :height: 800px
   :width: 2000 px
   :scale: 50 %
   :alt: alternate text
   :align: center

This plot is probably the most useful one, as with one glance important information can be retrieved.
The most dominant activities in this example are *leave_house* and *go_to_bed*. The device events frequency
as well as regularities in activation can be retrieved. The above example shows the *washing_machine* to be
turned on every two weeks and only 5 times in the whole recorded dataset. On the other hand the *toilet_flush* triggers
on a daily bases. Furthermore some during some activities some devices don't fire.
For example when an inhabitant leaves the house no activity occurs at all. Most of data cleaning can be done
using solely this plot.


Events ~ Activities
^^^^^^^^^^^^^^^^^^^

The following code shows how to compute triggers happening during different activities.

.. code:: python

    >>> from pyadlml.stats import contingency_events

        >>> contingency_events(data.df_devices, data.df_activities)
        activity                     get drink ...             use toilet
        Hall-Bedroom door Off  0 days 00:01:54 ... 0 days 00:12:24.990000
        Hall-Bedroom door On   0 days 00:14:48 ... 0 days 03:02:49.984000
        ...                                ...
        Washingmachine On      0 days 00:00:00 ...        0 days 00:00:00
        [28 rows x 7 columns]

        >>> from pyadlml.plot import contingency_events
        >>> plot_contingency_events(data.df_devices, data.df_activities)

        >>> contingency_events(data.df_devices, data.df_activities)
        activity                     get drink ...             use toilet
        Hall-Bedroom door Off  0 days 00:01:54 ... 0 days 00:12:24.990000
        Hall-Bedroom door On   0 days 00:14:48 ... 0 days 03:02:49.984000
        ...                                ...
        Washingmachine On      0 days 00:00:00 ...        0 days 00:00:00
        [28 rows x 7 columns]

        >>> from pyadlml.plot import contingency_events
        >>> plot_contingency_events(data.df_devices, data.df_activities)

    >>> contingency_events(data.df_devices, data.df_activities)
    activity                     get drink ...             use toilet
    Hall-Bedroom door Off  0 days 00:01:54 ... 0 days 00:12:24.990000
    Hall-Bedroom door On   0 days 00:14:48 ... 0 days 03:02:49.984000
    ...                                ...
    Washingmachine On      0 days 00:00:00 ...        0 days 00:00:00
    [28 rows x 7 columns]

    >>> from pyadlml.plot import plot_contingency_events
    >>> plot_contingency_events(data.df_devices, data.df_activities)

.. image:: ../_static/images/plots/cont_hm_trigger.png
   :height: 300px
   :width: 500 px
   :scale: 100 %
   :alt: alternate text
   :align: center

The next plot takes in addition to the device events, the state of the device at that event into account.
This would e.g show devices that turn *on* but not *off* during a specific activity.

.. code:: python

    >>> from pyadlml.stats import plot_contingency_events

    >>> plot_contingency_events(data.df_devices, data.df_activities, by_state=True)
    activity                     get drink ...             use toilet
    Hall-Bedroom door Off  0 days 00:01:54 ... 0 days 00:12:24.990000
    Hall-Bedroom door On   0 days 00:14:48 ... 0 days 03:02:49.984000
    ...                                ...
    Washingmachine On      0 days 00:00:00 ...        0 days 00:00:00
    [28 rows x 7 columns]

    >>> from pyadlml.plot import plot_hm_contingency_trigger_01
    >>> plot_hm_contingency_trigger_01(data.df_devices, data.df_activities)

.. image:: ../_static/images/plots/cont_hm_trigger_01.png
   :height: 300px
   :width: 500 px
   :scale: 100 %
   :alt: alternate text
   :align: center

Cross-correlogram
^^^^^^^^^^^^^^^^^

The next plot captures events that may not be present during an activity but fire before or after an activity occurs.
Those events may be important to models using the sequential data whereas iid models would neglect the additional
information. Fixing one activity only events that fall into a certain time-lag before the activity starts as
well as events that occur after the activity ends are counted. Therefore the histogramm
As the spread of events varies a lot the lag of interest (loi) has to be passed as a parameter. Choosing a lag
of ``1min`` includes events that fall into that time range.

.. code:: python

    >>> from pyadlml.stats import cross_correlogram

    >>> cross_correlogram(data.df_devices, data.df_activities, loi='1m')
    activity                     get drink ...             use toilet
    Hall-Bedroom door Off  0 days 00:01:54 ... 0 days 00:12:24.990000
    Hall-Bedroom door On   0 days 00:14:48 ... 0 days 03:02:49.984000
    ...                                ...
    Washingmachine On      0 days 00:00:00 ...        0 days 00:00:00
    [28 rows x 7 columns]

    >>> from pyadlml.plot import plot_cross_correlogram
    >>> plot_cross_correlogram(data.df_devices, data.df_activities)

.. image:: ../_static/images/plots/dev_event_cc.png
   :height: 300px
   :width: 500 px
   :scale: 100 %
   :alt: alternate text
   :align: center

TODO interpretation of plot

Dashboard
=========

An interactive dashboard.

.. image:: ../_static/images/dashboard.png
   :height: 936px
   :width: 918 px
   :scale: 60 %
   :alt: alternate text
   :align: center


ther is::

    $ git clone https://github.com/tcsvn/pyadlml
    $ cd pyadlml
    $ python3 examples/dash_board.py --dataset kasteren_C


Theming
=======

There are global options to set the color and colormaps of the plots.

.. code:: python

    from pyadlml.dataset import set_primary_color, set_secondary_color

    set_primary_color("#1234567")
    set_secondary_color("#1234567")

You can set global values for diverging and converging colormaps.

.. code:: python

    from pyadlml.dataset import set_converging_cmap, set_diverging_cmap

    set_primary_color()


.. rubric:: Sources

.. [#f1] Kasteren et al. 2010 (TODO)