from typing import List, Dict, Any
from requests import Request, Session, Response
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import datetime
import os


def set_starting_parameters(stop_file_name: str) -> None:
    """
    Set starting parameters for the API request and call the set_parameters_for_requests function.
    """
    # Print that a file is being created with the name specified
    print('create file', stop_file_name)
    # Create an empty list to hold requests
    list_for_requests: List[Any] = []
    # Define the URL for the API call
    url: str = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    # Add the stop file name and URL to the list of requests
    list_for_requests.append(stop_file_name)
    list_for_requests.append(url)
    # Call the set_parameters_for_requests function with the list of requests
    set_parameters_for_requests(list_for_requests)


def get_api_key() -> str:
    """
    Read and return the API key from a file.
    """
    # Open the file 'api_key.txt' and read the contents, stripping any whitespace from the beginning and end
    with open('api_key.txt', 'r') as f:
        api_key: str = f.read().strip()
    # Return the API key
    return api_key


def set_parameters_for_requests(list_for_requests: List[Any]) -> None:
    """
    Set parameters for the API request and call the set_headers_for_session_to_requests function.
    """
    # Create a dictionary of parameters to send with the request
    parameters: Dict[str, str] = {
        'start': '1',
        'limit': '5000',
        'convert': 'USD'
    }
    # Add the parameters to the list of requests
    list_for_requests.append(parameters)
    # Call the set_headers_for_session_to_requests function with the list of requests
    set_headers_for_session_to_requests(list_for_requests)


def set_headers_for_session_to_requests(list_for_requests: List[Any]) -> None:
    """
    Set headers for the API request and call the get_data_raw_from_requests function.
    """
    # Create a dictionary of headers to send with the request
    headers: Dict[str, str] = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': get_api_key()
    }
    # Add the headers to the list of requests
    list_for_requests.append(headers)
    # Call the get_data_raw_from_requests function with the list of requests
    get_data_raw_from_requests(list_for_requests)


def get_data_raw_from_requests(list_for_requests: List[Any]) -> None:
    """
    Make the API request, extract data and call the write_json_from_loads function to write data to a file.
    """
    # Print the name of the file being created for the day
    print('file for the day:', list_for_requests[0])
    try:
        # Create a session and set the headers
        session: Session = Session()
        session.headers.update(list_for_requests[3])
        # Send a GET request to the API with the specified URL and parameters
        response: Response = session.get(list_for_requests[1], params=list_for_requests[2])
        # Load the JSON data from the response
        data: Dict[str, Any] = json.loads(response.text)
        # Extract the data for the coins in USD
        coins_usd_raw: List[Dict[str, Any]] = data.get('data')
        # Write the full set of data to a file with a name corresponding to the current date
        write_json_from_loads(list_for_requests[0], coins_usd_raw)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        # Print any errors encountered during the request
        print(e)


def create_json_file_name() -> None:
    """
    Create a file name based on the current date and call the check_previous_upload_file function.
    """
    # Print the current date
    print("Current date:", datetime.date.today())
    # Get the current date and save it as a variable
    stop_file_name_raw: datetime.date = datetime.date.today()
    # Append the extension ".json" to the current date to form the filename
    stop_file_name: str = str(stop_file_name_raw) + '.json'
    # Call the check_previous_upload_file function with the newly created filename
    check_previous_upload_file(stop_file_name)


def check_previous_upload_file(stop_file_name: str) -> None:
    """
    Check the presence of the previous upload file for today.
    If the file is not found, call the set_starting_parameters function.
    If the file is found, resume uploading with that file by calling the set_starting_parameters function.
    """
    # Initialize an empty list to store the names of existing JSON files in the directory
    json_files_upload_list: List[str] = []
    # Print the current directory
    print("Current directory:", os.getcwd())
    # Change the directory to the JSON subdirectory
    os.chdir("JSON")
    # Print the current working directory
    print("Working directory:", os.getcwd())
    # Get a list of all files in the directory and save it in json_files_upload_list
    json_files_upload_list = os.listdir()

    # If there are no files in the directory, start a new file with the filename specified
    if not json_files_upload_list:
        print("Directory is empty. Starting new file.")
        set_starting_parameters(stop_file_name)
    else:
        # If there are files in the directory, loop through them to find the file with the same name as the one specified
        for file_name in json_files_upload_list:
            if file_name == stop_file_name:
                # If the file is found, resume uploading with that file
                print(f"{file_name} already exists. Resuming with that file.")
                set_starting_parameters(stop_file_name)
                break
        else:
            # If the file is not found, start a new file with the filename specified
            print(f"No file exists with name {stop_file_name}. Starting new file.")
            set_starting_parameters(stop_file_name)


def write_json_from_loads(file_name: str, coins_usd_raw: List[dict[str, Any]]) -> None:
    """
    Write the full set of data received by the request to a file with a name corresponding to the current date.
    """
    # Print the filename and the data to be written to the file
    print(file_name)
    print(coins_usd_raw)
    # Change the directory to the JSON subdirectory
    os.chdir("../JSON")
    # Open the file with the specified filename in write mode and write the data to the file
    with open(file_name, 'w') as f:
        json.dump(coins_usd_raw, f)


if __name__ == '__main__':
    create_json_file_name()