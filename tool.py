#!/usr/bin/env python3
import os, sys, time, math, shutil, threading, urllib.request, urllib.error, subprocess, tempfile, struct, zlib, base64, itertools as it, traceback, platform, json, uuid
from pathlib import Path
import hmac, hashlib
from dataclasses import dataclass
from functools import lru_cache
from collections import Counter

# ==========================================
# 🛡️ SECURITY CHECK: DO NOT EDIT CREDIT
# ==========================================
CREDIT = "TG: @C_4_CRAZYBOY"

if CREDIT != "TG: @C_4_CRAZYBOY":
    print("\n\033[91m[!] FATAL ERROR: Unauthorized Modification Detected.\033[0m")
    print("\033[91m[!] Please download the official version.\033[0m\n")
    sys.exit(1)

_SECRET = "df8a36cee203abef25eb153ebbf1b340"

def _sign(key_val, endpoint):
    ts = str(int(time.time()))
    msg = f"{key_val}:{ts}:{endpoint}".encode()
    sig = hmac.new(_SECRET.encode(), msg, hashlib.sha256).hexdigest()
    return ts, sig

from rich.console import Console
from rich.panel import Panel
from rich.box import ROUNDED, HEAVY
from rich.text import Text
from rich.align import Align
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn

console = Console()
SERVER_URL = "https://crazyboy-tool-1.onrender.com/"

GOLD, CRIMSON, CYAN, NEON = "#FFD700", "#DC143C", "#00E5FF", "#00FFAA"
WHITE, DIM = "#FFFFFF", "#5A5A5A"
SUCCESS, ERRC, WARN = "#22FF88", "#FF3B5C", "#FFA500"

JAR_URL = "https://raw.githubusercontent.com/chandrakant-chavan/Crazyboy-tool-luaencrypt/main/unluac_patched.jar"

ROOT = Path(__file__).resolve().parent / "CRAZYBOY_HACKER"
LUA_EDIT = ROOT / "LUA_EDIT"
COMPILED = ROOT / "COMPILED"
LUA_ORIGINAL = ROOT / "LUA_ORIGINAL"
PAK_ORIGINAL = ROOT / "PAK_ORIGINAL"
PAK_RESULT = ROOT / "PAK_RESULT"
PAK_UNPACK = ROOT / "PAK_UNPACK"

_WAVE = "▁▂▃▄▅▆▇█"

# --- OBFUSCATED KEY DECODER ---
def _c(s): return base64.b64decode(s).decode('utf-8')
def _cb(s): return base64.b64decode(s)

# --- PAK DEPENDENCY CHECKS ---
try:
    from Crypto.Cipher import AES
    from Crypto.Cipher.AES import MODE_CBC
    from Crypto.Hash import SHA1
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    print("\n\033[91m[!] Missing Library: pycryptodome. Run: pip install pycryptodome\033[0m\n")
    sys.exit(1)

try:
    from zstandard import ZstdDecompressor, ZstdCompressor, ZstdCompressionDict, DICT_TYPE_AUTO
except ImportError:
    print("\n\033[91m[!] Missing Library: zstandard. Run: pip install zstandard\033[0m\n")
    sys.exit(1)

try:
    import gmalg
except ImportError:
    print("\n\033[91m[!] Missing Library: gmalg. Run: pip install gmalg\033[0m\n")
    sys.exit(1)

def setup_dirs():
    for d in [LUA_EDIT, COMPILED, LUA_ORIGINAL, PAK_ORIGINAL, PAK_RESULT, PAK_UNPACK]:
        d.mkdir(parents=True, exist_ok=True)

def ensure_jar():
    jar_path = Path("unluac_patched.jar")
    if not jar_path.exists():
        alert("unluac_patched.jar not found locally.", "warning")
        console.print(f"  [bold {CYAN}]⬇️  Downloading from GitHub...[/bold {CYAN}]")
        try:
            req = urllib.request.Request(JAR_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as response, open(jar_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            alert("Download complete!", "success")
            time.sleep(1)
        except Exception as e:
            alert(f"Failed to download jar: {e}", "error")
            return False
    return True

def wave_text(length=58, phase=0.0):
    t = time.time() + phase
    s = ""
    for i in range(length):
        v = (math.sin(t*2.0+i*0.35)*0.5 + math.sin(t*3.3+i*0.18)*0.3 + math.sin(t*1.7+i*0.62)*0.2)
        idx = max(0, min(len(_WAVE)-1, int((v+1.0)*0.5*(len(_WAVE)-1))))
        s += _WAVE[idx]
    return s

def rainbow_wave(length=58, phase=0.0):
    s = wave_text(length, phase)
    t = Text()
    for i, ch in enumerate(s):
        p = (time.time()*0.6 + i/length) % 2.0
        if p < 1.0:
            f = p; r,g,b = int(0xFF*(1-f)+0xDC*f), int(0xD7*(1-f)+0x14*f), int(0x00*(1-f)+0x3C*f)
        else:
            f = p-1.0; r,g,b = int(0xDC*(1-f)+0xFF*f), int(0x14*(1-f)+0xD7*f), int(0x3C*(1-f)+0x00*f)
        t.append(ch, style=f"bold #{r:02x}{g:02x}{b:02x}")
    return t

def banner(title=""):
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print()
    console.print(Align.center(rainbow_wave(58, 0.0)))
    console.print()
    for line in [
        "╔═══════════════════════════════════════════════════╗",
        "║                                                   ║",
        "║           C R A Z Y B O Y   H A C K E R           ║",
        "║                                                   ║",
        "╚═══════════════════════════════════════════════════╝",
    ]:
        console.print(Align.center(Text(line, style=f"bold {GOLD}")))
    console.print(Align.center(Text("v2.5  ·  PREMIUM", style=DIM)))
    console.print()
    console.print(Align.center(Text("🔥 A REAL BGMI MODDER 🔥", style=f"bold {CRIMSON}")))
    console.print()
    console.print(Align.center(rainbow_wave(58, 1.5)))
    console.print()
    info = Text()
    info.append("  🎯  ", style=f"bold {GOLD}")
    info.append(CREDIT, style=f"bold {GOLD}")
    info.append("   ·   ", style=DIM)
    info.append("🛡️ ONLINE", style=f"bold {CYAN}")
    info.append("   ·   ", style=DIM)
    info.append("👑 PREMIUM", style=f"bold {NEON}")
    console.print(Align.center(info))
    console.print()
    console.print(Align.center(rainbow_wave(58, 3.14)))
    console.print()
    if title:
        console.print(Align.center(Text(f"──  {title}  ──", style=f"bold {CRIMSON}")))
        console.print()

def print_credit():
    t = Text()
    t.append("  ✦  ", style=f"bold {GOLD}")
    t.append("MADE BY ", style=DIM)
    t.append(CREDIT, style=f"bold {GOLD}")
    t.append("  ✦  ", style=f"bold {GOLD}")
    console.print(Align.center(t))

def render_menu(rows, title):
    banner(title)
    for i, (num, name, desc) in enumerate(rows):
        mw = wave_text(10, i * 1.2)
        t = Text()
        t.append("  ")
        t.append(num, style=f"bold {CRIMSON}")
        t.append("  ▸ ", style=DIM)
        t.append(mw, style=f"bold {GOLD}")
        t.append("   ")
        t.append(name, style=f"bold {WHITE}")
        t.append("   ")
        t.append(desc, style=DIM)
        console.print(t)
    console.print()
    print_credit()
    console.print()

def live_monitor_animation(filename=""):
    labels = ["CPU", "MEM", "KEY", "ENT"]
    final = [52, 78, 100, 100]
    bar_len = 16

    def make_line(label, pct):
        filled = int(bar_len * pct / 100)
        empty = bar_len - filled
        color = SUCCESS if pct >= 100 else (WARN if pct >= 70 else CYAN)
        check = " ✓" if pct >= 100 else "  "
        return f"│   {label}  [bold {color}]{'█' * filled}[/bold {color}][dim]{'░' * empty}[/dim] {pct:3d}%{check}  │"

    top = f"[bold {GOLD}]┌─ ENCRYPTION MONITOR ───────────────────────┐[/bold {GOLD}]"
    bot = f"[bold {GOLD}]└────────────────────────────────────────────┘[/bold {GOLD}]"

    for step in range(0, 21):
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(top)
        for i, lbl in enumerate(labels):
            cur = int(final[i] * step / 20)
            console.print(make_line(lbl, cur))
        console.print(f"│   [bold {CYAN}]STATUS :[/bold {CYAN}]  ⚡ ENCRYPTING...            │")
        console.print(f"│   [bold {CYAN}]METHOD :[/bold {CYAN}]  AES-256-CBC + SM4 Hybrid   │")
        console.print(f"│   [bold {CYAN}]LAYERS :[/bold {CYAN}]  ▰▰▰▰▰▰▰▰▰▰  4/4  ✓           │")
        prog = int(30 * step / 20)
        console.print(f"│   [bold {GOLD}]PROGRESS[/bold {GOLD}] [bold {SUCCESS}]{'█' * prog}[/bold {SUCCESS}][dim]{'░' * (30 - prog)}[/dim] {int(step * 5):3d}%   │")
        console.print(bot)
        time.sleep(0.05)

    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(top)
    for i, lbl in enumerate(labels):
        console.print(make_line(lbl, final[i]))
    console.print(f"│   [bold {SUCCESS}]STATUS :[/bold {SUCCESS}]  ✅ SECURED                  │")
    console.print(f"│   [bold {CYAN}]METHOD :[/bold {CYAN}]  AES-256-CBC + SM4 Hybrid   │")
    console.print(f"│   [bold {CYAN}]LAYERS :[/bold {CYAN}]  ▰▰▰▰▰▰▰▰▰▰  4/4  ✓           │")
    console.print(f"│   [bold {SUCCESS}]PROGRESS[/bold {SUCCESS}] [bold {SUCCESS}]{'█' * 30}[/bold {SUCCESS}] 100%   │")
    console.print(bot)
    console.print()

def _spinner_loop(stop_event, label="ENCRYPTING"):
    frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    i = 0
    start = time.time()
    while not stop_event.is_set():
        elapsed = time.time() - start
        if elapsed < 5:
            pct = int(elapsed / 5 * 60)
        elif elapsed < 15:
            pct = 60 + int((elapsed - 5) / 10 * 35)
        else:
            pct = 95 + int(min(elapsed - 15, 10))
        pct = min(pct, 99)
        filled = pct // 5
        bar = "█" * filled + "░" * (20 - filled)
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r  {frame}  🔒 {label}... {bar} {pct:3d}%")
        sys.stdout.flush()
        i += 1
        time.sleep(0.08)
    sys.stdout.write("\r" + " " * 70 + "\r")
    sys.stdout.flush()

def upload(endpoint, files_dict, form_dict):
    boundary = "----CrazyBoyBoundary" + os.urandom(8).hex()
    body = bytearray()
    for k, v in form_dict.items():
        body += f'--{boundary}\r\n'.encode()
        body += f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode()
        body += f'{v}\r\n'.encode()
    for k, (fname, data) in files_dict.items():
        body += f'--{boundary}\r\n'.encode()
        body += f'Content-Disposition: form-data; name="{k}"; filename="{fname}"\r\n'.encode()
        body += b'Content-Type: application/octet-stream\r\n\r\n'
        body += data + b'\r\n'
    body += f'--{boundary}--\r\n'.encode()
    req = urllib.request.Request(f"{SERVER_URL}{endpoint}", data=bytes(body), method='POST')
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    req.add_header('X-Credit', CREDIT)
    _ts, _sig = _sign(form_dict.get('key', ''), endpoint)
    req.add_header('X-Timestamp', _ts)
    req.add_header('X-Signature', _sig)
    with urllib.request.urlopen(req, timeout=600) as resp:
        return resp.read()

def safe_upload(endpoint, files, form, label="ENCRYPTING"):
    stop = threading.Event()
    t = threading.Thread(target=_spinner_loop, args=(stop, label))
    t.daemon = True
    t.start()
    try:
        result = upload(endpoint, files, form)
        stop.set()
        t.join(timeout=1)
        return result, None
    except urllib.error.HTTPError as e:
        stop.set()
        t.join(timeout=1)
        err_msg = e.read().decode(errors='replace')[:300]
        if not err_msg:
            err_msg = f"HTTP Error {e.code}: {e.reason}"
        return None, err_msg
    except Exception as e:
        stop.set()
        t.join(timeout=1)
        return None, str(e)

def prompt(label):
    console.print(f"  [bold {GOLD}]{label}[/bold {GOLD}]  [dim]· {CREDIT}[/dim]")
    try:
        return input("  ❯ ").strip()
    except (KeyboardInterrupt, EOFError):
        return ""

def alert(msg, kind="info"):
    tags = {"success": ("✓", SUCCESS), "error": ("✗", ERRC), "warning": ("⚠", WARN), "info": ("▶", CYAN)}
    tag, color = tags.get(kind, tags["info"])
    console.print(f"  {tag}  {msg}  [dim]| {CREDIT}[/dim]", style=color)

def verify_key(key):
    body = f'--b\r\nContent-Disposition: form-data; name="key"\r\n\r\n{key}\r\n--b--\r\n'.encode()
    req = urllib.request.Request(f"{SERVER_URL}/verify", data=body, method='POST')
    req.add_header('Content-Type', 'multipart/form-data; boundary=b')
    req.add_header('X-Credit', CREDIT)
    _ts, _sig = _sign(key, '/verify')
    req.add_header('X-Timestamp', _ts)
    req.add_header('X-Signature', _sig)
    try:
        urllib.request.urlopen(req, timeout=15)
        return True, "OK"
    except urllib.error.HTTPError as e:
        try:
            import json as _j
            return False, _j.loads(e.read().decode()).get('error', 'Invalid key')
        except Exception:
            return False, 'Invalid key'
    except Exception as e:
        return False, f"Network: {e}"

def list_files(folder, extensions=None):
    if not folder.exists():
        return []
    files = [f for f in folder.iterdir() if f.is_file()]
    if extensions:
        files = [f for f in files if f.suffix.lower() in extensions]
    return sorted(files)

def pick_file(folder, extensions=None, title="Select file"):
    files = list_files(folder, extensions)
    if not files:
        alert(f"No files found in {folder.name}/", "error")
        console.print(f"  [dim]Put your files in: {folder}[/dim]")
        return None
    if len(files) == 1:
        console.print(f"  [dim]Only 1 file found: {files[0].name}[/dim]")
        confirm = prompt("Process this file? (Y/n)").lower()
        return files[0] if confirm != 'n' else None
    console.print(f"\n  [bold {GOLD}]{title}[/bold {GOLD}]")
    for i, f in enumerate(files, 1):
        sz = f.stat().st_size
        console.print(f"  [{i}] {f.name} ({sz:,} bytes)")
    console.print("  [0] Cancel")
    while True:
        c = prompt("Your choice")
        if c == '0': return None
        if c.isdigit():
            i = int(c)
            if 1 <= i <= len(files): return files[i-1]

def pick_lua_file():
    console.print(f"\n  [bold {GOLD}]Where is the file you want to inject?[/bold {GOLD}]")
    console.print(f"  [1] LUA_EDIT (Original / Decompiled)")
    console.print(f"  [2] COMPILED (Encrypted / Modded)")
    c = prompt("Select source folder")
    if c == '2':
        return pick_file(COMPILED, {'.lua', '.luac'}, "Files in COMPILED/")
    else:
        return pick_file(LUA_EDIT, {'.lua', '.luac'}, "Files in LUA_EDIT/")


# ==============================================================================
#  PAK UNPACK ENGINE (OFFLINE) - OBFUSCATED KEYS
# ==============================================================================

ZUC_KEY = bytes.fromhex("01010101010101010101010101010101")
ZUC_IV = bytes.fromhex("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")

RSA_MOD_1 = bytes.fromhex("".join("CBE8B9F2504050EF9831B719E9A6249A6D238505ADE909BDE78C180DED6072A0|C3347B8AF4780E1F212D952D82D4BF7F233C1ECA499E1F9D9A85B4FAD759F54B|ABC1666C5DE411EA9E4B2374425DD6C6F54333BBC8F2610FE6063E4D0D6C21A|671A8F7C3740555E5DC06D4E1691C456DB4116C0C012BF7B206E8311AAAEC689|952BF804EF638F09D5822B4117B114208F14DEB459E80CB770E5B0D7978E21F|5E6CED4999D3583108221A7AB28B960277ADB5690A332784019D9C195BE4EA9|EA0A09459010F236465DE0D59C3EF7324E954E1118D93EE19F299760C2CDB96|3CE87973EA5ECC9BBE81C27D4C7C8572AC07E9BCEAC9BD72AB7A56A3C0AD736|ABCE4".split("|")))

RSA_MOD_2 = bytes.fromhex("".join("7F58E8A39A4DA4E87357DDD650EAA16D3B5CE95B213D1030A662566444796A78|A84AE9AC3DBFFDE7F41094896696835DAF13B89E6EC2B84963B1B1BAF7151DA|245C3FBFAE2A6AE18B2684D03F9229DE2C91440F2A3A3BCDE1E5680C16722A8|8039C73560D5D43F4B6562C2EEA5B1D926D86B51108A2643C70FB74D6442CE3|A08339B8FD8F660AE88129B7AB8C46F2FA58124485CCCB1E987B05A6DA65A01|858ED3F89905449AE42BB07290FCB9994BF22E26610BCABB9804783A3B958791|7F3D97316EDDA15C5E13F79066407B55A93B291B68A4AC42A98D6E35FED84B1|4A792D154E62028DDAD20FC301951E5924BE9AD62FB719DD94CC30CAB871BEC|4377A8".split("|")))

SIMPLE1_DECRYPT_KEY = 121
SIMPLE2_DECRYPT_KEY = _cb("5VtO0Q==")
SIMPLE2_BLOCK_SIZE = 16

SM4_SECRET_4 = _c("ZWI2OTFlZmVhOTE0MjQxMzE3YTg=")
SM4_SECRET_2 = _c("UTBoVlRrZXkkYXMqMVpGbFFDaUE=")
SM4_SECRET_NEW = _c("eEcycVc1bFA3bFYyaU41Zk41cEd8eFQxY0o2ZEw1d0Mwa0sxckI0ZEt8cUM0alM1Ylo2Zkw1eEU2bkQ0ekF8Z0Q0alEyYUwzYlMzbEMzeFQwaVd8eFUxeVE4d0U5elkzZ1ozYlQ1YUV8dVEzY08yZFg3eFk0eFU3Z0g3aVN8Z1cxZlIwaks2d1E0b04wb0sxa1p8YUo0cFY3aVo3cFU0d1AyYUMyY1p8Y1g2alQzY00yb1Qzdkswa0oxcU58aVQydlMwY1M2eVQ2Y1oxc0UxbE98aE0xcEg5aVk4d005aFQ0bE41dUp8a0c2YkM4akswZkwwZEU0c0g0bUx8ZEI2bEIzdkUwZVo4d004cjAwYUN8dFA3c1A3bkk5ckEydlE0Y1Y1eVF8YVQwY0wxeU40cFQzc1o3ZU0ydll8dVY2ZlU4ZkM5ek4zbVA1ZEg4bU58clQ2YVE2b1oxeU0wZ081dE8xYU58alU1Ykg3bFEwZk05aEsyazAwb3xpUTBlTTBtSjd1VDBrVjZrTDVwWQ==").split('|')

EM_SIMPLE1 = 1
EM_SIMPLE2 = 16
EM_SM4_2 = 2
EM_SM4_4 = 4
EM_SM4_NEW_BASE = 31
EM_SM4_NEW_MASK = ~EM_SM4_NEW_BASE

CM_NONE = 0
CM_ZLIB = 1
CM_ZSTD = 6
CM_ZSTD_DICT = 8
CM_MASK = 15

class SM4:
    _S_BOX = bytes([
        52, 102, 37, 116, 137, 120, 228, 169, 90, 65, 188, 122, 214, 22, 33, 35,
        77, 97, 218, 148, 155, 223, 19, 60, 105, 58, 49, 10, 95, 215, 153, 149,
        241, 174, 114, 61, 7, 96, 36, 182, 152, 238, 196, 162, 45, 136, 221, 141,
        4, 234, 187, 17, 202, 62, 93, 161, 246, 63, 176, 151, 128, 71, 43, 166,
        230, 247, 217, 177, 89, 192, 124, 190, 84, 40, 183, 126, 79, 248, 67, 110,
        160, 80, 14, 245, 144, 184, 251, 163, 123, 98, 25, 70, 3, 42, 185, 143,
        159, 119, 180, 91, 131, 135, 8, 235, 226, 30, 66, 240, 15, 232, 113, 106,
        117, 173, 85, 31, 181, 171, 51, 250, 127, 21, 189, 133, 216, 6, 104, 179,
        82, 48, 72, 11, 0, 237, 239, 178, 87, 142, 231, 108, 213, 229, 46, 83,
        130, 5, 249, 129, 244, 86, 191, 140, 75, 227, 219, 74, 145, 76, 44, 211,
        64, 41, 78, 32, 20, 54, 121, 9, 111, 209, 55, 224, 57, 12, 138, 146,
        56, 18, 53, 109, 225, 253, 147, 154, 23, 212, 201, 156, 107, 132, 38, 157,
        175, 118, 193, 158, 208, 150, 197, 203, 233, 115, 73, 210, 205, 100, 195, 199,
        1, 125, 243, 172, 252, 222, 164, 68, 50, 27, 194, 186, 28, 2, 198, 39,
        69, 139, 242, 24, 167, 16, 81, 29, 200, 207, 99, 255, 47, 13, 88, 206,
        101, 165, 220, 26, 59, 134, 254, 34, 92, 168, 94, 103, 170, 236, 112, 204
    ])
    _FK = [1184304796, 1270900830, 1493524870, 3164752158]
    _CK = [964907, 973793155, 2654690407, 2916866751, 2071233739, 1226140771, 3348805095, 2045549823, 388349611, 800627875, 612403927, 3721562911, 1195432523, 3150178931, 612053223, 2445162591, 67183755, 1174197155, 1393249511, 3331183455, 3822152747, 1332317203, 1804781383, 1990130463, 1282653851, 3376591251, 2910902311, 925872959, 332098219, 735840931, 396665415, 3588844719]

    @staticmethod
    def ROL32(x, n):
        return (x << n) & 0xFFFFFFFF | (x >> (32 - n))

    @staticmethod
    def _BS(X):
        return (SM4._S_BOX[X >> 24 & 255] << 24 | SM4._S_BOX[X >> 16 & 255] << 16 | SM4._S_BOX[X >> 8 & 255] << 8 | SM4._S_BOX[X & 255])

    @staticmethod
    def _T0(X):
        X = SM4._BS(X)
        return X ^ SM4.ROL32(X, 2) ^ SM4.ROL32(X, 10) ^ SM4.ROL32(X, 18) ^ SM4.ROL32(X, 24)

    @staticmethod
    def _T1(X):
        X = SM4._BS(X)
        return X ^ SM4.ROL32(X, 13) ^ SM4.ROL32(X, 23)

    @staticmethod
    def _key_expand(key: bytes, rkey: list):
        K0 = int.from_bytes(key[0:4], 'big') ^ SM4._FK[0]
        K1 = int.from_bytes(key[4:8], 'big') ^ SM4._FK[1]
        K2 = int.from_bytes(key[8:12], 'big') ^ SM4._FK[2]
        K3 = int.from_bytes(key[12:16], 'big') ^ SM4._FK[3]
        for i in range(0, 32, 4):
            K0 = K0 ^ SM4._T1(K1 ^ K2 ^ K3 ^ SM4._CK[i]); rkey[i] = K0
            K1 = K1 ^ SM4._T1(K2 ^ K3 ^ K0 ^ SM4._CK[i + 1]); rkey[i + 1] = K1
            K2 = K2 ^ SM4._T1(K3 ^ K0 ^ K1 ^ SM4._CK[i + 2]); rkey[i + 2] = K2
            K3 = K3 ^ SM4._T1(K0 ^ K1 ^ K2 ^ SM4._CK[i + 3]); rkey[i + 3] = K3

    @classmethod
    def key_length(cls): return 16
    @classmethod
    def block_length(cls): return 16

    def __init__(self, key: bytes):
        self._key = key
        self._rkey = [0] * 32
        SM4._key_expand(self._key, self._rkey)
        self._block_buffer = bytearray()

    def decrypt(self, block: bytes) -> bytes:
        RK = self._rkey
        X0 = int.from_bytes(block[0:4], 'big'); X1 = int.from_bytes(block[4:8], 'big')
        X2 = int.from_bytes(block[8:12], 'big'); X3 = int.from_bytes(block[12:16], 'big')
        for i in range(0, 32, 4):
            X0 = X0 ^ SM4._T0(X1 ^ X2 ^ X3 ^ RK[31 - i])
            X1 = X1 ^ SM4._T0(X2 ^ X3 ^ X0 ^ RK[30 - i])
            X2 = X2 ^ SM4._T0(X3 ^ X0 ^ X1 ^ RK[29 - i])
            X3 = X3 ^ SM4._T0(X0 ^ X1 ^ X2 ^ RK[28 - i])
        BUFFER = self._block_buffer; BUFFER.clear()
        BUFFER.extend(X3.to_bytes(4, 'big')); BUFFER.extend(X2.to_bytes(4, 'big'))
        BUFFER.extend(X1.to_bytes(4, 'big')); BUFFER.extend(X0.to_bytes(4, 'big'))
        return bytes(BUFFER)

class Misc:
    @staticmethod
    def pad_to_n(data: bytes, n: int) -> bytes:
        padding = n - len(data) % n
        if padding == n: return data
        return data + b'\x00' * padding
    @staticmethod
    def align_up(x: int, n: int) -> int:
        return (x + n - 1) // n * n

class Reader:
    def __init__(self, buffer, cursor=0):
        self._buffer = buffer; self._cursor = cursor
    def u1(self, move_cursor=True) -> int: return self.unpack('B', move_cursor=move_cursor)[0]
    def u4(self, move_cursor=True) -> int: return self.unpack('<I', move_cursor=move_cursor)[0]
    def u8(self, move_cursor=True) -> int: return self.unpack('<Q', move_cursor=move_cursor)[0]
    def i4(self, move_cursor=True) -> int: return self.unpack('<i', move_cursor=move_cursor)[0]
    def s(self, n: int, move_cursor=True) -> bytes: return self.unpack(f'{n}s', move_cursor=move_cursor)[0]
    def unpack(self, f: str, offset=0, move_cursor=True):
        x = struct.unpack_from(f, self._buffer, self._cursor + offset)
        if move_cursor: self._cursor += struct.calcsize(f)
        return x
    def string(self, move_cursor=True) -> str:
        length = self.i4(move_cursor=move_cursor)
        if length == 0: return str()
        offset = 0 if move_c
