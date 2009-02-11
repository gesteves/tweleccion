$(document).ready(function() {
   initjQuery();
 });

function initjQuery() {
	getNextTweet();
}

function getTweet(url) {
	 $.ajax({
		type: "GET",
		url: "/tweets/"+url,
		dataType: "xml",
		error: function(xhr, desc, exceptionobj) {
			$('span.loading').show();
			setTimeout("getNextTweet()", 30000);
		},
		success: function(xml) {
			$('span.loading').hide();
			var entities = $(xml).find("entities").children();
			var times = entities.length;
			
			for (var i = 0; i < times; i++) {
				var tweet = $(entities[i]);
				showTweet(tweet);
			}
			
			setTimeout("getNextTweet()", 3000);
			
		}
	});
}

function getNextTweet() {
	var id = $('ul li:first-child').attr("id");
	if (id) {
		id = id.substring(2, id.length);
		getTweet(id);
	}
	
}

function showTweet(tweet) {
	var content = tweet.find("property[name='content']").text();
	var tweet_id = tweet.find("property[name='tweet_id']").text();
	var author = tweet.find("property[name='author']").text();
	var author_uri = tweet.find("property[name='author_uri'] link").attr("href");
	var uri = tweet.find("property[name='uri'] link").attr("href");
	var published = tweet.find("property[name='published_ve']").text();
	var a = $('<a class="author"></a>').attr({href: author_uri});
	a.append(author);
	var li = $('<li style="display:none;"></li>').attr({id: "t_" + tweet_id });
	li.append(a);
	li.append(" ");
	li.append(content);
	li.append(" ");
	var span = $('<span class="meta"></span>');
	a = $('<a>A las </a>').attr({href: uri});
	a.append(time(published));
	span.append(a);
	li.append(span);
	$('ul').prepend(li);
	li.fadeIn(1000);
	pageTracker._trackEvent('Tweet', 'View', tweet_id);
}

function time(date) {
//	2009-02-10 20:51:46
	var hours = date.substring(11,13);
	var minutes = date.substring(14,16);
	var ampm;
	if (hours == 0) {
		hours = "12";
		ampm = "a.m.";
	} else if (hours < 12) {
		ampm = "a.m.";
	} else if (hours == 12 ){
		ampm = "p.m.";
	} else {
		hours = hours - 12;
		ampm = "p.m.";
	}
	return hours+":"+minutes+" "+ampm;
}
