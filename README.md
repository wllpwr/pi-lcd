# pi-lcd

## summary

This program utilizes the [rpi-lcd](https://pypi.org/project/rpi-lcd/) library to display text on a 1602 LCD hooked up with an I2C module.

There's a few things built-in already with ```subprocess``` -- ping, RPi temp and memory, and others.

## schematics

coming soon

## TODO

- server w/ threading
- ~~mute subprocess output on curl and netcat~~ (supressed with ```subprocess.DEVNULL```)
- figure out HOW TO DISABLE THE BACKLIGHT PROGRAMMATICALLY (it's so bright) if possible
- ~~break data grabs into separate file~~ (they're organized into their own class. Think it's alright.)
