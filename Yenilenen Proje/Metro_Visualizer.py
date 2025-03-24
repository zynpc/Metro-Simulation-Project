import networkx as nx
import matplotlib.pyplot as plt

def draw_metro_graph():
    # Graf oluşturma
    G = nx.Graph()

    # İstasyonlar ve hatları
    stations = {
        "K1": ("Kızılay", "Kırmızı Hat"),
        "K2": ("Ulus", "Kırmızı Hat"),
        "K3": ("Demetevler", "Kırmızı Hat"),
        "K4": ("OSB", "Kırmızı Hat"),
        "M1": ("AŞTİ", "Mavi Hat"),
        "M2": ("Kızılay", "Mavi Hat"),
        "M3": ("Sıhhiye", "Mavi Hat"),
        "M4": ("Gar", "Mavi Hat"),
        "T1": ("Batıkent", "Turuncu Hat"),
        "T2": ("Demetevler", "Turuncu Hat"),
        "T3": ("Gar", "Turuncu Hat"),
        "T4": ("Keçiören", "Turuncu Hat"),
    }

    # Bağlantılar ve mesafeleri
    connections = [
        ("K1", "K2", 4), ("K2", "K3", 6), ("K3", "K4", 8),
        ("M1", "M2", 5), ("M2", "M3", 3), ("M3", "M4", 4),
        ("T1", "T2", 7), ("T2", "T3", 9), ("T3", "T4", 5),
        ("K1", "M2", 2), ("K3", "T2", 3), ("M4", "T3", 2)
    ]

    # Düğümler ve bağlantıları ekleme
    for key, (name, line) in stations.items():
        G.add_node(key, label=name, line=line)

    for u, v, weight in connections:
        G.add_edge(u, v, weight=weight)

    # Renkler
    line_colors = {
        "Kırmızı Hat": "red",
        "Mavi Hat": "blue",
        "Turuncu Hat": "orange",
    }

    edge_colors = []
    for u, v in G.edges:
        if stations[u][1] == stations[v][1]:
            edge_colors.append(line_colors[stations[u][1]])
        else:
            edge_colors.append("gray")

    # Çizim için konumlar
    pos = nx.spring_layout(G, seed=42)

    # Düğümler
    labels = {key: f"{stations[key][0]} ({key})" for key in stations}
    nx.draw(G, pos, labels=labels, node_size=600, node_color='lightgray', edge_color=edge_colors, font_size=8)

    # Ağırlıklar
    edge_labels = {(u, v): f"{d['weight']}dk" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

    plt.title("Metro Hattı Şeması")
    plt.show()
