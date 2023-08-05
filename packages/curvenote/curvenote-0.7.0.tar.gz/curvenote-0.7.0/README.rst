.. role:: bash(code)
   :language: bash

curvenote
#########

The Curvenote helper library for working in Jupyter Notebooks with Python kernels


Installation
************

.. code-block:: bash

    ~$ python -m pip install curvenote

Function Summary
================

 - :code:`stash` save a dict or pandas dataframe in a cell output without diaplying the data
    .. code-block:: Python

        from curvenote import stash

        stash('myvars', myvars)
