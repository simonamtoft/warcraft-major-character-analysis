# Warcraft Major Character Analysis
Analysis of the [Major characters in Warcraft](https://wowpedia.fandom.com/wiki/Major_characters), by examining their character pages on [wowpedia](https://wowpedia.fandom.com/wiki/Wowpedia) and analysing the user comments on their [wowhead](https://www.wowhead.com/) threads.



[YouTube Video for Part A](https://www.youtube.com/watch?v=JJx5f5nSYfs)


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
Perform text analysis computations by referencing the `Text Analysis.ipynb` notebook.
Then do text analysis by `text_analysis.py`.


## References
- [Extracting the multiscale backbone of complex
weighted networks](https://www.pnas.org/content/pnas/106/16/6483.full.pdf)
