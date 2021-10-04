# pi-lcd

## summary

This program utilizes the [rpi-lcd](https://pypi.org/project/rpi-lcd/) library to display text on a 1602 LCD hooked up with an I2C module.

There's a few things built-in already with ```subprocess``` -- ping, RPi temp and memory, and others.

```newdisplay.py``` and ```pythoninterfacing.ino``` contain the server Python code and client Arduino code respectively.

## schematics

coming soon

## TODO

- server w/ threading (partial support. Server cannot detect if client has severed connection -- due to wireless or power loss -- and won't reconnect properly)
- ~~mute subprocess output on curl and netcat~~ (supressed with ```subprocess.DEVNULL```)
- ~~figure out HOW TO DISABLE THE BACKLIGHT PROGRAMMATICALLY (it's so bright) if possible~~ (don't believe it's possible without additional hardware... see [here](https://www.instructables.com/I2C-Backlight-Control-of-an-LCD-Display-1602-or-20/))
- ~~break data grabs into separate file~~ (they're organized into their own class. Think it's alright.)
