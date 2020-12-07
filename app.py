# -*- coding: UTF-8 -*-
#Kutuphane Eklemeleri
from flask import Flask, render_template, request, Response, redirect, abort, url_for, flash, session
from functools import wraps
import sqlite3 as sql #veri tabani islemleri icin
import threading
from datetime import datetime,date 
from passlib.hash import sha256_crypt
import gc #bellek temizleme icin
import os
from time import sleep #bekleme islemi icin
#yuz tanima ve kaydetme islemleri icin
import cv2  
import numpy as np
from PIL import Image
import RPi.GPIO as GPIO #raspberry pin kontrol
import shutil #foto tasıma
#mail islemleri icin
import smtplib
from picamera import PiCamera  
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText  
from email.utils import formatdate  
from email import encoders
from PIL import Image


app = Flask(__name__)
app.secret_key= "j2T*Ao37" #Flask icin sifre

conn = sql.connect('veritabani.db') #veritabani baglantisi
#giris yapabilecek olan kisilerin tablosu
conn.execute('CREATE TABLE IF NOT EXISTS yetki (yetkiID INTEGER PRIMARY KEY AUTOINCREMENT,kullanici_adi nvarchar(20) not null, sifre nvarchar(20) not null)')
#kasaya erisim icin kisi tablosu
conn.execute('CREATE TABLE IF NOT EXISTS kisi (kisiID INTEGER PRIMARY KEY AUTOINCREMENT, tc int(11) not null, ad nvarchar(20) not null, soyad nvarchar(20) not null, aktif bit not null,daimi tinyint not null)')
#kasaya erisim hareket tablosu
conn.execute('CREATE TABLE IF NOT EXISTS hareket (hID INTEGER PRIMARY KEY AUTOINCREMENT, tc int(11) not null, ad nvarchar(20) not null, soyad nvarchar(20) not null , tarih datetime)')

AdminSifre=sha256_crypt.hash('aa') #veritabanina gonderilen sifreyi hashliyoruz
conn.execute("INSERT INTO yetki(kullanici_adi,sifre) values (?,?)", ('admin',AdminSifre))
conn.commit() #islemleri kaydet
conn.close() #veritabani baglantisini kapat


@app.route('/') #Kullanici giris ekrani
def home():
    return render_template('/index.html')

def login_required(f): #giris gereklilik fonksiyonu
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Giriş Gerekli")
            return redirect(url_for('home'))
    return wrap

@app.route('/ekran') #Ana ekran yonlendirme
@login_required
def ekran():
    return render_template('/anaEkran.html')

@app.route('/yeni') #Yeni kisi ekleme sayfasi
@login_required
def yeni():
    con = sql.connect("veritabani.db")
    con.row_factory= sql.Row
    curr= con.cursor()
    curr.execute("SELECT * FROM kisi where daimi=?", ['1']) #aktif kisileri listele
    rows= curr.fetchall()
    con.close()
    return render_template("yeniKisi.html",kisi=len(rows))

@app.route('/bilgilendirme') #Program kullanim bilgileri
@login_required
def bilgilendirme():
    return render_template('/bilgi.html')

@app.route('/yuzTanima') #Kasaya erisim sayfasi
@login_required
def yuzTanima():
    relay = 23
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay, GPIO.OUT)
    GPIO.output(relay ,1) #kilit kapali
    return render_template('/kGiris.html')

@app.route('/cikis') #Aktif kullanici cikisi
@login_required
def cikis():
    session.clear()
    flash("Başarı ile çıkış yaptınız.")
    gc.collect() 
    return redirect(url_for('home'))

@app.route('/liste') #Kisi listesi
@login_required
def liste():
    conn = sql.connect("veritabani.db")
    conn.row_factory= sql.Row
    cur= conn.cursor()
    cur.execute("SELECT * FROM kisi where aktif=?",[1]) #aktif kisileri listele
    rows= cur.fetchall()
    cur.execute("SELECT * FROM kisi where aktif=?",[0]) #pasif kisileri listele
    rows2= cur.fetchall()
    conn.close()
    return render_template("liste.html",kListe=rows, kListe2=rows2)

@app.route('/hListe') #kasaya erisim hareketleri listesi
@login_required
def hListe():
    conn = sql.connect("veritabani.db")
    conn.row_factory= sql.Row
    cur= conn.cursor()
    cur.execute("SELECT * FROM hareket")
    rows= cur.fetchall()
    conn.close()
    return render_template("hListe.html",hListe=rows)
    
@app.route('/login', methods=['POST','GET']) #kullanici giris fonksiyonu
def login():
    conn = sql.connect("veritabani.db")
    c= conn.cursor()
    if request.method == 'POST':
        oku=c.execute("SELECT * FROM yetki")
        if oku:
            data=c.fetchone()
            kullanici_adii= data[1]
            sifree= data[2]
                 
            if sha256_crypt.verify(request.form['sifre'],sifree) and kullanici_adii==request.form['mail']:
                print("basarili")
                session['logged_in']=True
                session['kullanici_adi']=data[1]
                session['sifre']=data[2]
                session['yetkiID']=data[0]
                return redirect(url_for('ekran'))
            else:
                flash("Bilgiler hatalı")
                return redirect(url_for('home'))
        else:
            flash("Yetkisiz Giris")
            return redirect(url_for('home'))
    return redirect(url_for('ekran'))

@app.route('/yeniKisiEkle', methods=['POST','GET']) #yeni kisi ekleme fonksiyonu
def yeniKisiEkle():    
    if request.method == 'POST':
        try:
            #Formdan alinan bilgiler degiskene aktariliyor.
            ad= request.form['ad']
            soyad= request.form['soyad']
            tc= request.form['tc']
            daimi= len(request.form.getlist("daimi"))
            with sql.connect("veritabani.db") as conn:              
                cur= conn.cursor()
                cur.execute("SELECT * FROM kisi where tc=?", [tc])
                adlar = cur.fetchone()
                if str(adlar) == "None": #Ayni tc yok ise kayit islemi
                    cur.execute("INSERT INTO kisi (ad,soyad,tc,aktif,daimi) values (?,?,?,?,?)", (ad,soyad,tc,True,daimi))
                    conn.commit()
                    flash("Kişi Eklendi")
                    #Kamera ile yuz tanima islemi
                    oku=cur.execute("SELECT * FROM kisi where tc=?", [tc])
                    if oku:
                        data=cur.fetchone()
                        face_id= data[0]
                        cam = cv2.VideoCapture(0)
                        cam.set(3, 640) #video genisligi ayari
                        cam.set(4, 480) #video yuksekligi ayari
                        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                        count = 0
                        while(True):
                            ret, img = cam.read()
                            img = cv2.flip(img, -1) #video goruntusunu dikey olarak cevir
                            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            faces = face_detector.detectMultiScale(gray, 1.3, 5)
                            for (x,y,w,h) in faces:
                                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)    
                                count += 1
                                #Resimleri belirlenen adrese kayit et
                                cv2.imwrite("static/dataset/aktif/Kisi." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
                                #cv2.imshow('image', img)
                            #k = cv2.waitKey(100) & 0xff #'ESC' basinca programi durdur
                            #if k == 27:
                                #break
                            if count >= 30: #30 adet foto cekindiyse
                                break
                        #Kamera ve pencereleri kapat
                        cam.release()
                        #cv2.destroyAllWindows()
                        return redirect(url_for('kaydet',yol='yeni'))
                else:
                    flash("TC no kayıtlı")
            conn.close()
        except:
            flash("HATA")
    return redirect(url_for('yeni'))
   
@app.route('/kaydet/<yol>') #Yuz resmi kodlama islemi
def kaydet(yol=0):    
    try:
        #yol belirlenir
        path = 'static/dataset/aktif'
        recognizer = cv2.face.createLBPHFaceRecognizer()
        detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml');
        #goruntu ve etiketi al
        def getImagesAndLabels(path):
            imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
            faceSamples=[]
            ids = []
            for imagePath in imagePaths:
                PIL_img = Image.open(imagePath).convert('L') #gri tonlama
                img_numpy = np.array(PIL_img,'uint8')
                id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces = detector.detectMultiScale(img_numpy)
                for (x,y,w,h) in faces:
                    faceSamples.append(img_numpy[y:y+h,x:x+w])
                    ids.append(id)
            return faceSamples,ids
        faces,ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))
        #Kaydedilecek adres
        recognizer.save('trainer/trainer.yml') # recognizer.save() Mac'te calisir, Pİ'de calismaz
        #Bilgi mesajlari
        flash("\n [BİLGİ] Yüzler tarandı")
        
    except:
        flash("YÜZ TARAMA HATA")
    return redirect(url_for(yol))

@app.route('/kErisim') #Kasayi acma 
def kErisim():
    try:
        #pin ayarlari
        relay = 23
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(relay, GPIO.OUT)
        GPIO.output(relay ,1) #kilit kapali
        recognizer = cv2.face.createLBPHFaceRecognizer()
        recognizer.load('trainer/trainer.yml')
        cascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath);
        font = cv2.FONT_HERSHEY_SIMPLEX
        id = 0
        # names, id'lere bagli: Ornek ==> Beyza: id=1
        #ID'ler 1den basladıgı icin 0.indisler bos
        names = ['Bos']
        surnames = ['Bos']
        
        conn = sql.connect("veritabani.db")
        c= conn.cursor()
        c.execute("SELECT ad FROM kisi where aktif=?", [True])
        adlar = c.fetchall() #isimleri ata
        for i in adlar:
            names.extend(i)
        
        c.execute("SELECT soyad FROM kisi where aktif=?", [True])
        soyadlar = c.fetchall() #soyadlari ata
        for i in soyadlar:
            surnames.extend(i)
        
        cam = cv2.VideoCapture(0)
        cam.set(3, 640)
        cam.set(4, 480)
        #Yuz olarak taninacak minimum pencere boyutu
        minW = 0.1*cam.get(3)
        minH = 0.1*cam.get(4)
        cc=0
        while cc==0:
            ret, img =cam.read()
            img = cv2.flip(img, -1)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale( 
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (int(minW), int(minH)),
               )
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
                id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
                #Benzerlik kontrolu. 100 ==> "0" mukemmel eslesme 
                if (confidence < 60): #benzerlik %40 uzerinde ise
                    id2 = names[id]
                    id3 = surnames[id]
                    ad_soyad= str(id2) +" "+ str(id3)
                    c.execute("SELECT * FROM kisi where kisiID=?", [id])
                    data = c.fetchone()
                    now = datetime.now()
                    tarih = now.strftime("%d/%m/%Y %H:%M:%S")
                    c.execute("INSERT INTO hareket (tc, ad, soyad, tarih) values (?,?,?,?)", [data[1],data[2],data[3],tarih])
                    conn.commit()
                    confidence = "{0}%".format(round(100 - confidence))
                    GPIO.output(relay, 0) #kilit acik
                    sleep(3) #3 saniye bekle
                    GPIO.output(relay, 1) #kilit kapali
                    flash("Kilit açılıyor. Kişi >>>> " + ad_soyad)
                    cc+=1
                else: #benzerlik %40 ve altinda ise
                    id = "Bilinmiyor"
                    confidence = " {0}%".format(round(100 - confidence))
                    GPIO.output(relay, 1) #kilit kapali
                    ad_soyad= str(id)
                    flash("Kilit açılmıyor. Kişi >>>> " +ad_soyad)
                    cc+=1
                    return redirect(url_for('mail')) #bilinmeyen kisi ise mail gönder
                #cv2.putText(img, str(ad_soyad), (x+5,y-5), font, 1, (255,255,255), 2)
                #cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
            #cv2.imshow('Kamera',img)

            #k = cv2.waitKey(10) & 0xff
            #if k == 27:
                #break
        cam.release()
        #cv2.destroyAllWindows()
        conn.close()
        return redirect(url_for('yuzTanima'))
    except:
        flash("YÜZ TANIMA HATA")
        return redirect(url_for('yuzTanima'))
    finally:
        cam.release()
        #cv2.destroyAllWindows()
        conn.close()
    return redirect(url_for('yuzTanima'))

@app.route('/mail') #mail gonderme islemi
def mail():
    camera = PiCamera()  
    camera.start_preview() #mail icin resim cek
    sleep(1) #1saniye bekle
    camera.capture('/home/pi/fizi/bilinmeyen.jpg') #resmi bu yola kaydet
    sleep(1) #1saniye bekle
    camera.stop_preview() #resim cekimi kapar
    camera.close() #kamera kapat

    to='beyzagumus64@gmail.com' #Gonderilecek mail
    me='guvenliKasaErisim@gmail.com' #Gonderen kisi
    subject = "Kasa UYARI !!"  #Mail Konu
    #mail icin ayarlamalar                  
    msg = MIMEMultipart()  
    msg['Subject'] = subject  
    msg['From'] = me 
    msg['To'] = to
    msg.preamble ="test"
    text="Bilinmeyen kişi kasaya erişmeye çalıştı !!" #mail icerik
    msg.attach(MIMEText(text))  
                      
    part = MIMEBase('application', "octet-stream")
    resim= Image.open("bilinmeyen.jpg")
    resim2= resim.rotate(180)
    resim2.save("bilinmeyen2.jpg")
    part.set_payload(open("bilinmeyen2.jpg", "rb").read())  #resim yukle
    encoders.encode_base64(part)  
    part.add_header('Content-Disposition', 'attachment; filename="image.jpg"')  #dosya ismi ve format ismi
    msg.attach(part)  
                      
    s = smtplib.SMTP('smtp.gmail.com', 587)  # Protokol (server)
    s.starttls() 
    s.login("guvenliKasaErisim@gmail.com", "kasa.erisim.001") #mail icin giris 
    s.sendmail("guvenliKasaErisim@gmail.com", "beyzagumus64@gmail.com", msg.as_string()) #mail gonderme islemi
    s.quit() #server cikis
    return redirect(url_for('yuzTanima'))

@app.route('/kisi_sil/<id>/<aktif>') #kisi silme islemi
def kisi_sil(id=0,aktif=0):    
    try:
        conn = sql.connect("veritabani.db")
        conn.row_factory= sql.Row
        cur= conn.cursor()
        if int(aktif)==1:
            for sayi in range(1,31): #kisinin butun fotolarini sil
                os.remove(r'/home/pi/fizi/static/dataset/aktif/Kisi.'+id+'.'+str(sayi)+'.jpg')
        elif int(aktif)==0:
            for sayi in range(1,31): #kisinin butun fotolarini sil
                os.remove(r'/home/pi/fizi/static/dataset/pasif/Kisi.'+id+'.'+str(sayi)+'.jpg')
        #kisiyi veritabanindan sil
        cur.execute("delete from kisi where kisiID=?",[id]) 
        conn.commit()
        flash('Kişi Silindi')
        return redirect(url_for('kaydet', yol='liste'))
        conn.close()
    except:
        flash('Hata Oluştu')
    return redirect(url_for('liste'))

@app.route('/kisi_duzenle/<id>/<no>', methods=['POST','GET']) #kisi duzenleme islemi
def kisi_duzenle(id=0,no=0):    
    try:
        if request.method == 'POST':
            conn = sql.connect("veritabani.db")
            #form bilgilerini degiskene atama islemi
            ad= request.form['ad']
            soyad= request.form['soyad']
            tc= request.form['tc']
            cur= conn.cursor()
            cur.execute("SELECT * FROM kisi where tc=?", [tc]) #kisiyi veritabanindan sec
            kisi = cur.fetchall()
        
            if len(kisi) == 0: #yeni ve daha once olmayan tc ise düzenle
                cur.execute("update kisi set ad=?, soyad=?, tc=? where kisiID=?", [ad,soyad,tc,id])
                conn.commit()
                flash("Kişi Düzenlendi")
            elif len(kisi)==1 and int(kisi[0][0])==int(id): #ayni tc uzerinde duzenleme islemi
                cur.execute("update kisi set ad=?, soyad=?, tc=? where kisiID=?",[ad,soyad,tc,id])
                conn.commit()
                flash('Kişi Düzenlendi')
            else: #ayni tc baska kisi uzerinde var ise
                flash('TC No kayıtli. Kişi düzenleme başarısız..')
            conn.close()
    except:
        flash('Hata Oluştu')
    return redirect(url_for('liste'))

@app.route('/pasif/<id>', methods=['POST','GET']) #kisiyi pasif yapma islemi
#NOT: Kisi pasif olunca kasaya erisim engellenir ancak fotolari ve bilgileri silinmez.
def pasif(id=0):    
    try:
        conn = sql.connect("veritabani.db")
        cur= conn.cursor()
        cur.execute("update kisi set aktif=? where kisiID=?", [False,id]) #secilen kisinin aktifligini boz
        conn.commit()
        for sayi in range(1,31): #kisi fotosunu pasif klasorune tasir. Boylelikle kasaya giris engellenir.
            shutil.move('/home/pi/fizi/static/dataset/aktif/Kisi.'+id+'.'+str(sayi)+'.jpg', '/home/pi/fizi/static/dataset/pasif/Kisi.'+id+'.'+str(sayi)+'.jpg')
        flash('Kişi Pasifleştirildi')
        conn.close()
        return redirect(url_for('kaydet',yol='liste')) #aktif yuzleri yeniden tara
    except:
        flash('Hata Oluştu')
    return redirect(url_for('liste'))

@app.route('/aktif/<id>', methods=['POST','GET']) #kisiyi aktif yapma islemi
def aktif(id=0):    
    try:
        conn = sql.connect("veritabani.db")
        cur= conn.cursor()
        cur.execute("update kisi set aktif=? where kisiID=?", [True,id]) #secilen kisinin aktif yap
        conn.commit()
        for sayi in range(1,31): #kisi fotosunu aktif klasorune tasir. Boylelikle kasaya erisim saglanabilir.
           shutil.move('/home/pi/fizi/static/dataset/pasif/Kisi.'+id+'.'+str(sayi)+'.jpg', '/home/pi/fizi/static/dataset/aktif/Kisi.'+id+'.'+str(sayi)+'.jpg')
        flash('Kişi Aktifleştirildi')
        conn.close()
        return redirect(url_for('kaydet',yol='liste')) #aktif yuzleri yeniden tara
    except:
        flash('Hata Oluştu')
    return redirect(url_for('liste'))

if __name__ == '__main__':
    app.run(debug=True)
