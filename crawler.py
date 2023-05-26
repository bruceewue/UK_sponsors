import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# find the link
links = soup.select('a.govuk-link')
csv_link = None
for link in links:
    href = link.get('href')
    if href and href.startswith('https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file'):
        csv_link = href
        break

# find csv
if csv_link:

    df = pd.read_csv(csv_link)
    # filter data
    unique_org_names = df[df['Route'] == 'Skilled Worker']['Organisation Name'].unique()
    # save
    unique_org_names = pd.Series(unique_org_names)
    unique_org_names.to_json('skilled_worker.json', orient='values')