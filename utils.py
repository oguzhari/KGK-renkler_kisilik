import streamlit as st
from docx import Document
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import random
import string
import color_tone

st.config.set_option("theme.primaryColor", "white")

css_code = """
<style>
    .content-container {
        border-top: 3px solid black;
        border-bottom: 3px solid black;
    }
    .row-divider {
        border-bottom: 1px solid gray;
        margin: 10px 0;
    }
</style>
"""

# CSS kodlarını uygulamaya ekleyin
st.markdown(css_code, unsafe_allow_html=True)

# Metinler
a = "Aşağıdakilerden hangisi sizi daha iyi anlatır?"
a1 = "Güçlü, kararlı, girişken ve doğuştan liderim. Kimseye minnet etmem; düşer kalkar ve yoluma devam ederim."
a2 = "Hayata anlamlı renkler katar, eğlenceyi severim. Ömür boyu herkesin mutlu ve neşeli olmasını dilerim"
a3 = "Her anımı huzurlu ve sakin geçirmek isterim. Kavga-gürültü sevmem, işlerimde en kolay yolu seçerim."
a4 = "Her şeyin mükemmel, düzgün ve kusursuz olmasını isterim. İlişkilerimde saygılı ve mesafeli olmayı severim."
b = "Genellikle hangi tempoda ve nasıl konuşursunuz?"
b1 = "Hızlı ve sonuca yönelik."
b2 = "Çok hızlı, heyecanlı ve eğlenceli."
b3 = "Daha yavaş ve sakin."
b4 = "Normal ve söyleyeceklerimi aklımda tutarak."
c = "Bir işe motive olmanızı sağlayan en önemli unsur hangisidir?"
c1 = "Sonuçları düşünmek."
c2 = "Onaylanmak, takdir edilmek."
c3 = "Gruptaki arkadaşlarımın desteği."
c4 = "Etkinlik, düzen ve disiplin."
d = "Çalışma tarzınız hangisine uygundur?"
d1 = "Yoğun ve hızlıyımdır. Aynı anda birkaç işi bir arada yapabilirim."
d2 = "Özgür bir ortamda çalışırım. İnsan ilişkileri odaklıyımdır."
d3 = "Ön planda olmayan ama gruba her zaman destek veren bir yapım vardır."
d4 = "Ayrıntıları önemserim ve tek bir konuya odaklanarak çalışırım."
e = "Çalışma temponuzu nasıl değerlendiriyorsunuz?"
e1 = "Hızlı bir tempoda çalışır, çabuk karar almayı severim."
e2 = "İşlerin rutin ve sıkıcı olmadığı ortamlarda yüksek motivasyonla çalışırım."
e3 = "Nadiren aceleciyimdir. Geç de olsa üstlendiğim işi bitiririm."
e4 = "Ayrıntılı düşünerek karar veririm, ağır ama iş bitirici bir tempoyla çalışırım."
f = "Hangisi sizi daha çok rahatsız eder?"
f1 = "Zaman israfı ve işlerin gecikmesi."
f2 = "Tekrar gerektiren işler ve monotonluk."
f3 = "Çalışma ortamı ve anlaşmazlıklar."
f4 = "Yanılmak ve yapılan hatanın tekrarlanması."
g = "Bulunduğunuz gruplarda hangi konumda daha başarılı olursunuz?"
g1 = "Olaylara yön veren ve otoriteyi kullanan."
g2 = "İnsanları motive eden ve neşelendiren."
g3 = "Uzlaştırıcı ve grup içindeki uyumu sağlayan"
g4 = "Bilgi sağlayıcı, araştırıcı ve olayları takip eden."
h = "Hangisi sizi daha çok strese sokar?"
h1 = "Olayların üzerindeki güç ve kontrolümün azaldığını hissetmek."
h2 = "Sıkıcı, rutin işler yapılan bir ortamda bulunmak."
h3 = "Beni aşacağını düşündüğüm sorumluluklar üstlenmek."
h4 = "Düzensiz ortamlar ve eksik yapılan işler."
i = "Bir öğrenci olsanız ve öğretmeniniz sınav kağıdınızı ikinci defa incelediğinde puanınızın arttığını söylese, " \
    "nası bir tepki verirsiniz?"
i1 = "Bunu zaten hakettiğimi düşünürüm."
i2 = "Çok sevinirim ve sevincimi belli ederim."
i3 = "Hocama teşekkür eder ve saygı duyarım."
i4 = "Hocamın nerede hata yaptığını merak eder, kağıdımı görmek isterim."
j = "Saatler sürecek bir iş toplantısına katılmanız gerektiğinde aşağıdakilerden hangisini benimsersiniz?"
j1 = "Toplantı başında genellikle konunun ana hatları konuşulduğu için biraz geç girerim. Sonucun belli olmasından " \
     "hemen sonra da çıkmayı tercih ederim."
j2 = "Toplantı eğlenceli bir şekilde devam ederse sonuna kadar kalırım. Toplantı sıkıcı olmaya " \
     "başladığında erken çıkarım."
j3 = "Toplantının huzur içinde geçmesi ve güzel kararlar alınması için üstüme düşeni yaparım."
j4 = "Toplantıya tam vaktinde veya vaktinden önce gelirim. Toplantı esnasında notlar alır, " \
     "sonunda biraz kalarak değerlendirme yaparım."
k = "Kendinizde gördüğünüz en zayıf yönünüz hangisidir?"
k1 = "İşler zamanında ve istediğim gibi yapılmadığında sinirlenmek."
k2 = "Düzensiz, dağınık ve plansız olmak."
k3 = "Kimseye 'hayır' diyememek, başkalarının işine koşarken kendi işimi aksatmak."
k4 = "Her şeyin kusursuz, mükemmel olmasını istemek; insanlarda bunu görmediğimde sinirlenmek."
m = "Kendinizde gördüğünüz en güçlü yönünüz hangisidir?"
m1 = "Kısa sürede karar alıp hemen harekete geçmem."
m2 = "Girdiğim ortama neşe ve heyecan katabilmem."
m3 = "Her türlü ortama uyum sağlamam ve çatışmaları önleme gayretim."
m4 = "Her şeyi planlı, programlı ve düzenli yapmam."
n = "Aşağıdaki ifadelerden hangisi sizi daha iyi tanımlar?"
n1 = "Güçlü, kararlı, otoriter ve yönlendirici."
n2 = "Popüler, neşeli, sevimli ve muzip."
n3 = "Barışçıl, sevecen, uyumlu ve sakin."
n4 = "Tertipli, düzenli, disiplinli ve planlı."
o = "Çalışma masanızda nelere dikkat edersiniz?"
o1 = "Öncelikli işlerime göre düzenlenmiş, sade bir masayı tercih ederim."
o2 = "İnsanlara karma karışık gelen ama benim aradığım her şeyi kolayca bulduğum bir masada çalışırım."
o3 = "Önce masamın üzerine gerekli olan her türlü araç gereci koyarım, " \
     "çünkü sık sık kalkarak enerjimi harcamak istemem."
o4 = "İyi bir iş çıkarmam için masam son derece derli ve düzenli olmalıdır."
p = "Ertesi gün çözülmesi gereken bir problem varsa, o akşamki ruh haliniz nasıl olur?"
p1 = "Büyük bir tedirginlik duymam, çünkü ertesi gün olması gerektiği gibi yapacağımdan eminimdir."
p2 = "Çok tedirginlik duymam, çünkü nasıl olsa işler bir şekilde halolacaktır."
p3 = "Sorumluluğun üstümde olmasından dolayı tedirginlik duyarım."
p4 = "Tedirginlik duyarım ve gecenin büyük bir bölümünde problemin nasıl çözüleceğiyle ilgili planlar yaparım."

# Analiz Sonuçları
sari = """
Sizin öncelikli renk temanızın "sarı" olduğu tespit edilmiştir. Sarı renk, temelde enerjik, neşeli ve dinamik bir kişiliği temsil eder. İşte sizinle ilgili daha detaylı bir analiz:

Sosyal İlişkiler ve Popülerlik: Sarı kişilik tipi olarak, sosyal becerileriniz ve iletişim kabiliyetiniz oldukça gelişmiştir. İnsanlarla kurduğunuz ilişkilerde empati ve samimiyet ön plandadır. Bu nedenle, grup içerisinde sevilen ve takdir edilen bir birey olma eğilimindesiniz.

Yenilikçilik ve Esneklik: Sarı renkli kişilikler, yaşamlarında hareketlilik ve değişiklik arayışındadırlar. Yeniliklere açık olmanız ve esnek yaklaşımınız, sizin adaptasyon sürecini başarıyla yönetebilmenize ve farklı deneyimler kazanabilmenize olanak tanır.

Duygu İfadesi ve Duyarlılık: Duygusal zekanızın yüksek olması, insanlarla olan iletişiminizde duygu ve düşüncelerinizi etkili bir şekilde ifade etmenize yardımcı olur. Bu özellik, çevrenizdeki kişilerin sizinle daha derin bağlar kurmasını ve sizi daha iyi anlamasını sağlar.

Girişimcilik ve Tepkisel Davranışlar: Sarı kişilik özelliklerine sahip bireyler, aktif ve girişimci bir yapıya sahiptirler. Bu durum, projelerde ve işbirliklerinde başkalarını motive edebilme ve enerji seviyelerini yüksek tutma kabiliyetinizi destekler. Ancak, tepkisel davranışlarınız kontrol altına alınmalı ve dikkatli analizler yaparak kararlar verilmelidir.

Yukarıda belirtilen sarı renkli kişilik özelliklerinizi göz önünde bulundurarak, sosyal ve iş hayatınızdaki başarınızı artırabilir ve insanlarla daha uyumlu bir şekilde iletişim kurabilirsiniz. Kendi özelliklerinizi tanıyarak, potansiyelinizi en iyi şekilde kullanmaya yönelik stratejiler geliştirmek önemlidir.

Başarılar ve mutluluklar dileriz!
"""

mavi = """
Sizin öncelikli renk temanızın "mavi" olduğu tespit edilmiştir. Mavi renk, temelde asil, ciddi ve düzenli bir kişiliği temsil eder. İşte sizinle ilgili daha detaylı bir analiz:

Düşünce Yapısı ve Planlama: Mavi kişilik tipi olarak, analitik düşünme ve planlama becerileriniz oldukça gelişmiştir. İş ve özel yaşamınızda gerçekleştirmeyi düşündüğünüz projelerde detaylı ve kapsamlı planlar yaparak başarıya ulaşma olasılığınızı artırırsınız.

Disiplin ve Düzen: Yaşamınızda düzen ve disiplini önemseyen bir bireysiniz. İşlerinizi titizlikle ve zamanında yaparak, başkalarına güvenilir ve sorumluluk sahibi bir izlenim bırakırsınız. Bu özellikleriniz, iş hayatında ve sosyal ilişkilerinizde takdir edilen yönlerinizdendir.

Kuralcılık ve İstikrar: Mavi renkli kişilikler, kurallara ve prosedürlere bağlı kalmayı tercih ederler. İstikrarlı ve tutarlı bir yaşam sürdürmeyi amaçlarlar. Bu yaklaşım, özellikle iş yaşamında başarı elde etmenize katkıda bulunur.

İlişkisel Yaklaşım ve Mesafeli Tutum: İnsanlarla kurduğunuz ilişkilerde daha mesafeli ve ilişkisel bir tutum sergileyebilirsiniz. Bu durum, başkalarıyla daha derin bağlar kurma sürecinde daha fazla zaman ve emek harcamanız gerektiği anlamına gelebilir.

Yukarıda belirtilen mavi renkli kişilik özelliklerinizi göz önünde bulundurarak, sosyal ve iş hayatınızdaki başarınızı artırabilir ve insanlarla daha uyumlu bir şekilde iletişim kurabilirsiniz. Kendi özelliklerinizi tanıyarak, potansiyelinizi en iyi şekilde kullanmaya yönelik stratejiler geliştirmek önemlidir.

Başarılar ve mutluluklar dileriz!
"""

kirmizi = """
Sizin öncelikli renk temanızın "kırmızı" olduğu tespit edilmiştir. Kırmızı renk, temelde canlı, güçlü ve kararlı bir kişiliği temsil eder. İşte sizinle ilgili daha detaylı bir analiz:

Liderlik ve Kararlılık: Kırmızı kişilik tipi olarak, doğuştan liderlik yetenekleriniz ve kararlılık özellikleriniz bulunmaktadır. İş ve özel yaşamınızda başkalarını yönlendirebilir ve onlara ilham verebilirsiniz. Bu sayede, gruplar ve projeler için değerli bir üye olursunuz.

Hedef Odaklılık ve Başarı: Yaşamınızda belirlediğiniz hedeflere ulaşmak için azimli ve kararlı bir şekilde çalışırsınız. Bu durum, başarıya giden yolda sizi daha hızlı ilerletir ve iş hayatında veya sosyal ilişkilerinizde önemli kazanımlar elde etmenize yardımcı olur.

Sorumluluk ve İnisiyatif: Kırmızı renkli kişilikler, sorumluluklarını yerine getirmeyi önemseyen ve inisiyatif kullanabilen bireylerdir. İş yaşamında ve sosyal çevrenizde, problemlere çözüm getirebilme ve başkalarının güvendiği bir isim olma eğilimindesiniz.

Tartışmacı ve Mücadeleci: İnsanlarla kurduğunuz ilişkilerde, düşüncelerinizi ve fikirlerinizi savunma eğiliminiz olabilir. Bu durum, bazen çatışma ve anlaşmazlıklara yol açsa da, doğru iletişim stratejileri kullanarak etkili bir uyum sağlayabilirsiniz.

Yukarıda belirtilen kırmızı renkli kişilik özelliklerinizi göz önünde bulundurarak, sosyal ve iş hayatınızdaki başarınızı artırabilir ve insanlarla daha uyumlu bir şekilde iletişim kurabilirsiniz. Kendi özelliklerinizi tanıyarak, potansiyelinizi en iyi şekilde kullanmaya yönelik stratejiler geliştirmek önemlidir.

Başarılar ve mutluluklar dileriz!
"""

yesil = """
Sizin öncelikli renk temanızın "yeşil" olduğu tespit edilmiştir. Yeşil renk, temelde rahatlatıcı, huzur verici ve uyumlu bir kişiliği temsil eder. İşte sizinle ilgili daha detaylı bir analiz:

Barışçı ve Uyumlu: Yeşil kişilik tipi olarak, insanlarla kurduğunuz ilişkilerde barışçıl ve uyumlu bir tutum sergilersiniz. Çatışmalardan kaçınarak, ortamın huzurunu ve dengesini koruma eğilimindesiniz. Bu sayede, sosyal çevrenizde sevilen ve saygı gören bir birey olursunuz.

İşbirliği ve Destek: İş yaşamında ve sosyal ilişkilerinizde işbirliğine ve desteklemeye büyük önem verirsiniz. Başkalarının fikirlerini dinlemeye ve onlara yardımcı olmaya açık bir yapıya sahipsiniz. Bu özellikleriniz, grup çalışmalarında ve işbirliği gerektiren projelerde başarılı olmanıza katkı sağlar.

Sevecenlik ve Empati: Yeşil renkli kişilikler, sevecen ve empati sahibi bireylerdir. İnsanlarla kurduğunuz ilişkilerde, onların duygularını ve düşüncelerini anlama ve paylaşma eğilimindesiniz. Bu durum, çevrenizdeki kişilerin sizinle daha derin bağlar kurmasını ve sizi daha iyi anlamasını sağlar.

Duyarlılık ve Kişisel Yaklaşım: İnsanlarla olan iletişiminizde, duyarlılık ve kişisel yaklaşım sergileyebilirsiniz. Bu durum, başkalarıyla daha sıcak ve samimi bir ilişki kurma sürecinde olumlu etkiler yaratabilir. Ancak, gerektiğinde sınırlarınızı koruyarak dengeli bir iletişim sağlamak önemlidir.

Yukarıda belirtilen yeşil renkli kişilik özelliklerinizi göz önünde bulundurarak, sosyal ve iş hayatınızdaki başarınızı artırabilir ve insanlarla daha uyumlu bir şekilde iletişim kurabilirsiniz. Kendi özelliklerinizi tanıyarak, potansiyelinizi en iyi şekilde kullanmaya yönelik stratejiler geliştirmek önemlidir.

Başarılar ve mutluluklar dileriz!
"""

resimle_ilgili_not = ""
dosya_adi = ""

# Cevapları kontrol et
def cevaplari_kontrol_et(bir, iki, uc, dort):
    bir, iki, uc, dort = int(bir), int(iki), int(uc), int(dort)
    if bir + iki + uc + dort == 3:
        pass
    elif bir + iki + uc + dort == 2:
        pass
    elif bir + iki + uc + dort == 0:
        pass
    else:
        st.error("Soruları cevaplama konusunda bir sorun var. "
                 "Cevaplarda en az bir adet 2 olmalıdır. "
                 "Bunun yanında en fazla bir adet 1 olabilir.")


# Global değerler.
options = [0, 1, 2]
value_a1, value_a2, value_a3, value_a4 = 0, 0, 0, 0
value_b1, value_b2, value_b3, value_b4 = 0, 0, 0, 0
value_c1, value_c2, value_c3, value_c4 = 0, 0, 0, 0
value_d1, value_d2, value_d3, value_d4 = 0, 0, 0, 0
value_e1, value_e2, value_e3, value_e4 = 0, 0, 0, 0
value_f1, value_f2, value_f3, value_f4 = 0, 0, 0, 0
value_g1, value_g2, value_g3, value_g4 = 0, 0, 0, 0
value_h1, value_h2, value_h3, value_h4 = 0, 0, 0, 0
value_i1, value_i2, value_i3, value_i4 = 0, 0, 0, 0
value_j1, value_j2, value_j3, value_j4 = 0, 0, 0, 0
value_k1, value_k2, value_k3, value_k4 = 0, 0, 0, 0
value_m1, value_m2, value_m3, value_m4 = 0, 0, 0, 0
value_n1, value_n2, value_n3, value_n4 = 0, 0, 0, 0
value_o1, value_o2, value_o3, value_o4 = 0, 0, 0, 0
value_p1, value_p2, value_p3, value_p4 = 0, 0, 0, 0
ad_soyad, meslek, unvan, bolum, yas, cinsiyet, mail, telefon = "", "", "", "", "", "", "", ""
erid = ""


def head():
    st.markdown("""
        <h1 style='text-align: center'>
        Renkler ve Kişilik Envanteri
        </h1>
    """, unsafe_allow_html=True
                )

    st.caption("""
        <p style='text-align: center;margin-bottom: 50px;'>
        Sakarya Üniversitesi Kariyer ve Yetenek Yönetimi Koordinatörlüğü
        </p>
    """, unsafe_allow_html=True
               )


def kisisel_bilgiler():
    global ad_soyad, meslek, unvan, bolum, yas, cinsiyet, mail, telefon
    ad_soyad = st.text_input("Adınız ve Soyadınız", key="ad_soyad")
    meslek = st.text_input("Mesleğiniz", key="meslek")
    unvan = st.text_input("Ünvanınız", key="unvan")
    bolum = st.text_input("Bölümünüz", key="bolum")
    yas = st.text_input("Yaşınız", key="yas")
    cinsiyet = st.selectbox("Cinsiyetiniz", ["Erkek", "Kadın"], key="cinsiyet")
    mail = st.text_input("Mail Adresiniz", key="mail")
    telefon = st.text_input("Telefon Numaranız", key="telefon")


def sorular():
    global value_a1, value_a2, value_a3, value_a4, value_b1, value_b2, value_b3, value_b4, value_c1, value_c2, \
        value_c3, value_c4, value_d1, value_d2, value_d3, value_d4, value_e1, value_e2, value_e3, value_e4, value_f1, \
        value_f2, value_f3, value_f4, value_g1, value_g2, value_g3, value_g4, value_h1, value_h2, value_h3, value_h4, \
        value_i1, value_i2, value_i3, value_i4, value_j1, value_j2, value_j3, value_j4, value_k1, value_k2, value_k3, \
        value_k4, value_m1, value_m2, value_m3, value_m4, value_n1, value_n2, value_n3, value_n4, value_o1, value_o2, \
        value_o3, value_o4, value_p1, value_p2, value_p3, value_p4
    st.info("Farklı karakterlerin özelliklerini tespit etmede bir ölçü olarak aşağıda bir test uygulaması "
            "yer almaktadır. Aşağıdaki test, her biri dört şıktan oluşan 15 soru içermektedir. Seçeneklerde belirtilen "
            "özellikler, size ne derece uyar ise ona göre puan veriniz.")
    st.warning("Her sorunun altında dört şık yer almaktadır. Soruları cevaplarken size EN UYGUN seçeneğe 2 puan, "
               "o seçenekten sonra size EN UYGUN ise 1 puan yazın. Seçeneklerden sadece iki şıkka puan verin, "
               "eğer sadece tek şıkka işaret koyacaksanız, o şıkka 2 puan verin.")
    st.success("Envanteri telefondan dolduruyorsanız, telefonu yatay modda kullanmak okunabilirliği arttırabilir.")
    with st.container():
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

        st.subheader(a)
        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{a1}", unsafe_allow_html=True)
            value_a1 = col2.selectbox("Seçin", options, key="a1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{a2}", unsafe_allow_html=True)
            value_a2 = col2.selectbox("Seçin", options, key="a2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{a3}", unsafe_allow_html=True)
            value_a3 = col2.selectbox("Seçin", options, key="a3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{a4}", unsafe_allow_html=True)
            value_a4 = col2.selectbox("Seçin", options, key="a4")

        cevaplari_kontrol_et(value_a1, value_a2, value_a3, value_a4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

    with st.container():
        st.subheader(b)

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{b1}", unsafe_allow_html=True)
            value_b1 = col2.selectbox("Seçin", options, key="b1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{b2}", unsafe_allow_html=True)
            value_b2 = col2.selectbox("Seçin", options, key="b2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{b3}", unsafe_allow_html=True)
            value_b3 = col2.selectbox("Seçin", options, key="b3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{b4}", unsafe_allow_html=True)
            value_b4 = col2.selectbox("Seçin", options, key="b4")

        cevaplari_kontrol_et(value_b1, value_b2, value_b3, value_b4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

    with st.container():
        st.subheader(c)

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{c1}", unsafe_allow_html=True)
            value_c1 = col2.selectbox("Seçin", options, key="c1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{c2}", unsafe_allow_html=True)
            value_c2 = col2.selectbox("Seçin", options, key="c2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{c3}", unsafe_allow_html=True)
            value_c3 = col2.selectbox("Seçin", options, key="c3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{c4}", unsafe_allow_html=True)
            value_c4 = col2.selectbox("Seçin", options, key="c4")

        cevaplari_kontrol_et(value_c1, value_c2, value_c3, value_c4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

    with st.container():
        st.subheader(d)

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{d1}", unsafe_allow_html=True)
            value_d1 = col2.selectbox("Seçin", options, key="d1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{d2}", unsafe_allow_html=True)
            value_d2 = col2.selectbox("Seçin", options, key="d2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{d3}", unsafe_allow_html=True)
            value_d3 = col2.selectbox("Seçin", options, key="d3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{d4}", unsafe_allow_html=True)
            value_d4 = col2.selectbox("Seçin", options, key="d4")

        cevaplari_kontrol_et(value_d1, value_d2, value_d3, value_d4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

    with st.container():
        st.subheader(e)

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{e1}", unsafe_allow_html=True)
            value_e1 = col2.selectbox("Seçin", options, key="e1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{e2}", unsafe_allow_html=True)
            value_e2 = col2.selectbox("Seçin", options, key="e2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{e3}", unsafe_allow_html=True)
            value_e3 = col2.selectbox("Seçin", options, key="e3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{e4}", unsafe_allow_html=True)
            value_e4 = col2.selectbox("Seçin", options, key="e4")

        cevaplari_kontrol_et(value_e1, value_e2, value_e3, value_e4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

    with st.container():
        st.subheader(f)

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{f1}", unsafe_allow_html=True)
            value_f1 = col2.selectbox("Seçin", options, key="f1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{f2}", unsafe_allow_html=True)
            value_f2 = col2.selectbox("Seçin", options, key="f2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{f3}", unsafe_allow_html=True)
            value_f3 = col2.selectbox("Seçin", options, key="f3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{f4}", unsafe_allow_html=True)
            value_f4 = col2.selectbox("Seçin", options, key="f4")

        cevaplari_kontrol_et(value_f1, value_f2, value_f3, value_f4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

    with st.container():
        st.subheader(g)

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{g1}", unsafe_allow_html=True)
            value_g1 = col2.selectbox("Seçin", options, key="g1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{g2}", unsafe_allow_html=True)
            value_g2 = col2.selectbox("Seçin", options, key="g2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{g3}", unsafe_allow_html=True)
            value_g3 = col2.selectbox("Seçin", options, key="g3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{g4}", unsafe_allow_html=True)
            value_g4 = col2.selectbox("Seçin", options, key="g4")

        cevaplari_kontrol_et(value_g1, value_g2, value_g3, value_g4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

    with st.container():
        st.subheader(h)

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{h1}", unsafe_allow_html=True)
            value_h1 = col2.selectbox("Seçin", options, key="h1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{h2}", unsafe_allow_html=True)
            value_h2 = col2.selectbox("Seçin", options, key="h2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{h3}", unsafe_allow_html=True)
            value_h3 = col2.selectbox("Seçin", options, key="h3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{h4}", unsafe_allow_html=True)
            value_h4 = col2.selectbox("Seçin", options, key="h4")

        cevaplari_kontrol_et(value_h1, value_h2, value_h3, value_h4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

    with st.container():
        st.subheader(i)

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{i1}", unsafe_allow_html=True)
            value_i1 = col2.selectbox("Seçin", options, key="i1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{i2}", unsafe_allow_html=True)
            value_i2 = col2.selectbox("Seçin", options, key="i2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{i3}", unsafe_allow_html=True)
            value_i3 = col2.selectbox("Seçin", options, key="i3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{i4}", unsafe_allow_html=True)
            value_i4 = col2.selectbox("Seçin", options, key="i4")

        cevaplari_kontrol_et(value_i1, value_i2, value_i3, value_i4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

    with st.container():
        st.subheader(j)

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{j1}", unsafe_allow_html=True)
            value_j1 = col2.selectbox("Seçin", options, key="j1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{j2}", unsafe_allow_html=True)
            value_j2 = col2.selectbox("Seçin", options, key="j2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{j3}", unsafe_allow_html=True)
            value_j3 = col2.selectbox("Seçin", options, key="j3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{j4}", unsafe_allow_html=True)
            value_j4 = col2.selectbox("Seçin", options, key="j4")

        cevaplari_kontrol_et(value_j1, value_j2, value_j3, value_j4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

    with st.container():
        st.subheader(k)

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{k1}", unsafe_allow_html=True)
            value_k1 = col2.selectbox("Seçin", options, key="k1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{k2}", unsafe_allow_html=True)
            value_k2 = col2.selectbox("Seçin", options, key="k2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{k3}", unsafe_allow_html=True)
            value_k3 = col2.selectbox("Seçin", options, key="k3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{k4}", unsafe_allow_html=True)
            value_k4 = col2.selectbox("Seçin", options, key="k4")

        cevaplari_kontrol_et(value_k1, value_k2, value_k3, value_k4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

    with st.container():
        st.subheader(m)

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{m1}", unsafe_allow_html=True)
            value_m1 = col2.selectbox("Seçin", options, key="m1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{m2}", unsafe_allow_html=True)
            value_m2 = col2.selectbox("Seçin", options, key="m2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{m3}", unsafe_allow_html=True)
            value_m3 = col2.selectbox("Seçin", options, key="m3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{m4}", unsafe_allow_html=True)
            value_m4 = col2.selectbox("Seçin", options, key="m4")

        cevaplari_kontrol_et(value_m1, value_m2, value_m3, value_m4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

    with st.container():
        st.subheader(n)

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{n1}", unsafe_allow_html=True)
            value_n1 = col2.selectbox("Seçin", options, key="n1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{n2}", unsafe_allow_html=True)
            value_n2 = col2.selectbox("Seçin", options, key="n2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{n3}", unsafe_allow_html=True)
            value_n3 = col2.selectbox("Seçin", options, key="n3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{n4}", unsafe_allow_html=True)
            value_n4 = col2.selectbox("Seçin", options, key="n4")

        cevaplari_kontrol_et(value_n1, value_n2, value_n3, value_n4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

    with st.container():
        st.subheader(o)

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{o1}", unsafe_allow_html=True)
            value_o1 = col2.selectbox("Seçin", options, key="o1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{o2}", unsafe_allow_html=True)
            value_o2 = col2.selectbox("Seçin", options, key="o2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{o3}", unsafe_allow_html=True)
            value_o3 = col2.selectbox("Seçin", options, key="o3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{o4}", unsafe_allow_html=True)
            value_o4 = col2.selectbox("Seçin", options, key="o4")

        cevaplari_kontrol_et(value_o1, value_o2, value_o3, value_o4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)

    with st.container():
        st.subheader(p)

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{p1}", unsafe_allow_html=True)
            value_p1 = col2.selectbox("Seçin", options, key="p1")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{p2}", unsafe_allow_html=True)
            value_p2 = col2.selectbox("Seçin", options, key="p2")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{p3}", unsafe_allow_html=True)
            value_p3 = col2.selectbox("Seçin", options, key="p3")

        st.markdown("<div class='row-divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([9, 1])
        with col1.container():
            col1.markdown(f"{p4}", unsafe_allow_html=True)
            value_p4 = col2.selectbox("Seçin", options, key="p4")

        cevaplari_kontrol_et(value_p1, value_p2, value_p3, value_p4)
        st.markdown("<div class='content-container'></div>", unsafe_allow_html=True)


def dosya_olustur():
    global dosya_adi
    document = Document()

    section = document.sections[0]
    footer = section.footer
    paragraph = footer.paragraphs[0]
    paragraph.text = "\tSakarya Üniversitesi Kariyer ve Yetenek Yönetimi Koordinatörlüğü"
    paragraph.style = document.styles["Header"]

    document.add_heading(ad_soyad.title(), 0)
    p = document.add_paragraph()
    p.add_run("Doldurulma tarihi").bold = True
    p.add_run(f": {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}").italic = True

    document.add_heading("A. Kişisel Bilgiler", level=1)

    p = document.add_paragraph()
    p.add_run("Mesleği").bold = True
    p.add_run(f": {meslek}").italic = True

    p = document.add_paragraph()
    p.add_run("Ünvanı").bold = True
    p.add_run(f": {unvan}").italic = True

    p = document.add_paragraph()
    p.add_run("Bölümü").bold = True
    p.add_run(f": {bolum}").italic = True

    p = document.add_paragraph()
    p.add_run("Yaş").bold = True
    p.add_run(f": {yas}").italic = True

    p = document.add_paragraph()
    p.add_run("Cinsiyet").bold = True
    p.add_run(f": {cinsiyet}").italic = True

    p = document.add_paragraph()
    p.add_run("Mail").bold = True
    p.add_run(f": {mail}").italic = True

    document.add_heading("B. Analiz Sonuçları", level=1)

    gorseli_olustur()
    document.add_picture('gradient.png')

    p = document.add_paragraph()
    p.add_run("Buraya analiz gelecek.").italic = True

    erid = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))

    p = document.add_paragraph()
    p.add_run(resimle_ilgili_not).italic = True

    p = document.add_paragraph()
    p.add_run("ERID: ").bold = True
    p.add_run(f"{erid}").italic = True

    dosya_adi = f"{ad_soyad.title()}-{erid}.docx"
    document.save(dosya_adi)


def kontrol_butonu():
    if st.button("Envanteri Kaydet"):
        # ad_soyad, meslek, unvan, bolum, yas, cinsiyet, mail, telefon
        with st.empty():
            st.success("Analiz oluşturuluyor...")
            dosya_olustur()
            st.success("Analiz oluşturuldu! Kaydediliyor...")
            dosyayi_kaydet()
            st.success("Analiz Kaydedildi, kariyer@sakarya.edu.tr üzerinden bizimle iletişime geçebilirsiniz.")
        st.balloons()


def dosyayi_kaydet():
    global dosya_adi
    gauth = GoogleAuth()
    create_cred_file()

    gauth.LoadCredentialsFile('mycreds_test.txt')

    drive = GoogleDrive(gauth)
    folderName = 'RenkveKelimeTesti'  # Please set the folder name.
    file_name = dosya_adi
    folders = drive.ListFile(
        {
            'q': "title='" + folderName + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    for folder in folders:
        if folder['title'] == folderName:
            file2 = drive.CreateFile({'parents': [{'id': folder['id']}]})
            file2.SetContentFile(file_name)
            file2.Upload()


def create_cred_file():
    cred_str = '{"access_token": "' + st.secrets["access_token"] +\
               '", "client_id": "' + st.secrets["client_id"] +\
               '", "client_secret": "' + st.secrets["client_secret"] + \
               '", "refresh_token": "' + st.secrets["refresh_token"] + \
               '", "token_expiry": "' + st.secrets["token_expiry"] + \
               '", "token_uri": "' + st.secrets["token_uri"] + \
               '", "user_agent": null' + \
               ', "revoke_uri": "' + st.secrets["revoke_uri"] + \
               '", "id_token": null' + \
               ', "id_token_jwt": null' + \
               ', "token_response": {"access_token": "' + st.secrets["token_response"]["access_token"] + \
               '", "expires_in": ' + str(st.secrets["token_response"]["expires_in"]) + \
               ', "refresh_token": "' + st.secrets["token_response"]["refresh_token"] + \
               '", "scope": "' + st.secrets["token_response"]["scope"] + \
               '", "token_type": "' + st.secrets["token_response"]["token_type"] + \
               '"}, "scopes": ["https://www.googleapis.com/auth/drive"]' + \
               ', "token_info_uri": "' + st.secrets["token_info_uri"] + \
               '", "invalid": false' + \
               ', "_class": "' + st.secrets["_class"] + \
               '", "_module": "' + st.secrets["_module"] + '"}'
    text_file = open("mycreds_test.txt", "w")
    text_file.write(cred_str)
    text_file.close()


def gorseli_olustur():
    global resimle_ilgili_not
    total_1 = int(value_a1) + int(value_b1) + int(value_c1) + int(value_d1) + int(value_e1) + int(value_f1) + \
              int(value_g1) + int(value_h1) + int(value_i1) + int(value_j1) + int(value_k1) + int(value_m1) + \
              int(value_n1) + int(value_o1) + int(value_p1)
    total_2 = int(value_a2) + int(value_b2) + int(value_c2) + int(value_d2) + int(value_e2) + int(value_f2) + \
              int(value_g2) + int(value_h2) + int(value_i2) + int(value_j2) + int(value_k2) + int(value_m2) + \
              int(value_n2) + int(value_o2) + int(value_p2)
    total_3 = int(value_a3) + int(value_b3) + int(value_c3) + int(value_d3) + int(value_e3) + int(value_f3) + \
              int(value_g3) + int(value_h3) + int(value_i3) + int(value_j3) + int(value_k3) + int(value_m3) + \
              int(value_n3) + int(value_o3) + int(value_p3)
    total_4 = int(value_a4) + int(value_b4) + int(value_c4) + int(value_d4) + int(value_e4) + int(value_f4) + \
              int(value_g4) + int(value_h4) + int(value_i4) + int(value_j4) + int(value_k4) + int(value_m4) + \
              int(value_n4) + int(value_o4) + int(value_p4)

    total_names = ['kırmızı', 'sarı', 'yeşil', 'mavi']
    total = total_1 + total_2 + total_3 + total_4
    total1, total2, total3, total4 = total_1/total, total_2/total, total_3/total, total_4/total
    rational = [total1, total2, total3, total4]
    color_tone.create_gradient_image(total_names, rational, 430, 80, 'gradient.png')

    if 1 in rational:
        resimle_ilgili_not = "* Resimle ilgili ufak bir not: Analiziniz sonucunda sadece bir renk çıktı. Ancak " \
                             "bu demek değildir ki sadece bir renk ifade ediyorsunuz. Hayatta her şey siyah veya " \
                             "beyaz olmadığı gibi, tek renk de değildir. Sadece bir renk çıksanız bile, bu rengin " \
                             "birçok tonu olduğunu unutmayın."
    else:
        resimle_ilgili_not = "* Resimle ilgili ufak bir not: Analiziniz sonucunda birkaç renk çıktı. Ancak " \
                             "bu demek değildir ki sadece birkaç renk ifade ediyorsunuz. Hayatta her şey siyah veya " \
                             "beyaz olmadığı gibi, sadece birkaç renk de değildir. Sadece birkaç renk çıksanız bile, " \
                             "bu renklerin birçok tonu olduğunu unutmayın. Bu görsel için toplam dağılımın envanter " \
                             "sonucunuzdan elde edildi. ("
        for r, n in zip(rational, total_names):
            if r != 0:
                resimle_ilgili_not += f" %{str(round(r*100))} {n}"
        resimle_ilgili_not += ")"

def versiyon():
    st.caption("""
                <p style='text-align: center;'>
                ver 1.0.0
                </p>
            """, unsafe_allow_html=True
               )
