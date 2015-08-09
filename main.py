import flickrapi
import requests

api_key = u""
api_secret = u"" 
keyword = u""

flickr = flickrapi.FlickrAPI(api_key, api_secret)
count = 0
for photo in flickr.walk(text=keyword):
  farm_id = photo.get('farm')
  server_id = photo.get('server')
  photo_id = photo.get('id')
  secret = photo.get('secret')
  print "farm-id = %s, server-id = %s, photo-id = %s, secret = %s" %  (farm_id, server_id, photo_id, secret)
  url = "https://farm%s.staticflickr.com/%s/%s_%s.jpg" % (farm_id, server_id, photo_id, secret)
  r = requests.get(url)
  with open("%s.jpg" % photo_id, 'wb') as f:
    f.write(r.content)
    count += 1
  if count == 1:
    break
