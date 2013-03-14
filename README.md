python-datalanche
=================

Python client for Datalanche's REST API.

## Install

[Create an account](https://www.datalanche.com/signup) and obtain an API key. Then install the client using the
 following command:

    pip install datalanche
 
## Establishing a Connection

Create a connection object then call `authenticate()` using your account's API key which can be found in your 
[account settings](https://www.datalanche.com/account). A future release will support 
[OAuth](http://en.wikipedia.org/wiki/OAuth) which will require an API secret as well.

```python
from datalanche import *

key = 'your_api_key'
secret = '' # leave empty, needed when OAuth supported

try:
    connection = DLConnection()

    # only need to authenticate once for a given connection
    connection.authenticate(key, secret)
except DLException as e:
    print repr(e)
```
    
## GetList

`connection.get_list()` will retrieve a list of all data sets you have access to. Data sets are also listed on our 
[website](https://www.datalanche.com/datasets).

```python
try:
    data = connection.get_list()
    print json.dumps(data)
except DLException as e:
    print repr(e)
```
 
## GetSchema

`connection.get_schema()` will retrieve the schema for a given data set. It has the following format:
* `description` Description of the data set.
* `last_update` The date and time when the data set was last updated with this format: `YYYY-mm-dd HH:ii:ss`.
* `license` The license for the data set.
    * `name` The name of the license.
    * `url` A URL to the license (optional).
* `fields` A list of fields each with the following attributes:
    * `name` The name of the field.
    * `data_type` The field's type: `boolean, int16, int32, int64, float, double, string, uuid`.
    * `description` The field's description.

```python
try:
    dataset_name = 'medical_codes_ndc'
    data = connection.get_schema(dataset_name)
    print json.dumps(data)
except DLException as e:
    print repr(e)
```

## Read

`connection.read()` will retrieve rows of data for a given data set. The returned data can be 
filtered, sorted, and you can choose which fields are returned. It is similar to a SELECT statement 
in SQL.

#### Parameters

* `fields` An array of fields to return. `default = all`
* `filter` A filter which defines which rows are returned. See [Filtering](#filtering) for details.
* `limit` The number of rows to return. `default = 25, min = 1, max = 100`
* `skip` The number of rows to skip. `default = 0`
* `sort` An array of field and sort type pairs. Returned rows will be sorted in the order specified 
with the following sort types: `asc, desc`.
* `total` Boolean whether or not to include the total number of rows in the result. This may increase query time.

```python
try:
    dataset_name = 'medical_codes_ndc'
    
    params = DLReadParams()
    params.fields = ['dosage_form', 'route', 'product_type']
    params.filter = my_filter # look at the Filtering section below
    params.limit = 5
    params.skip = 0
    params.sort = ['dosage_form:asc', 'product_type:desc']
    params.total = false
    
    # you can also use helper methods for params.sort
    params.sort_asc('dosage_form')
    params.sort_desc('product_type')

    data = connection.read(dataset_name, params)
    print json.dumps(data)
except DLException as e:
    print repr(e)
```

<a name='filtering'/>
#### Filtering

Filters allow you to only return rows which meet a specified criteria. Simple filters consist of 
a field, operator, and value. Complex filters can be created by combining multiple filters using 
the AND and OR operators. It is similar to a WHERE clause in SQL.

```python
# simple filter
# dosage_form = 'capsule'
simple_filter = DLFilter('dosage_form', DLFilterOp.EQ, 'capsule')

# complex filter
# (dosage_form = 'capsule' OR dosage_form = 'tablet') AND product_type.contains('esc')
complex_filter = DLFilter(
    DLFilter(
        DLFilter('dosage_form', DLFilterOp.EQ, 'capsule'),
        DLFilterOp.OR,
        DLFilter('dosage_form', DLFilterOp.EQ, 'tablet')
    ),
    DLFilterOp.AND,
    DLFilter('product_type', DLFilterOp.CONTAINS, 'esc')
)
```

**DLFilterOp**

| Operators    | Description             | Data Types          |
|:------------ |:----------------------- |:------------------- |
| AND          | logical AND             | filter objects      |
| OR           | logical OR              | filter objects      |
| EQ           | equals                  | numeric, text, uuid |
| NOT_EQ       | not equals              | numeric, text, uuid |
| IN           | equals any in array     | numeric, text, uuid |
| NOT_IN       | not equals any in array | numeric, text, uuid |
| GT           | greater than            | numeric             |
| GTE          | greater than or equal   | numeric             |
| LT           | less than               | numeric             |
| LTE          | less than or equal      | numeric             |
| EW           | ends with               | text                |
| NOT_EW       | not ends with           | text                |
| SW           | starts with             | text                |
| NOT_SW       | not starts with         | text                |
| CONTAINS     | contains                | text                |
| NOT_CONTAINS | not contains            | text                |
