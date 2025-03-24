from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

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
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
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
                return yol
            
            # Komşu istasyonları ziyaret et
            for komsu, sure in mevcut_istasyon.komsular:
                if komsu not in ziyaret_edildi: # Komşu daha önce ziyaret edilmediyse
                    ziyaret_edildi.add(komsu)  # Komşuyu ziyaret edilmiş olarak işaretle
                    kuyruk.append((komsu,yol + [komsu]))  # Komşuyu kuyruğa ekle ve yolunu güncelle

        # Eğer hedefe ulaşamadıysak, None döndür            
        return None



    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
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
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota)) 
        
  # Ek test senaryoları
  # Senaryo 4: Kızılay'dan OSB'ye
    print("\n4. Kızılay'dan OSB'ye:")
    rota = metro.en_az_aktarma_bul("M2", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M2", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))       

   # Senaryo 5: Sıhhiye'den Demetevler'e
    print("\n5. Sıhhiye'den Demetevler'e:")
    rota = metro.en_az_aktarma_bul("M3", "K3")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M3", "K3")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))            