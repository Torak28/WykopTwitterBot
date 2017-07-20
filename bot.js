console.log("Lecimy");

var Twit = require('twit');

var config = require('./config');

var T = new Twit(config);

var tweet = {
	status: '#FirstTime Pierwszy raz z wykorzystaniem API!'
}

T.post('statuses/update', tweet, tweeted);

function tweeted(err, data, response){
	if(err){
		console.log("Nie działa :c");
	}else{
		console.log("Działa :)");
	}
}