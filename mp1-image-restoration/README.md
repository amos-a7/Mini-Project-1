# Mini Project 1 — Image Restoration: Lena

Repositori ini berisi implementasi manual pengolahan citra menggunakan pustaka NumPy di Python untuk merestorasi citra "Lena" yang mengalami degradasi berupa *low contrast*, *Gaussian noise*, *salt-and-pepper noise*, dan *blur*. Proyek ini disusun untuk memenuhi tugas mata kuliah Pengolahan Citra dan Video.

---

## 1. Identitas
* **Nama:** Amos Harol Turnip
* **NRP:** 5024241023
---

## 2. Penjelasan Pipeline Restorasi

Sesuai dengan batasan tugas, seluruh proses *filtering*, *histogram*, dan transformasi diimplementasikan secara **manual menggunakan NumPy** tanpa menggunakan fungsi *processing* bawaan dari OpenCV. 

Berikut adalah urutan *pipeline* yang digunakan beserta alasannya:

1. **Denoising 1: Median Filter (Kernel 3x3)**
   * **Tujuan:** Menghilangkan *salt-and-pepper noise*.
   * **Alasan:** Median filter sangat efektif untuk mengatasi *impulse noise* (titik hitam/putih ekstrem) tanpa merusak garis tepi (*edges*) gambar. Ukuran kernel 3x3 dipilih agar tekstur asli citra (seperti bulu pada topi) tidak ikut terhapus atau menjadi terlalu *blur*.
2. **Denoising 2: Gaussian Filter (Kernel 3x3, Sigma 1.0)**
   * **Tujuan:** Menghaluskan sisa *Gaussian noise*.
   * **Alasan:** Setelah *salt-and-pepper* hilang, filter linear (Gaussian) digunakan untuk meratakan sisa bintik-bintik halus. Kernel kecil digunakan untuk menjaga ketajaman detail.
3. **Contrast Enhancement: Manual Histogram Equalization (HE)**
   * **Tujuan:** Memperbaiki rentang intensitas citra yang sempit (*low contrast*).
   * **Alasan:** HE meratakan distribusi nilai piksel. Implementasi manual ini juga menggunakan *masking* pada nilai nol untuk memastikan Cumulative Distribution Function (CDF) dinormalisasi dengan benar, sehingga gambar tidak menjadi terlalu *overexposed*.
4. **Sharpening: Unsharp Masking**
   * **Tujuan:** Mempertajam detail yang kabur akibat proses denoising dan degradasi awal.
   * **Alasan:** Dibandingkan menggunakan *Laplacian filter* yang cenderung memperkuat sisa *noise* menjadi bintik kasar, *Unsharp Masking* bekerja dengan cara menambahkan selisih detail (Citra Original - Citra Blurred) kembali ke citra aslinya. Hasilnya, tepi objek menjadi lebih tegas namun tetap natural.

---

## 3. Perbandingan Visual

| Input: Citra Rusak (Noisy) | Output: Citra Restorasi |
| :---: | :---: |
| <img src="input/lena_noisy.png" width="300" alt="Lena Noisy"> | <img src="output/lena_restored.png" width="300" alt="Lena Restored"> |


---

## 4. Analisis Singkat

* **Apa yang Berhasil (Hasil Eksperimen):** Ternyata pemilihan ukuran kernel dan urutan *filter* itu ngaruh banget. Awalnya sempat mencoba Median Filter dengan ukuran 5x5, tapi hasilnya tekstur halus (seperti pori-pori wajah dan serat topi Lena) malah ikut hilang karena terlalu *blur*. Akhirnya kernel diturunkan jadi 3x3 dan dipadukan dengan Gaussian filter ringan. 
  
  Untuk *sharpening*, awalnya mencoba filter Laplacian murni. Tapi karena citra dari awal sudah rusak dan di-HE (*Histogram Equalization*), Laplacian malah bikin sisa-sisa *noise* kecil makin menonjol (berbintik). Setelah tekniknya diganti menggunakan *Unsharp Masking* (mengurangkan citra asli dengan citra *blur*-nya), bagian tepi seperti mata dan garis topi bisa tajam tanpa merusak kehalusan kulit.

* **Apa yang Bisa Ditingkatkan:** 1. **Running Time (Performa):** Kodenya lumayan berat dan memakan waktu saat di-*run*. Karena ada aturan larangan menggunakan fungsi *built-in* dari `cv2`, proses konvolusi dan *filtering* dilakukan murni pakai *nested loop* di Python yang secara komputasi cukup lambat. Ke depannya, ini bisa dioptimasi lagi menggunakan teknik *vectorization* atau `stride_tricks` di NumPy biar eksekusinya lebih instan.
  2. **Batasan Grayscale:** Restorasi ini cuma mentok di *grayscale*. Karena citra input bawaannya (`lena_noisy.png`) di-*load* sebagai citra 1-*channel* (hitam putih), informasi warna asli RGB-nya sudah hilang dan nggak bisa diselamatkan lagi pakai metode *spatial filtering* biasa.

---

## 5. Cara Menjalankan Program

**Prasyarat:**
Pastikan Anda telah menginstal pustaka yang dibutuhkan:
```bash
pip install numpy opencv-python matplotlib
