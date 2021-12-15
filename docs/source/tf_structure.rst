========================
Transfer Functions
========================

The `transfer_functions` module deals with various formats that transfer functions are stored in.  This includes reading and writing for most formats.      

Supported Formats
------------------

.. list-table:: 
    :widths: 25 50 20 20
    :header-rows: 1
	
    * - Format
      - Description
      - Read
      - Write
    * - **EDI**
      - Common `SEG format <https://library.seg.org/doi/abs/10.1190/1.1892244>`_ 
      - Yes
      - Yes
    * - **EMTFXML**
      - Anna Kelbert's `XML format <https://library.seg.org/doi/10.1190/geo2018-0679.1>`_, archive format at `IRIS <https://eos.org/science-updates/taking-magnetotelluric-data-out-of-the-drawer>`_  
      - Yes
      - Yes
    * - **ZFiles**
      - Output from Gary Egbert's EMFT processing code [.zmm, .zrr, .zss]
      - Yes
      - Yes
    * - **JFiles**
      - Jones' format, also output of Alan Chave's BIRRP code [.j]
      - Yes
      - No
    * - **Zonge AVG**
      - Zonge International .avg format out put by their MTEdit code [.avg]
      - Yes
      - No
	  
Structure
-------------

Modules exists for each supported format, but should only be used under the hood.  Instead, the `transfer_functions` module was set up to have a common container for any transfer function.  This is the :class:`mt_metadata.transfer_functions.core.TF` object.  It can read any supported format and write those that have write methods.  

The :class:`mt_metadata.transfer_functions.core.TF` object contains standard metadata and the data are stored in an :class:`xarray.DataSet` for generalization and easy access to elements.  
