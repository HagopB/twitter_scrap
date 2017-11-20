# Twitter scrap #

### What is this repository for? 
A python script for Twitter Search scraping based on an [implementation provided by Tom Dickinson](https://github.com/tomkdickinson/Twitter-Search-API-Python). 

### How do I get set up ?
##### Step by step:
Install:
* requests 
* pickle
* BeautifulSoup
```
pip install requests
pip install pickle
pip install BeautifulSoup
```
### How do I get tweets ?
you may have information on how to run ```scrap.py``` by:
```
python scrap.py --help
```
you can get tweets (streaming) by running:
```
python scrap.py --scrap_type="stream" --search_query_list="deep learning,machine learning" --max_tweets=100
```
you can get old tweets between scpecified dates (slice) by running:
```
python scrap.py --scrap_type="slice" --search_query_list="deep learning,machine learning" --tweets_since="2012-01-01" --tweets_until="2012-03-01"
```
### How do I access to the scraped tweets ?
All scraped tweets matching the request will be saved in a pickle file. If you do not precise a directoory name (i.e. ```--save_tweets"./save_dir"```) a specific directory will automatically be created by the script where all .pkl files will be saved.

### Acknowledgement
Based on:
* [https://github.com/tomkdickinson/Twitter-Search-API-Python](https://github.com/tomkdickinson/Twitter-Search-API-Python) by Tom Dickinson



