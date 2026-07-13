"""
Real-time market data fetcher
Gets live prices from CoinGecko and Yahoo Finance APIs
"""
import requests
import json
from datetime import datetime

def fetch_crypto_prices():
    """Fetch live crypto prices from CoinGecko"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': 'bitcoin,ethereum,microstrategy',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true'
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'BTC': {
                    'price': data['bitcoin']['usd'],
                    'change_24h': data['bitcoin'].get('usd_24h_change', 0)
                },
                'ETH': {
                    'price': data['ethereum']['usd'],
                    'change_24h': data['ethereum'].get('usd_24h_change', 0)
                },
                'MSTR': {
                    'price': data['microstrategy']['usd'] if 'microstrategy' in data else None,
                    'change_24h': data.get('microstrategy', {}).get('usd_24h_change', 0)
                }
            }
    except Exception as e:
        return {'error': str(e)}
    
    return {}

def fetch_stock_price(symbol):
    """Fetch stock price from Yahoo Finance"""
    try:
        # Yahoo Finance API endpoint
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            result = data['chart']['result'][0]
            meta = result['meta']
            
            price = meta.get('regularMarketPrice', 0)
            prev_close = meta.get('previousClose', price)
            change_pct = ((price - prev_close) / prev_close * 100) if prev_close else 0
            
            return {
                'price': price,
                'change_24h': round(change_pct, 2)
            }
    except Exception as e:
        return {'error': str(e)}
    
    return {}

def fetch_all_market_data():
    """Fetch all market data"""
    result = {
        'timestamp': datetime.now().isoformat(),
        'source': 'live_api',
        'assets': {}
    }
    
    # Get crypto prices
    crypto = fetch_crypto_prices()
    if 'error' not in crypto:
        result['assets'].update(crypto)
    
    # Get stock prices (for MSTR and HIMS)
    for symbol in ['MSTR', 'HIMS']:
        stock = fetch_stock_price(symbol)
        if 'error' not in stock and stock:
            result['assets'][symbol] = stock
    
    return result

if __name__ == '__main__':
    data = fetch_all_market_data()
    print(json.dumps(data, indent=2))
