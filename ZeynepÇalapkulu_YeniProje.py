from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional
import random

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.maks_kapasite = 100
        self.mevcut_yolcu = 0
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

    def kapasite_guncelle(self, yeni_yolcu_sayisi: int):
        self.mevcut_yolcu = max(0, min(yeni_yolcu_sayisi, self.maks_kapasite))
         

    def renk_durumu(self):
        """İstasyonun yoğunluğuna göre renk durumunu döndürür"""
        oran = self.mevcut_yolcu / self.maks_kapasite
        if oran < 0.5:
            return '🟢'  # Yeşil: %50'den az yoğunluk
        elif oran < 0.8:
            return '🟡'  # Sarı: %50 - %80 yoğunluk
        else:
            return '🔴'  # Kırmızı: %80 ve üstü yoğunluk   
                
    def tahmini_bekleme_süresi(self):
        """İstasyonun yoğunluğuna göre bekleme süresi hesaplar"""
        renk = self.renk_durumu()
        if renk == "🟢":
            bekleme_süresi = random.randint(1, 2)  # 1-2 dakika
        elif renk == "🟡":
            bekleme_süresi = random.randint(2, 4)  # 2-4 dakika
        else:
            bekleme_süresi = random.randint(4, 7)  # 4-7 dakika
        return bekleme_süresi
    
class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def yoğunluk_durumu(self,istasyonlar: List[Istasyon]):
        # Tüm istasyonları dolaşarak her bir istasyonun yoğunluk oranını hesaplar ve renk durumunu gösterir.
        for istasyon in istasyonlar:
           # Mevcut yolcu sayısının maksimum kapasiteye oranı hesaplanır.
           oran = istasyon.mevcut_yolcu / istasyon.maks_kapasite
           # İstasyonun renk durumu, adını ve yoğunluk oranını yüzde formatında ekrana yazdırır.
           print(f"{istasyon.renk_durumu()} {istasyon.ad}: {istasyon.mevcut_yolcu}/{istasyon.maks_kapasite} ({oran*100:.2f}%) Tahmini bekleme süresi: {istasyon.tahmini_bekleme_süresi()} dk")

    
    
    def rastgele_yogunluk_olustur(self,istasyonlar: List[Istasyon]):
        # Burada rastgele yoğunluk oluşturma işlemleri yapılacak
        for istasyon in istasyonlar:
            yeni_yolcu = random.randint(0, istasyon.maks_kapasite)
            istasyon.kapasite_guncelle(yeni_yolcu)
        self.yoğunluk_durumu(istasyonlar)


    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) :
        # Başlangıç ve hedef istasyonlarının geçerli olup olmadığını kontrol et
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        # Başlangıç ve hedef istasyonlarını al
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        # BFS kuyruğunu başlat: (istasyon, yol)
        kuyruk=deque([(baslangic, [baslangic])])
        # Ziyaret edilen istasyonları takip et
        ziyaret_edildi = {baslangic} 

        # Kuyruk boşalana kadar devam et
        while kuyruk:
             # Kuyruktan bir istasyon ve yol al
            mevcut_istasyon,yol = kuyruk.popleft()

            # Hedef istasyona ulaşıldıysa, yolu döndür
            if mevcut_istasyon==hedef:
                # Yolu rastgele yoğunluk oluşturma metoduna gönder
                self.rastgele_yogunluk_olustur(yol)
                return yol
            
            # Komşu istasyonları ziyaret et
            for komsu, sure in mevcut_istasyon.komsular:
                if komsu not in ziyaret_edildi: # Komşu daha önce ziyaret edilmediyse
                    ziyaret_edildi.add(komsu)  # Komşuyu ziyaret edilmiş olarak işaretle
                    kuyruk.append((komsu,yol + [komsu]))  # Komşuyu kuyruğa ekle ve yolunu güncelle

        # Eğer hedefe ulaşamadıysak, None döndür            
        return None



    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) :
        # Başlangıç ve hedef istasyonlarının geçerli olup olmadığını kontrol et
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        # Başlangıç ve hedef istasyonlarını al
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        # Ziyaret edilen istasyonları takip et
        ziyaret_edildi = set()

        # Öncelikli kuyruk (heap), her eleman (f(n), id, istasyon, yol)
        # f(n) = g(n) + h(n) ama burada h(n) = 0, o yüzden f(n) sadece g(n)'dir (yani toplam süre)
        pq = [(0, id(baslangic), baslangic, [baslangic])]
        heapq.heapify(pq) # Kuyruğu bir öncelikli kuyruğa dönüştürür

        # Kuyruk boşalana kadar devam et
        while pq:
            # En az süreye sahip istasyonu çıkar
            gn,_,mevcut_istasyon,yol=heapq.heappop(pq) 

            # Hedef istasyona ulaşıldıysa, yolu ve süreyi döndür
            if mevcut_istasyon==hedef:
                return yol,gn
            
            # Eğer mevcut istasyon daha önce ziyaret edilmediyse, ziyaret et
            if mevcut_istasyon not in ziyaret_edildi:
                ziyaret_edildi.add(mevcut_istasyon)

            # Komşu istasyonları kontrol et
            for komsu,sure in mevcut_istasyon.komsular:
               if komsu not in ziyaret_edildi:  # Komşu daha önce ziyaret edilmediyse
                   fn =gn+sure  # f(n) = g(n) + h(n), burada h(n) = 0 olduğu için sadece g(n) hesaplanır
                   # Komşu istasyonu, mevcut yol ile birlikte öncelikli kuyruğa ekle
                   heapq.heappush(pq, (fn, id(komsu), komsu, yol + [komsu])) 
                   
        # Eğer hedefe ulaşamadıysak, None döndür            
        return None
    
    # Alternatif rota bulmak için BFS (Breadth-First Search) algoritması kullanılır.
    # Yoğunluğu kırmızı olmayan istasyonlar üzerinden hedefe ulaşmaya çalışır.
    def alternatif_rota_bul(self, baslangic_id: str, hedef_id: str):
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        kuyruk = deque([(baslangic, [baslangic])]) # Kuyrukta başlangıç istasyonu ve mevcut yol tutulur.
        ziyaret_edildi = {baslangic} # Ziyaret edilen istasyonlar takip edilir.

        while kuyruk:
            mevcut_istasyon, yol = kuyruk.popleft()
            # Hedef istasyona ulaşıldığında mevcut yol döner.
            if mevcut_istasyon == hedef:
                return yol
            # Komşu istasyonlar kontrol edilir.
            for komsu, sure in mevcut_istasyon.komsular:
                # Kırmızı yoğunlukta olmayan ve daha önce ziyaret edilmemiş komşu istasyonlar eklenir.
                # Ancak hedef istasyon kırmızı olsa bile dahil edilir.
                if komsu not in ziyaret_edildi and komsu.renk_durumu() != '🔴' or komsu==hedef:
                    ziyaret_edildi.add(komsu)
                    kuyruk.append((komsu, yol + [komsu]))

        return None

    def alternatif_yol_onayi(self, baslangic_id: str, hedef_id: str) -> None:
        
        print(f"Alternatif rota bulunmaya çalışılıyor...")
        alternatif_yol = self.alternatif_rota_bul(baslangic_id, hedef_id)
        if alternatif_yol:
            print(f"Alternatif rota: {' -> '.join(i.ad for i in alternatif_yol)}")
        else:
            print("Alternatif yol bulunamadı.")


    # Başlangıç ve hedef istasyonları dışında kırmızı yoğunlukta istasyon olup olmadığını kontrol eder.
    # Varsa kullanıcıdan alternatif rota isteyip istemediğini sorar.    
    def kırmızı_var_mı(self,istasyonlar: List[Istasyon],baslangic_id: str, hedef_id: str):
        sayı=0
        # Her istasyonun yoğunluk durumunu kontrol eder.
        for istasyon in istasyonlar:
            # Başlangıç ve hedef istasyonları hariç kırmızı yoğunlukta olanları sayar.
            if istasyon.renk_durumu()=='🔴'and istasyon.idx!=baslangic_id and istasyon.idx!=hedef_id :
                sayı+=1
        # Eğer kırmızı istasyon varsa kullanıcıya bilgi verilir ve alternatif rota isteyip istemediği sorulur.        
        if sayı>0:
            cevap=input(f"En az aktarmalı rota üzerinde başlangıç ve hedef istasyonları dışında {sayı} tane kırmızı yoğunlukta istasyon bulunuyor. Alternatif rota ister misiniz? Evet/Hayır\n").strip().lower()
            if cevap=="evet":
               self.alternatif_yol_onayi(baslangic_id, hedef_id) 
            elif cevap != "hayır":
                print("Geçersiz giriş. Lütfen 'Evet' veya 'Hayır' şeklinde yanıt verin.")




# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    

    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        metro.kırmızı_var_mı(rota,"M1", "K4" )
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        metro.kırmızı_var_mı(rota,"T1", "T4")

    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        metro.kırmızı_var_mı(rota,"T4", "M1")

    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota)) 

  # Senaryo 4: Kızılay'dan OSB'ye
    print("\n4. Kızılay'dan OSB'ye:")
    rota = metro.en_az_aktarma_bul("M2", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        metro.kırmızı_var_mı(rota,"M2", "K4")

    sonuc = metro.en_hizli_rota_bul("M2", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))       

   # Senaryo 5: Sıhhiye'den Demetevler'e
    print("\n5. Sıhhiye'den Demetevler'e:")
    rota = metro.en_az_aktarma_bul("M3", "K3")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        metro.kırmızı_var_mı(rota,"M3", "K3")
        
    sonuc = metro.en_hizli_rota_bul("M3", "K3")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota)) 

  # Senaryo 6: Sıhhiye'den Demetevler'e
    print("\n6. Kızılay'dan Gar'a:")
    rota = metro.en_az_aktarma_bul("K1", "T3")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        metro.kırmızı_var_mı(rota,"K1", "T3")
        
    sonuc = metro.en_hizli_rota_bul("K1", "T3")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))         

