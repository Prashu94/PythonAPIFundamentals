import requests

url = "https://coinranking1.p.rapidapi.com/coins"
# querystring = {"referenceCurrencyUuid": "yhjMzLPhuIDl", "timePeriod": "24h", "tiers[0]": "1", "orderBy": "marketCap",
#               "orderDirection": "desc", "limit": "50", "offset": "0"}

queryStringStats = {"referenceCurrencyUuid": "yhjMzLPhuIDl"}
headers = {
    "X-RapidAPI-Host": "coinranking1.p.rapidapi.com",
    "X-RapidAPI-Key": "5e827a7b2dmshc14d9a2393c5257p18e1e0jsnef1466f1cc4f"
}


def get_stats_data():
    # response = requests.request('GET', url, headers=headers, params=querystring)
    response = requests.request('GET', url, headers=headers, params=queryStringStats)
    stats = {}
    if response.json().get('status') == 'success':
        stats = response.json().get('data').get('stats')
    return stats


print(get_stats_data())
