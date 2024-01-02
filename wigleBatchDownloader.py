import argparse
import requests
import json
import time
import base64
from datetime import datetime
import pymongo

# MongoDB setup
MONGO_CONNECTION_STRING = "mongodb://username:password@host:port/dbname"
MONGO_COLLECTION_NAME = "wigle_data"

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
    parser.add_argument('-w', '--wifi', action='store_true', default=True, help='Fetch Wi-Fi network data (default: True).')
    parser.add_argument('-b', '--bluetooth', action='store_true', help='Fetch Bluetooth network data.')
    parser.add_argument('-f', '--filename', type=str, help='Custom filename for output.')
    parser.add_argument('-m', '--mongodb', action='store_true', help='Store data in MongoDB instead of a file.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output for debugging.')
    parser.add_argument('-d', '--dryRun', action='store_true', help='Calculate number of prepared requests only. Does not execute requests.')
    return parser.parse_args()

class WigleAPI:
    def __init__(self, api_name, api_token):
        self.base_url = "https://api.wigle.net/api/v2"
        self.session = requests.Session()
        credentials = f"{api_name}:{api_token}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.session.headers.update({"Authorization": f"Basic {encoded_credentials}"})

    def fetch_data(self, endpoint, north, south, west, east, lastupdt=None, verbose=False):
        search_url = f"{self.base_url}/{endpoint}"
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

def save_to_mongodb(data, collection_name):
    client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
    db = client.get_default_database()
    collection = db[collection_name]
    collection.insert_many(data)

def save_networks_to_file(networks, filename):
    with open(filename, 'w') as file:
        json.dump(networks, file)
    print(f"[info] {len(networks)} networks saved to {filename}")

def get_output_filename(custom_filename):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    return f"{custom_filename or 'wigle_dump'}_{timestamp}.json"

def main():
    args = parse_arguments()
    wigle_client = WigleAPI(args.apiName, args.apiToken)
    all_data = []

    if args.wifi:
        wifi_chunks = get_chunk_objects(args.north, args.south, args.west, args.east, args.chunkSize)
        if args.dryRun:
            print(f"[Dry Run] Wi-Fi: {len(wifi_chunks)} requests prepared.")
            if args.verbose:
                for i, chunk in enumerate(wifi_chunks):
                    print(f"Wi-Fi Request {i+1}: {chunk}")
        else:
            wifi_data = []
            for chunk in wifi_chunks:
                result = wigle_client.fetch_data("network/search", chunk['latrange1'], chunk['latrange2'], chunk['longrange1'], chunk['longrange2'], args.lastupdt, args.verbose)
                if result and 'results' in result:
                    wifi_data.extend(result['results'])
            all_data.extend(wifi_data)

    if args.bluetooth:
        bluetooth_chunks = get_chunk_objects(args.north, args.south, args.west, args.east, args.chunkSize)
        if args.dryRun:
            print(f"[Dry Run] Bluetooth: {len(bluetooth_chunks)} requests prepared.")
            if args.verbose:
                for i, chunk in enumerate(bluetooth_chunks):
                    print(f"Bluetooth Request {i+1}: {chunk}")
        else:
            bluetooth_data = []
            for chunk in bluetooth_chunks:
                result = wigle_client.fetch_data("bluetooth/search", chunk['latrange1'], chunk['latrange2'], chunk['longrange1'], chunk['longrange2'], args.lastupdt, args.verbose)
                if result and 'results' in result:
                    bluetooth_data.extend(result['results'])
            all_data.extend(bluetooth_data)

    if args.dryRun:
        return  # Exit the script after completing the dry run checks


    if args.mongodb:
        save_to_mongodb(all_data, MONGO_COLLECTION_NAME)
        if args.filename:
            filename = get_output_filename(args.filename)
            save_networks_to_file(all_data, filename)
    else:
        filename = get_output_filename(args.filename)
        save_networks_to_file(all_data, filename)

if __name__ == "__main__":
    main()
