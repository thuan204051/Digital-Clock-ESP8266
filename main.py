import network
import ntptime
import time
import urequests
import urandom
import gc
from machine import Pin, I2C, WDT
import ssd1306

gc.collect()

SSID = "YOUR_WIFI"
PASSWORD = "YOUR_PASSWORD"

ap = network.WLAN(network.AP_IF)
ap.active(False)

i2c = I2C(scl=Pin(YOUR_SCL), sda=Pin(YOUR_SDA))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

wdt = WDT()

def glitch_boot():

    oled.fill(0)

    # ===== TEXT =====
    text = "SYSTEM BOOT"
    x_text = (128 - len(text) * 8) // 2
    oled.text(text, x_text, 18)

    # ===== BAR =====
    bar_w = 100
    bar_h = 10
    bar_x = (128 - bar_w) // 2
    bar_y = 38

    inner_w = bar_w - 2
    inner_h = bar_h - 2

    # Vẽ khung 1 lần
    oled.rect(bar_x, bar_y, bar_w, bar_h, 1)

    # Cắt góc giả bo
    oled.pixel(bar_x, bar_y, 0)
    oled.pixel(bar_x+bar_w-1, bar_y, 0)
    oled.pixel(bar_x, bar_y+bar_h-1, 0)
    oled.pixel(bar_x+bar_w-1, bar_y+bar_h-1, 0)

    oled.show()
    time.sleep(0.5)

    fast_limit = int(inner_w * 0.8)
    hold_point = int(inner_w * 0.95)

    # ===== 0 → 80% =====
    for progress in range(fast_limit):
        wdt.feed()
        oled.fill_rect(bar_x+1, bar_y+1, progress, inner_h, 1)
        oled.show()
        time.sleep(0.005)

    # ===== 80 → 100% =====
    for progress in range(fast_limit, inner_w + 1):

        wdt.feed()
        oled.fill_rect(bar_x+1, bar_y+1, progress, inner_h, 1)
        oled.show()

        # khựng tại 95%
        if progress == hold_point:
            for _ in range(20):  # giữ nhưng vẫn feed WDT
                wdt.feed()
                time.sleep(0.02)

        slowdown = (progress - fast_limit) / (inner_w - fast_limit)
        time.sleep(0.01 + slowdown * 0.04)

    # đảm bảo full
    oled.fill_rect(bar_x+1, bar_y+1, inner_w, inner_h, 1)
    oled.show()
    time.sleep(0.15)

    for _ in range(2):
        wdt.feed()
        oled.invert(1)
        oled.show()
        time.sleep(0.08)
        oled.invert(0)
        oled.show()
        time.sleep(0.08)

    oled.fill(0)
    oled.show()
    time.sleep(0.2)

glitch_boot()

font = {
    "0":[0x3C,0x66,0x6E,0x76,0x66,0x66,0x3C,0x00],
    "1":[0x18,0x38,0x18,0x18,0x18,0x18,0x7E,0x00],
    "2":[0x3C,0x66,0x06,0x1C,0x30,0x66,0x7E,0x00],
    "3":[0x3C,0x66,0x06,0x1C,0x06,0x66,0x3C,0x00],
    "4":[0x0C,0x1C,0x3C,0x6C,0x7E,0x0C,0x0C,0x00],
    "5":[0x7E,0x60,0x7C,0x06,0x06,0x66,0x3C,0x00],
    "6":[0x1C,0x30,0x60,0x7C,0x66,0x66,0x3C,0x00],
    "7":[0x7E,0x66,0x06,0x0C,0x18,0x18,0x18,0x00],
    "8":[0x3C,0x66,0x66,0x3C,0x66,0x66,0x3C,0x00],
    "9":[0x3C,0x66,0x66,0x3E,0x06,0x0C,0x38,0x00]
}

def draw_big_digit(x, y, num, scale=3):
    pattern = font[num]
    for row in range(8):
        line = pattern[row]
        for col in range(8):
            if (line >> (7 - col)) & 1:
                oled.fill_rect(
                    x + col * scale,
                    y + row * scale,
                    scale,
                    scale,
                    1
                )

def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    if not wifi.isconnected():
        wifi.connect(SSID, PASSWORD)
        timeout = 15
        while not wifi.isconnected() and timeout > 0:
            wdt.feed()
            time.sleep(1)
            timeout -= 1
    return wifi

wifi = connect_wifi()

def sync_time():
    try:
        ntptime.settime()
        return True
    except:
        return False

def get_temperature():
    try:
        url = "YOUR_API"
        r = urequests.get(url)
        data = r.json()
        r.close()
        t = data["current_weather"]["temperature"]
        return "{:.1f}".format(t).replace(".", ",")
    except:
        return "--"

if wifi.isconnected():
    sync_time()

last_sync = time.time()
last_temp_update = 0
temperature = "--"

def get_vn_time():
    return time.localtime(time.time() + 7 * 3600)

weekdays = ["Th2","Th3","Th4","Th5","Th6","Th7","CN"]
last_second = -1

while True:

    wdt.feed()
    now = time.time()

    if not wifi.isconnected():
        wifi = connect_wifi()

    if wifi.isconnected() and now - last_sync >= 300:
        if sync_time():
            last_sync = time.time()

    if wifi.isconnected() and now - last_temp_update >= 600:
        temperature = get_temperature()
        last_temp_update = now

    t = get_vn_time()

    if t[5] != last_second:
        last_second = t[5]

        oled.fill(0)
        oled.rect(0, 0, 128, 64, 1)

        # ===== GIỜ =====
        hour = "{:02d}".format(t[3])
        minute = "{:02d}".format(t[4])

        scale = 3
        digit_w = 24
        spacing = 4
        colon_w = 8

        total_width = digit_w*4 + spacing*4 + colon_w
        start_x = (128 - total_width) // 2
        y_pos = 22
        x = start_x

        for ch in hour:
            draw_big_digit(x, y_pos, ch, scale)
            x += digit_w + spacing
        digit_height = 8 * scale
        center_y = y_pos + digit_height // 2
        
        dot_size = 4
        offset = 6
        
        if t[5] % 2 == 0:
            oled.fill_rect(x+2, center_y - offset, dot_size, dot_size, 1)
            oled.fill_rect(x+2, center_y + offset - dot_size, dot_size, dot_size, 1)
        x += colon_w + spacing

        for ch in minute:
            draw_big_digit(x, y_pos, ch, scale)
            x += digit_w + spacing

        date_line = "{} {:02d}/{:02d}/{}".format(
            weekdays[t[6]], t[2], t[1], t[0]
        )
        date_x = (128 - len(date_line)*8) // 2
        oled.text(date_line, date_x, 8)

        oled.text(temperature, 4, 54)

        temp_width = len(temperature) * 8
        x_deg = 4 + temp_width + 2
        y_deg = 54

        oled.pixel(x_deg+1, y_deg, 1)
        oled.pixel(x_deg+2, y_deg, 1)
        oled.pixel(x_deg, y_deg+1, 1)
        oled.pixel(x_deg+3, y_deg+1, 1)
        oled.pixel(x_deg, y_deg+2, 1)
        oled.pixel(x_deg+3, y_deg+2, 1)
        oled.pixel(x_deg+1, y_deg+3, 1)
        oled.pixel(x_deg+2, y_deg+3, 1)

        oled.text("C", x_deg+6, 54)

        oled.show()

    time.sleep_ms(50)


