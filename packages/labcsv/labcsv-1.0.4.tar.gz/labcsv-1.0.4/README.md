# labcsv.py
You can easily get the data you need columns from [lab.js](https://github.com/FelixHenninger/lab.js).csv!

# Installation
`pip install labcsv`


# How to Use
## Read CSV
```python
from labcsv import read_csv,DefaultHeaderName as LHName
rlab = read_csv("tests/test.csv") #<- path
```
### Read columns as any type
+ default: "001" -> 1.0
+ str type: "001" -> "001"
```python
rlab = read_csv("tests/test.csv",dtype={"Param2":str})
```
*"Param2" is a header name  
*The specifications are the same as for pandas.
## Get columns data
### The return type is ndarry (get_column_values)

```python
values = rlab.get_column_values(LHName.SENDER) #n×1 size
# or
values = rlab.get_column_values([LHName.SENDER,LHName.RESPONSE,LHName.DURATION]) # n×3 size
# or
values = rlab.get_column_values("Param1") #custom column name
# or 
values = rlab.get_column_values([LHName.SENDER, "Param1"]) #multiple
```
### The return type is list (get_column_list)

```py
senders,time_commits = rlab.get_column_list([LHName.SENDER,LHName.TIME_COMMIT])
print(senders)
print(time_commits)
```

## nan to Empty String

```python
from labcsv import read_csv,DefaultHeaderName as LHName
rlab = read_csv("tests/test.csv")
rlab.pandas_data.fillna('', inplace=True) #<---
print(rlab.get_column_values("Param1"))
```
You can use pandas functions.

## Get meta
```python
meta = rlab.get_meta()
print(meta["labjs_version"])
print(meta["language"])
print(meta["location"])
```

