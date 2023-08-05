# Shield Cloud API Examples

The following examples require an API key to run.
A key can be obtained from https://developers.intrusion.com

This key can be placed in a file named ```apikey``` in your home directory, or coded into each of the scripts with the ```apikey``` variable

## dns_query.py
Takes a parameter and returns the result in the same format as dnspython would return it

  ```python dns_query.py intrusion.com```
  
## shieldapi_domainresolution.py
Takes a parameter, and outputs the extended information available from the Shield Cloud API

  ```python shieldapi_domainresolution.py intrusion.com```
  
## Dependencies

shieldpython has been written with the features of Python 3.8 in mind.

shieldpython requires that the common libraries ```dnspython``` and ```requests``` be installed. This can usually be done with:
```
pip3 install dnspython
pip3 install requests
```


### pfSense
On pfSense pip is not installed by default, it can be added with:
```python3.8 --ensurepip```

This will make it accessable as a module, which can be accessed with 
```python3.8 -m pip <parameters>```
