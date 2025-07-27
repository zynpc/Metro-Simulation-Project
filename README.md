# Metro-Simulation-Project

Bu proje, bir metro ağı üzerindeki istasyonlar arasındaki en hızlı ve en az aktarmalı rotaları bulmak amacıyla geliştirilmiştir. Kullanıcılar, başlangıç ve hedef istasyonları belirleyerek, bu iki istasyon arasındaki en verimli rotayı keşfedebilir. Proje, BFS (Breadth-First Search) ve A* (A-Star) algoritmalarını kullanarak hem en kısa yolu hem de aktarma sayısını minimize etmeye çalışır. 

## Kullanılan Teknolojiler ve Kütüphaneler

Bu projede kullanılan bazı teknolojiler ve kütüphaneler:

- **Python 3**: Projenin geliştirilmesinde Python programlama dili kullanılmıştır.
 
- **heapq**: A* algoritmasında kullanılan öncelik sırasını oluşturmak için kullanılan bir Python kütüphanesidir. Min-heap veri yapısı sağlar ve bu yapıyı en hızlı yolu bulmak için kullanırız.
 
- **collections**: BFS algoritmasında kullanmak için kuyruk (queue) yapısını verimli şekilde yönetmek için kullanılır.
 
- **deque**: BFS algoritmasında, istasyonları keşfederken kuyruk yapısını verimli bir şekilde kullanmak için `deque` veri yapısı kullanılmıştır. Bu veri yapısı, baştan ve sondan veri ekleme ve çıkarma işlemlerini hızlı bir şekilde yapmamıza olanak tanır.

- **defaultdict**: `defaultdict`, her anahtar için varsayılan bir değer döndüren bir `dict` türüdür. Bu, özellikle istasyonlar arasındaki komşulukları tutarken çok kullanışlıdır. `defaultdict(list)` kullanarak, her bir istasyonun komşuları için boş bir liste oluşturduk ve her yeni bağlantı eklediğimizde, bu listeye öğe ekleyebilmemizi sağladık.

- **`typing` Modülü**: Projemizde, veri türlerini belirlemek ve kodun anlaşılabilirliğini artırmak amacıyla Python'un `typing` modülünden `Dict`, `List`, `Set`, `Tuple` ve `Optional` gibi tipler kullanılmıştır.



## Algoritmaların Çalışma Mantığı

### BFS (Breadth-First Search) Algoritması

BFS, bir graf üzerindeki en kısa yolu bulmak için kullanılan bir algoritmadır. Bu proje bağlamında, BFS algoritması, en az aktarmalı rotayı bulma amacıyla tercih edilmiştir. Bu algoritma, başlangıç noktasından başlayarak her seferinde komşu düğümleri (istasyonları) keşfeder. Her adımda, önceki adımda keşfedilen tüm istasyonlar işaretlenir ve sırasıyla en yakın olanlar ziyaret edilir.

**BFS çalışma mantığı:**
1. Başlangıç istasyonu kuyruk yapısına eklenir.
   - İlk olarak, arama başlangıç istasyonundan başlar. Bu istasyon kuyruk (queue) veri yapısına eklenir.
2. Kuyruk boşalana kadar şu adımlar tekrarlanır:
   - Kuyruktan bir istasyon alınır.
   - Bu istasyonun komşuları (bağlantılı diğer istasyonlar) ziyaret edilir.
   - Ziyaret edilen komşular kuyruk yapısına eklenir.
3. Sonuç olarak, başlangıç ve hedef arasındaki en kısa yol bulunur.



### A* (A Star) Algoritması

A* algoritması, Açıklık Arama (Heuristic Search) algoritmasıdır. Bu algoritma, başlangıç noktasından hedefe en kısa ve en hızlı yolu bulmak için kestirim (heuristic) ve gerçek maliyet (g) değerlerini birleştirir.

A* algoritması, her bir noktaya ulaşmanın toplam maliyetini şu formülle hesaplar: f(n)=g(n)+h(n)

f(n) : Düğüme ulaşmanın toplam maliyeti

𝑔(n) : Başlangıçtan düğüme kadar olan gerçek maliyet

h(n) : Düğümden hedefe olan tahmini maliyet (heuristic)
                          
Bu projede A* algoritması, istasyonlar arasındaki mesafeleri ve tahmini süreleri dikkate alarak uygulanmıştır. Algoritma, daha hızlı ve optimize edilmiş rotalar sunarak yolcuların ulaşım süresini minimize etmeyi hedefler. Özellikle, istasyonlar arasındaki doğrudan mesafeyi veya ulaşım süresini kestirim fonksiyonu olarak kullanarak daha az maliyetli ve zaman açısından verimli yolları tercih eder.

**A * çalışma mantığı:**
1. Başlangıç İstasyonunun Ekleme İşlemi:
  - Başlangıç istasyonu, toplam maliyet değeri f(n)=g(n)+h(n) ile birlikte heapq (min-heap) yapısına eklenir.
  - Heapq, her zaman en düşük maliyetli düğümü çıkarmayı sağlar.
   
2. En Düşük Maliyetli İstasyonun Seçilmesi:
  - Heapq içindeki istasyonlardan f(n) değeri en düşük olan istasyon çıkartılır.

3. Komşu İstasyonların İncelenmesi:
  - Seçilen istasyonun tüm komşu istasyonları değerlendirilir.
  - Komşu istasyonun yeni maliyeti şu şekilde hesaplanır:
    g(yeni)=g(mevcut)+mesafe(mevcut,komşu)
    f(yeni)=g(yeni)+h(komşu)
    Eğer bu komşu istasyon daha düşük bir maliyetle ulaşılabiliyorsa veya daha önce keşfedilmediyse, bu maliyet güncellenir ve komşu istasyon tekrar heapq’ye eklenir.

4. Hedefe Ulaşma Kontrolü: Eğer hedef istasyon seçilen istasyon ile eşleşirse, algoritma sonlanır ve en kısa rota elde edilir.


### Neden Bu Algoritmalar Kullanıldı?

-BFS algoritması, minimum aktarma sayısını garanti ederken, A* algoritması daha kısa ve verimli yolları bulma konusunda katkı sağlar. Bu iki algoritma birlikte, projenin temel hedefi olan en hızlı ve en az aktarmalı rotaları bulma amacına güçlü bir şekilde hizmet eder.

-Her iki algoritma, metro ağı gibi düğümler ve kenarlardan oluşan sistemlerde performans ve doğruluk açısından etkili çözümler sunar.


### Örnek Kullanım ve Test Sonuçları
![image](https://github.com/user-attachments/assets/e6e73976-5e7c-4f75-9746-1e57a22f740b)

![](Yenilenen%20Proje/Output.png)





