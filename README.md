# wigle.net data dumper
A simple dumper for the Wigle.net API

v.0.4

## Example usage

### Find appropriate dump size
Using the `-d` parameter (dry run) you should experiment to keep the number of requests within the range of the limit your account has. Usually a free account provides 50 requests in 24h.
```bash
python3 wigleBatchDownloader.py --north 46.072528 --south 43.960146 --east 4.929610 --west 4.763731 -n <your API Name> -t <Your API Token> -c 0.05 -d
```
 Some users had success requesting a higher limit, IDK if there's a payed option. 

### Dump data
Simply remove `-d` to start the real dump. Optionally add `-v` for verbose output. In v.0.4 the output will be written to `downloaded_data.json`.
```bash
python3 wigleBatchDownloader.py --north 46.072528 --south 43.960146 --east 4.929610 --west 4.763731 -n <your API Name> -t <Your API Token> -c 0.05 -v
[info] Query returned 100 networks.
[info] 1109 networks saved to downloaded_data.json
```

### Outlook
The next version is already in development supporting:
- date/time within the filename
- custom filename
- mongodb support
- extended data (optional bluetooth)

