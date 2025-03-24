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
2. Kuyruk boşalana kadar şu adımlar tekrarlanır:
   - Kuyruktan bir istasyon alınır.
   - Bu istasyonun komşuları (bağlantılı diğer istasyonlar) ziyaret edilir.
   - Ziyaret edilen komşular kuyruk yapısına eklenir.
3. Sonuç olarak, başlangıç ve hedef arasındaki en kısa yol bulunur.



### A* (A Star) Algoritması

A* algoritması, Açıklık Arama (Heuristic Search) algoritmasıdır ve BFS'ye benzer şekilde çalışırken, hedefe daha hızlı ulaşmak için bir kestirim (heuristic) kullanır. A* algoritması, yolun maliyetini ve hedefe olan tahmini mesafeyi göz önünde bulundurarak en kısa ve en hızlı rotayı seçmeye çalışır. Bu projede A*, daha optimum ve zaman açısından verimli rotalar sağlamak için kullanılmaktadır. Özellikle, istasyonlar arasındaki mesafeyi dikkate alarak, daha az maliyetli yolları tercih eder. 

**A* çalışma mantığı:**
1. Başlangıç istasyonu açık listeye eklenir.
2. İstasyonlar arasında, hem mevcut mesafe (gerçek mesafe) hem de hedef istasyona olan tahmini mesafe (heuristic) dikkate alınarak en düşük toplam maliyetli (gerçek mesafe + tahmini mesafe) istasyon seçilir.
3. Bu süreç, hedef istasyona ulaşana kadar devam eder.

### Neden Bu Algoritmalar Kullanıldı?

-BFS algoritması, minimum aktarma sayısını garanti ederken, A* algoritması daha kısa ve verimli yolları bulma konusunda katkı sağlar. Bu iki algoritma birlikte, projenin temel hedefi olan en hızlı ve en az aktarmalı rotaları bulma amacına güçlü bir şekilde hizmet eder.

-Her iki algoritma, metro ağı gibi düğümler ve kenarlardan oluşan sistemlerde performans ve doğruluk açısından etkili çözümler sunar.


### Örnek Kullanım ve Test Sonuçları
![image](https://github.com/user-attachments/assets/e6e73976-5e7c-4f75-9746-1e57a22f740b)

![Ekran Görüntüsü (1452)](https://github.com/user-attachments/assets/9dbbfd8f-ede9-4f68-8f90-b0a454f2d890)


### Projeyi Geliştirme Fikirleri

- Kullanıcıların metro ağı üzerinde rahatça gezinmesini sağlamak için görsel bir arayüz geliştirmek.
- Her istasyonun kapasitesine göre kapasite aşımını analiz etmek.
- Metro hattında bakım çalışmaları, arızalar veya acil durumlar olduğunda, anında kullanıcıları bilgilendiren bir sistem oluşturma.



