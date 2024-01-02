# Wigle.net data dumper
A simple dumper for the Wigle.net API

v.0.9

`Warning`: MongoDB support is untested yet. 

## Wigle.net API token
Get it here: https://wigle.net/account   

Note: API Name / Token is different from `user` / `password`

## Parameters
```bash
$ python wigleBatchDownloader.py -h
usage: wigleBatchDownloader.py [-h] --north NORTH --south SOUTH --west WEST --east EAST -n APINAME -t APITOKEN [-c CHUNKSIZE] [-l LASTUPDT] [-w] [-b]
                               [-f FILENAME] [-m] [-v] [-d]

Batch download data from Wigle.net API.

options:
  -h, --help            show this help message and exit
  --north NORTH         Maximum latitude (north boundary).
  --south SOUTH         Minimum latitude (south boundary).
  --west WEST           Minimum longitude (west boundary).
  --east EAST           Maximum longitude (east boundary).
  -n APINAME, --apiName APINAME
                        Wigle.net API Name.
  -t APITOKEN, --apiToken APITOKEN
                        Wigle.net API Token.
  -c CHUNKSIZE, --chunkSize CHUNKSIZE
                        Set the chunkSize. Default is 0.005.
  -l LASTUPDT, --lastupdt LASTUPDT
                        Search only networks found since YYYYMMDDHHMMSS.
  -w, --wifi            Fetch Wi-Fi network data (default: True).
  -b, --bluetooth       Fetch Bluetooth network data.
  -f FILENAME, --filename FILENAME
                        Custom filename for output.
  -m, --mongodb         Store data in MongoDB instead of a file.
  -v, --verbose         Enable verbose output for debugging.
  -d, --dryRun          Calculate number of prepared requests only. Does not execute requests.

```

## Example usage

### Find appropriate dump size
Using the `-d` parameter (dry run) you should experiment with the `chunk size` `-c` to keep the number of requests within the range of the limit your account has. Usually a free account provides 50 requests in 24h.  

E.g. try: `-c 0.01` vs `-c 0.001` so the number of `requests prepared` is below 50.   

```bash
$ python3 wigleBatchDownloader.py --north 46.072528 --south 43.960146 --east 4.929610 --west 4.763731 -n <your API Name> -t <Your API Token> -c 0.05 -d -b -v
[Dry Run] Wi-Fi: 12 requests prepared.
Wi-Fi Request 1: {'latrange1': 45.072528, 'latrange2': 45.022528, 'longrange1': 4.763731, 'longrange2': 4.813731}
Wi-Fi Request 2: {'latrange1': 45.072528, 'latrange2': 45.022528, 'longrange1': 4.813731, 'longrange2': 4.863731}
Wi-Fi Request 3: {'latrange1': 45.072528, 'latrange2': 45.022528, 'longrange1': 4.863731, 'longrange2': 4.913730999999999}
Wi-Fi Request 4: {'latrange1': 45.072528, 'latrange2': 45.022528, 'longrange1': 4.913730999999999, 'longrange2': 4.92961}
Wi-Fi Request 5: {'latrange1': 45.022528, 'latrange2': 44.972528000000004, 'longrange1': 4.763731, 'longrange2': 4.813731}
Wi-Fi Request 6: {'latrange1': 45.022528, 'latrange2': 44.972528000000004, 'longrange1': 4.813731, 'longrange2': 4.863731}
Wi-Fi Request 7: {'latrange1': 45.022528, 'latrange2': 44.972528000000004, 'longrange1': 4.863731, 'longrange2': 4.913730999999999}
Wi-Fi Request 8: {'latrange1': 45.022528, 'latrange2': 44.972528000000004, 'longrange1': 4.913730999999999, 'longrange2': 4.92961}
Wi-Fi Request 9: {'latrange1': 44.972528000000004, 'latrange2': 44.960146, 'longrange1': 4.763731, 'longrange2': 4.813731}
Wi-Fi Request 10: {'latrange1': 44.972528000000004, 'latrange2': 44.960146, 'longrange1': 4.813731, 'longrange2': 4.863731}
Wi-Fi Request 11: {'latrange1': 44.972528000000004, 'latrange2': 44.960146, 'longrange1': 4.863731, 'longrange2': 4.913730999999999}
Wi-Fi Request 12: {'latrange1': 44.972528000000004, 'latrange2': 44.960146, 'longrange1': 4.913730999999999, 'longrange2': 4.92961}
[Dry Run] Bluetooth: 12 requests prepared.
Bluetooth Request 1: {'latrange1': 45.072528, 'latrange2': 45.022528, 'longrange1': 4.763731, 'longrange2': 4.813731}
Bluetooth Request 2: {'latrange1': 45.072528, 'latrange2': 45.022528, 'longrange1': 4.813731, 'longrange2': 4.863731}
Bluetooth Request 3: {'latrange1': 45.072528, 'latrange2': 45.022528, 'longrange1': 4.863731, 'longrange2': 4.913730999999999}
Bluetooth Request 4: {'latrange1': 45.072528, 'latrange2': 45.022528, 'longrange1': 4.913730999999999, 'longrange2': 4.92961}
Bluetooth Request 5: {'latrange1': 45.022528, 'latrange2': 44.972528000000004, 'longrange1': 4.763731, 'longrange2': 4.813731}
Bluetooth Request 6: {'latrange1': 45.022528, 'latrange2': 44.972528000000004, 'longrange1': 4.813731, 'longrange2': 4.863731}
Bluetooth Request 7: {'latrange1': 45.022528, 'latrange2': 44.972528000000004, 'longrange1': 4.863731, 'longrange2': 4.913730999999999}
Bluetooth Request 8: {'latrange1': 45.022528, 'latrange2': 44.972528000000004, 'longrange1': 4.913730999999999, 'longrange2': 4.92961}
Bluetooth Request 9: {'latrange1': 44.972528000000004, 'latrange2': 44.960146, 'longrange1': 4.763731, 'longrange2': 4.813731}
Bluetooth Request 10: {'latrange1': 44.972528000000004, 'latrange2': 44.960146, 'longrange1': 4.813731, 'longrange2': 4.863731}
Bluetooth Request 11: {'latrange1': 44.972528000000004, 'latrange2': 44.960146, 'longrange1': 4.863731, 'longrange2': 4.913730999999999}
Bluetooth Request 12: {'latrange1': 44.972528000000004, 'latrange2': 44.960146, 'longrange1': 4.913730999999999, 'longrange2': 4.92961}
```
 Some users had success requesting a higher limit, IDK if there's a payed option.   

### Dump data
Simply remove `-d` to start the real dump. Optionally add `-v` for verbose output. By default the output will be written to `wigle_dump_2024-01-02_03-34.json`. You can supply a custom filename using `-f <your filename>`.
```bash
$ python3 wigleBatchDownloader.py --north 46.072528 --south 43.960146 --east 4.929610 --west 4.763731 -n <your API Name> -t <Your API Token> -c 0.05 -v
[info] Query returned 100 networks.
[info] Query returned 100 networks.
[info] Query returned 100 networks.
[info] Query returned 100 networks.
...
[info] 1109 networks saved to downloaded_data.json
```
Keep in mind, json uses `unicode` for special chars, this is not an error. 

