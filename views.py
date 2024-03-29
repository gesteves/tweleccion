from django.shortcuts import render_to_response
from django import http
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.template import Template
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from xml.dom import minidom
from models import *
from datetime import datetime
import re

def fetch_tweets(request):
	latest = Tweet.last()
	if latest is None:
		url = "http://search.twitter.com/search.atom?q=+venezuela+OR+geocode%3A10.49605%2C-66.898277%2C700km&rpp=100"
	else:
		url = "http://search.twitter.com/search.atom?q=+venezuela+OR+geocode%3A10.49605%2C-66.898277%2C700km&rpp=100&since_id=" + str(latest.tweet_id)
	fetch_xml(url)
	return HttpResponse("OK")

def fetch_xml(url):
	result = urlfetch.fetch(url)
	if result.status_code == 200:
		parse_tweets(result.content)

def parse_tweets(xml):
	dom = minidom.parseString(xml.encode( "utf-8" ))
	for node in dom.getElementsByTagName('entry'):
		tweet_id = node.getElementsByTagName('id')[0].childNodes[0].nodeValue
		uri = node.getElementsByTagName('link')[0].getAttribute('href')
		author = node.getElementsByTagName('name')[0].childNodes[0].nodeValue
		author_uri = node.getElementsByTagName('uri')[0].childNodes[0].nodeValue
		title = node.getElementsByTagName('title')[0].childNodes[0].nodeValue
		content = node.getElementsByTagName('content')[0].childNodes[0].nodeValue
		published = node.getElementsByTagName('published')[0].childNodes[0].nodeValue
		t = re.search('(?<=:)\d+', tweet_id)
		tweet_id = int(t.group(0))
		author = author.split(" ")[0]
		tweet = Tweet(tweet_id = tweet_id, uri = uri, author = author, author_uri = author_uri, title = title, content = content, published = datetime.strptime(published, '%Y-%m-%dT%H:%M:%SZ'))
		tweet.put()


def next(request, tweet_id):
	tweet = memcache.get(tweet_id)
	if tweet is None:
		tweet = Tweet.by_tweet_id(int(tweet_id)).next()
		if len(tweet) == 0:
			t = Template('<?xml version="1.0" encoding="UTF-8"?><error>Not Found</error>')
			xml = t.render(Context())
			return http.HttpResponseNotFound(xml)
		else:
			memcache.add(tweet_id, tweet, 60)
	t = get_template('tweet.xml')
	xml = t.render(Context({'tweets': tweet}))
	response = HttpResponse(xml, mimetype="text/xml")
	return response
	
def previous(request, tweet_id):
	tweet = memcache.get(tweet_id+"-previous")
	if tweet is None:
		tweet = Tweet.by_tweet_id(int(tweet_id)).previous(5)
		if len(tweet) == 0:
			t = Template('<?xml version="1.0" encoding="UTF-8"?><error>Not Found</error>')
			xml = t.render(Context())
			return http.HttpResponseNotFound(xml)
		else:
			memcache.add(tweet_id+"-previous", tweet)
	t = get_template('tweet.xml')
	xml = t.render(Context({'tweets': tweet}))
	response = HttpResponse(xml, mimetype="text/xml")
	return response

def first(request):
	tweet = Tweet.first()
	return HttpResponse(tweet.to_xml(), mimetype="text/xml")

def index(request):
	subdomain = request.META['HTTP_HOST'].split('.')[0]
	if subdomain == "m":
		return mobile(request)
	else:
		response = memcache.get("index")
		if response is None:
			tweets = Tweet.latest(20, 0)
			response = render_to_response("index.html", {'tweets': tweets})
			memcache.add("index", response, 300)
		return response

def index2(request):
	response = memcache.get("index")
	if response is None:
		tweets = Tweet.latest(20, 0)
		response = render_to_response("index.html", {'tweets': tweets})
		memcache.add("index", response, 60)
	return response

def mobile(request):
	response = memcache.get("mobile")
	if response is None:
		tweets = Tweet.latest(20, 0)
		response = render_to_response("mobile-index.html", {'tweets': tweets})
		memcache.add("mobile", response, 60)
	return response

def redirect_to_search(request):
	return http.HttpResponsePermanentRedirect("http://search.twitter.com/search?" + request.GET.urlencode())
	
def not_found(request):
	t = get_template('404.html')
	html = t.render(Context())
	return http.HttpResponseNotFound(html)
	
def sitemap(request):
	response = memcache.get("sitemap")
	if response is None:
		latest = Tweet.last()
		response = render_to_response('sitemap.xml', {'tweet': latest})
		response['Content-Type'] = "text/xml"
		memcache.add("sitemap", response, 3600)
	return response

	
	
	
	
			