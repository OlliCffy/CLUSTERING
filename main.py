import pandas as pd
import math
import copy

# =========================================
# LOAD DATA
# =========================================
df = pd.read_excel(r"C:\Users\ASUS\Documents\PYTHON\matfor.xlsx")

# =========================================
# AMBIL FITUR
# =========================================

# NAMA HARUS SESUAI DENGAN NAMA KOLOM DI EXCEL

# MEMBUAT LIST ANGKA PER BARIS (ORANG)
features = df[
	["Motivasi_Pendidik",
	"Karier_Teknologi",
	"Motivasi_Akademik",
	"Motivasi_Eksternal"]
].values.tolist()

# MEMBUAT LIST NAMA PER BARIS
names = df["Nama"].tolist()

# =========================================
# CENTROID AWAL
# =========================================
K = 7

# CENTROID YANG DIPILIH ADALAH LIST BARIS INDEX 0-6
centroids = copy.deepcopy(features[:K])

clusters_lama = None
iterasi = 1

# =========================================
# EUCLIDEAN
# =========================================
def euclidean(a, b):
	total = 0

	for i in range(len(a)):
		total += (a[i] - b[i]) ** 2

	return math.sqrt(total)

# =========================================
# NAMA CLUSTER
# =========================================
def nama_cluster(centroid):
	pendidik = centroid[0]
	karier = centroid[1]
	akademik = centroid[2]
	eksternal = centroid[3]

	if pendidik < 3 and karier < 3 and akademik < 3 and eksternal < 3:
		return "Motivasi Rendah"

	# KALAU (SEMUA) NILAI SAMA
	if pendidik == karier == akademik == eksternal:
		return "Motivasi Netral (Seimbang)"

	nilai_tertinggi = max(pendidik, karier, akademik, eksternal)

	# KALAU ADA YANG NILAI SAMA (BUKAN SEMUA)
	list_nilai = [pendidik, karier, akademik, eksternal]
	if list_nilai.count(nilai_tertinggi) > 1:
		return "Motivasi Campuran"

	# 1 NILAI DOMINAN
	if nilai_tertinggi == pendidik:
		return "Calon Pendidik"
	elif nilai_tertinggi == karier:
		return "Berkarir di bidang Teknologi"
	elif nilai_tertinggi == akademik:
		return "Orientasi Akademik Tinggi"
	else:
		return "Motivasi Eksternal Dominan"

# =========================================
# K-MEANS
# =========================================
for loop in range(1000):
	print("\n")
	print("=" * 60)
	print(f"ITERASI {iterasi}")
	print("=" * 60)

	clusters = [[] for _ in range(K)]

	# =====================================
	# MEMASUKAN DATA (PER ORANG) KE CLUSTER TERDEKAT
	# =====================================
	for idx, data in enumerate(features):
		distances = []

		for centroid in centroids:
			distances.append(euclidean(data, centroid))

		cluster_terdekat = distances.index(min(distances))
		clusters[cluster_terdekat].append(idx)

	# =====================================
	# TAMPILKAN CLUSTER
	# =====================================
	for i in range(K):
		nama = nama_cluster(centroids[i])

		print("\n")
		print(f"CLUSTER {i+1} : {nama}")
		print(f"Jumlah anggota : {len(clusters[i])}")

		print("-" * 40)

		for idx in clusters[i]:
			print(f"- {names[idx]}")

	# =====================================
	# TAMPILKAN CENTROID
	# =====================================
	print("\n")
	print("=" * 60)
	print("CENTROID")
	print("=" * 60)

	for i, centroid in enumerate(centroids):
		print(f"\nCluster {i+1}")

		print(f"Motivasi Pendidik     : {round(centroid[0], 2)}")
		print(f"Karier Teknologi      : {round(centroid[1], 2)}")
		print(f"Motivasi Akademik     : {round(centroid[2], 2)}")
		print(f"Motivasi Eksternal    : {round(centroid[3], 2)}")

	# =====================================
	# KONDISI BERHENTI KE-2
	# =====================================
	if clusters == clusters_lama:
		print("\n")
		print("=" * 60)
		print("ALGORITMA BERHENTI")
		print("=" * 60)

		print(f"Konvergen pada iterasi ke-{iterasi}")
		break

	clusters_lama = copy.deepcopy(clusters)

	# =====================================
	# HITUNG CENTROID BARU
	# =====================================
	centroids_baru = []

	for cluster in clusters:
		if len(cluster) == 0:
			centroids_baru.append([0, 0, 0, 0])
			continue

		centroid_baru = [0, 0, 0, 0]

		for idx in cluster:
			for j in range(4):
				centroid_baru[j] += features[idx][j]

		for j in range(4):
			centroid_baru[j] /= len(cluster)
			centroid_baru[j] = round(centroid_baru[j], 2)

		centroids_baru.append(centroid_baru)

	centroids = centroids_baru
	iterasi += 1

# =========================================
# HASIL AKHIR
# =========================================
print("\n")
print("=" * 60)
print("HASIL AKHIR CLUSTERING")
print("=" * 60)

for i in range(K):
	nama = nama_cluster(centroids[i])

	print("\n")
	print(f"CLUSTER {i+1} : {nama}")
	print(f"Jumlah anggota : {len(clusters[i])}")

	print("-" * 40)

	for idx in clusters[i]:
		print(f"- {names[idx]}")

	print("\nCentroid:")
	print(f"Motivasi Pendidik     : {round(centroids[i][0], 2)}")
	print(f"Karier Teknologi      : {round(centroids[i][1], 2)}")
	print(f"Motivasi Akademik     : {round(centroids[i][2], 2)}")
	print(f"Motivasi Eksternal    : {round(centroids[i][3], 2)}")
