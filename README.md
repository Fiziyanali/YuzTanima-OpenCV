# YuzTanima-OpenCV
 Raspberry pi3 ile yüz tanımalı güvenlikli kasa projesi.


# Kullanım Bilgileri
*Yeni Kişi Ekleme
Kasaya erişim için kişi bilgileri ve yüz tanıma işlemi gerçekleştirilmelidir. Eğer kişi kayıtlı değilse buradan kayıt edebilirsiniz. Kayıt işlemi için kişinin Adı-Soyadı-TC no gereklidir. Eğer TC no daha önce kayıtlı ise işlem yapılamaz. Bilgiler girildikten sonra yüzünüz tamamen açık ve belirgin olacak şekilde kameraya bakılmalıdır. Bu işlem birkaç dakika sürebilir. Kişiyi kayıt işlemi sonrası buradan kontrol edebilirsiniz.
Not: Kasada tanımlı daimi kullanıcı asla pasif olamaz veya silinemez. Bu kullanıcı tanımı genelde kasa sahibidir.


*Kişi Listesi
Sistemde kayıtlı olan kişilerin listesi bu ekranda yer alır. Aktif ve pasif kişiler ayrı tablolarda listelenir. Kişiler üzerinde düzenleme ve silme işlemleri yapılabilmektedir.

Aktif Kişiler: Sistemde kayıtlı ve kasaya erişimi olan kişi listesidir. Bu kişiler istenilen takdirde pasif yapılabilir, bilgileri düzenlenebilir ve silinebilir.

Pasif Kişiler: Sistemde kayıtlı ve kasaya erişimi olmayan kişi listesidir. Pasif olan kişilerin bilgileri ve yüz taraması silinmez. Yalnızca kasaya erişimi engellenir. Pasif halde kasaya erişmeye çalışılır ise belirlenmiş olan e-posta adresine uyarı maili gitmektedir. Bu kişiler istenilen takdirde aktif yapılabilir, bilgileri düzenlenebilir ve silinebilir.

Silme İşlemi: Seçilen kişinin bilgilerini ve yüz taramasını sistemden tamamen siler. Kişi kasaya erişmek isterse yeniden kayıt olması gerekir.

Düzenleme İşlemi: Seçilen kişinin bilgileri düzenlenebilir. TC no sistemde başkasına ait ise düzenleme işlemi gerçekleşmez.

Resim: Kayıtlı kişinin fotoğrafını gösterir. (Kaydedilen 5. fotoğrafı)


*Kasaya Erişim
Kasaya erişim için kayıtlı olan kişinin yüz taraması yapılır. Tarama için yüz belirgin olacak şekilde sabit kalarak kameraya bakılmalıdır. İşlem yalnızca birkaç saniye sürer. Kişi sistemde bulunamaz veya pasif halde ise belirlenen e-postaya uyarı gider. Yüzü tanımlı olan kişiler ise kasaya erişir. Erişimi sağlayan kişinin bilgileri ve erişim saati hareket listesine eklenir.


*Hareket Listesi
Kasaya önceden erişim sağlamış kişiler burada listelenir. Kişinin bilgileri, erişim tarihi ve saati yer alır.

