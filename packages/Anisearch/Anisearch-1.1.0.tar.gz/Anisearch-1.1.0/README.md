# Anisearch
Anilist API module for python. you only need to copy the Anilist folder to your own script.

### Executing program

* How to run the program
* Import module

```python
from Anisearch import Anilist

instance = Anilist()
```

From there you can get information from Anilist using their new GraphQL API.
To get data on a known ID.
```python
instance.get.anime(13601) # Return data on PSYCHO-PASS 
instance.get.manga(64127) # Return data on Mahouka Koukou no Rettousei
instance.get.staff(113803) # Return data on Kantoku
instance.get.studio(7) # Return data on J.C. Staff
```

Searching is also making a return.
```python
instance.search.anime("Sword") # Anime search results for Sword.
instance.search.manga("Sword") # Manga search results for Sword.
instance.search.character("Tsutsukakushi") # Character search results for Tsutsukakushi.
instance.search.staff("Kantoku") # Staff search results for Kantoku.
instance.search.studio("J.C. Staff") # Studio search result for J.C. Staff.
```
A note about the searching and getting:
```python
search(term, page = 1, perpage = 10)
get(item_id)
```
Pagination is done automatically in the API. By default, you'll get 10 results per page. 
If you want more, just change the per page value. pageInfo is always the first result in the returned data.
Pages start at 1 and if you want another page, just replace page with the next number. 
query_string is to set what info you want to display.

### Customization
You can set your own settings as follows
```python
import logging
from Anisearch import Anilist
# for init instance
SETTINGS = {
    'header': {
        'Content-Type': 'application/json',
        'User-Agent': 'Anisearch (github.com/MeGaNeKoS/Anisearch)',
        'Accept': 'application/json'},
    'api_url': 'https://graphql.anilist.co'
}
request_param = {}  # this is for the requests lib parameters.
instance = Anilist(log_level=logging.INFO, settings = SETTINGS, request_param = request_param)

# for instance get/search parameters
retry = 10
instance.get.anime(13601, num_retries=retry)  # default 10
```

### Todo
* Add more error handling when the API returns an error.
    - currently is limited to 429 too many requests. You can help me by providing a log when other errors occur.