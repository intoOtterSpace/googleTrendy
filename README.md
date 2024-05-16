# googleTrendy
Simple script for building csv files with large quantities of data from Google Trends using pytrends unofficial API

## Input fields:  

**item_list:** The keywords that you want trends results for.  

**primary_key:** Select the most responsive keyword from item_list to be the primary key, then remove or comment out the keyword from item_list.  
You may need to experiment with keywords to find which is strongest.

**timeframe:** Provide start and end dates in YYYY-MM-DD format.

**gproperty:** The Google property to filter i.e. web, images news etc.  
Can be images, news, youtube or froogle (for Google Shopping results).  
Defaults to web searches.

**region:** Uses 2 letter abbreviations.  
Complete list available [here](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).

**category:** Narrow results by selecting a topic by entering its assigned code i.e. food and drink is 71  
Complete list available [here](https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories).
