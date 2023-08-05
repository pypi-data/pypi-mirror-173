UVData
======

UVData is the main user class for intereferometric data (visibilities).
It provides import and export functionality to and from the supported file
formats (UVFITS, MeasurementSets, Miriad, uvh5, FHD, MIR) as well as
numerous methods for transforming the data (phasing, averaging, selecting,
sorting) and can be interacted with directly.

Attributes
----------
The attributes on UVData hold all of the metadata and data required to
analyze interferometric data sets. Under the hood, the attributes are
implemented as properties based on :class:`pyuvdata.parameter.UVParameter`
objects but this is fairly transparent to users.

UVData objects can be initialized from a file using the
:meth:`pyuvdata.UVData.from_file` class method
(as ``uvd = UVData.from_file(<filename>)``) or be initialized as an empty
object (as ``uvd = UVData()``). When an empty UVData object is initialized,
it has all of these attributes defined but set to ``None``. The attributes
can be set by reading in a data file using the :meth:`pyuvdata.UVData.read`
method or by setting them directly on the object. Some of these attributes
are `required`_ to be set to have a fully defined data set while others are
`optional`_. The :meth:`pyuvdata.UVData.check` method can be called on the
object to verify that all of the required attributes have been set in a
consistent way.

Note that objects can be in a "metadata only" state where
all of the metadata is defined but the data-like attributes (``data_array``,
``flag_array``, ``nsample_array``) are not. The
:meth:`pyuvdata.UVData.check` method will still pass for metadata only
objects.

Note that angle type attributes also have convenience properties named the
same thing with ``_degrees`` appended through which you can get or set the
value in degrees. Similarly location type attributes (which are given in
topocentric xyz coordinates) have convenience properties named the
same thing with ``_lat_lon_alt`` and ``_lat_lon_alt_degrees`` appended
through which you can get or set the values using latitude, longitude and
altitude values in radians or degrees and meters.

Required
********
These parameters are required to have a sensible UVData object and
are required for most kinds of interferometric data files.

**Nants_data**
     Number of antennas with data present (i.e. number of unique entries in ant_1_array and ant_2_array). May be smaller than the number of antennas in the array.

**Nants_telescope**
     Number of antennas in the array. May be larger than the number of antennas with data.

**Nbls**
     Number of baselines.

**Nblts**
     Number of baseline-times (i.e. number of spectra). Not necessarily equal to Nbls * Ntimes.

**Nfreqs**
     Number of frequency channels.

**Npols**
     Number of polarizations.

**Nspws**
     Number of spectral windows (ie non-contiguous spectral chunks). 

**Ntimes**
     Number of times.

**ant_1_array**
     Array of numbers for the first antenna, which is matched to that in the antenna_numbers attribute. Shape (Nblts), type = int.

**ant_2_array**
     Array of numbers for the second antenna, which is matched to that in the antenna_numbers attribute. Shape (Nblts), type = int.

**antenna_names**
     List of antenna names, shape (Nants_telescope), with numbers given by antenna_numbers (which can be matched to ant_1_array and ant_2_array). There must be one entry here for each unique entry in ant_1_array and ant_2_array, but there may be extras as well. 

**antenna_numbers**
     List of integer antenna numbers corresponding to antenna_names, shape (Nants_telescope). There must be one entry here for each unique entry in ant_1_array and ant_2_array, but there may be extras as well.Note that these are not indices -- they do not need to start at zero or be continuous.

**antenna_positions**
     Array giving coordinates of antennas relative to telescope_location (ITRF frame), shape (Nants_telescope, 3), units meters. See the tutorial page in the documentation for an example of how to convert this to topocentric frame.

**baseline_array**
     Array of baseline numbers, shape (Nblts), type = int; baseline = 2048 * (ant1+1) + (ant2+1) + 2^16.

**channel_width**
     Width of frequency channels (Hz). If flex_spw = False and future_array_shapes=False, then it is a single value of type = float, otherwise it is an array of shape (Nfreqs), type = float.

**flex_spw**
     Option to construct a "flexible spectral window", which storesall spectral channels across the frequency axis of data_array. Allows for spectral windows of variable sizes, and channels of varying widths.

**freq_array**
     Array of frequencies, center of the channel, shape (1, Nfreqs) or (Nfreqs,) if future_array_shapes=True, units Hz.

**future_array_shapes**
     Flag indicating that this object is using the future array shapes.

**history**
     String of history, units English.

**instrument**
     Receiver or backend. Sometimes identical to telescope_name.

**integration_time**
     Length of the integration in seconds, shape (Nblts). The product of the integration_time and the nsample_array value for a visibility reflects the total amount of time that went into the visibility. Best practice is for the integration_time to reflect the length of time a visibility was integrated over (so it should vary in the case of baseline-dependent averaging and be a way to do selections for differently integrated baselines).Note that many files do not follow this convention, but it is safe to assume that the product of the integration_time and the nsample_array is the total amount of time included in a visibility.

**lst_array**
     Array of local apparent sidereal times (LAST) at the center of integration, shape (Nblts), units radians.

**multi_phase_center**
     Only relevant if phase_type = "phased". Specifies the that the data set contains multiple sources within it.

**object_name**
     Name(s) of source(s) or field(s) observed, type string. If multi_phase_center = True, set to "multi".

**phase_type**
     String indicating phasing type. Allowed values are "drift" and "phased" (n.b., "drift" is not the same as `cat_type="driftscan"`, the latter of which _is_ phased to a fixed az-el position).

**polarization_array**
     Array of polarization integers, shape (Npols). AIPS Memo 117 says: pseudo-stokes 1:4 (pI, pQ, pU, pV);  circular -1:-4 (RR, LL, RL, LR); linear -5:-8 (XX, YY, XY, YX). NOTE: AIPS Memo 117 actually calls the pseudo-Stokes polarizations "Stokes", but this is inaccurate as visibilities cannot be in true Stokes polarizations for physical antennas. We adopt the term pseudo-Stokes to refer to linear combinations of instrumental visibility polarizations (e.g. pI = xx + yy).

**spw_array**
     Array of spectral window numbers, shape (Nspws).

**telescope_location**
     Telescope location: xyz in ITRF (earth-centered frame). Can also be accessed using telescope_location_lat_lon_alt or telescope_location_lat_lon_alt_degrees properties.

**telescope_name**
     Name of telescope or array (string).

**time_array**
     Array of times, center of integration, shape (Nblts), units Julian Date.

**uvw_array**
     Projected baseline vectors relative to phase center, shape (Nblts, 3), units meters. Convention is: uvw = xyz(ant2) - xyz(ant1).Note that this is the Miriad convention but it is different from the AIPS/FITS convention (where uvw = xyz(ant1) - xyz(ant2)).

**vis_units**
     Visibility units, options are: "uncalib", "Jy" or "K str".

Optional
********
These parameters are defined by one or more file standard but are not
always required. Some of them are required depending on the
phase_type (as noted below).

**Nphase**
     Required if multi_phase_center = True. Specifies the number of phase centers contained within the data set.

**antenna_diameters**
     Array of antenna diameters in meters. Used by CASA to construct a default beam if no beam is supplied.

**blt_order**
     Ordering of the data array along the blt axis. A tuple with the major and minor order (minor order is omitted if order is "bda"). The allowed values are: time ,baseline ,ant1 ,ant2 ,bda.

**data_array**
     Array of the visibility data, shape: (Nblts, 1, Nfreqs, Npols) or (Nblts, Nfreqs, Npols) if future_array_shapes=True, type = complex float, in units of self.vis_units.

**dut1**
     DUT1 (google it) AIPS 117 calls it UT1UTC.

**earth_omega**
     Earth's rotation rate in degrees per day.

**eq_coeffs**
     Per-antenna and per-frequency equalization coefficients.

**eq_coeffs_convention**
     Convention for how to remove eq_coeffs from data.

**extra_keywords**
     Any user supplied extra keywords, type=dict. Keys should be 8 character or less strings if writing to uvfits or miriad files. Use the special key "comment" for long multi-line string comments.

**filename**
     List of strings containing the unique basenames (not the full path) of input files.

**flag_array**
     Boolean flag, True is flagged, same shape as data_array.

**flex_spw_id_array**
     Required if flex_spw = True. Maps individual channels along the frequency axis to individual spectral windows, as listed in the spw_array. Shape (Nfreqs), type = int.

**flex_spw_polarization_array**
     Optional, only used if flex_spw = True. Allows for labeling individual spectral windows with different polarizations. If set, Npols must be set to 1 (i.e., only one polarization per spectral window allowed). Shape (Nspws), type = int.

**gst0**
     Greenwich sidereal time at midnight on reference date.

**nsample_array**
     Number of data points averaged into each data element, NOT required to be an integer, type = float, same shape as data_array.The product of the integration_time and the nsample_array value for a visibility reflects the total amount of time that went into the visibility. Best practice is for the nsample_array to be used to track flagging within an integration_time (leading to a decrease of the nsample array value below 1) and LST averaging (leading to an increase in the nsample array value). So datasets that have not been LST averaged should have nsample array values less than or equal to 1.Note that many files do not follow this convention, but it is safe to assume that the product of the integration_time and the nsample_array is the total amount of time included in a visibility.

**phase_center_app_dec**
     Required if phase_type = "phased". Declination of phase center in the topocentric frame of the observatory, units radians. Shape (Nblts,), type = float.

**phase_center_app_ra**
     Required if phase_type = "phased". Apparent right ascension of phase center in the topocentric frame of the observatory, units radians.Shape (Nblts,), type = float.

**phase_center_catalog**
     Only relevant if multi_phase_center = True. Dictionary that acts as a catalog, containing information on individual phase centers. Keys are the names of the different phase centers in the UVData object. At a minimum, each dictionary must contain the key "cat_type", which can be either "sidereal" (fixed position in RA/Dec), "ephem" (position in RA/Dec whichmoves with time), "driftscan" (fixed postion in Az/El, NOT the same as `phase_type`="drift") and "unphased" (baseline coordinates in ENU, but data are not phased, similar to `phase_type`="drift"). Other typical keyworks include "cat_lon" (longitude coord, e.g. RA), "cat_lat" (latitude coord, e.g. Dec.), "cat_frame" (coordinate frame, e.g. icrs), "cat_epoch" (epoch and equinox of the coordinate frame), "cat_times" (times for the coordinates, only used for "ephem" types), "cat_pm_ra" (proper motion in RA), "cat_pm_dec" (proper motion in Dec), "cat_dist" (physical distance), "cat_vrad" (rest frame velocity), "info_source" (describes where catalog info came from), and "cat_id" (matched to the parameter `phase_center_id_array`. See the documentation of the `phase` method for more details.

**phase_center_dec**
     Required if phase_type = "phased". Declination of phase center (see uvw_array), units radians. Can also be accessed using phase_center_dec_degrees.

**phase_center_epoch**
     Required if phase_type = "phased". Epoch year of the phase applied to the data (eg 2000.)

**phase_center_frame**
     Only relevant if phase_type = "phased". Specifies the frame the data and uvw_array are phased to. Options are "icrs", "gcrs", and "fk5"; default is "icrs".

**phase_center_frame_pa**
     Required if phase_type = "phased". Position angle between the hour circle (which is a great circle that goes through the target postion and both poles) in the apparent/topocentric frame, and the frame given in the phase_center_frame attribute.Shape (Nblts,), type = float.

**phase_center_id_array**
     Required if multi_phase_center = True. Maps individual indices along the Nblt axis to an entry in `phase_center_catalog`, with the ID number of individual entries stored as `cat_id`, along with other metadata. Shape (Nblts), type = int.

**phase_center_ra**
     Required if phase_type = 'phased'. Right ascension of phase center (see uvw_array), units radians. Can also be accessed using phase_center_ra_degrees.

**rdate**
     Date for which the GST0 applies.

**scan_number_array**
     Optional when reading a MS. Retains the scan number when reading a MS. Shape (Nblts), type = int.

**timesys**
     We only support UTC.

**uvplane_reference_time**
     FHD thing we do not understand, something about the time at which the phase center is normal to the chosen UV plane for phasing.

**x_orientation**
     Orientation of the physical dipole corresponding to what is labelled as the x polarization. Options are 'east' (indicating east/west orientation) and 'north (indicating north/south orientation).

Methods
-------
.. autoclass:: pyuvdata.UVData
  :members:

last updated: 2022-07-30