import os
import requests
import re
import argparse

def get_data(url, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content_disposition = response.headers.get("Content-Disposition")
        if content_disposition:
            match = re.search(r'filename=(.+)', content_disposition)
            if match:
                filename = match.group(1)
            else:
                filename = "pages-export.csv"
        else:
            filename = "pages-export.csv"

        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        print(f"Error: {response.status_code} - {response.reason}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', default=os.getenv('API_KEY'), help='API key')
    args = parser.parse_args()

    api_key = args.api_key

    if not api_key:
        print("Error: No API key provided. Please set the API_KEY environment variable or use the --api_key argument.")
        exit(1)

    url = 'https://wilfordwoodruffpapers.org/api/v1/pages/export'
    get_data(url, api_key)
