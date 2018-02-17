#-*- coding=utf-8 -*-
from wb_upload import *
from wp_db import *
from localdb import *
import StringIO
import sys
import time

wb=Weibo()
wp = WPDB()
#wp.create_post(title='测试',content='ojbk',tag=['test','ojbk'],category=['test'],thumbnail='122.png')
local=DB('Post')

def postnew():
    post,pictures=local.get_a_item()
    content=''
    title=post.name
    tag=[post.category]
    category=[post.category]
    thumbnail=post.poster
    print u'try to post a new post,title {}'.format(title)
    total=len(pictures)
    i=0
    for picture in pictures:
        wb_img_url=wb.get_image(picture.url)
        content+='\n<img class="alignnone size-medium wp-image-42" src="{pic}" alt="" width="400" height="100%" />'.format(pic=wb_img_url)
        i+=1
        sys.stdout.write('upload {}/{}\r'.format(i,total))
        sys.stdout.flush()
    wp.create_post(title=title,content=content,tag=tag,category=category,thumnnail_path=thumbnail)
    local.update(id=post.id,status=True)


if __name__=='__main__':
    while 1:
        wb._login()
        postnew()
        time.sleep(30)


