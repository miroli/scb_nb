#SCB: Access SCB data from your IPython notebook

The goal of this project is to provide a simple and uniform interface to data from Statistics Sweden (_SCB, Statistiska Centralbyrån_) directly from the [IPython Notebook](http://ipython.org/notebook.html). Specifically, it is intended to be used together with [pandas](http://pandas.pydata.org/) for iterative data analysis and manipulation.

```python
import pandas as pd
from SCB import SCB
        
scb = SCB('http://api.scb.se/OV0104/v1/doris/sv/ssd/BE/BE0101/BE0101H/FoddaK')
response = scb.filter(code='Tid', kind='item', values=['2014']).get()
df = pd.read_csv(response)
```

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
data = scb.get() # fetch the data
```

####Plug in to pandas
`data` contains all the returned data in CSV format as a `StringIO` object. This means that we can just pass the object to a pandas DataFrame constructor with the `read_csv` method.
```python
import pandas as pd
df = pd.read_csv(data)
```

Boom! From this point on `df` is just your ordinary pandas dataframe. Have fun!

##Installation
Just clone this repository and import the SCB module.
