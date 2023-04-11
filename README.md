CoinMarketCap API parsing

This project is an implementation of the CoinMarketCap API to retrieve data on the latest cryptocurrency listings. The API retrieves data on cryptocurrencies' prices, volumes, and other market data.
Installation

Clone the repository to your local machine using the command:

bash

    git clone https://github.com/DrAnonim/CoinMarketCap-API.git

Install the required packages using the command:

bash

    pip install -r requirements.txt

Create a file api_key.txt in the project directory and paste your CoinMarketCap API key.
Create a folder named 'JSON'.

Usage

To start the program, run main.py from the command line.

The program retrieves data on the latest cryptocurrency listings and writes the data to a file in JSON format with a filename corresponding to the current date.

If a file with the same name already exists in the JSON folder, the program resumes with that file. Otherwise, the program creates a new file.
License

This project is licensed under the MIT License.