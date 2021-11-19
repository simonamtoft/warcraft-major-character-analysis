import json
from urllib import request
from urllib.parse import quote_plus


def generate_query(baseurl, title, content=None, dataformat="json"):
    # Action for the API
    action = "query"

    # Define how and what content to get
    if content == None:
        content = "prop=revisions&rvprop=content&rvslots=*" 

    # build title properly
    title = quote_plus(title)

    # Format together to form  a query
    query = f"{baseurl}?action={action}&{content}&titles={title}&format={dataformat}"
    return query


def get_response_from(query):
    # Get a response using the query
    response = request.urlopen(query)

    # Reformat
    data = response.read()
    text = data.decode("utf-8")

    # return as json
    return json.loads(text)


def get_main_from(response):
    pages = response['query']['pages']
    return pages[list(pages.keys())[0]]['revisions'][0]['slots']['main']['*']


def get_plaintext_from(response):
    pages = response['query']['pages']
    return pages[list(pages.keys())[0]]['extract']
