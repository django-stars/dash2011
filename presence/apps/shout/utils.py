def url2link(url):
	from lxml import html
	try:
		title = html.parse(url).find(".//title").text
		return title if title else url
	except AttributeError:
		return url

def is_private(message):
	return message.startswith("!! "), message[3:]

def user2link(message):
	return message