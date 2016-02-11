from datetime import datetime, timedelta
import httplib2
import os
import sys


import argparse
from oauth2client import file, client, tools

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets

import models


CLIENT_SECRETS_FILE = "client_secrets.json"

# We will require read-only access to the YouTube Data and Analytics API.
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube.readonly",
  "https://www.googleapis.com/auth/yt-analytics.readonly"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_ANALYTICS_API_SERVICE_NAME = "youtubeAnalytics"
YOUTUBE_ANALYTICS_API_VERSION = "v1"

# Helpful message to display if the CLIENT_SECRETS_FILE is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the APIs Console
https://code.google.com/apis/console#access

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  scope=" ".join(YOUTUBE_SCOPES))

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
  flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
  credentials = tools.run_flow(flow, storage, flags)

http = credentials.authorize(httplib2.Http())
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, http=http)
youtube_analytics = build(YOUTUBE_ANALYTICS_API_SERVICE_NAME,
  YOUTUBE_ANALYTICS_API_VERSION, http=http)

# Place the prameters in to .list() and a JSON response will be returned. This
# is a search against the YouTube Data API
def get_ytData_response(part='snippet', forMine=True, maxResults=50,
                         type='video', pageToken=None):
        youtube_data_response = youtube.search().list(
                                            part=part,
                                            forMine=forMine,
                                            maxResults=maxResults,
                                            type=type,
                                            pageToken=pageToken)
        youtube_data = youtube_data_response.execute()
        return youtube_data

def grab_video_ids(youtube_data):
    for item in youtube_data['items']:
        print(item['snippet']['title'])
        print(item['id']['videoId'])
        print(item['snippet']['publishedAt'])

        models.Video.create_video(video_id=item['id']['videoId'],
                     title=item['snippet']['title'],
                     publication_date=item['snippet']['publishedAt'])



# Currently this script counts as three requests. The final request only returns
# a blank page, but still counts as one request against the quota.
youtubeData = get_ytData_response()
counter = round(youtubeData['pageInfo']['totalResults']/50)-1
grab_video_ids(youtubeData)

while counter > 0:
    youtubeData2 = get_ytData_response(pageToken=youtubeData['nextPageToken'])
    grab_video_ids(youtubeData2)
    counter -= 1
# To-DO:
#       Send video titles, and IDs to database


# Place the prameters into .query() and a JSON response will be returned. This
# is a search against the YouTube Analytics API
#youtube_analytics_response = youtube_analytics.reports().query()