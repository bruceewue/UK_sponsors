import requests
from bs4 import BeautifulSoup
import pandas as pd
import re # Import the regular expression module

url = "https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# find the link - now using regex to find the link
links = soup.select('a.govuk-link')
csv_link = None
for link in links:
    href = link.get('href')
    if href and re.search(r'.*Worker_and_Temporary_Worker\.csv$', href): # Use regex to find the link, matching any characters before "Worker_and_Temporary_Worker.csv" and ensuring it ends with it.
        csv_link = href
        break

# find csv and process
if csv_link:
    print(f"Found CSV link: {csv_link}") # Print the found link for debugging

    try: # Add try-except block to handle potential errors during CSV reading
        df = pd.read_csv(csv_link)
        # filter data
        unique_org_names = df[df['Route'] == 'Skilled Worker']['Organisation Name'].unique()
        # save
        unique_org_names = pd.Series(unique_org_names)
        unique_org_names.to_json('skilled_worker.json', orient='values')
        print("Data successfully processed and saved to skilled_worker.json") # Confirmation message
    except Exception as e:
        print(f"Error processing CSV file: {e}") # Error message if CSV processing fails
else:
    print("CSV link not found on the page.") # Message if no CSV link is found
