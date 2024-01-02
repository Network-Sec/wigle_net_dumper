import argparse
import requests
import json
import time
import base64

def parse_arguments():
    parser = argparse.ArgumentParser(description='Batch download data from Wigle.net API.')
    parser.add_argument('--north', type=float, required=True, help='Maximum latitude (north boundary).')
    parser.add_argument('--south', type=float, required=True, help='Minimum latitude (south boundary).')
    parser.add_argument('--west', type=float, required=True, help='Minimum longitude (west boundary).')
    parser.add_argument('--east', type=float, required=True, help='Maximum longitude (east boundary).')
    parser.add_argument('-n', '--apiName', required=True, help='Wigle.net API Name.')
    parser.add_argument('-t', '--apiToken', required=True, help='Wigle.net API Token.')
    parser.add_argument('-c', '--chunkSize', type=float, default=0.005, help='Set the chunkSize. Default is 0.005.')
    parser.add_argument('-l', '--lastupdt', help='Search only networks found since YYYYMMDDHHMMSS.')
    parser.add_argument('-d', '--dryRun', action='store_true', help='Calculate number of prepared requests only. Does not execute requests.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output for debugging.')
    
    return parser.parse_args()

class WigleAPI:
    def __init__(self, api_name, api_token):
        self.base_url = "https://api.wigle.net/api/v2"
        self.session = requests.Session()
        credentials = f"{api_name}:{api_token}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.session.headers.update({"Authorization": f"Basic {encoded_credentials}"})

    def fetch_data(self, north, south, west, east, lastupdt=None, verbose=False):
        search_url = f"{self.base_url}/network/search"
        params = {
            "latrange1": south,
            "latrange2": north,
            "longrange1": west,
            "longrange2": east,
            "lastupdt": lastupdt
        }

        if verbose:
            print(f"Requesting: {search_url} with params: {params}")

        response = self.session.get(search_url, params=params)

        if verbose:
            print(f"Response Status: {response.status_code}")

        if response.status_code == 200:
            response_json = response.json()
            if verbose:
                print(f"Response JSON: {response_json}")
            return response_json
        else:
            if verbose:
                print(f"Error: {response.status_code}, {response.text}")
            return None

def get_chunk_objects(north, south, west, east, chunk_size):
    chunk_objects = []
    x = north
    while x > south:
        y = west
        while y < east:
            chunk = {
                "latrange1": x,
                "latrange2": max(x - chunk_size, south),
                "longrange1": y,
                "longrange2": min(y + chunk_size, east)
            }
            chunk_objects.append(chunk)
            y += chunk_size
        x -= chunk_size
    return chunk_objects

def save_networks_to_file(networks, filename):
    with open(filename, 'w') as file:
        json.dump(networks, file)
    print(f"[info] {len(networks)} networks saved to {filename}")

def main():
    args = parse_arguments()
    wigle_client = WigleAPI(args.apiName, args.apiToken)

    chunks = get_chunk_objects(args.north, args.south, args.west, args.east, args.chunkSize)
    if args.dryRun:
        print(f"[info] Dry Run: {len(chunks)} requests prepared.")
        if args.verbose:
            for i, chunk in enumerate(chunks):
                print(f"Prepared Request {i+1}: North: {chunk['latrange1']}, South: {chunk['latrange2']}, "
                      f"West: {chunk['longrange1']}, East: {chunk['longrange2']}")
    else:
        all_networks = []
        for i, chunk in enumerate(chunks):
            result = wigle_client.fetch_data(chunk['latrange1'], chunk['latrange2'], chunk['longrange1'], chunk['longrange2'], args.lastupdt, args.verbose)
            if result and 'results' in result and result['results']:
                networks = result['results']
                if args.verbose:
                    print(f"[info] Query returned {len(networks)} networks.")
                all_networks.extend(networks)
            else:
                if args.verbose:
                    print(f"[info] No networks found for chunk {i+1}.")
            time.sleep(1)  # Implementing rate limiting

        unique_networks = {network['netid']: network for network in all_networks}.values()
        save_networks_to_file(list(unique_networks), 'downloaded_data.json')

if __name__ == "__main__":
    main()
