# repLookup

A SMS based application to get your state and national reps' contact information on your phone 🇺🇸 ☎️ 

<img src="screenshot.png" width="300">

This application uses the [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/intro), [Open States API](http://docs.openstates.org/api/index.html), [Sunlight Foundation Congress API](https://sunlightlabs.github.io/congress/) (soon to be merged with ProPublica Congress API), [Twilio](https://www.twilio.com), and [Heroku](https://www.heroku.com/) for deployment.

### Setup:

You will need to get a [Google Maps API Key] to use this application. After you have gotten a key, store it as an environment varible. To run it locally, you can store it like this:

```
export GOOGLEMAPSKEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### FAQs:

**Is it sketchy to give a random number your address?**
Yes, I think it is too. You are doing so at your own risk. The addresses are not being used for anything other than lookup and neither will the phone numbers. Be aware, Twilio will have a record of it in their logs though. 

**Why do I need to give an exact address and not just a zip code?**
Fequently a single zip code can be part of mutliple districts. For the most accurate results, latitude and longitude of addresses is being used for lookup. 
