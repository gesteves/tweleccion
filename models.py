from google.appengine.ext import db
from datetime import timedelta

class Tweet(db.Model):
	
	tweet_id = db.IntegerProperty()
	title = db.TextProperty()
	published = db.DateTimeProperty()
	content = db.TextProperty()
	uri = db.LinkProperty()
	author = db.StringProperty()
	author_uri = db.LinkProperty()
	published_ve = db.DateTimeProperty()
	
	
#	<entry>
#    <id>tag:search.twitter.com,2005:1192675369</id>
#    <published>2009-02-09T18:24:12Z</published>
#    <link type="text/html" rel="alternate" href="http://twitter.com/carolaccs/statuses/1192675369"/>
#    <title>Un excelente post sobre la enmienda en el blog de @hectorpal http://tinyurl.com/am7zcv #15F</title>
#    <content type="html">Un excelente post sobre la enmienda en el blog de &lt;a href="http://twitter.com/hectorpal"&gt;@hectorpal&lt;/a&gt; &lt;a href="http://tinyurl.com/am7zcv"&gt;http://tinyurl.com/am7zcv&lt;/a&gt; &lt;a href="/search?q=%2315F"&gt;&lt;b&gt;#15F&lt;/b&gt;&lt;/a&gt;</content>
#    <updated>2009-02-09T18:24:12Z</updated>
#    <link type="image/png" rel="image" href="http://s3.amazonaws.com/twitter_production/profile_images/65103135/AutoretratoFragmento3_normal.png"/>
#    <author>
#      <name>carolaccs (carolaccs)</name>
#      <uri>http://twitter.com/carolaccs</uri>
#    </author>
#  </entry>

	def put(self):
		self.published_ve = self.published + timedelta(hours = -4.5)
		super(Tweet, self).put()

	def next(self, number):
		query = db.Query(Tweet)
		return query.filter("tweet_id >", self.tweet_id).order('tweet_id').fetch(number)
		
	def next(self):
		query = db.Query(Tweet)
		return query.filter("tweet_id >", self.tweet_id).order('tweet_id').fetch(100)
		
	def previous(self, number):
		query = db.Query(Tweet)
		return query.filter("tweet_id <", self.tweet_id).order('-tweet_id').fetch(number)
	
	@staticmethod
	def by_tweet_id(id):
		query = db.Query(Tweet)
		return query.filter("tweet_id =", id).get()
		
	@staticmethod
	def last():
		query = db.Query(Tweet)
		results = query.order('-tweet_id').get()
		return results
		
	@staticmethod
	def latest(number, offset):
		query = db.Query(Tweet)
		results = query.order('-tweet_id').fetch(number, offset)
		return results