import os
import gdata
import gdata.youtube
import gdata.youtube.service

from pycvf.core import settings
from pycvf.lib.video.simplevideoreader7 import SimpleVideoReader7

def print_entry_details(entry):
  print 'Video title: %s' % entry.media.title.text
  print 'Video published on: %s ' % entry.published.text
  print 'Video description: %s' % entry.media.description.text
  print 'Video category: %s' % entry.media.category[0].text
  print 'Video tags: %s' % entry.media.keywords.text
  print 'Video watch page: %s' % entry.media.player.url
  print 'Video flash player URL: %s' % entry.GetSwfUrl()
  print 'Video duration: %s' % entry.media.duration.seconds

  # non entry.media attributes
  print 'Video geo location: %s' % str(entry.geo)
  print 'Video view count: %s' % entry.statistics.view_count
  print 'Video rating: %s' % entry.rating.average

  # show alternate formats
  for alternate_format in entry.media.content:
    if 'isDefault' not in alternate_format.extension_attributes:
      print 'Alternate format: %s | url: %s ' % (alternate_format.type,
                                                 alternate_format.url)

  # show thumbnails
  for thumbnail in entry.media.thumbnail:
    print 'Thumbnail url: %s' % thumbnail.url

def download_and_play_entry(entry):
  vfile=os.tmpnam()
  os.system("youtube-dl -o '%s' '%s'"%(vfile,entry.media.player.url))
  vf=SimpleVideoReader7(vfile)
  os.remove(vfile)
  return vf

def print_video_feed(uri):
  for entry in feed.entry:
    print_entry_details(entry)

def YoutubeSearch(search_terms):
  """
Here are some of the most common YouTubeVideoQuery properties for setting search parameters:

author
    Sets the author of the entry. Author is synonymous with YouTube username.
format
    Specifies a video format. Accepts numeric parameters to specify one of two kinds of RTSP streaming URLs for mobile video playback or a HTTP URL to the embeddable Flash player.
racy
    Indicates whether restricted content should be included in the results. Accepts only two parameters: 'include' or 'exclude'.
max_results
    Sets the maximum number of entries to return at one time.
start_index
    Sets the 1-based index of the first result to be retrieved (for paging).
orderby
    Sets the order in which to list entries, such as by relevance, viewCount, published, or rating.
time
    Sets a time period to limit standard feed results to: today, this_week, this_month, or all_time.
vq
    Sets a search query term. Searches for the specified string in all video metadata, such as titles, tags, and descriptions.


  """
  yt_service = gdata.youtube.service.YouTubeService()
  yt_service.developer_key = settings.YOUTUBE_DEV_KEY
  yt_service.client_id = settings.YOUTUBE_CLIENT_ID
  query = gdata.youtube.service.YouTubeVideoQuery()
  query.vq = search_terms
  query.orderby = 'viewCount'
  query.racy = 'include'
  feed = yt_service.YouTubeQuery(query)
  #PrintVideoFeed(feed)
  return feed.entry


def YoutubeSearchManyTerms(list_of_search_terms):
  yt_service = gdata.youtube.service.YouTubeService()
  yt_service.developer_key = settings.YOUTUBE_DEV_KEY
  yt_service.client_id = settings.YOUTUBE_CLIENT_ID
  query = gdata.youtube.service.YouTubeVideoQuery()
  query.orderby = 'viewCount'
  query.racy = 'include'
  for search_term in list_of_search_terms:
    new_term = search_term.lower()
    query.categories.append('/%s' % new_term)
  feed = yt_service.YouTubeQuery(query)
  #PrintVideoFeed(feed)
  return feed.entry

from pycvf.core import database
from pycvf.datatypes import video

class DB(database.ContentsDatabase, video.Datatype):
  def __init__(self,query):
    self.feede=YoutubeSearch(query)
  def __iter__(self):
    for i in self.feede:
       print_entry_details(i)
       yield (download_and_play_entry(i),i.media.player.url)

__call__=DB
