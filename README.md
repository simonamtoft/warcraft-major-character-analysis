# Warcraft Major Character Analysis
Analysis of the [Major characters in Warcraft](https://wowpedia.fandom.com/wiki/Major_characters), by examining their character pages on [wowpedia](https://wowpedia.fandom.com/wiki/Wowpedia) and analysing the user comments on their [wowhead](https://www.wowhead.com/) threads.

The end products are an initial [YouTube Video for Part A](https://www.youtube.com/watch?v=JJx5f5nSYfs), and the final [Website for Part B](https://youngpenguin.github.io/WOW/).

For a detailed explanation of the project, which tools are used etc., refer to the `Explainer.ipynb` notebook.

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

Then we can create wordclouds for different graph partitions for both wowpedia and wowhead by 
```
python create_wordclouds.py -s wowpedia
python create_wordclouds.py -s wowhead
```

We can also compute sentiments for character quotes and wowhead user comments, and perform time-series analysis, which is done in `Sentiment Analysis.ipynb`.


Every part of the network analysis is done in the `Graph Analysis.ipynb` notebook.

## References
- [Network Science, Albert-Laszlo Barabasi](http://networksciencebook.com/)
- [GitHub Repo for Website](https://github.com/YoungPenguin/WOWenShittyWebsite)
