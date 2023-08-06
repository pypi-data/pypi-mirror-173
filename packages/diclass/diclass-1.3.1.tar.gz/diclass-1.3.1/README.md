# diclass: convert python dict to python class object
[![PyPI Latest Release](https://img.shields.io/pypi/v/pandas.svg)](https://pypi.org/project/diclass/)

## What is it?

**diclass** It fully converts a python dict to a python class object and all dict keys and internal dict are converted to python class objects as well.


```python
# !pip install diclass
```

## Example


```python
from diclass import DictClass
import pandas as pd
import numpy as np
obj = DictClass({'id':1, 'data':{'name':'John', 'age':31, 'wife':{'name':'Jessica', 'age':np.nan}}})

print(obj.id, obj.data.name, obj.data.wife.name)
```

    1 John Jessica



```python
obj
```




    {'id': 1, 'data': {'name': 'John', 'age': 31, 'wife': {'name': 'Jessica', 'age': nan}}}


