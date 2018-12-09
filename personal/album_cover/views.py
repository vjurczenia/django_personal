from django.shortcuts import render
from django.conf import settings
import requests
import wikiquotes
import random

def index(request):
    """ http://i.imgur.com/tbVr3WT.jpg """

    title_response = requests.post('https://en.wikipedia.org/w/api.php', {
        'action': 'query',
        'list': 'random',
        'format': 'json'
    })
    random_title = title_response.json()['query']['random'][0]['title']

    # original spec dictates that we use the last quote from a random page, but to minimize api calls we might just use random quotes
    random_quotes = []
    while len(random_quotes) <= 0:
        quote_response = requests.post('https://en.wikiquote.org/w/api.php', {
            'action': 'query',
            'list': 'random',
            'format': 'json'
        })
        random_quotes = wikiquotes.get_quotes(quote_response.json()['query']['random'][0]['title'], 'english')
    random_quote = random_quotes[-1].split()[-1]

    """     
        the original spec dictates that you take the 5th image from flickr.com/explore/interesting/7days/
        not sure how to make the api return a fresh page each time, so we're going to get creative with it 
    """    

    photo_response = requests.post('https://api.flickr.com/services/rest/', {
        'method': 'flickr.interestingness.getList',
        'api_key': settings.FLICKR_API_KEY,
        #'per_page': 5,
        'format': 'json',
        'nojsoncallback': 1
    })
    random_photo_json = photo_response.json()['photos']['photo'][random.randint(0,101)]
    # use ** to unpack dict
    random_photo_url = 'https://farm{farm}.staticflickr.com/{server}/{id}_{secret}.jpg'.format(**random_photo_json)

    return render(request, 'album_cover/index.html', {
        'random_title': random_title,
        'random_quote': random_quote,
        'random_photo': random_photo_url
    })

def index_test(request):
        return render(request, 'album_cover/index.html', {
        'random_title': """User talk:59.140.246.34""",
        'random_quote': """If anything, evolution teaches us that from one or a few forms wondrously many kinds will arise.""",
        'random_photo': """https://farm5.staticflickr.com/4820/45489386554_9fdce4cb6c.jpg"""
    })
