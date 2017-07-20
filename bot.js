console.log("Lecimy");

var Twit = require('twit');
var config = require('./config');
var T = new Twit(config);

var stream = T.stream('user');

function followed(eventMsg){
	var nazwa = eventMsg.source.name;
	var uzytkownik = eventMsg.source.screen_name;
	tweetIt('Elo @' + uzytkownik + ' dzieki za folołka!');
}

function tweetIt(txt){
	var tweet = {
		status: txt
	}

	T.post('statuses/update', tweet, tweeted);

	function tweeted(err, data, response){
		if(err){
			console.log("Nie działa :c");
		}else{
			console.log("Działa :)");
		}
	}
}

//setInterval(tweetIt, 1000*60*60);
stream.om('follow', followed);
