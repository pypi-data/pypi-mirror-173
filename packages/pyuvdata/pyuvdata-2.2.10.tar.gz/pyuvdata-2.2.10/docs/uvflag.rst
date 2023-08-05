UVFlag
======
UVFlag is a main user class that is still in the development and
beta-testing phase, which holds metadata and data related to flagging and
metric information for interferometric data sets. It provides import and
export functionality to and from all file formats supported by
:class:`pyuvdata.UVData` and :class:`pyuvdata.UVCal` objects as well as an
HDF5 file format specified by this object.
It supports three different "shapes" of data (all with time and frequency
axes): visibility based, antenna based, and waterfall (a single value for
the entire array at each time and frequency).
It has methods for transforming the data between different shapes and 
converting metrics to flags, and can be interacted with directly.

Attributes
----------
The attributes on UVFlag hold all of the metadata and data required to
specify flagging and metric information for interferometric data sets.
Under the hood, the attributes are implemented as properties based on
:class:`pyuvdata.parameter.UVParameter` objects but this is fairly
transparent to users.

UVFlag objects can be initialized from a file or a :class:`pyuvdata.UVData`
or :class:`pyuvdata.UVCal` object
(as ``flag = UVFlag(<filename or object>)``). Some of these attributes
are `required`_ to be set to have a fully defined data set while others are
`optional`_. The :meth:`pyuvdata.UVFlag.check` method can be called on the
object to verify that all of the required attributes have been set in a
consistent way.

Required
********
These parameters are required to have a sensible UVFlag object and 
are required for most kinds of uv data files.

**Nants_data**
     Number of antennas with data present. Only available for "baseline" or "antenna" type objects.May be smaller than the number of antennas in the array

**Nants_telescope**
     Number of antennas in the array. Only available for "baseline" type objects. May be larger than the number of antennas with data.

**Nbls**
     Number of baselines. Only Required for "baseline" type objects.

**Nblts**
     Number of baseline-times (i.e. number of spectra). Not necessarily equal to Nbls * Ntimes

**Nfreqs**
     Number of frequency channels

**Npols**
     Number of polarizations

**Nspws**
     Number of spectral windows (ie non-contiguous spectral chunks). More than one spectral window is not currently supported.

**Ntimes**
     Number of times

**ant_1_array**
     Array of first antenna indices, shape (Nblts). Only available for "baseline" type objects. type = int, 0 indexed

**ant_2_array**
     Array of second antenna indices, shape (Nblts). Only available for "baseline" type objects. type = int, 0 indexed

**baseline_array**
     Array of baseline indices, shape (Nblts). Only available for "baseline" type objects. type = int; baseline = 2048 * (ant1+1) + (ant2+1) + 2^16

**freq_array**
     Array of frequencies, center of the channel, shape (Nspws, Nfreqs), units Hz

**history**
     String of history, units English

**label**
     String used for labeling the object (e.g. 'FM'). Default is empty string.

**lst_array**
     Array of lsts, center of integration, shape (Nblts), units radians

**metric_array**
     Floating point metric information, only availble in metric mode. shape (Nblts, Nspws, Nfreq, Npols).

**mode**
     The mode determines whether the object has a floating point metric_array or a boolean flag_array. Options: {"metric", "flag"}. Default is "metric".

**polarization_array**
     Array of polarization integers, shape (Npols). AIPS Memo 117 says: pseudo-stokes 1:4 (pI, pQ, pU, pV);  circular -1:-4 (RR, LL, RL, LR); linear -5:-8 (XX, YY, XY, YX). NOTE: AIPS Memo 117 actually calls the pseudo-Stokes polarizations "Stokes", but this is inaccurate as visibilities cannot be in true Stokes polarizations for physical antennas. We adopt the term pseudo-Stokes to refer to linear combinations of instrumental visibility polarizations (e.g. pI = xx + yy).

**time_array**
     Array of times, center of integration, shape (Nblts), units Julian Date

**type**
     The type of object defines the form of some arrays  and also how metrics/flags are combined. Accepted types:"waterfall", "baseline", "antenna"

**weights_array**
     Floating point weight information, shape (Nblts, Nspws, Nfreq, Npols).

Optional
********
These parameters are defined by one or more type but are not always required.
Some of them are required depending on the type (as noted below).

**ant_array**
     Array of antenna numbers, shape (Nants_data), Only available for "antenna" type objects. type = int, 0 indexed

**extra_keywords**
     Any user supplied extra keywords, type=dict.Use the special key 'comment' for long multi-line string comments.Default is an empty dictionary.

**filename**
     List of strings containing the unique basenames (not the full path) of input files.

**flag_array**
     Boolean flag, True is flagged, only availble in flag mode. shape (Nblts, Nspws, Nfreq, Npols).

**weights_square_array**
     Floating point weight information about sum of squares of weights when weighted data converted from baseline to waterfall  mode.

**x_orientation**
     Orientation of the physical dipole corresponding to what is labelled as the x polarization. Options are "east" (indicating east/west orientation) and "north" (indicating north/south orientation)

Methods
-------
.. autoclass:: pyuvdata.UVFlag
  :members:

last updated: 2022-07-30