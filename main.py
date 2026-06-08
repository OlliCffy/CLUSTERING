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
K = 4

# CENTROID YANG DIPILIH ADALAH LIST BARIS INDEX 0-3
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
		print("\n")
		print(f"CLUSTER {i+1}")
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

		centroids_baru.append(centroid_baru)

	centroids = centroids_baru
	iterasi += 1

# =========================================
# SILHOUETTE
# =========================================
def silhouette_per_cluster(features, clusters):
	hasil_cluster = []

	for cluster_idx, cluster in enumerate(clusters):
		nilai_cluster = []

		for point_idx in cluster:
			point = features[point_idx]

			# a(i)
			if len(cluster) <= 1:
				a = 0
			else:
				total = 0

				for other_idx in cluster:
					if other_idx != point_idx:
						total += euclidean(point, features[other_idx])

				a = total / (len(cluster) - 1)

			# b(i)
			b = float("inf")

			for other_cluster_idx, other_cluster in enumerate(clusters):

				if other_cluster_idx == cluster_idx:
					continue

				if len(other_cluster) == 0:
					continue

				total = 0

				for other_idx in other_cluster:
					total += euclidean(point, features[other_idx])

				avg = total / len(other_cluster)

				b = min(b, avg)

			# s(i)
			if max(a, b) == 0:
				s = 0
			else:
				s = (b - a) / max(a, b)

			nilai_cluster.append(s)

		if len(nilai_cluster) == 0:
			hasil_cluster.append(0)
		else:
			hasil_cluster.append(sum(nilai_cluster) / len(nilai_cluster))

	return hasil_cluster

silhouette_cluster = silhouette_per_cluster(features, clusters)

# =========================================
# HASIL AKHIR
# =========================================
print("\n")
print("=" * 60)
print("HASIL AKHIR CLUSTERING")
print("=" * 60)

for i in range(K):
	print("\n")
	print(f"CLUSTER {i+1}")
	print(f"Jumlah anggota : {len(clusters[i])}")
	print(f"Silhouette: {round(silhouette_cluster[i], 2)}")

	print("-" * 40)

	for idx in clusters[i]:
		print(f"- {names[idx]}")

	print("\nCentroid:")
	print(f"Motivasi Pendidik     : {round(centroids[i][0], 2)}")
	print(f"Karier Teknologi      : {round(centroids[i][1], 2)}")
	print(f"Motivasi Akademik     : {round(centroids[i][2], 2)}")
	print(f"Motivasi Eksternal    : {round(centroids[i][3], 2)}")
