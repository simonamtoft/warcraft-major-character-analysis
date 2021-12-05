# Warcraft Major Character Analysis
Analysis of the [Major characters in Warcraft](https://wowpedia.fandom.com/wiki/Major_characters), by examining their character pages on [wowpedia](https://wowpedia.fandom.com/wiki/Wowpedia) and analysing the user comments on their [wowhead](https://www.wowhead.com/) threads.



[YouTube Video for Part A](https://www.youtube.com/watch?v=JJx5f5nSYfs)

[Website for Part B](https://youngpenguin.github.io/WOWenShittyWebsite/)


## Prepare text data etc.
Setup environment
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
Start by downloading raw and clean wowpedia pages from the api with the following two scripts
```
python download_character_pages.py
python download_character_pages_clean.py
```
Create the `networkx` graph along with a `pandas` dataframe. The resulting graph and dataframe should already be store in `G_wow.gexf` and `Gcc_wow.gexf`, and `df_chars.csv` in the folder `/store/`. 
```
python create_wow_graph.py
```
Download necessary stuff in relation to comments. This takes a long time, if repo is not too old, just use the comments already stored in `/data/char_comments/`.
```
python download_character_comments.py
```
Clean the user comments from wowhead and convert the cleaned character pages from wowhead and wowpedia to list of words.
```
python comments_clean.py
python pages_to_words.py -f -s wowhead
python pages_to_words.py -f -s wowpedia
```
Extract quotes from the raw wowpedia pages, used for sentiment analysis.
```
python extract_character_quotes.py
```

## Text and Network analysis
Perform text analysis computations by referencing the `Text Analysis.ipynb` notebook. These computation are (and should already be) stored in the json files under `/store/wowhead/` and `/store/wowpedia/`.

Then we can do text analysis on either the user comments from wowhead or character pages on wowpedia by
```
python text_analysis.py -s wowpedia
python text_analysis.py -s wowhead
```

We can also compute sentiments for character quotes and wowhead user comments, and perform time-series analysis, which is done in `Sentiment Analysis.ipynb`.


Every part of the network analysis is done in the `Graph Analysis.ipynb` notebook.

## References
- [Extracting the multiscale backbone of complex
weighted networks](https://www.pnas.org/content/pnas/106/16/6483.full.pdf)
- [GitHub Repo for Website](https://github.com/YoungPenguin/WOWenShittyWebsite)
