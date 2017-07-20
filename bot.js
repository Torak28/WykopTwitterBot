var Twit = require('twit');
var config = require('./config');
var exec = require('child_process').exec;
var fs = require('fs');

var T = new Twit(config);
var index = 0;
//6 - sam tekst
//5 - tekst + obrazek

var text = './output.txt';
var picture = './output.jpg';

function tweetIt(){
	var cmd = 'python3 300.py ' + index;
	/*Wykonanie i obrobienie wyniku*/
	exec(cmd, wykonanie);
	function wykonanie(){
		if (fs.existsSync(text) && fs.existsSync(picture)){
			//Jest tekst i obrazek
			fs.readFile(text, 'utf8', odczytanie);

			function odczytanie(err, data){
				if(err){
					console.log("Nie działa odczytanie :c");
				} else {
					var tweetText = data;
					var b64 = fs.readFileSync(picture, { encoding: 'base64' })
					T.post('media/upload', { media_data: b64 }, uploaded);
					function uploaded(err, data, response) {
						var id = data.media_id_string;
						var tweet = {
							status : tweetText,
							media_ids: [id]
						}
						T.post('statuses/update', tweet, tweeted);
						function tweeted(err, data, response){
							if(err){
								console.log("Nie działa text i obrazek :c");
							}else{
								console.log("Działa text i obrazek :)");	
							}
						}
					}
				}
			}
		} else if(fs.existsSync(text)){
			//Jest tylko tekst
			fs.readFile(text, 'utf8', odczytanie);

			function odczytanie(err, data){
				if(err){
					console.log("Nie działa odczytanie :c");
				} else {
					var tweet = {
						status : data
					}
					T.post('statuses/update', tweet, tweeted);

					function tweeted(err, data, response){
						if(err){
							console.log("Nie działa text :c");
						}else{
							console.log("Działa text :)");
						}
					}
				}
			}
		} else if(fs.existsSync(picture)){
			//Jest tylko obrazek
			var b64 = fs.readFileSync(picture, { encoding: 'base64' })
			T.post('media/upload', { media_data: b64 }, uploaded);
			function uploaded(err, data, response) {
				var id = data.media_id_string;
				var tweet = {
					status : 'XD',
					media_ids: [id]
				}
				T.post('statuses/update', tweet, tweeted);

				function tweeted(err, data, response){
					if(err){
						console.log("Nie działa obrazek :c");
					}else{
						console.log("Działa obrazek :)");			
					}
				}
			}
		}
	}
	/**/
	index++;
	if(index == 15){
		index = 1;
	}
}

setInterval(tweetIt, 1000*30);
