import urllib.parse

def extract_params(request):
    url = (request.split('\n')[0]).split(" ")[1]
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    query_params = list(query_params.values())
    valueList = [item for sublist in query_params for item in sublist]
    return valueList
