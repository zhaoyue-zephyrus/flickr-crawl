import flickrapi
import requests
import sys
import os

## sign in flickr api
api_key = u'8166f787473b9564a3d67ac95759120a'
api_secret = u'971bae30c95d1e65'
flickr = flickrapi.FlickrAPI(api_key, api_secret)

## argc
if (len(sys.argv)!=4):
  print "usage: main.py <Tag-list> <Root-directory/> <image number for each keyword>"
else:
  tag_list = sys.argv[1]
  root_dir = sys.argv[2]
  imageNr = int(sys.argv[3])

## keyword list
keyword_list=[]
fin = open(tag_list)
for line in fin:
  if line.endswith('\n'):
    line = line[:-1]
    keyword_list.append(line)
fin.close()

if not os.path.exists(root_dir):
  os.mkdir(root_dir)

for keyword in keyword_list:
  sub_dir = root_dir + keyword + "/"
  if not os.path.exists(sub_dir):
    os.mkdir(sub_dir)
  
  count = 0
  for photo in flickr.walk(text=keyword):
    farm_id = photo.get('farm')
    server_id = photo.get('server')
    photo_id = photo.get('id')
    secret = photo.get('secret')
    #print "farm-id = %s, server-id = %s, photo-id = %s, secret = %s" %  (farm_id, server_id, photo_id, secret)
    url = "https://farm%s.staticflickr.com/%s/%s_%s.jpg" % (farm_id, server_id, photo_id, secret)
    r = requests.get(url)
    with open(sub_dir+"%s.jpg" % photo_id, 'wb') as f:
      f.write(r.content)
    count += 1
    if count == imageNr:
      break
  print "For keyword: %s, %i images crawled." % (keyword, count)

