#!/usr/bin/env bash
# ============================================================
#  SHIMUL SNI FINDER (shimul.py / shimul2.py) - ONE CLICK INSTALLER
#  Termux / Debian / Ubuntu / Arch / Fedora / Alpine
#  Run:  bash install.sh
# ============================================================
set -u

RED='\033[1;31m'; GRN='\033[1;32m'; YEL='\033[1;33m'; CYN='\033[1;36m'; RST='\033[0m'
info() { echo -e "${CYN}[*]${RST} $*"; }
ok()   { echo -e "${GRN}[+]${RST} $*"; }
warn() { echo -e "${YEL}[!]${RST} $*"; }
err()  { echo -e "${RED}[x]${RST} $*"; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FAILED=()

# Log file: Termux e /tmp writable na, tai TMPDIR/HOME use kori
PIP_LOG=""
for d in "${TMPDIR:-}" "$HOME/.cache" "$HOME" "$SCRIPT_DIR"; do
    [ -z "$d" ] && continue
    mkdir -p "$d" 2>/dev/null
    if ( : > "$d/shimul_pip.log" ) 2>/dev/null; then PIP_LOG="$d/shimul_pip.log"; break; fi
done
[ -z "$PIP_LOG" ] && PIP_LOG="/dev/null"

echo -e "${RED}"
echo "  ╔══════════════════════════════════════════╗"
echo "  ║   SHIMUL SNI FINDER - AUTO INSTALLER     ║"
echo "  ╚══════════════════════════════════════════╝"
echo -e "${RST}"

# ---------- 1. Environment detect ----------
IS_TERMUX=0
if [ -n "${TERMUX_VERSION:-}" ] || [ -d /data/data/com.termux/files/usr ]; then
    IS_TERMUX=1
fi

SUDO=""
if [ "$IS_TERMUX" -eq 0 ] && [ "$(id -u)" -ne 0 ]; then
    if command -v sudo >/dev/null 2>&1; then
        SUDO="sudo"
    else
        warn "root/sudo nai - system package install skip hobe, shudhu pip install hobe."
    fi
fi

PM=""
if   [ "$IS_TERMUX" -eq 1 ];              then PM="termux"
elif command -v apt-get >/dev/null 2>&1;  then PM="apt"
elif command -v dnf     >/dev/null 2>&1;  then PM="dnf"
elif command -v pacman  >/dev/null 2>&1;  then PM="pacman"
elif command -v apk     >/dev/null 2>&1;  then PM="apk"
fi
info "Environment: $([ "$IS_TERMUX" -eq 1 ] && echo Termux || echo Linux) | Package manager: ${PM:-none}"

# ---------- 2. System packages ----------
info "System packages install hocche..."
case "$PM" in
    termux)
        export DEBIAN_FRONTEND=noninteractive
        pkg update -y -o Dpkg::Options::="--force-confnew" >/dev/null 2>&1 || pkg update -y
        # Core + build tools + extras (clear command = ncurses-utils, DNS tools = dnsutils)
        for p in python python-pip clang make cmake binutils pkg-config libffi openssl openssl-tool \
                 libcurl curl wget libxml2 libxslt zlib libjpeg-turbo ncurses-utils dnsutils \
                 git zip unzip nano termux-api termux-tools; do
            pkg install -y "$p" >/dev/null 2>&1 && ok "pkg: $p" || warn "pkg: $p install hoyni (skip)"
        done
        ;;
    apt)
        $SUDO apt-get update -y >/dev/null 2>&1
        $SUDO apt-get install -y python3 python3-pip python3-venv python3-dev build-essential pkg-config \
            libcurl4-openssl-dev libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev \
            curl wget git zip unzip nano ncurses-bin dnsutils \
            || warn "kichu system package install hoyni"
        ;;
    dnf)
        $SUDO dnf install -y python3 python3-pip python3-devel gcc make pkgconf-pkg-config libcurl-devel \
            openssl-devel libffi-devel libxml2-devel libxslt-devel curl wget git zip unzip nano ncurses bind-utils \
            || warn "kichu system package install hoyni"
        ;;
    pacman)
        $SUDO pacman -Sy --noconfirm python python-pip base-devel curl wget openssl libffi libxml2 libxslt \
            git zip unzip nano ncurses bind \
            || warn "kichu system package install hoyni"
        ;;
    apk)
        $SUDO apk add --no-cache python3 python3-dev py3-pip build-base curl-dev openssl-dev libffi-dev \
            libxml2-dev libxslt-dev curl wget git zip unzip nano ncurses bind-tools \
            || warn "kichu system package install hoyni"
        ;;
esac

# ---------- 3. Python detect ----------
PY=""
for c in python3 python; do
    if command -v "$c" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ]; then
    err "Python paoya jayni! Age python install koro."
    exit 1
fi
ok "Python: $($PY --version 2>&1)"

# ---------- 4. pip helper ----------
$PY -m pip --version >/dev/null 2>&1 || $PY -m ensurepip --upgrade >/dev/null 2>&1

PIP_EXTRA=""
if $PY -m pip install --help 2>/dev/null | grep -q -- "--break-system-packages"; then
    PIP_EXTRA="--break-system-packages"
fi

info "pip upgrade hocche..."
$PY -m pip install --upgrade pip setuptools wheel $PIP_EXTRA >/dev/null 2>&1 \
    || $PY -m pip install --upgrade pip setuptools wheel >/dev/null 2>&1 \
    || warn "pip upgrade hoyni (continue korchi)"

pip_install() {
    # usage: pip_install <package> [optional]
    local pkg="$1" optional="${2:-required}"
    info "Installing ${pkg} ..."
    if $PY -m pip install --upgrade "$pkg" $PIP_EXTRA >"$PIP_LOG" 2>&1 \
       || $PY -m pip install --upgrade "$pkg" >"$PIP_LOG" 2>&1; then
        ok "${pkg} OK"
        return 0
    fi
    if [ "$optional" = "optional" ]; then
        warn "${pkg} install hoyni (optional, skip)"
    else
        err "${pkg} install hoyni  (log: $PIP_LOG)"
        FAILED+=("$pkg")
    fi
    return 1
}

# Termux e C-extension compile problem avoid korar jonno
if [ "$IS_TERMUX" -eq 1 ]; then
    export MULTIDICT_NO_EXTENSIONS=1 YARL_NO_EXTENSIONS=1 FROZENLIST_NO_EXTENSIONS=1 AIOHTTP_NO_EXTENSIONS=1
fi

# ---------- 5. Python packages ----------
REQUIRED_PKGS=(
    aiohttp
    requests
    beautifulsoup4
    colorama
    tqdm
    termcolor
    pyperclip
    websocket-client
    dnspython
    multithreading
)
for p in "${REQUIRED_PKGS[@]}"; do
    pip_install "$p"
done

# pycurl optional (option "FILE.TXT SCANNER" er jonno lagbe)
info "pycurl (optional) install hocche..."
if [ "$IS_TERMUX" -eq 1 ]; then
    export PYCURL_SSL_LIBRARY=openssl
    export LDFLAGS="-L${PREFIX:-/data/data/com.termux/files/usr}/lib"
    export CPPFLAGS="-I${PREFIX:-/data/data/com.termux/files/usr}/include"
fi
pip_install pycurl optional || warn "pycurl chara o baki sob option cholbe; shudhu 'FILE.TXT SCANNER (small file)' kaj korbe na."

# ---------- 5b. multithreading.MultiThreadRequest fallback ----------
# shimul scripts "from multithreading import MultiThreadRequest" use kore.
# PyPI package e eta na-o thakte pare, tai na pele compatible module banai.
info "multithreading.MultiThreadRequest check korchi..."
if (cd / && $PY -c "from multithreading import MultiThreadRequest" >/dev/null 2>&1); then
    ok "MultiThreadRequest already available"
else
    warn "MultiThreadRequest nai - local compatible module banacchi: $SCRIPT_DIR/multithreading.py"
    cat > "$SCRIPT_DIR/multithreading.py" <<'SHIMEOF'
# Compatible MultiThreadRequest (auto-generated by install.sh)
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

import requests

try:
    requests.packages.urllib3.disable_warnings()
except Exception:
    pass


class MultiThreadRequest:
    threads = 30
    _threads = 30

    def __init__(self, *args, **kwargs):
        self._lock = threading.Lock()
        self._success = []
        self._total = 0
        self._done = 0
        self._stop = False

    # ---- hooks (subclass override kore) ----
    def init(self):
        pass

    def complete(self):
        pass

    def get_task_list(self):
        return []

    def task(self, payload):
        pass

    def request_connection_error(self, *args, **kwargs):
        return 1

    def request_read_timeout(self, *args, **kwargs):
        return 1

    def request_timeout(self, *args, **kwargs):
        return 1

    # ---- helpers ----
    def filter_list(self, data):
        seen, out = set(), []
        for x in data or []:
            if x is None or x == "":
                continue
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    def log(self, *args):
        with self._lock:
            sys.stdout.write("\r\033[K" + " ".join(str(a) for a in args) + "\n")
            sys.stdout.flush()
            self._progress()

    def log_replace(self, *args):
        with self._lock:
            sys.stdout.write("\r\033[K" + " ".join(str(a) for a in args))
            sys.stdout.flush()

    def _progress(self):
        if self._total:
            sys.stdout.write("\r\033[K%d/%d" % (self._done, self._total))
            sys.stdout.flush()

    def task_success(self, data):
        with self._lock:
            self._success.append(data)

    def request(self, method, url, **kwargs):
        retry = kwargs.pop("retry", 1)
        kwargs.setdefault("timeout", 5)
        kwargs.setdefault("verify", False)
        for _ in range(max(1, retry)):
            try:
                return requests.request(method, url, **kwargs)
            except requests.exceptions.ConnectTimeout:
                if self.request_timeout(method, url) == 1:
                    break
            except requests.exceptions.ReadTimeout:
                if self.request_read_timeout(method, url) == 1:
                    break
            except requests.exceptions.ConnectionError:
                if self.request_connection_error(method, url) == 1:
                    break
            except Exception:
                break
        return None

    def _run_one(self, payload):
        if self._stop:
            return
        try:
            self.task(payload)
        except Exception:
            pass
        finally:
            with self._lock:
                self._done += 1
            self.log_replace("%d/%d" % (self._done, self._total))

    def start(self):
        self.init()
        tasks = list(self.get_task_list())
        self._total = len(tasks)
        self._done = 0
        workers = getattr(self, "threads", None) or getattr(self, "_threads", 30) or 30
        ex = ThreadPoolExecutor(max_workers=int(workers))
        try:
            list(ex.map(self._run_one, tasks))
        except KeyboardInterrupt:
            self._stop = True
            print("\nScan stopped by user.")
        finally:
            ex.shutdown(wait=False, cancel_futures=True)
        sys.stdout.write("\r\033[K")
        self.complete()
        return self._success
SHIMEOF
    ok "multithreading.py banano hoyeche"
fi

# ---------- 6. Verify ----------
echo
info "Verify korchi..."
$PY - <<'PYEOF'
import importlib, sys
mods = [
    ("aiohttp", True), ("requests", True), ("bs4", True), ("colorama", True),
    ("tqdm", True), ("termcolor", True), ("pyperclip", True), ("websocket", True),
    ("dns.resolver", False), ("multithreading", True), ("pycurl", False),
]
bad = []
for m, required in mods:
    try:
        importlib.import_module(m)
        print(f"  \033[1;32m✔\033[0m {m}")
    except Exception as e:
        tag = "REQUIRED" if required else "optional"
        print(f"  \033[1;31m✖\033[0m {m}  ({tag}) -> {e.__class__.__name__}")
        if required:
            bad.append(m)

# shimul scripts MultiThreadRequest class use kore (Proxy scanner)
try:
    from multithreading import MultiThreadRequest  # noqa
    print("  \033[1;32m✔\033[0m multithreading.MultiThreadRequest")
except Exception:
    print("  \033[1;33m!\033[0m multithreading.MultiThreadRequest nai -> PROXY SCANNER option kaj korbe na")

sys.exit(1 if bad else 0)
PYEOF
VERIFY_RC=$?

# ---------- 7. Launcher shortcuts ----------
if [ "$IS_TERMUX" -eq 1 ]; then
    BIN_DIR="${PREFIX:-/data/data/com.termux/files/usr}/bin"
else
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"
fi

# ---- Switch menu script (V5 <-> V6) ----
SWITCH="$SCRIPT_DIR/switch.sh"
cat > "$SWITCH" <<'SWEOF'
#!/usr/bin/env bash
# SHIMUL SWITCH - V5 (shimul.py) <-> V6 (shimul2.py)
# Use:  bash switch.sh        -> menu (script shesh hole abar menu te ferot ashe)
#       bash switch.sh 1      -> direct V5
#       bash switch.sh 2      -> direct V6
DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" 2>/dev/null || echo "${BASH_SOURCE[0]}")")" && pwd)"

RED='\033[1;31m'; GRN='\033[1;32m'; YEL='\033[1;33m'; CYN='\033[1;36m'; DIM='\033[2m'; RST='\033[0m'

PY=""
for c in python3 python; do command -v "$c" >/dev/null 2>&1 && { PY="$c"; break; }; done
[ -z "$PY" ] && { echo -e "${RED}Python nai! age bash install.sh cholao.${RST}"; exit 1; }

status() { [ -f "$DIR/$1" ] && echo -e "${GRN}READY${RST}" || echo -e "${RED}FILE NAI${RST}"; }

run_script() {
    local file="$1" name="$2"
    if [ ! -f "$DIR/$file" ]; then
        echo -e "${RED}$file paoya jayni ($DIR)${RST}"; sleep 2; return 1
    fi
    printf '\033c'
    echo -e "${CYN}>>> Starting ${name} ...${RST}"
    ( cd "$DIR" && "$PY" "$file" )
    return 0
}

if [ -n "${1:-}" ]; then
    case "$1" in
        1|v5|V5|shimul)   run_script shimul.py  "V5 (shimul.py)";  exit $? ;;
        2|v6|V6|shimul2)  run_script shimul2.py "V6 (shimul2.py)"; exit $? ;;
        *) echo "Use: $0 [1|2]"; exit 1 ;;
    esac
fi

while true; do
    printf '\033c'
    echo -e "${RED}╔══════════════════════════════════════════╗${RST}"
    echo -e "${RED}║${YEL}        SHIMUL SNI FINDER - SWITCH        ${RED}║${RST}"
    echo -e "${RED}╚══════════════════════════════════════════╝${RST}"
    echo
    echo -e "  ${YEL}1.${RST} ${CYN}V5${RST}  SHIMUL V1  ${DIM}(shimul.py)${RST}   [$(status shimul.py)]"
    echo -e "  ${YEL}2.${RST} ${CYN}V6${RST}  SHIMUL V2  ${DIM}(shimul2.py)${RST}  [$(status shimul2.py)]"
    echo -e "  ${YEL}0.${RST} ${RED}EXIT${RST}"
    echo
    echo -e "${DIM}  Tool er vitore 'Exit' dile ekhane ferot ashbe.${RST}"
    echo
    read -r -p "$(echo -e "${CYN}Select (0-2): ${RST}")" ch || exit 0
    case "$ch" in
        1) run_script shimul.py  "V5 (shimul.py)" ;;
        2) run_script shimul2.py "V6 (shimul2.py)" ;;
        0|q|Q) echo -e "${GRN}Bye!${RST}"; exit 0 ;;
        *) echo -e "${RED}Invalid choice${RST}"; sleep 1; continue ;;
    esac
    echo
    read -r -p "$(echo -e "${YEL}Enter chaple switch menu te ferot jabe...${RST}")" _ || exit 0
done
SWEOF
chmod +x "$SWITCH"
ok "Switch menu ready: $SWITCH"

make_launcher() {
    # usage: make_launcher <command-name> <switch-arg or empty>
    local name="$1" arg="${2:-}"
    cat > "$BIN_DIR/$name" <<EOF
#!/usr/bin/env bash
exec bash "$SWITCH" $arg "\$@"
EOF
    chmod +x "$BIN_DIR/$name"
}
make_launcher shimul  ""    # switch menu
make_launcher shimul1 "1"   # direct V5
make_launcher shimul2 "2"   # direct V6
ok "Commands ready:  shimul (switch menu) | shimul1 (V5) | shimul2 (V6)"
[ -f "$SCRIPT_DIR/shimul.py" ]  || warn "shimul.py install.sh er pasher folder e nai"
[ -f "$SCRIPT_DIR/shimul2.py" ] || warn "shimul2.py install.sh er pasher folder e nai"

case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *) [ "$IS_TERMUX" -eq 0 ] && warn "PATH e $BIN_DIR add koro:  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc" ;;
esac

# Termux clipboard/storage hint
if [ "$IS_TERMUX" -eq 1 ] && [ ! -d "$HOME/storage" ]; then
    warn "Phone storage access chaile ekbar cholao:  termux-setup-storage"
fi

# ---------- 8. Summary ----------
echo
if [ "$VERIFY_RC" -eq 0 ] && [ "${#FAILED[@]}" -eq 0 ]; then
    echo -e "${GRN}══════════════════════════════════════════${RST}"
    echo -e "${GRN}  ✅ SOB INSTALL COMPLETE!${RST}"
    echo -e "${GRN}══════════════════════════════════════════${RST}"
    echo -e "  Switch menu : ${CYN}shimul${RST}   (V5 / V6 choose koro)"
    echo -e "  Direct V5   : ${CYN}shimul1${RST}  (python shimul.py)"
    echo -e "  Direct V6   : ${CYN}shimul2${RST}  (python shimul2.py)"
else
    echo -e "${YEL}══════════════════════════════════════════${RST}"
    echo -e "${YEL}  ⚠ Install shesh, kintu kichu package fail:${RST}"
    for f in "${FAILED[@]:-}"; do [ -n "$f" ] && echo -e "    - ${RED}${f}${RST}"; done
    echo -e "  Log dekho: ${CYN}cat $PIP_LOG${RST}"
    echo -e "  Abar cholao: ${CYN}bash install.sh${RST}"
    echo -e "${YEL}══════════════════════════════════════════${RST}"
    exit 1
fi
