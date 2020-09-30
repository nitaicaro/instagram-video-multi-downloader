from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
import sys
import json
import os

class instaPostObject:
    def __init__(self, video_url):
        self.video_url = video_url

def lineIsEmpty(line):
	return len(line.split()) == 0

def getUrlsFromFile(file):
	urls = []
	file = open(file, "r")
	for line in file:
		if not lineIsEmpty(line):
			urls.append(line)
	return urls
	
def removeSemiColumnFromEnd(string):
	if (string[-1] == ";"):
		return string[:-1]
	return string

def getPostDataJSON(url): 
	soup = BeautifulSoup(urlopen(url), features="html.parser")
	script = soup.find_all("script", type="text/javascript")[3].string
	data = removeSemiColumnFromEnd(script.split("window._sharedData = ", 1)[-1])
	try:
		return json.loads(data)
	except:
		return None

def extractPostVideoURL(data):
	if (data is None):
		return None
	return data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["video_url"]

def getPostData(url):
    data = getPostDataJSON(url)
    if (not data is None):
        video_url = extractPostVideoURL(data)
        return instaPostObject(video_url)
    else:
        return None

def getDataObjects(urls):
	postObjects = []
	failedObjects = []
	for url in urls:
		data = getPostData(url)
		if not data is None:
			postObjects.append(data)
			continue
		failedObjects.append(url)
	return (postObjects, failedObjects)

def printFailedObjects(failedObjects):
	if (len(failedObjects) > 0):
		print("Failed to fetch data from the following urls:")
		for url in failedObjects:
			print(url)

def downloadVideo(url, name):
	urlretrieve(url, name + '.mp4') 

def downloadAllVideos(postObjects):
    id = 1
    for post in postObjects:
        downloadVideo(post.video_url, str(id))
        id = id + 1

def makeVideosDirectory():
    os.mkdir("videos")
    os.chdir("videos")

def main():
    urls = getUrlsFromFile("example.txt")
    postObjects, failedObjects = getDataObjects(urls)
    printFailedObjects(failedObjects)
    makeVideosDirectory()
    downloadAllVideos(postObjects)

main()
