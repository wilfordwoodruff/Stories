import requests
import re
import os

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Define the remote file to retrieve
    url = 'https://wilfordwoodruffpapers.org/api/v1/pages/export'

    # Get the value of the GH_TOKEN environment variable
    woodruff_token = os.environ.get('WOODRUFF_AUTHORIZATION_HEADER')

    # Set the authorization header with the appropriate token or key
    headers = {"Authorization": woodruff_token}

    # Make http request for remote file data
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the filename from the Content-Disposition header, if present
        content_disposition = response.headers.get("Content-Disposition")
        if content_disposition:
            # Use regular expressions to extract the filename from the Content-Disposition header
            match = re.search(r'filename=(.+)', content_disposition)
            if match:
                filename = match.group(1)
            else:
                filename = "pages-export.csv"
        else:
            filename = "pages-export.csv"

        # If the request was successful, write the contents of the file to a local file
        with open(filename, "wb") as f:
            f.write(response.content)
    else:
        # If the request was not successful, print the status code and reason
        print(f"Error: {response.status_code} - {response.reason}")