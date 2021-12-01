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
Start by downloading pages from the api in two different versions
```
python download_character_pages.py
python download_character_pages_clean.py
```
Create the `networkx` graph along with a `pandas` dataframe
```
python create_wow_graph.py
```
Download necessary stuff in relation to comments
```
python download_character_comments.py
```
Clean and tokenize words on text from wowpedia (wiki pages) and text from wowhead (user comments)
```
python pages_to_words.py
python comments_clean.py
python comments_to_words.py
```

## Text and Network analysis
Perform text analysis computations by referencing the `Text Analysis.ipynb` notebook.

Then we can do text analysis on either the user comments from wowhead or character pages on wowpedia by
```
python text_analysis.py -s wowpedia
python text_analysis.py -s wowhead
```

We can also compute sentiments by ....


## References
- [Extracting the multiscale backbone of complex
weighted networks](https://www.pnas.org/content/pnas/106/16/6483.full.pdf)
- [GitHub Repo for Website](https://github.com/YoungPenguin/WOWenShittyWebsite)
