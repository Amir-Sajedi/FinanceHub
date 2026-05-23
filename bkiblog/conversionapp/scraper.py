import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re

class PriceScraperError(Exception):
    """Custom exception for scraper errors"""
    pass

def clean_price(price_text: str) -> float:
    if not price_text:
        raise ValueError("Empty price text")
    
    cleaned = price_text.strip().replace(',', '').replace(' ', '')
    persian_to_english = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
    arabic_to_english = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
    cleaned = cleaned.translate(persian_to_english).translate(arabic_to_english)
    
    match = re.search(r'-?\d+\.?\d*', cleaned)
    if not match:
        raise ValueError(f"No numeric value found in: {price_text}")
    
    return float(match.group())

def scrape_market_prices(url: str = 'https://www.tgju.org/', timeout: int = 10) -> Dict[str, float]:
    """
    Scrape gold, silver, and USD prices from tgju.org
    
    Returns:
        Dictionary with keys: gold_oz, gold_18k, gold_24k, silver_gram, silver_oz, usd
    """
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
    except requests.exceptions.Timeout:
        raise PriceScraperError(f"Request timed out after {timeout} seconds")
    except requests.exceptions.ConnectionError:
        raise PriceScraperError("Failed to connect to the server")
    except requests.exceptions.HTTPError as e:
        raise PriceScraperError(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise PriceScraperError(f"Request failed: {e}")
    
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        results = {}
        
        # Find all rows with data-market-row attribute
        rows = soup.find_all('tr', {'data-market-row': True})
        
        if not rows:
            raise PriceScraperError("No market data rows found on page")
        
        for row in rows:
            market_id = row.get('data-market-row')
            
            # Gold ounce
            if market_id == 'ons':
                price_td = row.find('td', class_='nf')
                if price_td:
                    try:
                        results['gold_oz'] = clean_price(price_td.text)
                    except ValueError as e:
                        print(f"Warning: Failed to parse gold_oz: {e}")
            
            # Gold 18k
            elif market_id == 'geram18':
                price_td = row.find('td', class_='nf')
                if price_td:
                    try:
                        results['gold_18k'] = clean_price(price_td.text)
                    except ValueError as e:
                        print(f"Warning: Failed to parse gold_18k: {e}")
            
            # Gold 24k
            elif market_id == 'geram24':
                price_td = row.find('td', class_='nf')
                if price_td:
                    try:
                        results['gold_24k'] = clean_price(price_td.text)
                    except ValueError as e:
                        print(f"Warning: Failed to parse gold_24k: {e}")
            
            # Silver gram
            elif market_id == 'silver_999':
                price_td = row.find('td', class_='nf')
                if price_td:
                    try:
                        results['silver_gram'] = clean_price(price_td.text)
                    except ValueError as e:
                        print(f"Warning: Failed to parse silver_gram: {e}")
            
            # Silver ounce
            elif market_id == 'silver':
                price_td = row.find('td', class_='nf')
                if price_td:
                    try:
                        results['silver_oz'] = clean_price(price_td.text)
                    except ValueError as e:
                        print(f"Warning: Failed to parse silver_oz: {e}")
            
            # USD
            elif market_id == 'price_dollar_rl':
                price_td = row.find('td', class_='market-price')
                if price_td:
                    try:
                        results['usd'] = clean_price(price_td.text)
                    except ValueError as e:
                        print(f"Warning: Failed to parse usd: {e}")
        
        # Verify we got data
        if not results:
            raise PriceScraperError("No valid prices extracted from page")
        
        expected_keys = {'gold_oz', 'gold_18k', 'gold_24k', 'silver_gram', 'silver_oz', 'usd'}
        missing_keys = expected_keys - set(results.keys())
        if missing_keys:
            print(f"Warning: Missing data for: {', '.join(missing_keys)}")
        
        return results
        
    except Exception as e:
        if isinstance(e, PriceScraperError):
            raise
        raise PriceScraperError(f"Failed to parse HTML: {e}")

def main():
    try:
        prices = scrape_market_prices()
        return prices

    except PriceScraperError as e:
        print(f"Scraper error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
if __name__ == "__main__":
    main()    