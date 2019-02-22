# XRPL-monitor-ESP32
XRPL monitor is a micropython script to monitor the XRP Ledger volume and price through a ESP32 board with a 2.4" screen attached. 

![Imgur](https://i.imgur.com/i0DS0fm.jpg)

![Imgur](https://i.imgur.com/zkVikQz.jpg)

# Hardware
You will need the following hardware or equivalent (15$ approx plus shipping costs if they apply):

* A ESP32 board like the [Wemos Lolin D32 PRO](https://www.aliexpress.com/item/LOLIN-D32-Pro-V2-0-0-wifi-bluetooth-board-based-ESP-32-esp32-Rev1-ESP32-WROVER/32883116057.html?spm=2114.search0104.3.2.1a8273cabbu9ri&ws_ab_test=searchweb0_0,searchweb201602_4_10065_10068_10547_319_10891_317_10548_10696_10084_453_454_10083_10618_10307_10820_10821_10301_10303_537_536_10902_10059_10884_10887_321_322_10103,searchweb201603_57,ppcSwitch_0&algo_expid=e5ac4c33-9e09-4534-bb6c-90b82a0f0790-0&algo_pvid=e5ac4c33-9e09-4534-bb6c-90b82a0f0790&transAbTest=ae803_4) (8.8$ - I used the 4MB-flash one)

* A [2.4" TFT display](https://www.aliexpress.com/store/product/TFT-2-4-Touch-Shield-V1-0-0-for-LOLIN-WEMOS-D1-mini-2-4-inch/1331105_32919729730.html?spm=a2g1y.12024536.productList_2500252.subject_0) (5.9$)

* A [display cable](https://www.aliexpress.com/store/product/TFT-Cable-10P-200mm-20cm-for-WEMOS-SH1-0-10P-double-head-cable/1331105_32848833474.html?spm=a2g1y.12024536.productList_2559252.subject_1) to connect both (0.8$)


# Installation instructions

## Install Loboris' Micropython firmware

Loboris has a wiki[ a wiki](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/build)  with complete instructions to build and/or install its firmware. The following is a shortened version for Linux only:

* Download or clone[ Loboris' MicroPython firmware for the ESP32 ](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo), and unzip it.

* Open a terminal and change directory to the firmware's location: 
```cd .../MicroPython_ESP32_psRAM_LoBo-master/MicroPython_BUILD/firmware/esp32_psram_all_bt/```


* Plug the board to your computer's USB port, and get your device location (usually /dev/ttyUSB0):
```ls /dev/ttyUSB*```

* Flash the firmware:
```../flash.sh -p dev/ttyUSB0```

## Install XRPL monitor

* Clone or download this repository, unzip it and and change directory to your extracted copy.

* Edit the file **boot.py** to set your wifi ESSID (the network's name) and its password instead of < WIFI_ESSID > and < WIFI_PASSWORD >.

* Install rshell (you'll need the python3-pip package):
```sudo pip3 install rshell```

* Reset your ESP32 device with the reset button, and connect into it with rshell:
```rshell --buffer-size=30 -p /dev/ttyUSB0``` 

* Copy the needed files into the ESP32: *boot.py, consola18.fon, RippleDataAPI.py, xrp.jpg, xrp_basic.jpg and XRPLmonitor.py*
```cp <file_name> /pyboard/flash```

* Reset your ESP32 device
