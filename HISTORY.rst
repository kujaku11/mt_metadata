History
=========


0.1.0 (2020-12-30)
------------------

* First release on PyPI.

0.1.3 (2021-06-25)
-------------------

* Added time series filters

 - PoleZeroFilter
 - CoefficientFilter
 - FIRFilter
 - TimeDelayFilter
 - FrequencyAmplitudePhaseFilter

* Added translations to/from StationXML
* Updated tests
* Fixed minor bugs
* Updated documentation	

0.1.5 (2021-11-13)
-------------------

* Bug fixes
* Updated how units are handled
* If survey.id is None set it to fdsn.network if available (mainly an IRIS DMC fix)
* Updated translation of Experiment to StationXML
* Updated tests

0.1.6 (2021-12-07)
--------------------

* Bug fixes (mainly in mt_metadata.timeseries.filters)
* Updated tests
* Channel codes are handled "better"
* Updating translation between Experiment and StationXML
* Updated how filters are plotted
* Adding notebooks to documentation

0.1.7 (2022-01-10)
--------------------

* Updating how transfer functions are handled
* Added readers and metadata standards for
    - EDI files
	- Z-files 
	- J-Files
	- AVG file
	- EMTF XML files
* Added tests for transfer functions
* Updated mt_metadata.transfer_functions.core.TF
* Added documentation on transfer functions

0.1.8 (2022-04-07)
--------------------

* Bug fixes (mainly in the transfer functions)
* Combined timeseries and transfer_function metadata where similar, so now transfer_function metadata imports from timeseries when applicable.  Reduces files and redundancy.
* Updated documentation

0.2.0 (2022-09-10)
---------------------

* minor bug fixes
* update reading .AVG files

0.2.1 (2023-01-18)
---------------------

* Update setup.py 
* updating reading emtfxml files 
* Fix issue 95 
* Add model error 
* Make sure filter names are unique 
* Fix Empty Z file
* Add metadata 
* added test for multiple networks in stationxml 
* updating to make mth5 work with single metadata object in ChannelTS and RunTS 
* added test for null channel component 
* Mth5 patch129 fixes 
* Update edi.py 
* add a line to allow aux channel component to be empty 
* Update edi.py 
* Mth5 patch129 fixes

0.2.2 (2023-02-17)
--------------------- 

* Fixed bug in Station.channels_recorded when a string is input

0.2.3 (2023-04-24)
---------------------

* Add methods for t0/from transfer function file type 
* Update when an np.datetime64 is input 
* MTime update to handle nanosecond accuracy 
* MTime and pandas Timestamp cannot handle large future or past dates 
* Fix input time with `isoformat` attribute
* updating if a timedelta is subtracted 
* Updates from main into fix_issue_133
* Fix issue #133 
* Update EMTFXML ouptut format 
* Add FC Metadata 

0.3.0 (2023-09-29)
---------------------

* Fixing Bugs in https://github.com/kujaku11/mt_metadata/pull/138
* adding a merge for TFs in https://github.com/kujaku11/mt_metadata/pull/136
* Fix write EDI bugs in https://github.com/kujaku11/mt_metadata/pull/149
* Use loguru instead of builtin logging in https://github.com/kujaku11/mt_metadata/pull/153
* Loguru in https://github.com/kujaku11/mt_metadata/pull/154
* Try to fix bug with filter assignment in https://github.com/kujaku11/mt_metadata/pull/155
* Empower edi in https://github.com/kujaku11/mt_metadata/pull/158
* TF survey metadata in https://github.com/kujaku11/mt_metadata/pull/159
* added logic for if channel location values are None in https://github.com/kujaku11/mt_metadata/pull/160
* Changes to support writing z-files with channel_nomenclature in https://github.com/kujaku11/mt_metadata/pull/161
* Minor changes to support zfiles tests in https://github.com/kujaku11/mt_metadata/pull/163
* Test aurora issue 295 in https://github.com/kujaku11/mt_metadata/pull/165
* Fcs in https://github.com/kujaku11/mt_metadata/pull/142
* Fcs in https://github.com/kujaku11/mt_metadata/pull/166
* Update environment.yml in https://github.com/kujaku11/mt_metadata/pull/167
* updating documentation in https://github.com/kujaku11/mt_metadata/pull/168

0.3.1 (2023-10-15)
-----------------------

* Minor bug fixes

0.3.2 (2023-11-08)
-----------------------

* remove restriction on Pandas < 2
* minor bug fixes

0.3.3 (2023-11-08)
-----------------------

* update pandas.append to concat

0.3.4 ()
-----------------------

* Update HISTORY.rst by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/179
* Remove filter direction attributes by @kkappler in https://github.com/kujaku11/mt_metadata/pull/181
* Fix issue 173 by @kkappler in https://github.com/kujaku11/mt_metadata/pull/182
* Patch 173 by @kkappler in https://github.com/kujaku11/mt_metadata/pull/183
* Add some common helper functions by @kkappler in https://github.com/kujaku11/mt_metadata/pull/185
* Bug fix in FC layer by @kkappler in https://github.com/kujaku11/mt_metadata/pull/186
* Fix mth5 issue 187 by @kkappler in https://github.com/kujaku11/mt_metadata/pull/187
* bug fixes by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/180
* updating how a TF is initiated, initialize xarray is expensive by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/188
* Change default value of `get_elevation` to False by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/191
* Updating git clone address in the readme by @xandrd in https://github.com/kujaku11/mt_metadata/pull/189
* Fix how Z-files read/write by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/192
* Adjust how TF._initialize_transfer_function is setup by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/193
* Add Ability to store processing configuration in TF by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/196
* Bump version: 0.3.3 → 0.3.4 by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/198


0.3.5 ()
---------------------

* Patches by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/200
* Fix issue #202 by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/203
* Patches by @kkappler in https://github.com/kujaku11/mt_metadata/pull/205
* Bump version: 0.3.4 → 0.3.5 by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/206

0.3.6 ()
---------------------

* add method for accessing mag channel names by @kkappler in https://github.com/kujaku11/mt_metadata/pull/210
* Patches by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/208
* Fix mth5 issue 207 by @kkappler in https://github.com/kujaku11/mt_metadata/pull/209
* Minor changes  by @kkappler in https://github.com/kujaku11/mt_metadata/pull/211
* Patches by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/212

0.3.7 (2024-08-16)
---------------------

* Minor fixes numpy 2.0 by @kkappler in https://github.com/kujaku11/mt_metadata/pull/213
* Fix issue 216 by @kkappler in https://github.com/kujaku11/mt_metadata/pull/218
* Patches  by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/219
* add u0 and r0 as regression parameters by @kkappler in https://github.com/kujaku11/mt_metadata/pull/220
* Updating EMTF XML and StationXML writers by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/217
* Patches by @kkappler in https://github.com/kujaku11/mt_metadata/pull/221
* Patches by @kkappler in https://github.com/kujaku11/mt_metadata/pull/223
* Bump version: 0.3.6 → 0.3.7 by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/225 

0.3.8 (2024-09-30)
----------------------

* Add pop to ListDict by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/226
* Fix EDI Tipper flip by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/228
* Patches by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/227
* Bump version: 0.3.7 → 0.3.8 by @kujaku11 in https://github.com/kujaku11/mt_metadata/pull/229 
