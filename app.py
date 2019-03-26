from bs4 import BeautifulSoup
from flask import Flask
import requests as req
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:toor@localhost/rumahginjal'
app.config['SECRET_KEY'] = 'p9Bv<3Eid9%$i01'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)


class HalDepan(db.Model):
    __tablename__ = 'haldepan'
    id_ = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.TEXT)


class DetailedNews(db.Model):
    __tablename__ = 'detail_news'
    iddetail_news = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.TEXT)
    content = db.Column(db.TEXT)
    url = db.Column(db.TEXT)


@app.route('/')
def hello_world():
    urls = HalDepan.query.with_entities(HalDepan.url).all()
    base_url = 'http://rumahginjal.id'
    url = 'http://rumahginjal.id/category/berita'
    for i in range(1, 11):
        get_data(url + '?page=' + str(i), base_url)
    for i in urls:
        get_detail_berita(i.url)

    return "Selesai"


def save_berita(judul, content, url):
    data = DetailedNews(
        judul=judul,
        url=url,
        content=content
    )
    db.session.add(data)
    db.session.commit()
    return True


def scrapt(url):
    requests = req.get(url).text
    return requests


def sorting_html(url):
    a = scrapt(url)
    bs = BeautifulSoup(a, 'lxml')
    dat = bs.find('section', {'class': 'g-pt-100 g-pb-50'})
    listartikel = dat.find_all('div', {'class': 'col-md-8 align-self-center g-pl-20'})
    return listartikel


def simpan_database_haldepan(url):
    if url is not None:
        hal = HalDepan(url=url)
        db.session.add(hal)
        db.session.commit()
        return True
    return False


def get_data(url, base_url):
    data = sorting_html(url)
    # arr_url = []
    for i in range(len(data)):
        get_detail_berita(base_url + data[i].a['href'])
        simpan_database_haldepan(base_url + data[i].a['href'])
    return "Selesai"


def get_detail_berita_khusus(url):
    mentah = req.get('http://rumahginjal.id/rumah-ginjal-fatma-saifullah-yusuf-anak-difabel-jangan-disembunyikan').text
    bs = BeautifulSoup(mentah, 'lxml')
    artikel = bs.find('div', {'class': 'g-font-size-16 g-line-height-1_8 g-mb-30'})
    artikel1 = artikel.find_all('div')
    judul = bs.find('h2', {'class': 'h1 g-mb-15'}).text
    gabungan_artikel = []
    for i in range(len(artikel1)):
        gabungan_artikel.append(artikel1[i].text.strip())
    content = ' '.join(gabungan_artikel)
    return save_berita(judul, content, url)


def get_detail_berita(url):
    mentah = scrapt(url)
    bs = BeautifulSoup(mentah, 'lxml')
    artikel = bs.find('div', {'class': 'g-font-size-16 g-line-height-1_8 g-mb-30'})
    if url == 'http://rumahginjal.id/rumah-ginjal-fatma-saifullah-yusuf-anak-difabel-jangan-disembunyikan':
        artikel1 = artikel.find_all('div')
    else:
        artikel1 = artikel.find_all('p')
    judul = bs.find('h2', {'class': 'h1 g-mb-15'}).text
    gabungan_artikel = []
    for i in range(len(artikel1)):
        gabungan_artikel.append(artikel1[i].text.strip())
    content = ' '.join(gabungan_artikel)
    return save_berita(judul, content, url)


if __name__ == '__main__':
    app.run()
