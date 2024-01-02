# wigle.net data dumper
A simple dumper for the Wigle.net API

v.0.4

## Example usage

### Find appropriate dump size
Using the `-d` parameter (dry run) you should experiment with the `chunk size` `-c` to keep the number of requests within the range of the limit your account has. Usually a free account provides 50 requests in 24h.
E.g. try: `-c 0.01` vs `-c 0.001` so the number of `requests prepared` is below 50. 
```bash
python3 wigleBatchDownloader.py --north 46.072528 --south 43.960146 --east 4.929610 --west 4.763731 -n <your API Name> -t <Your API Token> -c 0.05 -d
[info] Dry Run: 35 requests prepared.
Prepared Request 1: North: 45.072528, South: 45.047528, West: 5.763731, East: 5.788731
Prepared Request 2: North: 45.072528, South: 45.047528, West: 5.788731, East: 5.813731000000001
Prepared Request 3: North: 45.072528, South: 45.047528, West: 5.813731000000001, East: 5.838731000000001
Prepared Request 4: North: 45.072528, South: 45.047528, West: 5.838731000000001, East: 5.863731000000001
Prepared Request 5: North: 45.072528, South: 45.047528, West: 5.863731000000001, East: 5.888731000000002
Prepared Request 6: North: 45.072528, South: 45.047528, West: 5.888731000000002, East: 5.913731000000002
Prepared Request 7: North: 45.072528, South: 45.047528, West: 5.913731000000002, East: 5.92961
Prepared Request 8: North: 45.047528, South: 45.022528, West: 5.763731, East: 5.788731
Prepared Request 9: North: 45.047528, South: 45.022528, West: 5.788731, East: 5.813731000000001
...
```
 Some users had success requesting a higher limit, IDK if there's a payed option. 

### Dump data
Simply remove `-d` to start the real dump. Optionally add `-v` for verbose output. In v.0.4 the output will be written to `downloaded_data.json`.
```bash
python3 wigleBatchDownloader.py --north 46.072528 --south 43.960146 --east 4.929610 --west 4.763731 -n <your API Name> -t <Your API Token> -c 0.05 -v
[info] Query returned 100 networks.
[info] Query returned 100 networks.
[info] Query returned 100 networks.
[info] Query returned 100 networks.
...
[info] 1109 networks saved to downloaded_data.json
```

### Outlook
The next version is already in development supporting:
- date/time within the filename
- custom filename
- mongodb support
- extended data (optional bluetooth)

