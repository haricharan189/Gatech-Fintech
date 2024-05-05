
# Text Analysis of SEC 10-K Filings using multiple LLM APIs

This repository contains the step-wise implementation of the tasks provided as a part of the Fintech Lab intern recruitment. Various Tech Stacks are used and certain modifications and assumptions are made for convenience.


## Tech Stack

**Pre-Processing:** sec-edgar-downloader,SEC Extractor and Query API,BeautifulSoup4

**LLM APIs:** OpenAI (gpt 3.5-turbo), Hugging Face Inference API

**App Dev:** Kivy

**Others:** Langchain



## Pre-Processing
Throughout the process, the Implementation of all the tasks has been demonstrated on Apple Filings for easy evaluation purposes.

1) **Scraping:** All the filings from 1995 to 2023 were extracted using sec-edgar python package. Due to length of the reports and repeated occurances of words, sec extractor api was used to extract certain sections for further analysis. The code for both is provided nonetheless.

2) **Cleaning:** Cleaning is done with respect to the needs of each insight that is provided which will be detailed in the upcoming sections and general cleaning technique is coded out using BeautifulSoup4.


## Insight 1 - Risk Factor Intensity Analysis
For an Investor, it is pivotal to be aware of the potential risks with which the company can be hit and the Risk Factors section (1A) ensures that investors are aware of the various risks that could impact the company's future performance and prospects. This analysis gives a crisp insight into the intensity of each risk factor mentioned in the report through which the investor can make a wise decision according to his situation.


## Steps Involved
![insight1 drawio](https://github.com/haricharan189/Gatech-Fintech/assets/127864767/11373ddd-ae86-4c58-8066-1c46544c7901)



1. **Extraction**: As the risks associated vary from time to time, it makes sense to analyse the latest report to get an up-to-date insight. We use the Extractor API to scrape Section 1A of 2023 Report.

2. **Recursive Splitting and Summarization:** As this section is large in itself, it becomes difficult to feed all the text at once through the OpenAI inference api. Hence we employ Langchain's Recursive text splitting to split the text into chunks and generate summary on each chunk and finally combine them to form a final summary.

3. **One Word and Ratings:** We use the OpenAI inference api (gpt 3.5-turbo model) to generate one word for each risk explanation in the summary and analyse it to generate an intensity rating on a scale of 10.

4. **Visualization:** We plot a simple Bar plot for the investor to visualize the intensity of each risk without any hassle.


## Insight 2 : FLS and Positive Statement Analysis
The Section 7 of the SEC 10-K filing " Management's Discussion and Analysis of Financial Condition and Results of Operations" gives us the perspective of the management and is a goldmine for investors to carefully analyze and derive insights into the company's operations, financial health, and future prospects. 

In our analysis, we employ two different aspects namely:

a. **Forward Looking Statements**: Forward-looking statements are projections or predictions made by a company about future events, performance, or outcomes. By analysing the FLS,we can make predictions about industry trends, consumer behavior, or regulatory changes that could impact the company's performance.We try to visualize the percentage of FLS in Item 7 of SEC filings across 5 years.

1. **Extraction:** We write a small base query to extract filings of AAPL from 2019-2023 using the QueryAPI. We further remove all the HTML tags and remove the table content by start/end index matching technique.

2. **Hugging Face Inference API:** We split the cleaned text into sentences and pass that into a Fine-tuned Finbert model through an Inference API and store all the sentences labelled as FLS in a list.

3. **Percentage and visualization:** We calculate the percentage of FLS for each year and plot a line graph for visualization.

b. **Positive Statements:** The steps followed for this analysis is the same as above, except we use the original finbert model through inference api and calculate the percent of positive statements and plot a similar graph. (all FLS need not be positive).












## APP
We utilize KIVY, a cross-platform Python based application development framework to develop a very simple application that takes in a ticker to display the visualization needed. Kivy was chosen as it uses python and is simple to use compareed to other frameworks.
