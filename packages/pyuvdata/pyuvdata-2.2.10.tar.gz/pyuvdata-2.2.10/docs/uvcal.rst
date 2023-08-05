UVCal
=====
UVCal is the main user class for calibration solutions for interferometric
data sets. It provides import and export functionality to and from the
supported file formats (calfits, FHD) as well as methods for transforming
the data (converting types, selecting, sorting) and can be interacted with
directly.

Attributes
----------
The attributes on UVCal hold all of the metadata and data required to
work with calibration solutions for interferometric data sets. Under the
hood, the attributes are implemented as properties based on
:class:`pyuvdata.parameter.UVParameter` objects but this is fairly
transparent to users.

UVCal objects can be initialized as an empty object (as ``cal = UVCal()``).
When an empty UVCal object is initialized, it has all of these attributes
defined but set to ``None``. The attributes can be set by reading in a data
file using the :meth:`pyuvdata.UVCal.read_calfits` or
:meth:`pyuvdata.UVCal.read_fhd_cal` methods or by setting them directly on
the object. Some of these attributes are `required`_ to be set to have a
fully defined calibration data set while others are `optional`_. The
:meth:`pyuvdata.UVCal.check` method can be called on the object to verify
that all of the required attributes have been set in a consistent way.

Note that objects can be in a "metadata only" state where
all of the metadata is defined but the data-like attributes (``gain_array``,
``delay_array``, ``flag_array``, ``quality_array``) are not. The
:meth:`pyuvdata.UVCal.check` method will still pass for metadata only
objects.

Note location type attributes (which are given in topocentric xyz
coordinates) have convenience properties named the same thing with
``_lat_lon_alt`` and ``_lat_lon_alt_degrees`` appended through which you can
get or set the values using latitude, longitude and altitude values in
radians or degrees and meters.

Required
********
These parameters are required to have a sensible UVCal object and 
are required for most kinds of uv cal files.

**Nants_data**
     Number of antennas that have data associated with them (i.e. length of ant_array), which may be smaller than the numberof antennas in the telescope (i.e. length of antenna_numbers).

**Nants_telescope**
     Number of antennas in the antenna_numbers array. May be larger than the number of antennas with gains associated with them.

**Nfreqs**
     Number of frequency channels

**Njones**
     Number of Jones calibration parameters (Number of Jones matrix elements calculated in calibration).

**Nspws**
     Number of spectral windows (ie non-contiguous spectral chunks). 

**Ntimes**
     Number of times with different calibrations calculated (if a calibration is calculated over a range of integrations, this gives the number of separate calibrations along the time axis).

**ant_array**
     Array of integer antenna numbers that appear in self.gain_array, with shape (Nants_data,). This array is ordered to match the inherent ordering of the zeroth axis of self.gain_array.

**antenna_names**
     Array of antenna names with shape (Nants_telescope,). Ordering of elements matches ordering of antenna_numbers.

**antenna_numbers**
     Array of all integer-valued antenna numbers in the telescope with shape (Nants_telescope,). Ordering of elements matches that of antenna_names. This array is not necessarily identical to ant_array, in that this array holds all antenna numbers associated with the telescope, not just antennas with data, and has an in principle non-specific ordering.

**cal_style**
     Style of calibration. Values are sky or redundant.

**cal_type**
     cal type parameter. Values are delay, gain or unknown.

**channel_width**
     Width of frequency channels (Hz). If flex_spw = False and future_array_shapes=False, then it is a single value of type = float, otherwise it is an array of shape (Nfreqs,), type = float.Not required if future_array_shapes=True and wide_band=True.

**flex_spw**
     Option to construct a 'flexible spectral window', which storesall spectral channels across the frequency axis of data_array. Allows for spectral windows of variable sizes, and channels of varying widths.

**freq_array**
     Array of frequencies, center of the channel, shape (1, Nfreqs) or (Nfreqs,) if future_array_shapes=True, units Hz.Not required if future_array_shapes=True and wide_band=True.

**future_array_shapes**
     Flag indicating that this object is using the future array shapes.

**gain_convention**
     The convention for applying the calibration solutions to data.Values are "divide" or "multiply", indicating that to calibrate one should divide or multiply uncalibrated data by gains. Mathematically this indicates the alpha exponent in the equation: calibrated data = gain^alpha * uncalibrated data. A value of "divide" represents alpha=-1 and "multiply" represents alpha=1.

**history**
     String of history, units English

**integration_time**
     Integration time of a time bin, units seconds. If future_array_shapes=False, then it is a single value of type = float, otherwise it is an array of shape (Ntimes), type = float.

**jones_array**
     Array of antenna polarization integers, shape (Njones). linear pols -5:-8 (jxx, jyy, jxy, jyx).circular pols -1:-4 (jrr, jll. jrl, jlr).

**spw_array**
     Array of spectral window numbers, shape (Nspws).

**telescope_name**
     Name of telescope. e.g. HERA. String.

**time_array**
     Array of calibration solution times, center of integration, shape (Ntimes), units Julian Date

**wide_band**
     Option to support 'wide-band' calibration solutions with gains or delays that apply over a range of frequencies rather than having distinct values at each frequency. Delay type cal solutions are always 'wide-band' if future_array_shapes is True. If it is True several other parameters are affected: future_array_shapes is also True; the data-like arrays have a spw axis that is Nspws long rather than a frequency axis that is Nfreqs long; the `freq_range` parameter is required and the `freq_array` and `channel_width` parameters are not required.

**x_orientation**
     Orientation of the physical dipole corresponding to what is labelled as the x polarization. Options are "east" (indicating east/west orientation) and "north" (indicating north/south orientation)

Optional
********
These parameters are defined by one or more file standard but are not always required.
Some of them are required depending on the cal_type or cal_style (as noted below).

**Nsources**
     Number of sources used.

**antenna_positions**
     Array giving coordinates of antennas relative to telescope_location (ITRF frame), shape (Nants_telescope, 3), units meters. See the tutorial page in the documentation for an example of how to convert this to topocentric frame.

**baseline_range**
     Range of baselines used for calibration.

**delay_array**
     Required if cal_type = "delay". Array of delays with units of seconds. Shape: (Nants_data, 1, 1, Ntimes, Njones) or (Nants_data, Nspws, Ntimes, Njones) if future_array_shapes=True, type=float.

**diffuse_model**
     Name of diffuse model.

**extra_keywords**
     Any user supplied extra keywords, type=dict. Keys should be 8 character or less strings if writing to calfits files. Use the special key 'comment' for long multi-line string comments.

**filename**
     List of strings containing the unique basenames (not the full path) of input files.

**flag_array**
     Array of flags to be applied to calibrated data (logical OR of input and flag generated by calibration). True is flagged. Shape: (Nants_data, 1, Nfreqs, Ntimes, Njones) or (Nants_data, Nfreqs, Ntimes, Njones) if future_array_shapes=True and wide_band=False or (Nants_data, Nspws, Ntimes, Njones) if wide_band=True, type = bool.

**flex_spw_id_array**
     Required if flex_spw = True. Maps individual channels along the frequency axis to individual spectral windows, as listed in the spw_array. Shape (Nfreqs), type = int.

**freq_range**
     Required if cal_type='delay' or wide_band=True. Frequency range that solutions are valid for. If future_array_shapes is False it is a list: [start_frequency, end_frequency], otherwise it is an array of shape (Nspws, 2). Units are Hz.

**gain_array**
     Required if cal_type = "gain". Array of gains, shape: (Nants_data, 1, Nfreqs, Ntimes, Njones) or (Nants_data, Nfreqs, Ntimes, Njones) if future_array_shapes=True, or (Nants_data, Nspws, Ntimes, Njones) if wide_band=True, type = complex float.

**gain_scale**
     The gain scale of the calibration, which indicates the units of the calibrated visibilities. For example, Jy or K str.

**git_hash_cal**
     Commit hash of calibration software (from git_origin_cal) used to generate solutions.

**git_origin_cal**
     Origin (on github for e.g) of calibration software. Url and branch.

**input_flag_array**
     Array of input flags, True is flagged. shape: (Nants_data, 1, Nfreqs, Ntimes, Njones) or (Nants_data, Nfreqs, Ntimes, Njones) if future_array_shapes=True, type = bool.

**lst_array**
     Array of lsts, center of integration, shape (Ntimes), units radians

**observer**
     Name of observer who calculated solutions in this file.

**quality_array**
     Array of qualities of calibration solutions. The shape depends on cal_type, if the cal_type is 'gain' or 'unknown', the shape is: (Nants_data, 1, Nfreqs, Ntimes, Njones) or (Nants_data, Nfreqs, Ntimes, Njones) if future_array_shapes=True and wide_band=False or (Nants_data, Nspws, Ntimes, Njones) if wide_band=True, if the cal_type is 'delay', the shape is (Nants_data, 1, 1, Ntimes, Njones) or (Nants_data, Nspws, Ntimes, Njones) if future_array_shapes=True. The type is float.

**ref_antenna_name**
     Required if cal_style = "sky". Phase reference antenna.

**sky_catalog**
     Required if cal_style = "sky". Name of calibration catalog.

**sky_field**
     Required if cal_style = 'sky'. Short string describing field center or dominant source.

**telescope_location**
     Telescope location: xyz in ITRF (earth-centered frame). Can also be accessed using telescope_location_lat_lon_alt or telescope_location_lat_lon_alt_degrees properties

**time_range**
     Time range (in JD) that cal solutions are valid for.list: [start_time, end_time] in JD. Should only be set in Ntimes is 1.

**total_quality_array**
     Array of qualities of the calibration for entire arrays. The shape depends on cal_type, if the cal_type is 'gain' or 'unknown', the shape is: (1, Nfreqs, Ntimes, Njones) or (Nfreqs, Ntimes, Njones) if future_array_shapes=True, if the cal_type is 'delay', the shape is (1, 1, Ntimes, Njones) or (1, Ntimes, Njones) if future_array_shapes=True, type = float.

Methods
-------
.. autoclass:: pyuvdata.UVCal
  :members:

last updated: 2022-07-30