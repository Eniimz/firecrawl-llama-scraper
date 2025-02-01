from firecrawl import FirecrawlApp
import ollama
import json

app = FirecrawlApp(api_key="fc-6d74df6872c0461ebef360fce2f44ca0")

print("Starting scraping the url...")
# Scrape a website:
scrape_result = app.scrape_url('https://amazon.com/s?k=gaming laptops', params={'formats': ['markdown']})


print("Url has been scraped...?")

