# MacToManufacturer

#### A simple python library to find the manufacturer of a device by using macaddress.

### How to use:
<b>Example:</b>
```
from MacToManufacturer import MacToMan

macToManObj = MacToMan()
results = macToManObj.search("A8-93-4A-DA-6F-19")
print(results)
```
You can also pass the macaddress seprated by ":"
```
from MacToManufacturer import MacToMan

macToManObj = MacToMan()
results = macToManObj.search("A8:93:4A:DA:6F:19")
print(results)
```

### Installation:
```
pip3 install MacToManufacturer
```
### How does this work?
This library contains csv file which contains the starting 3 octlets and the manufacturer.
MacToMan searches through this csv file and returns the manufacturer.
#### How the csv is generated?
Wireshark has a file which contains all the IEEE lists of mac addresses and manufacturers & more.
The file is names manuf.
There is a script named as generate_csv.py in script/, It downloads the latest manuf file and converts it to a csv file.
