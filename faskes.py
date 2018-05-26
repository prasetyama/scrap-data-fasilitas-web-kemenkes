
import requests
from mysql.connector import connect, Error
from bs4 import BeautifulSoup

#making database connection
dbhost = 'localhost'
dbuser = 'root'
dbpass = 'root'
dbname = 'scrap_faskes'
dbport = 3306

conn = connect(host = dbhost,
        user = dbuser,
        password = dbpass,
        database = dbname,
        port = dbport)

cur = conn.cursor()

def making_table():
    try:
        cur.execute('''CREATE TABLE scrap_faskes
        (pr_id int(11) DEFAULT NULL,
        lat varchar(255) DEFAULT NULL,
        lng varchar(255) DEFAULT NULL,
        title varchar(255) DEFAULT NULL,
        kode_unit varchar(255) DEFAULT NULL,
        nama_unit varchar(255) DEFAULT NULL,
        alamat varchar(255) DEFAULT NULL,
        spesialis varchar(11) DEFAULT NULL,
        umum varchar(11) DEFAULT NULL,
        gigi varchar(11) DEFAULT NULL,
        perawat varchar(11) DEFAULT NULL,
        bidan varchar(11) DEFAULT NULL,
        farmasi varchar(11) DEFAULT NULL,
        nakes varchar(11) DEFAULT NULL,
        pendukung varchar(11) DEFAULT NULL
        );''')
        print "Table created successfully"
        conn.commit()
    except:
        pass


def cleansing(string):
    #rapihin string
        a = (string.encode("ASCII", 'ignore')).replace('\t','')
        b = a.replace('\r\n','')
        c = b.replace('({','')
        d = c.replace('});','')
        e = d.replace('#map','')
        f = e.replace("'",'')
        g = f.split('content:')
        h = g[0].split(',')

        #process lat
        lat = h[0].split(':')
        lat = lat[1].replace(' ','')


        #process lng
        lng = h[1].split(':')
        lng = lng[1].replace(' ','')

        #process title
        title = h[1].split(':')
        title = title[1]
        title = title.replace(' "','')
        title = title.replace('"','')
        title = title.replace('\\','')

        #get content
        content = g[1].replace('<div><table border=1><tr><td>','')
        content = content.replace('\\','')
        content = content.replace('<td>','')
        content = content.replace('</td>','')
        content = content.replace(';','')
        content = content.replace('<tr>',';')
        content = content.replace('</tr>','')
        content = content.replace('<br/>',';')
        content = content.split(';')

        #process kode unit
        kode_unit = content[0].split(':')
        kode_unit = kode_unit[1]

        #process nama unit
        nama_unit = content[1].split(':')
        nama_unit = nama_unit[1]

        #process alamat
        alamat = content[2].split(':')
        alamat = alamat[1]

        #process dokter spesialis
        spesialis = content[3].split('=')
        spesialis = spesialis[1]

        #process dokter umum
        umum = content[4].split('=')
        umum = umum[1]

        #process dokter gigi
        gigi = content[5].split('=')
        gigi = gigi[1]

        #process perawat
        perawat = content[6].split('=')
        perawat = perawat[1]

        #process bidan
        bidan = content[7].split('=')
        bidan = bidan[1]

        #process farmasi
        farmasi = content[8].split('=')
        farmasi = farmasi[1]

        #process nakes
        nakes = content[9].split('=')
        nakes = nakes[1]

        #process nakes
        pendukung = content[10].split('=')
        pendukung = pendukung[1]

        return lat,lng,title,kode_unit,nama_unit,alamat,spesialis,umum,gigi,perawat,bidan,farmasi,nakes,pendukung


def get_map(kode_prov):
    endpoint = 'http://bppsdmk.kemkes.go.id/info_sdmk/peta?prov='
    kode_prov = kode_prov
    r = requests.get(endpoint+kode_prov)
    content = r.text
    soup = BeautifulSoup(content,'lxml')
    script = soup.find_all('script')
    map = (script[len(script)-38].string).split('map.addMarker')
    print map
    i = len(map)
    while i>1:
        i -=1
        print i,kode_prov

        clean=cleansing(map[i])

        query = "insert into scrap_faskes values (%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
        %(kode_prov,clean[0],clean[1],clean[2],clean[3],clean[4],clean[5],clean[6],clean[7],clean[8],clean[9],clean[10],clean[11],clean[12],clean[13])
        print query
        cur.execute(query)
        conn.commit()


def kode_prov():
    endpoint = 'http://bppsdmk.kemkes.go.id/info_sdmk/peta'
    r = requests.get(endpoint)
    content = r.text
    soup = BeautifulSoup(content,'lxml')
    form = soup.find_all('form')
    option = form[1].find_all('option')
    for value in option:
        kode_prov = value.get('value')
        print kode_prov
        get_map(kode_prov)

def main():
    making_table()
    kode_prov()

main()
