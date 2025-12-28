import requests

url = "https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp"

params = {
    "csv.x": "yes",
    "Datefrom": "01/12/2025",
    "Dateto": "05/12/2025",
    "SeriesCodes": "IUDSOIA",
    "CSVF": "TN",
    "UsingCodes": "Y",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.bankofengland.co.uk/",
}

response = requests.get(url, params=params, headers=headers)
response.raise_for_status()

print(response.text)