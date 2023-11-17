import sqlite3 as sql

class Film():
    def __init__(self,sahip,isim,link):
        self.sahip = sahip
        self.isim = isim
        self.link = link
        
    def __dict__(self):
        return {
            'isim' : self.isim,
            'link' : self.link
        }
    
class Lboxd():
    def __init__(self):
        self.baglanti_olustur()
        
    def baglanti_olustur(self):
        self.baganti = sql.connect('lbox.db')
        self.cursor = self.baganti.cursor()
        sorgu = f'create table if not exists Letterboxd (sahip TEXT, isim TEXT, link TEXT)'
        self.cursor.execute(sorgu)
        self.baganti.commit()
        
    def baglantiyi_kes(self):
        self.baganti.close()
        
    def filmleri_goster(self,sahip):
        sorgu = f'select * from Letterboxd where sahip = ?'
        self.cursor.execute(sorgu,(sahip,))
        filmler = self.cursor.fetchall()
        return filmler
            
    def film_ekle(self,film):
        sorgu = 'insert into Letterboxd values(?,?,?)'
        self.cursor.execute(sorgu,(film.sahip,film.isim,film.link))
        self.baganti.commit()
        
    def temizle(self,sahip):
        sorgu = 'delete from Letterboxd where sahip = ?'
        self.cursor.execute(sorgu,(sahip,))
        self.baganti.commit()