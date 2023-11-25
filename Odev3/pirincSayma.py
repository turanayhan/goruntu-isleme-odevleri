import cv2
import numpy as np


def count_rice_tanels(image):
    # Gri tonlamaya çevir
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Eşikleme uygula ve tersine çevir (beyaz pirinç tanesi, siyah diğer alanlar olsun)
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

    # Morfolojik operasyonlar uygula (iyileştirme amaçlı)
    kernel = np.ones((5, 5), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Kenarları belirleme (Canny edge detection)
    edges = cv2.Canny(morph, 50, 150)

    # Kontur tespiti
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Belirli bir boyutun altındaki nesneleri filtrele
    min_contour_area = 100  # Ayarlanabilir bir eşik değeri
    valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

    # Pirinç taneleri sayısı
    rice_count = len(valid_contours)

    # Görüntü üzerine pirinç tanelerini çiz
    image_with_contours = cv2.cvtColor(morph, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(image_with_contours, valid_contours, -1, (0, 255, 0), 2)

    # Görüntüyü göster
    cv2.imshow('Rice Image with Countours', image_with_contours)

    return rice_count


# Kamera bağlantısını başlat
cap = cv2.VideoCapture(0)  # 0, varsayılan kamerayı temsil eder

while True:
    # Kameradan bir kare al
    ret, frame = cap.read()

    # Pirinç tanelerini say
    rice_count = count_rice_tanels(frame)

    # Sonucu ekrana yazdır
    print(f"Pirinç tane sayısı: {rice_count}")

    # 'q' tuşuna basılana kadar devam et
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera bağlantısını kapat
cap.release()
cv2.destroyAllWindows()

