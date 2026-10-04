# 🔥 SHIMUL SNI FINDER

Android (Termux) ar Linux er jonno SNI / Host finder toolkit. Duita version ek jaygay, **ek command e install**, ar **ek menu theke switch**.

| Version | File | Kaj |
|---|---|---|
| **V5** | `shimul.py` | SHIMUL V1, 12 ta option |
| **V6** | `shimul2.py` | SHIMUL V2, notun UI, 9 ta option |

---

## ⚡ One Click Install

### Termux

```bash
pkg install -y git && git clone https://github.com/Hackershimul07/shimul-sni.git && cd shimul-sni && bash install.sh
```

Install shesh hole eta type koro:

```bash
shimul
```

### Ubuntu / Debian / Kali

```bash
sudo apt update && sudo apt install -y git
git clone https://github.com/Hackershimul07/shimul-sni.git
cd shimul-sni && bash install.sh
```

---

## 🚀 Kivabe Chalabe

| Command | Ki kore |
|---|---|
| `shimul` | **Switch menu** — V5 / V6 choose koro |
| `shimul1` | Direct **V5** |
| `shimul2` | Direct **V6** |

Switch menu te:

```
1. SHIMUL V1   (shimul.py)
2. SHIMUL V2   (shimul2.py)
0. EXIT
```

Tool er vitore **Exit** dile abar switch menu te ferot ashe, tai terminal restart chhara V5 ↔ V6 jaoya jay.

> Command na pele: `bash switch.sh`

---

## 📦 Installer ki ki install kore

`install.sh` environment auto-detect kore (Termux / apt / dnf / pacman / apk).

**System package (Termux):**
`python` `python-pip` `clang` `make` `cmake` `binutils` `pkg-config` `libffi` `openssl` `openssl-tool` `libcurl` `curl` `wget` `libxml2` `libxslt` `zlib` `libjpeg-turbo` `ncurses-utils` `dnsutils` `git` `zip` `unzip` `nano` `termux-api` `termux-tools`

**Python package:**
`aiohttp` `requests` `beautifulsoup4` `colorama` `tqdm` `termcolor` `pyperclip` `websocket-client` `dnspython` `multithreading` + optional `pycurl`

**Extra jinis:**
- ✅ Install er por sob module **verify** kore
- ✅ `MultiThreadRequest` na pele compatible module auto banay
- ✅ Ekta package fail korleo baki gulo install hoy
- ✅ `shimul`, `shimul1`, `shimul2` shortcut banay

Abar chalale shudhu missing gulo update/install hoy:

```bash
bash install.sh
```

---

## 🧰 Tools

### V5 (`shimul.py`)
IP Scanner (CIDR) · Reverse IP · Subdomain Generator · File.txt Scanner · Proxy Scanner · Domain Extractor · Custom Port Scanner · Unlimited No-Freeze Scanner · Domain Finder (any country) · Anti-DPI Scanner · DNS Resolver file creator

### V6 (`shimul2.py`)
IP CIDR Scanner (custom port) · Reverse IP · Subdomain Scanner · File.txt Scanner · Proxy Scanner · No-Freeze Scanner (hostname IP format) · Domain Scanner · DNS Resolver file creator · SSH+SNI Direct Scanner (port 443)

Sob option e `back` type korle main menu te ferot jay.

---

## 📁 Result file

Tool jei folder theke chalabe, result oikhanei save hoy:

| Version | Default result file |
|---|---|
| V5 | `V4.txt` |
| V6 | `V6.txt` |

Phone storage e save korte chaile ekbar:

```bash
termux-setup-storage
```

---

## 🔄 Update

```bash
cd shimul-sni && git pull && bash install.sh
```

---



## 🛠️ Problem hole

| Problem | Fix |
|---|---|
| `shimul: command not found` | `bash switch.sh` cholao |
| Linux e shortcut kaj kore na | `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc` |
| Package install fail | `bash install.sh` abar cholao, log: `cat ~/.cache/shimul_pip.log` |
| `pycurl` fail | Optional, shudhu "FILE.TXT SCANNER" kaj korbe na |
| Clipboard kaj kore na | Termux:API app install koro |

---

## ⚠️ Disclaimer

Ei tool shudhu **nijer network ba jar permission ache** tar jonno use koro. Onner network e scan korle ei'r responsibility user er.

---

## 📬 Contact

Telegram: [@shimul00889](https://t.me/shimul00889)
