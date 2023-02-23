# TOOLS1_FINAL_PROJECT

COMP4447 Data Science Tools 1 Final Project
- This project uses Python:3.8

Project Members:
- Jimmy Zhang
- Max Condong

## Objective
Perform data cleaning, feature engineering, and exploratory analysis on web scraped data from Zillow to understand major factors that influence home listing sale price. 

## Analysis Summary
Due to the website's anti-scraping threshold, our analysis is limited to active home listings in Vancouver BC and Los Angeles CA. We created bounding boxes of 
latitudes and longitudes for two cities - Vancouver, BC in Canada and Los Angeles, CA in USA - and subdivided our search into smaller partitions to get around
Zillow's web scraper blocking. As both cities are coastal cities, we engineered a new feature to measure the distance of the listed properties to the city coastline
and this was done by creating a polyline that roughly traces the coast line to the pacific ocean and then estimating the property's distance to the nearest point 
along the polyline. Listings for both cities were merged to obtain an initial list of ~15,000 properties and the data was read using Pandas as dataframe objects.
The data collected suffered from duplicate columns and rows, erroneous data formats and existence of outliers and additional steps were taken to address these
issues and to transform key attributes.

## Project Directory
- [Webscraper Code](https://github.com/jimmyyih518/TOOLS1_FINAL_PROJECT/tree/main/src/webscraper)
- [Data Manipulation Code](https://github.com/jimmyyih518/TOOLS1_FINAL_PROJECT/tree/main/src/data_manipulation)
- [Scraped Data from Zillow](https://github.com/jimmyyih518/TOOLS1_FINAL_PROJECT/blob/main/data/zillow_all_listings_scraped.json)
- [Final Notebook](https://github.com/jimmyyih518/TOOLS1_FINAL_PROJECT/blob/main/Final_Notebook.ipynb)

## References
Data Analysis: predicting the housing market using Python, W.Weldon, Mar 2019, reference link

Real Estate House Price Prediction Using Data Science, Varun Sonavni, Sept 2021, reference link

House Prices - Exploratory Data Analysis, Amazon AWS, reference link

Web Scrape Zillow Real Estate Data, Manthan Koolwal, May 2022, reference link

Housing Market Activity Off to a Slow Start, Brendon Ogmundson, Feb 2023, BCREA, reference link

Canadian home sales begin 2023 at 14-year low, Pierre Leduc, Feb 2023, CREA, reference link

The Housing and Economic Experiences of Immigrants in US and Canadian Cities, Carlos Texeira, University of Toronto Press 2015, reference link

VANCOUVER REAL ESTATE MARKET UPDATE JANUARY 2023, Alan Kelly, Feb 2023, Bode, reference link

Los Angeles Housing Market: Prices, Trends, Forecast 2023, Marco Santarelli, Feb 2023, Norada, reference link

California Housing Market Report, Gord Collins, Jan 2023, ManageCasa, reference link

