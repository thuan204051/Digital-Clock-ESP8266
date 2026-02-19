# ⏰ Digital Clock ESP8266 OLED

Một dự án đồng hồ kỹ thuật số chạy trên ESP8266 + màn hình OLED 128x64 (SSD1306).

Thiết kế giao diện hiện đại, có boot animation kiểu Windows, thanh progress 80% nhanh – 20% chậm, hiệu ứng flash điện tử.

---

## 🚀 Tính năng

- Boot animation
- Thanh progress Windows style (80% nhanh – 20% chậm)
- Khựng nhẹ tại 95%
- Flash điện tử khi hoàn tất
- Hiển thị giờ:phút:giây
- Tự động đồng bộ NTP (WiFi)
- Tối ưu cho ESP8266 (không reset WDT)

---

## 🛠 Phần cứng

- ESP8266 (NodeMCU / Wemos D1 Mini)
- OLED 0.96" 128x64 SSD1306 (I2C)
- Nguồn ổn định 5V (khuyến nghị >1A)

---

## 🔌 Kết nối

| OLED | ESP8266 |
|------|----------|
| VCC  | 3V3      |
| GND  | GND      |
| SCL  | D1       |
| SDA  | D2       |

- Hoặc loại mạch có sẵn màn
  
---

## 📦 Thư viện cần

- `ssd1306`
- `machine`
- `network`
- `ntptime`
- `time`
- `urequests`
- `urandom`
  
---

## 🎨 Demo

Xem ảnh demo trên Tiktok:

👉 https://www.tiktok.com/@thuanazura

---

## 💻 Cài đặt

1. Flash MicroPython cho ESP8266
2. Upload file `main.py`
3. Chỉnh WiFi trong code
4. Reset board
5. Tận hưởng 😎

---

## 🔥 Tùy chỉnh

Bạn có thể chỉnh:

- Tốc độ boot animation
- Độ rộng thanh progress
- Font chữ 8x8

---

## 📜 License

Free for personal use.
Credit nếu bạn sử dụng lại code.

---

## ❤️ Tác giả

Made with passion by [@thuanazura]

Follow TikTok để xem thêm project ESP8266:

👉 https://www.tiktok.com/@thuanazura
