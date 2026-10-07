# pwnsorter

[![CI](https://github.com/itsdarklikehell/pwnsorter/actions/workflows/ci.yml/badge.svg)](https://github.com/itsdarklikehell/pwnsorter/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/itsdarklikehell/pwnsorter)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

A [pwnagotchi](https://github.com/evilsocket/pwnagotchi) plugin to sort cracked
access points and their passwords from a potfile into `wpa_supplicant` config
blocks.

## What it does

`potfilesorter.py` reads a WPA-Sec potfile, extracts BSSID + password pairs, and
appends `network={...}` blocks to:

- `/etc/wpa_supplicant/wpa_supplicant.conf`
- `~/WiFiConfigStore.xml`
- `~/WiFiConfigStoreSoftAp.xml`

It skips networks already present in the config files.

## Installation

```bash
git clone https://github.com/itsdarklikehell/pwnsorter.git
cd pwnsorter
```

Copy `potfilesorter.py` to your pwnagotchi's plugins directory:

```bash
sudo cp potfilesorter.py /usr/local/lib/pwnagotchi/plugins/custom/
sudo chmod +x /usr/local/lib/pwnagotchi/plugins/custom/potfilesorter.py
```

## Usage

### Standalone

```bash
sudo python3 potfilesorter.py
```

### As a pwnagotchi plugin

Add to `config.toml`:

```toml
[plugins.potfilesorter]
enabled = true
```

## Potfile format

Expected format (WPA-Sec potfile):

```
BSSID:password:latitude:longitude
```

Download your potfile from [WPA-Sec](https://wpa-sec.stanev.org/?api&dl=1) and
place it at `/home/rizzo/wpa-sec.founds.potfile`.

## Requirements

- Python 3.8+
- Root access (writes to `/etc/wpa_supplicant/`)

## Testing

```bash
python3 -m pytest tests/ -v
```

## License

GPL-3.0 (inherits Pwnagotchi's license).

---

## Gource Visualization

De ontwikkelhistorie van dit project in een film:

<video src="https://raw.githubusercontent.com/itsdarklikehell/pwnsorter/master/gource.mp4" controls width="100%"></video>

*Hover/click voor [Telegram-optimaliseerde versie](https://raw.githubusercontent.com/itsdarklikehell/pwnsorter/master/gource_telegram.mp4) (kleiner, 1.5MB)*

*De video wordt automatisch gegenereerd door de [Gource workflow](.github/workflows/gource.yml) bij elke push.*

Lokale video genereren:
```bash
gource --max-files 1000 --key -800x600 \
  --highlight-users --filename-time 3 --output-framerate 25 \
  -s 0.6 --multi-sampling --auto-skip-seconds 0.1 \
  --stop-at-end --hide mouse,progress -o gource.ppm

ffmpeg -y -r 15 -f image2pipe -vcodec ppm -i gource.ppm \
  -vcodec libx264 -preset medium -pix_fmt yuv420p \
  -crf 1 -threads 0 -bf 0 gource.mp4
```
