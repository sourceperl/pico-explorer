import time
import board
import busio
import terminalio
import displayio
# from https://circuitpython.org/libraries
from adafruit_display_text import label
from adafruit_st7789 import ST7789
import adafruit_bmp280
# custom code for VL53L1x (not official support at this time)
from custom_vl53l1x import VL53L1X

# release any resources currently in use for the displays
displayio.release_displays()

# init SPI for pico explorer ST7789 display
tft_cs = board.GP17
tft_dc = board.GP16
spi_mosi = board.GP19
spi_clk = board.GP18
spi = busio.SPI(spi_clk, spi_mosi)
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(display_bus, width=240, height=240, rowstart=80, rotation=180)

# init BMP280 and VL53L1X sensor
i2c_scl = board.GP21
i2c_sda = board.GP20
i2c = busio.I2C(scl=i2c_scl, sda=i2c_sda)
bmp = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)
vl53 = VL53L1X(i2c, address=0x29)

# create the text label with built-in font
temp_txt = label.Label(terminalio.FONT, text=" ", color=0x00FF00, scale=2, x=0, y=50)
maxmin_txt = label.Label(terminalio.FONT, text=" ", color=0x00FF00, scale=2, x=0, y=75)
pres_txt = label.Label(terminalio.FONT, text=" ", color=0x00FF00, scale=2, x=0, y=150)
dist_txt = label.Label(terminalio.FONT, text=" ", color=0x00FF00, scale=2, x=0, y=175)

# add text to display with a group
group = displayio.Group()
group.append(temp_txt)
group.append(maxmin_txt)
group.append(pres_txt)
group.append(dist_txt)
display.show(group)

# main loop
t_min = 50.0
t_max = -50.0
while True:
    t = bmp.temperature
    if t > t_max:
        t_max = t
    if t < t_min:
        t_min = t
    temp_txt.text = "temp = %.2f C" % t
    maxmin_txt.text = "max:%.2f/min:%.2f" % (t_max, t_min)
    pres_txt.text = "pres = %.2f hPa" % bmp.pressure
    (d, status, status_str) = vl53.read()
    dist_txt.text = "d = %i mm (%s)" % (d, status_str)
    time.sleep(.1)
