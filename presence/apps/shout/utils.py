def url2link(url):
    from lxml import html
    try:
        title = html.parse(url).find(".//title").text
        return title if title else url
    except AttributeError:
        return url

def is_private(message):
    result = message.startswith("!! ")
    return result, message[3:] if result else message

def user2link(message):
    return message