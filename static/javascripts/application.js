$(document).ready(function() {
   initjQuery();
 });

function initjQuery() {
	getNextTweet();
	$("p#more a").click(getPreviousTweets);
}

function getNextTweet() {
	var id = $('ul li:first-child').attr("id");
	if (id) {
		id = id.substring(2, id.length);
		 $.ajax({
			type: "GET",
			url: "/tweets/"+id,
			dataType: "xml",
			success: function(xml) {
				$('span.loading').hide();
				var entities = $(xml).find("entities").children();
				var times = entities.length;

				for (var i = 0; i < times; i++) {
					var tweet = $(entities[i]);
					var li = buildTweet(tweet)
					$('ul').prepend(li);
					li.slideDown(1000);
					pageTracker._trackEvent('Tweet', 'View', id);
				}


			},
			complete: function() {
				$('span.loading').show();
				setTimeout("getNextTweet()", 30000);
			}
		});
	}
	
}

function getPreviousTweets(event) {
	event.preventDefault();
	$('p#more').empty();
	$('p#more').html('<span class="loading">Cargando más tweets&hellip;</span>');
	var id = $('ul li:last-child').attr("id");
	if (id) {
		id = id.substring(2, id.length);
		 $.ajax({
			type: "GET",
			url: "/tweets/"+id+"/previous",
			dataType: "xml",
			error: function(xhr, desc, exceptionobj) {
				$('p#more').empty();
				$('p#more').html('<a href="#">Ver tweets anteriores</a>');
				$("p#more a").click(getPreviousTweets);
			},
			success: function(xml) {
				var entities = $(xml).find("entities").children();
				var times = entities.length;
				var i = 0;
				for (i; i < times; i++) {
					var tweet = $(entities[i]);
					var li = buildTweet(tweet);
					$('ul').append(li);
					li.fadeIn(1000);
					pageTracker._trackEvent('Tweet', 'Previous', id);
				} //end for
				
				if (i == 5) {
					$('p#more').empty();
					$('p#more').html('<a href="#">Ver tweets anteriores</a>');
					$("p#more a").click(getPreviousTweets);
				} else {
					$('p#more').empty();
					$('p#more').html('No hay más tweets.');
				}

			} // end sucess
		}); //and ajax
	} // end if
} // end function

function buildTweet(tweet) {
	var content = tweet.find("property[name='content']").text();
	var tweet_id = tweet.find("property[name='tweet_id']").text();
	var author = tweet.find("property[name='author']").text();
	var author_uri = tweet.find("property[name='author_uri'] link").attr("href");
	var uri = tweet.find("property[name='uri'] link").attr("href");
	var published = tweet.find("property[name='published_ve']").text();
	
	var li = $('<li style="display:none;" class="hentry"></li>').attr({id: "t_" + tweet_id });
	var vcard = $('<span class="vcard author"></span>');
	var title = $('<span class="entry-title"></span>');
	var abbr = $('<abbr class="published"></abbr>');
	
	var a = $('<a class="fn url"></a>').attr({href: author_uri});
	a.append(author);
	vcard.append(a);
	
	title.append(content);
	
	li.append(vcard);
	li.append(" ");
	li.append(title);
	var span = $('<span class="meta">A las </span>');
	
	abbr.append(time(published));
	abbr.attr({title: iso8601(published)});
	span.append(abbr);
	span.append(" &middot; ");
	var reply = "http://twitter.com/home?status=@"+author+"%20&in_reply_to_status_id="+tweet_id+"&in_reply_to=" + author;
	a = $('<a>Responder</a>').attr({href: reply});
	span.append(a);
	span.append(" &middot; ");
	a = $('<a rel="bookmark">Ver tweet</a>').attr({href: uri});
	span.append(a);
	li.append('<br/>');
	li.append(span);
	
	return li;
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

function iso8601(date) {
//	2009-02-10 20:51:46
	var year = date.substring(0,4);
	var month = date.substring(5,7);
	var day = date.substring(8,10);
	var hours = date.substring(11,13);
	var minutes = date.substring(14,16);
	var seconds = date.substring(17,19);
	return year+month+day+"T"+hours+":"+minutes+":"+seconds
}
