import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from extract_metdata import main as extract_data  # Import the extraction function
#from extract_hydro_data import main as extract_hydro_catchment_data
import time  # Import the time module

webpage_url = 'https://meteo.gov.lk/index.php?lang=en'

def get_daily_pdf_link(webpage_url):
    try:
        response = requests.get(webpage_url, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        specific_li = soup.find('li', {'data-id': '567', 'data-level': '2'})
        if specific_li:
            specific_link = specific_li.find('a', href=True)
            if specific_link:
                daily_link = specific_link['href']
                if not daily_link.startswith('http'):
                    daily_link = requests.compat.urljoin(webpage_url, daily_link)
                return daily_link

        print("Specific link not found.")
        return None

    except requests.RequestException as e:
        print(f"An error occurred while fetching the webpage: {e}")
        return None

def download_pdf(pdf_url):
    try:
        response = requests.get(pdf_url, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        date_string = datetime.now().strftime('%Y-%m-%d')
        local_filename = f'metdata/daily_climate_update_{date_string}.pdf'

        os.makedirs(os.path.dirname(local_filename), exist_ok=True)

        with open(local_filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded PDF: {local_filename}")
        return local_filename  # Return the full path of the downloaded PDF

    except requests.RequestException as e:
        print(f"An error occurred while downloading the PDF: {e}")
        return None

if __name__ == "__main__":
    # Download the PDF and return its path
   
        pdf_url = get_daily_pdf_link(webpage_url)
        if pdf_url:
            downloaded_pdf_path = download_pdf(pdf_url)
            if downloaded_pdf_path:
                # Call the extraction function with the downloaded PDF path
                extract_data(downloaded_pdf_path)
                #extract_hydro_catchment_data(downloaded_pdf_path)
        else:
            print("Failed to get PDF link, retrying...")
        
         
