from flask import Flask,jsonify,redirect,url_for
from urlParse import yt_parse,lboxd_parse
import random
import db
import os

app = Flask(__name__)

application = app

@app.route('/youtube/<string:id>')
def youtube(id=None):
    if not id.startswith('@'):
        id = f'@{id}'
    veri = yt_parse(id)
    return jsonify(veri)

@app.route('/letterboxd/<string:id>/random')
def letterboxd_random(id):
    lboxd = db.Lboxd()
    liste = lboxd.filmleri_goster(id)
    if len(liste) == 0: 
        a = {'error: liste bos':f'https://letterboxd.com/{id}/watchlist'}
        return jsonify(a)
    chosed = random.choice(liste)
    dct = {chosed[1]:chosed[2]}
    return jsonify(dct)

@app.route('/letterboxd/<string:id>/sync')
def letterboxd_sync(id):
    lboxd = db.Lboxd()
    lboxd.temizle(id)
    filmler = lboxd_parse(id)[1]
    
    if len(filmler) == 1:
        return jsonify(filmler[0])

    count = len(filmler)
    
    for film,index in zip(filmler,range(1,count+1)):
        isim = film[index]['isim']
        link = film[index]['link']
        eklenecek = db.Film(sahip=id,isim=isim,link=link)
        lboxd.film_ekle(eklenecek)
    return redirect(f'/letterboxd/{id}/random')

@app.route('/qr/liste')
def qr_liste():
    url = 'http://webapi.berkehanyavas.com/qr'
    a = {}
    resimler = os.listdir('C:/Users/berke/Desktop/qrapp/static/pictures')
    for i in resimler:
        a[i] = f'{url}/sec/{i}'
    return jsonify(a)

@app.route('/qr/sec/<string:isim>')
def qr_sec(isim):
    with open('C:/Users/berke/Desktop/qrapp/secilen.txt','w',encoding='utf-8') as yaz:
        yaz.write(isim)
    with open('C:/Users/berke/Desktop/qrapp/secilen.txt','r',encoding='utf-8') as oku:
        secilen = oku.read()
    return jsonify(secilen)

@app.route('/qr/secilen')
def qr_secilen():
    with open('C:/Users/berke/Desktop/qrapp/secilen.txt','r',encoding='utf-8') as f:
        secilen = f.read()
    return jsonify(secilen)

if __name__ == '__main__':
    app.run()