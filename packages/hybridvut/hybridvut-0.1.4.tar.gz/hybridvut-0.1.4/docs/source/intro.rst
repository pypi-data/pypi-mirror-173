#####
Usage
#####

This package provides functionalities to deal with hybrid IO-LCA based on the Make and Use framework.
Key features are:

* hybridization of a foreground and a background system
* unit handling using `iam_units <https://github.com/IAMconsortium/units>`_ (`pint units <https://pint.readthedocs.io/en/stable/>`_)
* functions for data handling (e.g. region aggregation, RAS)
* basic IO calculations (e.g. transaction and multiplier matrices)
* preprocessing to bring raw data into the right format (i.e. message-ix data)

Additional hybridization procedures might be implemented in future work. Furthermore, functions can be also applied just to a single system.

A detailed documentation can be found here: https://exiobase.gitlab.io/hybridvut/ .



Installation
------------
hybridvut is registered at PyPI. You can install it in your pathon environmnet by:

.. code-block:: bash

    pip install hybridvut


The source-code is available at GitLab repository: https://gitlab.com/exiobase/hybridvut .
You can flso ork and install it.



Core functions
--------------

After installing hybridvut, you can define your systems based on the make and use framework.

.. code-block:: python

    import hybridvut as hyb

    # define a foreground and a background system using pd.DataFrames
    foreground_VUT = hyb.VUT(V=V_for, U=U_for, F=F_for, Q=None)
    background_VUT = hyb.VUT(V=V_back, U=U_back, F=F_back, Q=Q_back)

    # combine both in a instance of class HybridTables
    HT = hyb.HybridTables(forground=foreground_VUT, background=background_VUT)

    # create a hybridized system by applying a hybridization procedure
    HT.hybridize(H, H1, HF) # H, H1 and HF are concordance matrices to be defined

    # show the resulting hybridized total system
    HT.total.V
    HT.total.U
    HT.total.F
    HT.total.Q

    # show the original data of the forgeground system
    HT.foreground.V
    HT.foreground.U
    HT.foreground.F
    HT.foreground.Q

    # show the of original data the background  system
    HT.background.V
    HT.background.U
    HT.background.F
    HT.background.Q


Utility functions
-----------------

The package include several functions those can be applied to make and use tables of the systems, e.g., unit conversion, country aggregation.
