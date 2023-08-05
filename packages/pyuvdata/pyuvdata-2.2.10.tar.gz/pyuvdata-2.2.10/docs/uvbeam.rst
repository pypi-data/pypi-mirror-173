UVBeam
======
UVBeam is the main user class for primary beam models for radio telescopes.
It provides import and export functionality to and from the supported file
formats (beamFITS, CST, MWA primary beam) as well as methods for
transforming the data (interpolating/regridding, selecting, converting
types) and can be interacted with directly.

Note that there are some tricks that can help with reading in CST beam
simulation files in `CST Settings Files`_.

Attributes
----------
The attributes on UVBeam hold all of the metadata and data required to
describe primary beam models. Under the hood, the attributes are implemented
as properties based on :class:`pyuvdata.parameter.UVParameter` objects but
this is fairly transparent to users.

UVBeam objects can be initialized from a file using the
:meth:`pyuvdata.UVBeam.from_file` class method
(as ``beam = UVBeam.from_file(<filename>)``) or be initialized as an empty
object (as ``beam = UVBeam()``). When an empty UVBeam object is initialized,
it has all of these attributes defined but set to ``None``. The attributes
can be set by reading in a data file using the :meth:`pyuvdata.UVBeam.read`
method or by setting them directly on the object. Some of these attributes
are `required`_ to be set to have a fully defined data set while others are
`optional`_. The :meth:`pyuvdata.UVBeam.check` method can be called on the
object to verify that all of the required attributes have been set in a
consistent way.

Required
********
These parameters are required to have a sensible UVBeam object and 
are required for most kinds of beam files.

**Naxes_vec**
     Number of basis vectors used to represent the antenna response in each pixel. These need not align with the pixel coordinate system or even be orthogonal. The mapping of these basis vectors to directions aligned withthe pixel coordinate system is contained in the `basis_vector_array`. The allowed values for this parameter are 2 or 3 (or 1 if beam_type is 'power').

**Nfreqs**
     Number of frequency channels

**antenna_type**
     String indicating antenna type. Allowed values are "simple", and "phased_array"

**bandpass_array**
     Frequency dependence of the beam. Depending on the data_normalization, this may contain only the frequency dependence of the receiving chain ('physical' normalization) or all the frequency dependence ('peak' normalization). Shape (1, Nfreqs) or (Nfreqs,) if future_array_shapes=True

**beam_type**
     String indicating beam type. Allowed values are 'efield', and 'power'.

**data_array**
     Depending on beam type, either complex E-field values ('efield' beam type) or power values ('power' beam type) for beam model. Units are normalized to either peak or solid angle as given by data_normalization. The shape depends on whether future_array_shapes is True, the beam_type and pixel_coordinate_system, If future_array_shapes is True, and it is a 'healpix' beam, the shape is: (Naxes_vec, Nfeeds or Npols, Nfreqs, Npixels), if it is not a healpix beam it is (Naxes_vec, Nfeeds or Npols, Nfreqs, Naxes2, Naxes1).If future_array_shapes is False, and it is a 'healpix' beam, the shape is: (Naxes_vec, 1, Nfeeds or Npols, Nfreqs, Npixels), if it is not a healpix beam it is (Naxes_vec, 1, Nfeeds or Npols, Nfreqs, Naxes2, Naxes1).

**data_normalization**
     Normalization standard of data_array, options are: "physical", "peak" or "solid_angle". Physical normalization means that the frequency dependence of the antenna sensitivity is included in the data_array while the frequency dependence of the receiving chain is included in the bandpass_array. Peak normalized means that for each frequency the data_arrayis separately normalized such that the peak is 1 (so the beam is dimensionless) and all direction-independent frequency dependence is moved to the bandpass_array (if the beam_type is "efield", then peak normalized means that the absolute value of the peak is 1). Solid angle normalized means the peak normalized beam is divided by the integral of the beam over the sphere, so the beam has dimensions of 1/stradian.

**feed_name**
     Name of physical feed (string)

**feed_version**
     Version of physical feed (string)

**freq_array**
     Array of frequencies, center of the channel, shape (1, Nfreqs) or (Nfreqs,) if future_array_shapes=True, units Hz.

**future_array_shapes**
     Flag indicating that this object is using the future array shapes.

**history**
     String of history, units English

**model_name**
     Name of beam model (string)

**model_version**
     Version of beam model (string)

**pixel_coordinate_system**
     Pixel coordinate system, options are: "az_za", "orthoslant_zenith", "healpix". "az_za" is a uniformly gridded azimuth, zenith angle coordinate system, where az runs from East to North in radians. It has axes [azimuth, zen_angle]. "orthoslant_zenith" is a orthoslant projection at zenith where y points North, x point East. It has axes [zenorth_x, zenorth_y]. "healpix" is a HEALPix map with zenith at the north pole and az, za coordinate axes (for the basis_vector_array) where az runs from East to North. It has axes [hpx_inds].

**telescope_name**
     Name of telescope (string)

Optional
********
These parameters are defined by one or more file standard but are not always required.
Some of them are required depending on the beam_type, antenna_type and pixel_coordinate_systems (as noted below).

**Naxes1**
     Number of elements along the first pixel axis. Not required if pixel_coordinate_system is "healpix".

**Naxes2**
     Number of elements along the second pixel axis. Not required if pixel_coordinate_system is "healpix".

**Ncomponents_vec**
     Number of orthogonal components required to map each basis vector to vectors aligned with the pixel coordinate system. This can be equal to or smaller than `Naxes_vec`. The allowed values for this parameter are 2 or 3. Only required for E-field beams.

**Nelements**
     Required if antenna_type = "phased_array". Number of elements in phased array

**Nfeeds**
     Number of feeds. Not required if beam_type is "power".

**Npixels**
     Number of healpix pixels. Only required if pixel_coordinate_system is 'healpix'.

**Npols**
     Number of polarizations. Only required if beam_type is "power".

**Nspws**
     Number of spectral windows (ie non-contiguous spectral chunks). More than one spectral window is not currently supported.

**axis1_array**
     Coordinates along first pixel axis. Not required if pixel_coordinate_system is "healpix".

**axis2_array**
     Coordinates along second pixel axis. Not required if pixel_coordinate_system is "healpix".

**basis_vector_array**
     Beam basis vector components, essentially the mapping between the directions that the electrical field values are recorded in to the directions aligned with the pixel coordinate system (or azimuth/zenith angle for HEALPix beams).Not required if beam_type is "power". The shape depends on the pixel_coordinate_system, if it is "healpix", the shape is: (Naxes_vec, Ncomponents_vec, Npixels), otherwise it is (Naxes_vec, Ncomponents_vec, Naxes2, Naxes1)

**coupling_matrix**
     Required if antenna_type = "phased_array". Matrix of complex element couplings, units: dB, shape: (Nelements, Nelements, Nfeeds, Nfeeds, 1, Nfreqs) or (Nelements, Nelements, Nfeeds, Nfeeds, Nfreqs) if future_array_shapes is True.

**delay_array**
     Required if antenna_type = "phased_array". Array of element delays, units: seconds, shape: (Nelements)

**element_coordinate_system**
     Required if antenna_type = "phased_array". Element coordinate system, options are: N-E or x-y

**element_location_array**
     Required if antenna_type = "phased_array". Array of element locations in element coordinate system,  shape: (2, Nelements)

**extra_keywords**
     Any user supplied extra keywords, type=dict. Keys should be 8 character or less strings if writing to beam fits files. Use the special key "comment" for long multi-line string comments.

**feed_array**
     Array of feed orientations. shape (Nfeeds). options are: N/E or x/y or R/L. Not required if beam_type is "power".

**filename**
     List of strings containing the unique basenames (not the full path) of input files.

**freq_interp_kind**
     String indicating frequency interpolation kind. See scipy.interpolate.interp1d for details. Default is linear.

**gain_array**
     Required if antenna_type = "phased_array". Array of element gains, units: dB, shape: (Nelements)

**interpolation_function**
     String indicating interpolation function. Must be set to use the interp_* methods. Allowed values are : "az_za_simple", "healpix_simple".

**loss_array**
     Array of antenna losses, units dB? Shape (1, Nfreqs) or (Nfreqs,) if future_array_shapes=True

**mismatch_array**
     Array of antenna-amplifier mismatches, units ? Shape (1, Nfreqs) or (Nfreqs,) if future_array_shapes=True

**nside**
     Healpix nside parameter. Only required if pixel_coordinate_system is 'healpix'.

**ordering**
     Healpix ordering parameter, allowed values are "ring" and "nested". Only required if pixel_coordinate_system is "healpix".

**pixel_array**
     Healpix pixel numbers. Only required if pixel_coordinate_system is 'healpix'.

**polarization_array**
     Array of polarization integers, shape (Npols). Uses the same convention as UVData: pseudo-stokes 1:4 (pI, pQ, pU, pV);  circular -1:-4 (RR, LL, RL, LR); linear -5:-8 (XX, YY, XY, YX). Only required if beam_type is "power".

**receiver_temperature_array**
     Array of receiver temperatures, units K. Shape (1, Nfreqs) or (Nfreqs,) if future_array_shapes=True

**reference_impedance**
     Reference impedance of the beam model. The radiated E-farfield or the realised gain depend on the impedance of the port used to excite the simulation. This is the reference impedance (Z0) of the simulation. units: Ohms

**s_parameters**
     S parameters of receiving chain, ordering: s11, s12, s21, s22. see https://en.wikipedia.org/wiki/Scattering_parameters#Two-Port_S-ParametersShape (4, 1, Nfreqs) or (4, Nfreqs) if future_array_shapes is True

**spw_array**
     Array of spectral window Numbers, shape (Nspws)

**x_orientation**
     Orientation of the physical dipole corresponding to what is labelled as the x polarization. Options are "east" (indicating east/west orientation) and "north" (indicating north/south orientation)

Methods
-------
.. autoclass:: pyuvdata.UVBeam
  :members:

CST Settings Files
------------------

The text files saved out of CST beam simulations do not have much of the
critical metadata needed for UVBeam objects. This required metadata can be set
via keywords when the files are read in, but it is better for the metadata to be
specified once and carried with the data files. To that end, we developed a yaml
settings file specification to carry all the metadata. This format is very human
readable and writeable and we encourage using such a file as the best way to
ensure the metadata is preserved. Note that reading a yaml settings file into
UVBeam requires that pyyaml is installed.

Required Fields
***************

The following are the required fields in a CST yaml settings file. The lists of
frequencies specifies the frequency in each filename, so the lists must be in
the same order (as must the feed_pol if it is a list):

- telescope_name (str)
- feed_name (str)
- feed_version (str)
- model_name (str)
- model_version (str)
- history (str)
- frequencies (list(float))
- cst text filenames (list(str)) -- path relative to yaml file location
- feed_pol (str) or (list(str))

Optional Fields
***************

The following are optional fields:

- ref_imp (float): beam model reference impedance
- sim_beam_type (str): e.g. 'E-farfield'
- any other field that contains useful information that should be propagated
  with the beam. These will go into the extra_keywords attribute (note that if the
  field names are more than 8 characters they will be truncated to 8 if the beam
  is written to a beamfits file).

Example Settings File
*********************

An example settings yaml file for a HERA Vivaldi feed simulation is shown below.
In this example, 'software', 'layout', and 'port_num' are extra fields that will
be propagated with the beam. Note that quotes are used around version numbers
that could be interpreted as floats and around filenames with spaces in them,
but other strings do not require quotes. The history field shows a way to make
a multi-line string (although this history is quite short, there could be many
lines of history information there.):

.. code-block:: yaml
    :caption: Example settings yaml file.

    telescope_name: HERA
    feed_name: Vivaldi
    feed_version: '1.0'
    model_name: Mecha design - dish - cables - soil
    model_version: '1.0'
    software: CST 2016
    history: |
        beams simulated in Nov 2018 by NF
    frequencies: [50e6, 51e6, 52e6, 53e6, 54e6, 55e6, 56e6, 57e6, 58e6, 59e6, 60e6, 61e6, 62e6, 63e6, 64e6, 65e6, 66e6, 67e6, 68e6, 69e6, 70e6, 71e6, 72e6, 73e6, 74e6, 75e6, 76e6, 77e6, 78e6, 79e6, 80e6, 81e6, 82e6, 83e6, 84e6, 85e6, 86e6, 87e6, 88e6, 89e6, 90e6, 91e6, 92e6, 93e6, 94e6, 95e6, 96e6, 97e6, 98e6, 99e6, 100e6, 101e6, 102e6, 103e6, 104e6, 105e6, 106e6, 107e6, 108e6, 109e6, 110e6, 111e6, 112e6, 113e6, 114e6, 115e6, 116e6, 117e6, 118e6, 119e6, 120e6, 121e6, 122e6, 123e6, 124e6, 125e6, 126e6, 127e6, 128e6, 129e6, 130e6, 131e6, 132e6, 133e6, 134e6, 135e6, 136e6, 137e6, 138e6, 139e6, 140e6, 141e6, 142e6, 143e6, 144e6, 145e6, 146e6, 147e6, 148e6, 149e6, 150e6, 151e6, 152e6, 153e6, 154e6, 155e6, 156e6, 157e6, 158e6, 159e6, 160e6, 161e6, 162e6, 163e6, 164e6, 165e6, 166e6, 167e6, 168e6, 169e6, 170e6, 171e6, 172e6, 173e6, 174e6, 175e6, 176e6, 177e6, 178e6, 179e6, 180e6, 181e6, 182e6, 183e6, 184e6, 185e6, 186e6, 187e6, 188e6, 189e6, 190e6, 191e6, 192e6, 193e6, 194e6, 195e6, 196e6, 197e6, 198e6, 199e6, 200e6, 201e6, 202e6, 203e6, 204e6, 205e6, 206e6, 207e6, 208e6, 209e6, 210e6, 211e6, 212e6, 213e6, 214e6, 215e6, 216e6, 217e6, 218e6, 219e6, 220e6, 221e6, 222e6, 223e6, 224e6, 225e6, 226e6, 227e6, 228e6, 229e6, 230e6, 231e6, 232e6, 233e6, 234e6, 235e6, 236e6, 237e6, 238e6, 239e6, 240e6, 241e6, 242e6, 243e6, 244e6, 245e6, 246e6, 247e6, 248e6, 249e6, 250e6]
    filenames: ['farfield (f=50) [1].txt', 'farfield (f=51) [1].txt', 'farfield (f=52) [1].txt', 'farfield (f=53) [1].txt', 'farfield (f=54) [1].txt', 'farfield (f=55) [1].txt', 'farfield (f=56) [1].txt', 'farfield (f=57) [1].txt', 'farfield (f=58) [1].txt', 'farfield (f=59) [1].txt', 'farfield (f=60) [1].txt', 'farfield (f=61) [1].txt', 'farfield (f=62) [1].txt', 'farfield (f=63) [1].txt', 'farfield (f=64) [1].txt', 'farfield (f=65) [1].txt', 'farfield (f=66) [1].txt', 'farfield (f=67) [1].txt', 'farfield (f=68) [1].txt', 'farfield (f=69) [1].txt', 'farfield (f=70) [1].txt', 'farfield (f=71) [1].txt', 'farfield (f=72) [1].txt', 'farfield (f=73) [1].txt', 'farfield (f=74) [1].txt', 'farfield (f=75) [1].txt', 'farfield (f=76) [1].txt', 'farfield (f=77) [1].txt', 'farfield (f=78) [1].txt', 'farfield (f=79) [1].txt', 'farfield (f=80) [1].txt', 'farfield (f=81) [1].txt', 'farfield (f=82) [1].txt', 'farfield (f=83) [1].txt', 'farfield (f=84) [1].txt', 'farfield (f=85) [1].txt', 'farfield (f=86) [1].txt', 'farfield (f=87) [1].txt', 'farfield (f=88) [1].txt', 'farfield (f=89) [1].txt', 'farfield (f=90) [1].txt', 'farfield (f=91) [1].txt', 'farfield (f=92) [1].txt', 'farfield (f=93) [1].txt', 'farfield (f=94) [1].txt', 'farfield (f=95) [1].txt', 'farfield (f=96) [1].txt', 'farfield (f=97) [1].txt', 'farfield (f=98) [1].txt', 'farfield (f=99) [1].txt', 'farfield (f=100) [1].txt', 'farfield (f=101) [1].txt', 'farfield (f=102) [1].txt', 'farfield (f=103) [1].txt', 'farfield (f=104) [1].txt', 'farfield (f=105) [1].txt', 'farfield (f=106) [1].txt', 'farfield (f=107) [1].txt', 'farfield (f=108) [1].txt', 'farfield (f=109) [1].txt', 'farfield (f=110) [1].txt', 'farfield (f=111) [1].txt', 'farfield (f=112) [1].txt', 'farfield (f=113) [1].txt', 'farfield (f=114) [1].txt', 'farfield (f=115) [1].txt', 'farfield (f=116) [1].txt', 'farfield (f=117) [1].txt', 'farfield (f=118) [1].txt', 'farfield (f=119) [1].txt', 'farfield (f=120) [1].txt', 'farfield (f=121) [1].txt', 'farfield (f=122) [1].txt', 'farfield (f=123) [1].txt', 'farfield (f=124) [1].txt', 'farfield (f=125) [1].txt', 'farfield (f=126) [1].txt', 'farfield (f=127) [1].txt', 'farfield (f=128) [1].txt', 'farfield (f=129) [1].txt', 'farfield (f=130) [1].txt', 'farfield (f=131) [1].txt', 'farfield (f=132) [1].txt', 'farfield (f=133) [1].txt', 'farfield (f=134) [1].txt', 'farfield (f=135) [1].txt', 'farfield (f=136) [1].txt', 'farfield (f=137) [1].txt', 'farfield (f=138) [1].txt', 'farfield (f=139) [1].txt', 'farfield (f=140) [1].txt', 'farfield (f=141) [1].txt', 'farfield (f=142) [1].txt', 'farfield (f=143) [1].txt', 'farfield (f=144) [1].txt', 'farfield (f=145) [1].txt', 'farfield (f=146) [1].txt', 'farfield (f=147) [1].txt', 'farfield (f=148) [1].txt', 'farfield (f=149) [1].txt', 'farfield (f=150) [1].txt', 'farfield (f=151) [1].txt', 'farfield (f=152) [1].txt', 'farfield (f=153) [1].txt', 'farfield (f=154) [1].txt', 'farfield (f=155) [1].txt', 'farfield (f=156) [1].txt', 'farfield (f=157) [1].txt', 'farfield (f=158) [1].txt', 'farfield (f=159) [1].txt', 'farfield (f=160) [1].txt', 'farfield (f=161) [1].txt', 'farfield (f=162) [1].txt', 'farfield (f=163) [1].txt', 'farfield (f=164) [1].txt', 'farfield (f=165) [1].txt', 'farfield (f=166) [1].txt', 'farfield (f=167) [1].txt', 'farfield (f=168) [1].txt', 'farfield (f=169) [1].txt', 'farfield (f=170) [1].txt', 'farfield (f=171) [1].txt', 'farfield (f=172) [1].txt', 'farfield (f=173) [1].txt', 'farfield (f=174) [1].txt', 'farfield (f=175) [1].txt', 'farfield (f=176) [1].txt', 'farfield (f=177) [1].txt', 'farfield (f=178) [1].txt', 'farfield (f=179) [1].txt', 'farfield (f=180) [1].txt', 'farfield (f=181) [1].txt', 'farfield (f=182) [1].txt', 'farfield (f=183) [1].txt', 'farfield (f=184) [1].txt', 'farfield (f=185) [1].txt', 'farfield (f=186) [1].txt', 'farfield (f=187) [1].txt', 'farfield (f=188) [1].txt', 'farfield (f=189) [1].txt', 'farfield (f=190) [1].txt', 'farfield (f=191) [1].txt', 'farfield (f=192) [1].txt', 'farfield (f=193) [1].txt', 'farfield (f=194) [1].txt', 'farfield (f=195) [1].txt', 'farfield (f=196) [1].txt', 'farfield (f=197) [1].txt', 'farfield (f=198) [1].txt', 'farfield (f=199) [1].txt', 'farfield (f=200) [1].txt', 'farfield (f=201) [1].txt', 'farfield (f=202) [1].txt', 'farfield (f=203) [1].txt', 'farfield (f=204) [1].txt', 'farfield (f=205) [1].txt', 'farfield (f=206) [1].txt', 'farfield (f=207) [1].txt', 'farfield (f=208) [1].txt', 'farfield (f=209) [1].txt', 'farfield (f=210) [1].txt', 'farfield (f=211) [1].txt', 'farfield (f=212) [1].txt', 'farfield (f=213) [1].txt', 'farfield (f=214) [1].txt', 'farfield (f=215) [1].txt', 'farfield (f=216) [1].txt', 'farfield (f=217) [1].txt', 'farfield (f=218) [1].txt', 'farfield (f=219) [1].txt', 'farfield (f=220) [1].txt', 'farfield (f=221) [1].txt', 'farfield (f=222) [1].txt', 'farfield (f=223) [1].txt', 'farfield (f=224) [1].txt', 'farfield (f=225) [1].txt', 'farfield (f=226) [1].txt', 'farfield (f=227) [1].txt', 'farfield (f=228) [1].txt', 'farfield (f=229) [1].txt', 'farfield (f=230) [1].txt', 'farfield (f=231) [1].txt', 'farfield (f=232) [1].txt', 'farfield (f=233) [1].txt', 'farfield (f=234) [1].txt', 'farfield (f=235) [1].txt', 'farfield (f=236) [1].txt', 'farfield (f=237) [1].txt', 'farfield (f=238) [1].txt', 'farfield (f=239) [1].txt', 'farfield (f=240) [1].txt', 'farfield (f=241) [1].txt', 'farfield (f=242) [1].txt', 'farfield (f=243) [1].txt', 'farfield (f=244) [1].txt', 'farfield (f=245) [1].txt', 'farfield (f=246) [1].txt', 'farfield (f=247) [1].txt', 'farfield (f=248) [1].txt', 'farfield (f=249) [1].txt', 'farfield (f=250) [1].txt']
    sim_beam_type: E-farfield
    feed_pol: x
    layout: 1 antenna
    port_num: 1
    ref_imp: 100


last updated: 2022-07-30