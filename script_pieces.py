def search_author(name):
    """Search by author name and return a generator of Author objects"""
    url = _AUTHSEARCH.format(requests.utils.quote(name))
    soup = _get_soup(_HOST+url)
    return _search_citation_soup(soup)
