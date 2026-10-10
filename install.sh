#!/usr/bin/env bash
# ============================================================
# SHIMUL SNI FINDER - ONE CLICK INSTALLER
# No git clone required
#
# Works:
#   bash install.sh
#   curl -fsSL URL/install.sh | bash
#
# Install location:
#   ~/.shimul-sni
# ============================================================

set -u

RED='\033[1;31m'
GRN='\033[1;32m'
YEL='\033[1;33m'
CYN='\033[1;36m'
RST='\033[0m'

info() { echo -e "${CYN}[*]${RST} $*"; }
ok()   { echo -e "${GRN}[+]${RST} $*"; }
warn() { echo -e "${YEL}[!]${RST} $*"; }
err()  { echo -e "${RED}[x]${RST} $*"; }

# ============================================================
# 1. INSTALL DIRECTORY
# ============================================================

SCRIPT_DIR="${SHIMUL_INSTALL_DIR:-$HOME/.shimul-sni}"
BASE_URL="${SHIMUL_BASE_URL:-https://raw.githubusercontent.com/Hackershimul07/shimul-sni/main}"

mkdir -p "$SCRIPT_DIR" 2>/dev/null || {
    err "Install directory create kora jayni: $SCRIPT_DIR"
    exit 1
}

FAILED=()

# ============================================================
# 2. LOG
# ============================================================

PIP_LOG="$SCRIPT_DIR/shimul_pip.log"

touch "$PIP_LOG" 2>/dev/null || PIP_LOG="/dev/null"

# ============================================================
# 3. BANNER
# ============================================================

echo -e "${RED}"
echo "  ╔══════════════════════════════════════════╗"
echo "  ║   SHIMUL SNI FINDER - AUTO INSTALLER     ║"
echo "  ╚══════════════════════════════════════════╝"
echo -e "${RST}"

info "Install directory: $SCRIPT_DIR"
info "Source: $BASE_URL"

# ============================================================
# 4. ENVIRONMENT DETECT
# ============================================================

IS_TERMUX=0

if [ -n "${TERMUX_VERSION:-}" ] || \
   [ -d "/data/data/com.termux/files/usr" ]; then
    IS_TERMUX=1
fi

SUDO=""

if [ "$IS_TERMUX" -eq 0 ] && [ "$(id -u)" -ne 0 ]; then
    if command -v sudo >/dev/null 2>&1; then
        SUDO="sudo"
    else
        warn "root/sudo nai - system package install skip hobe."
    fi
fi

PM=""

if [ "$IS_TERMUX" -eq 1 ]; then
    PM="termux"
elif command -v apt-get >/dev/null 2>&1; then
    PM="apt"
elif command -v dnf >/dev/null 2>&1; then
    PM="dnf"
elif command -v pacman >/dev/null 2>&1; then
    PM="pacman"
elif command -v apk >/dev/null 2>&1; then
    PM="apk"
fi

if [ "$IS_TERMUX" -eq 1 ]; then
    info "Environment: Termux | Package manager: $PM"
else
    info "Environment: Linux | Package manager: ${PM:-none}"
fi

# ============================================================
# 5. SYSTEM PACKAGES
# ============================================================

info "System packages install hocche..."

case "$PM" in

    termux)

        pkg update -y >/dev/null 2>&1 || true

        for p in \
            python \
            python-pip \
            clang \
            make \
            cmake \
            binutils \
            pkg-config \
            libffi \
            openssl \
            openssl-tool \
            libcurl \
            curl \
            wget \
            libxml2 \
            libxslt \
            zlib \
            libjpeg-turbo \
            ncurses-utils \
            dnsutils \
            zip \
            unzip \
            nano \
            termux-api \
            termux-tools
        do
            if pkg install -y "$p" >/dev/null 2>&1; then
                ok "pkg: $p"
            else
                warn "pkg: $p install hoyni - skip"
            fi
        done

        ;;

    apt)

        $SUDO apt-get update -y >/dev/null 2>&1 || true

        $SUDO apt-get install -y \
            python3 \
            python3-pip \
            python3-venv \
            python3-dev \
            build-essential \
            pkg-config \
            libcurl4-openssl-dev \
            libssl-dev \
            libffi-dev \
            libxml2-dev \
            libxslt1-dev \
            zlib1g-dev \
            curl \
            wget \
            zip \
            unzip \
            nano \
            ncurses-bin \
            dnsutils \
            || warn "Kichu system package install hoyni."

        ;;

    dnf)

        $SUDO dnf install -y \
            python3 \
            python3-pip \
            python3-devel \
            gcc \
            make \
            pkgconf-pkg-config \
            libcurl-devel \
            openssl-devel \
            libffi-devel \
            libxml2-devel \
            libxslt-devel \
            curl \
            wget \
            zip \
            unzip \
            nano \
            ncurses \
            bind-utils \
            || warn "Kichu system package install hoyni."

        ;;

    pacman)

        $SUDO pacman -Sy --noconfirm \
            python \
            python-pip \
            base-devel \
            curl \
            wget \
            openssl \
            libffi \
            libxml2 \
            libxslt \
            zip \
            unzip \
            nano \
            ncurses \
            bind \
            || warn "Kichu system package install hoyni."

        ;;

    apk)

        $SUDO apk add --no-cache \
            python3 \
            python3-dev \
            py3-pip \
            build-base \
            curl-dev \
            openssl-dev \
            libffi-dev \
            libxml2-dev \
            libxslt-dev \
            curl \
            wget \
            zip \
            unzip \
            nano \
            ncurses \
            bind-tools \
            || warn "Kichu system package install hoyni."

        ;;

    *)

        warn "Supported package manager paoya jayni."
        ;;

esac

# ============================================================
# 6. PYTHON
# ============================================================

PY=""

for c in python3 python; do
    if command -v "$c" >/dev/null 2>&1; then
        PY="$c"
        break
    fi
done

if [ -z "$PY" ]; then
    err "Python paoya jayni!"
    exit 1
fi

ok "Python: $($PY --version 2>&1)"

# ============================================================
# 7. CURL CHECK
# ============================================================

if ! command -v curl >/dev/null 2>&1; then
    err "curl paoya jayni."
    exit 1
fi

ok "curl ready"

# ============================================================
# 8. PIP
# ============================================================

if ! $PY -m pip --version >/dev/null 2>&1; then

    if $PY -m ensurepip --upgrade >/dev/null 2>&1; then
        ok "pip enabled"
    else
        warn "pip enable kora jayni."
    fi

fi

PIP_EXTRA=""

if $PY -m pip install --help 2>/dev/null | \
   grep -q -- "--break-system-packages"; then
    PIP_EXTRA="--break-system-packages"
fi

# ============================================================
# 9. PIP INSTALL FUNCTION
# ============================================================

pip_install() {

    local package="$1"
    local optional="${2:-required}"

    info "Installing $package ..."

    if $PY -m pip install \
        --disable-pip-version-check \
        --no-input \
        "$package" \
        $PIP_EXTRA \
        >"$PIP_LOG" 2>&1
    then
        ok "$package OK"
        return 0
    fi

    # Try without extra flag
    if $PY -m pip install \
        --disable-pip-version-check \
        --no-input \
        "$package" \
        >"$PIP_LOG" 2>&1
    then
        ok "$package OK"
        return 0
    fi

    if [ "$optional" = "optional" ]; then
        warn "$package install hoyni (optional)"
    else
        err "$package install hoyni"
        FAILED+=("$package")
    fi

    return 1
}

# ============================================================
# 10. TERMUX BUILD SETTINGS
# ============================================================

if [ "$IS_TERMUX" -eq 1 ]; then

    export MULTIDICT_NO_EXTENSIONS=1
    export YARL_NO_EXTENSIONS=1
    export FROZENLIST_NO_EXTENSIONS=1
    export AIOHTTP_NO_EXTENSIONS=1

    export PYCURL_SSL_LIBRARY=openssl

    export LDFLAGS="-L${PREFIX:-/data/data/com.termux/files/usr}/lib"
    export CPPFLAGS="-I${PREFIX:-/data/data/com.termux/files/usr}/include"

fi

# ============================================================
# 11. PYTHON PACKAGES
# ============================================================

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

for package in "${REQUIRED_PKGS[@]}"; do
    pip_install "$package"
done

# ============================================================
# 12. PYCURL OPTIONAL
# ============================================================

info "pycurl optional install hocche..."

pip_install pycurl optional || true

# ============================================================
# 13. MULTITHREADING FALLBACK
# ============================================================

MULTI_FILE="$SCRIPT_DIR/multithreading.py"

info "multithreading.MultiThreadRequest check korchi..."

if "$PY" -c \
"from multithreading import MultiThreadRequest" \
>/dev/null 2>&1
then

    ok "MultiThreadRequest already available"

else

    warn "MultiThreadRequest nai - compatible module create hocche."

    cat > "$MULTI_FILE" <<'PYEOF'
# ============================================================
# Compatible MultiThreadRequest
# Auto-generated by SHIMUL installer
# ============================================================

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

    def filter_list(self, data):

        seen = set()
        output = []

        for item in data or []:

            if item is None or item == "":
                continue

            if item not in seen:

                seen.add(item)
                output.append(item)

        return output

    def log(self, *args):

        with self._lock:

            sys.stdout.write(
                "\r\033[K" +
                " ".join(str(a) for a in args) +
                "\n"
            )

            sys.stdout.flush()

            self._progress()

    def log_replace(self, *args):

        with self._lock:

            sys.stdout.write(
                "\r\033[K" +
                " ".join(str(a) for a in args)
            )

            sys.stdout.flush()

    def _progress(self):

        if self._total:

            sys.stdout.write(
                "\r\033[K%d/%d" %
                (self._done, self._total)
            )

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

                return requests.request(
                    method,
                    url,
                    **kwargs
                )

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

            self.log_replace(
                "%d/%d" %
                (self._done, self._total)
            )

    def start(self):

        self.init()

        tasks = list(
            self.get_task_list()
        )

        self._total = len(tasks)
        self._done = 0

        workers = (
            getattr(self, "threads", None)
            or getattr(self, "_threads", 30)
            or 30
        )

        executor = ThreadPoolExecutor(
            max_workers=int(workers)
        )

        try:

            list(
                executor.map(
                    self._run_one,
                    tasks
                )
            )

        except KeyboardInterrupt:

            self._stop = True

            print(
                "\nScan stopped by user."
            )

        finally:

            executor.shutdown(
                wait=False,
                cancel_futures=True
            )

        sys.stdout.write("\r\033[K")

        self.complete()

        return self._success
PYEOF

    ok "multithreading.py created"

fi

# ============================================================
# 14. DOWNLOAD SHIMUL FILES
# ============================================================

download_file() {

    local url="$1"
    local output="$2"
    local name="$3"

    info "Downloading $name ..."

    rm -f "$output"

    if curl \
        -fsSL \
        --retry 3 \
        --connect-timeout 15 \
        --max-time 120 \
        "$url" \
        -o "$output"
    then

        if [ -s "$output" ]; then

            ok "$name download OK"

            return 0

        fi

    fi

    rm -f "$output"

    err "$name download failed"

    FAILED+=("$name")

    return 1
}


download_file \
    "$BASE_URL/shimul.py" \
    "$SCRIPT_DIR/shimul.py" \
    "shimul.py"

download_file \
    "$BASE_URL/shimul2.py" \
    "$SCRIPT_DIR/shimul2.py" \
    "shimul2.py"


chmod +x \
    "$SCRIPT_DIR/shimul.py" \
    "$SCRIPT_DIR/shimul2.py" \
    2>/dev/null || true

# ============================================================
# 15. VERIFY PYTHON MODULES
# ============================================================

echo

info "Python modules verify korchi..."

"$PY" <<'PYEOF'

import importlib
import sys

modules = [

    ("aiohttp", True),
    ("requests", True),
    ("bs4", True),
    ("colorama", True),
    ("tqdm", True),
    ("termcolor", True),
    ("pyperclip", True),
    ("websocket", True),
    ("dns.resolver", True),
    ("multithreading", True),
    ("pycurl", False),

]

failed = []

for module, required in modules:

    try:

        importlib.import_module(module)

        print(
            "  \033[1;32m✔\033[0m " +
            module
        )

    except Exception as e:

        label = (
            "REQUIRED"
            if required
            else "optional"
        )

        print(
            "  \033[1;31m✖\033[0m " +
            module +
            " (" + label + ")"
        )

        if required:
            failed.append(module)


try:

    from multithreading import MultiThreadRequest

    print(
        "  \033[1;32m✔\033[0m "
        "multithreading.MultiThreadRequest"
    )

except Exception:

    print(
        "  \033[1;33m!\033[0m "
        "multithreading.MultiThreadRequest "
        "available nai"
    )

sys.exit(
    1 if failed else 0
)

PYEOF

VERIFY_RC=$?

# ============================================================
# 16. CHECK SHIMUL FILES
# ============================================================

echo

info "SHIMUL files verify korchi..."

if [ -f "$SCRIPT_DIR/shimul.py" ]; then
    ok "shimul.py READY"
else
    err "shimul.py missing"
fi

if [ -f "$SCRIPT_DIR/shimul2.py" ]; then
    ok "shimul2.py READY"
else
    err "shimul2.py missing"
fi

# ============================================================
# 17. SWITCH MENU
# ============================================================

SWITCH="$SCRIPT_DIR/switch.sh"

cat > "$SWITCH" <<'SWEOF'
#!/usr/bin/env bash

# ============================================================
# SHIMUL SNI FINDER - SWITCH MENU
# ============================================================

set -u

DIR="$HOME/.shimul-sni"

RED='\033[1;31m'
GRN='\033[1;32m'
YEL='\033[1;33m'
CYN='\033[1;36m'
DIM='\033[2m'
RST='\033[0m'


PY=""

for c in python3 python; do

    if command -v "$c" >/dev/null 2>&1; then
        PY="$c"
        break
    fi

done


if [ -z "$PY" ]; then

    echo -e "${RED}Python nai!${RST}"
    exit 1

fi


status() {

    if [ -f "$DIR/$1" ]; then
        echo -e "${GRN}READY${RST}"
    else
        echo -e "${RED}FILE NAI${RST}"
    fi

}


run_script() {

    local file="$1"
    local name="$2"

    if [ ! -f "$DIR/$file" ]; then

        echo
        echo -e "${RED}$file paoya jayni ($DIR)${RST}"
        sleep 2

        return 1

    fi


    printf '\033c'

    echo -e "${CYN}>>> Starting ${name} ...${RST}"
    echo

    (
        cd "$DIR" || exit 1
        "$PY" "$file"
    )

    return $?

}


# Direct mode
if [ -n "${1:-}" ]; then

    case "$1" in

        1|v5|V5|shimul)

            run_script \
                "shimul.py" \
                "V5 (shimul.py)"

            exit $?
            ;;

        2|v6|V6|shimul2)

            run_script \
                "shimul2.py" \
                "V6 (shimul2.py)"

            exit $?
            ;;

        *)

            echo "Use: $0 [1|2]"
            exit 1
            ;;

    esac

fi


# ============================================================
# MAIN MENU
# ============================================================

while true; do

    printf '\033c'

    echo -e "${RED}╔══════════════════════════════════════════╗${RST}"
    echo -e "${RED}║${YEL}        SHIMUL SNI FINDER - SWITCH        ${RED}║${RST}"
    echo -e "${RED}╚══════════════════════════════════════════╝${RST}"

    echo

    echo -e \
        "  ${YEL}1.${RST} ${CYN}V5${RST}  SHIMUL V1 ${DIM}(shimul.py)${RST}   [$(status shimul.py)]"

    echo -e \
        "  ${YEL}2.${RST} ${CYN}V6${RST}  SHIMUL V2 ${DIM}(shimul2.py)${RST}  [$(status shimul2.py)]"

    echo -e \
        "  ${YEL}0.${RST} ${RED}EXIT${RST}"

    echo

    echo -e \
        "${DIM}  Tool er vitore 'Exit' dile ekhane ferot ashbe.${RST}"

    echo

    read -r \
        -p "$(echo -e "${CYN}Select (0-2): ${RST}")" \
        choice || exit 0


    case "$choice" in

        1)

            run_script \
                "shimul.py" \
                "V5 (shimul.py)"

            ;;

        2)

            run_script \
                "shimul2.py" \
                "V6 (shimul2.py)"

            ;;

        0|q|Q)

            echo -e "${GRN}Bye!${RST}"
            exit 0

            ;;

        *)

            echo -e "${RED}Invalid choice${RST}"
            sleep 1

            ;;

    esac


    echo

    read -r \
        -p "$(echo -e "${YEL}Enter chaple switch menu te ferot jabe...${RST}")" \
        _ || exit 0

done

SWEOF

chmod +x "$SWITCH"

ok "Switch menu ready: $SWITCH"

# ============================================================
# 18. COMMAND LAUNCHERS
# ============================================================

if [ "$IS_TERMUX" -eq 1 ]; then

    BIN_DIR="${PREFIX:-/data/data/com.termux/files/usr}/bin"

else

    BIN_DIR="$HOME/.local/bin"

    mkdir -p "$BIN_DIR"

fi


make_launcher() {

    local name="$1"
    local argument="${2:-}"

    cat > "$BIN_DIR/$name" <<EOF
#!/usr/bin/env bash
exec bash "$SWITCH" $argument "\$@"
EOF

    chmod +x "$BIN_DIR/$name"

}


make_launcher "shimul" ""
make_launcher "shimul1" "1"
make_launcher "shimul2" "2"

ok "Commands ready:"
echo "  shimul  = V5 / V6 switch menu"
echo "  shimul1 = V5"
echo "  shimul2 = V6"

# ============================================================
# 19. STORAGE HINT
# ============================================================

if [ "$IS_TERMUX" -eq 1 ]; then

    if [ ! -d "$HOME/storage" ]; then

        warn "Phone storage access chaile:"
        echo "      termux-setup-storage"

    fi

fi

# ============================================================
# 20. FINAL CHECK
# ============================================================

echo

if [ -f "$SCRIPT_DIR/shimul.py" ] &&
   [ -f "$SCRIPT_DIR/shimul2.py" ]; then

    echo -e "${GRN}"
    echo "══════════════════════════════════════════"
    echo "  ✅ SHIMUL INSTALL COMPLETE!"
    echo "══════════════════════════════════════════"
    echo -e "${RST}"

    echo "Install folder:"
    echo "  $SCRIPT_DIR"

    echo

    echo "Commands:"
    echo "  shimul   -> Switch menu"
    echo "  shimul1  -> V5"
    echo "  shimul2  -> V6"

    echo

    if [ "$IS_TERMUX" -eq 1 ]; then
        echo -e "${CYN}Run:${RST} shimul"
    else
        echo -e "${CYN}Run:${RST} $BIN_DIR/shimul"
    fi

else

    echo -e "${RED}"
    echo "══════════════════════════════════════════"
    echo "  ❌ SHIMUL FILE DOWNLOAD FAILED"
    echo "══════════════════════════════════════════"
    echo -e "${RST}"

    echo
    echo "Check manually:"
    echo "  $BASE_URL/shimul.py"
    echo "  $BASE_URL/shimul2.py"

    echo
    echo "Install log:"
    echo "  $PIP_LOG"

    exit 1

fi

# ============================================================
# 21. WARN ABOUT NON-FATAL PACKAGE FAILURES
# ============================================================

if [ "${#FAILED[@]}" -gt 0 ]; then

    echo
    warn "Kichu package/file issue chilo:"

    for item in "${FAILED[@]}"; do
        [ -n "$item" ] && echo "  - $item"
    done

fi

echo
ok "Done."
