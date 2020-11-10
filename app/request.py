import urllib.request, json
the_url = 'http://quotes.stormconsultancy.co.uk/random.json'

def get_quote():
    url = the_url
    with urllib.request.urlopen(url) as url:
        raw_data = url.read()
        data = json.loads(raw_data)
        author = data["author"]
        quote = data["quote"]
    return [author, quote]