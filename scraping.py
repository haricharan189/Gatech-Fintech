#pip install -U sec-edgar-downloader (Downloading the sec-edgar python package)

from sec_edgar_downloader import Downloader 
 
def get_sec_10k_filings(ticker, after="1995-01-01", before="2023-12-31"): #function to scrape the data to the current working dir
    dl = Downloader("NITK", "sharicharana@gmail.com")  #initializing org-name and email
    filings = dl.get("10-K", ticker, after=after, before=before)
    return filings

filings_aapl = get_sec_10k_filings("AAPL") #example usage

'''
def get_sec_10k_filings(tickers, after="1995-01-01", before="2023-12-31"): # function to get filings of multiple tickers
    dl = Downloader()
    all_filings = {}
    for ticker in tickers:
        filings = dl.get("10-K", ticker, after=after, before=before)
        all_filings[ticker] = filings
    return all_filings

    USAGE: (We obtain a dictionary through which we can iterate)
    tickers = ["AAPL", "GOOGL", "MSFT"]
all_filings = get_sec_10k_filings(tickers)
for ticker, filings in all_filings.items():
    print(f"Filings for {ticker}: {filings}")'''

