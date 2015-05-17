#SCB: Access SCB data from your IPython notebook

The goal of this project is to provide a simple and uniform interface to data from Statistics Sweden (_SCB, Statistiska Centralbyrån_) directly from the [IPython Notebook](http://ipython.org/notebook.html). Specifically, it is intended to be used together with [pandas](http://pandas.pydata.org/) for iterative data analysis and manipulation.

```python
import pandas as pd
from SCB import SCB
        
scb = SCB('http://api.scb.se/OV0104/v1/doris/sv/ssd/BE/BE0101/BE0101H/FoddaK')
df = scb.filter(code='Tid', kind='item', values=['2014']).get()
```

##Background
This section describes the general outline of the API provided by SCB. The original docs can be [found here](http://www.scb.se/Grupp/OmSCB/API/API-beskrivning.pdf) (Swedish).

For any given table, the URL for the table has the following format:
```
API-NAME/API-VERSION/LANGUAGE/DATABASE-ID/<LEVELS>/TABLE-ID
```

where `API-NAME` currently translates to `http://api.scb.se/OV0104/`. The current version is 1, and possible languages are `sv` or `en`, and the `DATABASE-ID` is `ssd`. The depth of the number of levels depend on the requested table. So, effectively, any given table URL will have the following structure:

```
http://api.scb.se/OV0104/v1/sv/ssd/<LEVELS>/TABLE-ID
```
It's rarely obvious where the data you're looking for is actually located. For that reason, this library provides a cursor-like object which allows you to quickly jump around between the levels of the database. Once you find the table you're looking for, you're provided with a number of filters. SCB implements a limit of 100,000 rows per request so filtering is often needed.


##Quickstart
Here's a workflow example. Note that these operations are executed within the notebook environment.

####Finding the right table
We start by listing all the top level categories in the database. Calling the `describe` method on the `scb` instance outputs a nicely formatted HTML table with all the categories.
```python
from SCB import SCB
scb = SCB('http://api.scb.se/OV0104/v1/doris/sv/ssd')
scb.describe() # outputs an HTML table
```
We select the top level category "Arbetsmarknad" by using the `go` method on the instance and passing in the proper level id. We continue to do so until we reach our destination table.
```python
scb.go('AM')
scb.go('AM0502')
scb.go('ArbOrsakSyssSNI2007')
```

####Query the table
At this point, `scb` points to an actual table and we can call `describe` to get a list of possible filters.
```python
scb.describe() # list possible filters
scb.filter(code='Tid', kind='item', values=['2014']) # filter the results
df = scb.get() # save the data in a pandas dataframe
```
The actual HTTP request is not made until we call `get` on the instance. Boom! From this point on `df` is just your ordinary pandas dataframe. Have fun!

##Installation
Just clone this repository and import the SCB module.
