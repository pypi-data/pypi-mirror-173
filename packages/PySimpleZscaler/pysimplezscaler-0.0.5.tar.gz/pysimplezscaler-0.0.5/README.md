# PySimpleZscaler

A simple wrapper for some basic ZScaler API functionality. Its purpose is to make it
developing of scripts which utilize ZIA.

Module mainly consists of functions for looking up URLs and updating categories.
Session is represented as ZscalerSession class' object.

## Example
Here is example of starting new session with ZScaler API and looking up some URLs.
```
from PySimpleZscaler import zscaler as zs

zscaler = zs.ZScalerSession(cloud_name, base_path, username, password, api_key)
lookupResult = zscaler.lookup_urls(['testurl1.com'])
print(lookupResult)
zscaler.delete()
```