import re
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import json
import requests

def yt_parse(kullanici_adi):
    url = f'https://www.youtube.com/{kullanici_adi}/videos'
    # URL'i acar ve icerigi okur
    try:
        url_search = urlopen(url)
    except:
        return {'error: channel not found':'https://www.youtube.com/'}
    youtube_page = url_search.read()

    # bs kullanarak html icerigini ayristirir
    youtube_html = bs(youtube_page, "html.parser")

    # # scripti uygular, okunmayan kodlari da okuyabilir hale gelir
    pattern = r'<script nonce="[-\w]+">\n\s+var ytInitialData = (.+)'
    script_data = re.search(pattern=pattern, string=youtube_html.prettify())[1].replace(';', '')

    # veriyi dictionary'den json'a cevirir.
    json_data = json.loads(script_data)

    # json verisinden 'videos_container' degiskeniyle listeden videolari alir ve saklar 
    try:
        videos_container = json_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content']['richGridRenderer']['contents']
    except:
        return {'error: bu kanalda video yok':url[:-7]}
    
    ktp = {}
    
    # her bir video icin dongu olusturup islemleri uygular
    for video in videos_container[:10]:
        try:
            video_name = video['richItemRenderer']['content']['videoRenderer']['title']['runs'][0]['text']
            video_id = video['richItemRenderer']['content']['videoRenderer']['videoId']
        except:
            return ktp
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        if len(video_name)>30:
            video_name = f'{video_name[:27]}...'
        ktp[video_name] = video_url
    return ktp 
    
def lboxd_parse(kullanici_adi):
    url = f'https://letterboxd.com/{kullanici_adi}/watchlist'

    ktp = {}
    tpl = []

    response = requests.get(url)
    
    if response.status_code != 200:
        return {'error: kullanici bulunamadi':'https://letterboxd.com/'},[{'error: kullanici bulunamadi':'https://letterboxd.com/'}]

    soup = bs(response.text, 'html.parser')

    sayfalar = soup.find_all('li',{'class':'paginate-page'})

    if sayfalar != []:
        a = 0
        for sayfa in sayfalar: # kac sayfa oldugunu kontrol eder
            try:
                if int(sayfa.text) > a:
                    a = int(sayfa.text)
            except: 
                pass
        
        count = 0
        for sayi in range(1,a+1):
            url2 = f'{url}/page/{sayi}'
            response2 = requests.get(url2)
            soup = bs(response2.text, 'html.parser')
            
            if response.status_code == 200:
                try:
                    liste = soup.find('ul',{'class':'poster-list'})
                    linkler = liste.find_all('div',{'class':'really-lazy-load'})
                    isimler = liste.find_all('img',{'class':'image'})
                except: return ktp,tpl

                for link,isim in zip(linkler,isimler):
                    count += 1
                    try:
                        l = 'https://letterboxd.com' + link['data-target-link']
                        i = isim['alt']
                        ktp[count] = {'isim':i,'link':l}
                        tpl.append({count:{'isim':i,'link':l}})
                    except: pass
        return ktp,tpl
    else:
        url2 = f'{url}/page/1'
        response2 = requests.get(url2)
        soup = bs(response2.text, 'html.parser')
        
        if response.status_code == 200:
            try:
                liste = soup.find('ul',{'class':'poster-list'})
                linkler = liste.find_all('div',{'class':'really-lazy-load'})
                isimler = liste.find_all('img',{'class':'image'})
            except: return ktp,tpl
            
            count = 0
            for link,isim in zip(linkler,isimler):
                count += 1
                try:
                    l = 'https://letterboxd.com' + link['data-target-link']
                    i = isim['alt']
                    ktp[count] = {'isim':i,'link':l}
                    tpl.append({count:{'isim':i,'link':l}})
                except Exception as e: pass
            return ktp,tpl
        

if __name__ == '__main__':
    # print(yt_parse('eceyazg8082'))
    # print(lboxd_parse('eceyzg'))[0]
    pass