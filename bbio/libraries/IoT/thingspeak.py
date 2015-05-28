"""
thingspeak.py
Copyright (c) 2015 - Gray Cat Labs 
Alexander Hiam <alex@graycat.io>

This module provides the ThingSpeakChannel class for sending data
to a ThingSpeak.com channel. It also provides the ThingTweet class
for using ThingSpeak's ThingTweet service.

This module is released as part of PyBBIO under its MIT license.
See PyBBIO/LICENSE.txt
"""

import requests, datetime


class ThingSpeakChannel(object):

  UPDATE_URL = "https://api.thingspeak.com/update"

  def __init__(self, api_key):
    self.api_key = api_key

  def post(self, data, coords=None, elevation=None, status='', thingtweet=None, 
           sample_datetime=None, timezone=''):
    """ Sends the given data to the channel in the given order starting with
        field1. """
    n_fields = len(data)
    assert n_fields > 0, "At least one field is required"
    assert n_fields <= 8, "Can't send more than 8 field maximum"
    
    params = {'api_key' : self.api_key}


    for i in range(0, len(data)):
        params['field%i' % (i+1)] = data[i]

    if coords:
      assert type(coords) == tuple or type(coords) == list, \
              "coords must be tuple or list"
      assert len(coords) == 2, \
        "coords must be of length 2: (latitude, longitude)"
      for i in coords:
        assert type(i) == int or type(i) == float, \
                "latitude and longitude must be integers or floats"
      params['lat'] = float(coords[0])
      params['long'] = float(coords[1])

    if elevation:
      assert type(i) == int or type(i) == float, \
              "elevation must be integer or float"
      params['elevation'] = int(elevation)

    if status:
      assert type(status) == str, "status message must be a string"
      params['status'] = status

    if thingtweet:
      assert type(thingtweet) == ThingTweet, \
              "thingtweet must be a ThingTweet instance"
      params['twitter'] = thingtweet.username
      params['tweet'] = thingtweet.message

    if sample_datetime:
      assert type(sample_datetime) == datetime.datetime, \
              "sample_datetime must be a datetime.datetime object"
      params['created_at'] = sample_datetime.strftime('%Y-%m-%d %H:%M:%S')

    if timezone:
      # Do some simple validation, far from thorough!
      assert type(timezone) == str and \
             timezone.count('/') == 1 and \
             timezone[0].isupper() and \
             timezone[timezone.index('/')+1].isupper() and \
             tz.count(' ') == 0, \
              "timezone must be string in IANA time zone format, e.g. America/New_York"

      params['timezone'] = timezone

    response = requests.post(self.UPDATE_URL, params=params)
    if response.status_code != 200:
      print "HTTP Error: [%i] - %s" % (response.status_code, response.reason)


class ThingTweet(object):
  def __init__(self, username, message):
    assert type(username) == str, "Twitter username must be a string"
    assert type(message) == str, "tweet message must be a string"

    if username[0] == '@': username = username[1:]
    self.username = username
    self.message = message

