# YuzTanima-OpenCV
 Raspberry pi3 ile yüz tanımalı güvenlikli kasa projesi.


# Kullanım Bilgileri
<b>*Yeni Kişi Ekleme</b> <br>
Kasaya erişim için kişi bilgileri ve yüz tanıma işlemi gerçekleştirilmelidir. Eğer kişi kayıtlı değilse buradan kayıt edebilirsiniz. Kayıt işlemi için kişinin Adı-Soyadı-TC no gereklidir. Eğer TC no daha önce kayıtlı ise işlem yapılamaz. Bilgiler girildikten sonra yüzünüz tamamen açık ve belirgin olacak şekilde kameraya bakılmalıdır. Bu işlem birkaç dakika sürebilir. Kişiyi kayıt işlemi sonrası buradan kontrol edebilirsiniz.<br>
<b>Not:</b> Kasada tanımlı daimi kullanıcı asla pasif olamaz veya silinemez. Bu kullanıcı tanımı genelde kasa sahibidir.


<b>*Kişi Listesi</b><br>
Sistemde kayıtlı olan kişilerin listesi bu ekranda yer alır. Aktif ve pasif kişiler ayrı tablolarda listelenir. Kişiler üzerinde düzenleme ve silme işlemleri yapılabilmektedir.

<b>Aktif Kişiler:</b> Sistemde kayıtlı ve kasaya erişimi olan kişi listesidir. Bu kişiler istenilen takdirde pasif yapılabilir, bilgileri düzenlenebilir ve silinebilir.
<br>
<b>Pasif Kişiler: </b>Sistemde kayıtlı ve kasaya erişimi olmayan kişi listesidir. Pasif olan kişilerin bilgileri ve yüz taraması silinmez. Yalnızca kasaya erişimi engellenir. Pasif halde kasaya erişmeye çalışılır ise belirlenmiş olan e-posta adresine uyarı maili gitmektedir. Bu kişiler istenilen takdirde aktif yapılabilir, bilgileri düzenlenebilir ve silinebilir.
<br>
<b>Silme İşlemi:</b> Seçilen kişinin bilgilerini ve yüz taramasını sistemden tamamen siler. Kişi kasaya erişmek isterse yeniden kayıt olması gerekir.
<br>
<b>Düzenleme İşlemi:</b> Seçilen kişinin bilgileri düzenlenebilir. TC no sistemde başkasına ait ise düzenleme işlemi gerçekleşmez.
<br>
<b>Resim:</b> Kayıtlı kişinin fotoğrafını gösterir. (Kaydedilen 5. fotoğrafı)
<br>

<b>*Kasaya Erişim</b><br>
Kasaya erişim için kayıtlı olan kişinin yüz taraması yapılır. Tarama için yüz belirgin olacak şekilde sabit kalarak kameraya bakılmalıdır. İşlem yalnızca birkaç saniye sürer. Kişi sistemde bulunamaz veya pasif halde ise belirlenen e-postaya uyarı gider. Yüzü tanımlı olan kişiler ise kasaya erişir. Erişimi sağlayan kişinin bilgileri ve erişim saati hareket listesine eklenir.


<b>*Hareket Listesi</b><br>
Kasaya önceden erişim sağlamış kişiler burada listelenir. Kişinin bilgileri, erişim tarihi ve saati yer alır.

