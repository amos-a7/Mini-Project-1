import cv2
import numpy as np
import matplotlib.pyplot as plt


# =========================
# 1. LOAD IMAGE
# =========================
img = cv2.imread('gambar/test_image_lena_noisy.png', 0)

# =========================
# 2. MEDIAN FILTER (dari praktikum - manual)
# =========================
def median_filter(img, ksize=3):
    pad = ksize // 2
    padded = np.pad(img, pad, mode='edge')
    output = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            window = padded[i:i+ksize, j:j+ksize].flatten()
            output[i, j] = np.median(window)

    return output


# =========================
# 3. GAUSSIAN KERNEL (dari praktikum)
# =========================
def gaussian_kernel(size, sigma):
    half = size // 2
    x, y = np.mgrid[-half:half+1, -half:half+1]
    kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    return kernel / kernel.sum()


# =========================
# 4. CONVOLUTION MANUAL
# =========================
def convolve(img, kernel):
    k = kernel.shape[0]
    pad = k // 2
    padded = np.pad(img, pad, mode='edge')
    output = np.zeros_like(img, dtype=np.float32)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            region = padded[i:i+k, j:j+k]
            output[i, j] = np.sum(region * kernel)
    return output


# =========================
# 5. HISTOGRAM EQUALIZATION
# =========================
def histogram_equalization(img):
    # Hitung histogram
    hist, bins = np.histogram(img.flatten(), 256, [0,256])
    # Hitung CDF (Cumulative Distribution Function)
    cdf = hist.cumsum()
    # Normalisasi CDF ke range 0-255
    cdf_m = np.ma.masked_equal(cdf, 0)
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')
    
    return cdf[img.astype('uint8')]


# =========================
# 6. PIPELINE
# =========================

# Step 1: Median (hilangkan salt & pepper)
img_med = median_filter(img, 3)

# Step 2: Gaussian (haluskan noise)
kernel = gaussian_kernel(3, 1.0)
img_denoised = convolve(img_med, kernel)

# Step 3: Perbaiki Kontras
img_contrast = histogram_equalization(img_denoised)

img_clean = convolve(img_contrast, gaussian_kernel(7, 0.9))

# =========================
# 7. SHARPENING (Unsharp Masking Manual)
# =========================
img_blur_for_sharp = convolve(img_clean, gaussian_kernel(5, 1.0))
detail_mask = img_clean.astype(np.float32) - img_blur_for_sharp
amount = 0.8 # Atur tingkat ketajaman 

img_final = img_clean.astype(np.float32) + (amount * detail_mask)
img_final = np.clip(img_final, 0, 255).astype(np.uint8)



# =========================
# 8. VISUALISASI
# =========================
cv2.imwrite('output/lena_restored.png', img_final)

plt.figure(figsize=(12,5))

plt.subplot(1,3,1)
plt.title("Original")
plt.imshow(img, cmap='gray')
plt.axis('off')

plt.subplot(1,3,2)
plt.title("After Denoise")
plt.imshow(img_denoised, cmap='gray')
plt.axis('off')

plt.subplot(1,3,3)
plt.title("Final Result")
plt.imshow(img_final, cmap='gray')
plt.axis('off')

plt.show()
