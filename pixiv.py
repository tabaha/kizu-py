import discord
import asyncio
import requests
import re
import io




async def pixivshit(client, message, pixiv_PHPSESSID):
    work_ids = list()
    tokens = message.content.split(' ')
    for token in tokens:
        try:
            work_ids.append(int(token))
        except ValueError:
            pass
    for work_id in work_ids:
        wp = getworkpage(work_id, pixiv_PHPSESSID)
        await client.send_file(message.channel, wp[0], filename=str(work_id) + '.' + wp[1])
    #print(wp)
    #await client.send_message(message.channel, '...')
    #await client.send_file(message.channel, wp, filename=str(work_id) +'.jpg')
    #print("nope")

def getworkpage(work_id, pixiv_PHPSESSID):
    singleworkexpression = 'https://i.pximg.net/img-original/img/\d+/\d+/\d+/\d+/\d+/\d+/\d+_p(?P<page>\d+).(?P<extension>\w+)'
    singlework = re.compile(singleworkexpression)

    cookies = dict(PHPSESSID=pixiv_PHPSESSID)
    headers = { 'referer':'http://https://www.pixiv.net', 'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}    
    
    r = requests.get('https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + str(work_id), headers = headers, cookies = cookies)
    result = singlework.search(r.text)
    if(result == None):
        return 'nope'
    imageurl = result.group(0)

    headers = { 'referer':'https://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + str(work_id), 'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
    r = requests.get(imageurl, headers = headers, cookies = cookies)
    #f = open(str(work_id) + '.' + result.group('extension'), 'wb')
    #f.write(r.content)
    #f.close()
    return (io.BytesIO(r.content), result.group('extension'))

