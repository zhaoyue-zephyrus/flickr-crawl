import flickrapi
import requests
from unidecode import unidecode
import sys
import os

## sign in flickr api
api_key = u''
api_secret = u''
flickr = flickrapi.FlickrAPI(api_key, api_secret)

## argc
if (len(sys.argv)!=4):
  print "usage: main.py <Tag-list> <Root-directory/> <image number for each keyword>"
  sys.exit()
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

fout = open("flickr-image.list",'w')
# <id>; <keyword>; <tag>,<tag>,...\n
# <id>; <keyword>; <tag>,<tag>,...\n
# ...

for keyword in keyword_list:
  sub_dir = root_dir + keyword + "/"
  if not os.path.exists(sub_dir):
    os.mkdir(sub_dir)
  
  count = 0
  for photo in flickr.walk(text=keyword,sort="relevance"):
    farm_id = photo.get('farm')
    server_id = photo.get('server')
    photo_id = photo.get('id')
    secret = photo.get('secret')
    print "farm-id = %s, server-id = %s, photo-id = %s, secret = %s" %  (farm_id, server_id, photo_id, secret)
    resp = flickr.tags.getListPhoto(photo_id=photo_id)
    tags = []
    for tag in resp.getchildren()[0].getchildren()[0].getchildren():
      tags.append(unidecode(tag.get("raw")))
    fout.write("%s%s.jpg;%s;%s\n"% (sub_dir,photo_id,keyword,','.join(tags)) )
    url = "https://farm%s.staticflickr.com/%s/%s_%s.jpg" % (farm_id, server_id, photo_id, secret)
    r = requests.get(url)
    with open(sub_dir+"%s.jpg" % photo_id, 'wb') as f:
      f.write(r.content)
    count += 1
    if count == imageNr:
      break
  print "For keyword: %s, %i images crawled." % (keyword, count)

