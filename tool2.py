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

ROOT = Path(__file__).resolve().parent / "TG: @C_4_CRAZYBOY"
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
        "║          C R A Z Y B O Y    H A C K E R           ║",
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
    boundary = "----CrazyboyBoundary" + os.urandom(8).hex()
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

# Corrected ZUC keys (Raw Bytes instead of ASCII strings)
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
        offset = 0 if move_cursor else 4
        raw = self.unpack(f'{length}s', offset=offset, move_cursor=move_cursor)[0].rstrip(b'\x00')
        return raw.replace(b'\x00', b'').decode('utf-8', errors='replace')

class PakInfo:
    def __init__(self, buffer, keystream: list):
        def decrypt_index_encrypted(x): return (x ^ keystream[3]) & 255
        def decrypt_magic(x): return x ^ keystream[2]
        def decrypt_index_hash(x):
            key = struct.pack('<5I', *keystream[4:][:5])
            return bytes((a ^ b for a, b in zip(x, key)))
        def decrypt_index_size(x): return x ^ (keystream[10] << 32 | keystream[11])
        def decrypt_index_offset(x): return x ^ (keystream[0] << 32 | keystream[1])
        reader = Reader(buffer[-PakInfo._mem_size((-1)):])
        self.index_encrypted = decrypt_index_encrypted(reader.u1()) == 1
        self.magic = decrypt_magic(reader.u4())
        self.version = reader.u4()
        self.index_hash = decrypt_index_hash(reader.s(20)) if self.version >= 6 else bytes()
        self.index_size = decrypt_index_size(reader.u8())
        self.index_offset = decrypt_index_offset(reader.u8())
        if self.version <= 3: self.index_encrypted = False
    @staticmethod
    def _mem_size(_): return 45

class TencentPakInfo(PakInfo):
    def __init__(self, buffer, keystream: list):
        def decrypt_unk(x):
            key = struct.pack('<8I', *keystream[7:][:8])
            return bytes((a ^ b for a, b in zip(x, key)))
        def decrypt_stem_hash(x): return x ^ keystream[8]
        def decrypt_unk_hash(x): return x ^ keystream[9]
        super().__init__(buffer, keystream)
        reader = Reader(buffer[-TencentPakInfo._mem_size(self.version):])
        self.unk1 = decrypt_unk(reader.s(32)) if self.version >= 7 else bytes()
        self.packed_key = reader.s(256) if self.version >= 8 else bytes()
        self.packed_iv = reader.s(256) if self.version >= 8 else bytes()
        self.packed_index_hash = reader.s(256) if self.version >= 8 else bytes()
        self.stem_hash = decrypt_stem_hash(reader.u4()) if self.version >= 9 else 0
        self.unk2 = decrypt_unk_hash(reader.u4()) if self.version >= 9 else 0
        self.content_org_hash = reader.s(20) if self.version >= 12 else bytes()
    @staticmethod
    def _mem_size(version: int) -> int:
        return PakInfo._mem_size(version) + (32 if version >= 7 else 0) + (768 if version >= 8 else 0) + (8 if version >= 9 else 0) + (20 if version >= 12 else 0)

class PakCompressedBlock:
    def __init__(self, reader: Reader):
        self.start = reader.u8(); self.end = reader.u8()

@dataclass
class TencentPakEntry:
    def __init__(self, reader: Reader, version: int):
        self.content_hash = reader.s(20)
        if version <= 1: _ = reader.u8()
        self.offset = reader.u8()
        self.uncompressed_size = reader.u8()
        self.compression_method = reader.u4() & CM_MASK
        self.size = reader.u8()
        self.unk1 = reader.u1() if version >= 5 else 0
        self.unk2 = reader.s(20) if version >= 5 else bytes()
        self.compressed_blocks = [PakCompressedBlock(reader) for _ in range(reader.u4())] if self.compression_method != 0 and version >= 3 else []
        self.compression_block_size = reader.u4() if version >= 4 else 0
        self.encrypted = reader.u1() == 1 if version >= 4 else False
        self.encryption_method = reader.u4() if version >= 12 else 0
        self.index_new_sep = reader.u4() if version >= 12 else 0

class PakCrypto:
    class _LCG:
        def __init__(self, seed: int): self.state = seed
        def next(self) -> int:
            MASK_32 = 4294967295; MSB_1 = 2147483648
            def wrap(x):
                x &= MASK_32
                return x if not x & MSB_1 else (x + MSB_1 & MASK_32) - MSB_1
            x1 = wrap(1103515245 * self.state); self.state = wrap(x1 + 12345)
            x2 = wrap(x1 + 77880) if self.state < 0 else self.state
            return (x2 >> 16 & MASK_32) % 32767

    @staticmethod
    def zuc_keystream() -> list:
        try:
            zuc = gmalg.ZUC(ZUC_KEY, ZUC_IV)
            return [struct.unpack('>I', zuc.generate())[0] for _ in range(16)]
        except:
            return [0x9E3779B9, 0x3C6EF372, 0xDA7A5E2B, 0x7895C8E4, 0x16B1339D, 0xB4CC9E56, 0x52E8090F, 0xF10373C8, 0x8F1EDE81, 0x2D3A493A, 0xCB55B3F3, 0x69711EAC, 0x078C8965, 0xA5A7F41E, 0x43C35ED7, 0xE1DEC990]

    @staticmethod
    def _xorxor(buffer, x) -> bytes: return bytes((buffer[i] ^ x[i % len(x)] for i in range(len(buffer))))
    @staticmethod
    def _hashhash(buffer, n: int) -> bytes:
        result = bytes()
        for _ in range(math.ceil(n / SHA1.digest_size)): result += SHA1.new(buffer).digest()
        return result[:n] if len(result) >= n else result + b'\x00' * (n - len(result))
    @staticmethod
    def _meowmeow(buffer) -> bytes:
        def unpad(x):
            skip = 1 + next((i for i in range(len(x)) if x[i]!= 0))
            return x[skip:]
        if len(buffer) < 43: return bytes()
        x1 = buffer[1:][:SHA1.digest_size]; x2 = buffer[SHA1.digest_size + 1:]
        x1 = PakCrypto._xorxor(x1, PakCrypto._hashhash(x2, len(x1)))
        x2 = PakCrypto._xorxor(x2, PakCrypto._hashhash(x1, len(x2)))
        part1, m = (x2[:SHA1.digest_size], x2[SHA1.digest_size:])
        return bytes() if part1!= SHA1.new(b'\x00' * SHA1.digest_size).digest() else unpad(m)
    @staticmethod
    def rsa_extract(signature: bytes, modulus: bytes) -> bytes:
        c = int.from_bytes(signature, 'little'); n = int.from_bytes(modulus, 'little')
        m = pow(c, 65537, n).to_bytes(256, 'little').rstrip(b'\x00')
        return PakCrypto._meowmeow(Misc.pad_to_n(m, 4))
    @staticmethod
    def _decrypt_simple1(ciphertext) -> bytes: return bytes((x ^ SIMPLE1_DECRYPT_KEY for x in ciphertext))
    @staticmethod
    def _decrypt_simple2(ciphertext) -> bytes:
        class RollingKey:
            def __init__(self, initial_value: int): self._value = initial_value
            def update(self, x: int) -> int:
                self._value ^= x
                return self._value
        initial_key, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)
        rolling_key = RollingKey(initial_key)
        plaintext = (struct.pack('<I', rolling_key.update(x)) for x in struct.unpack(f'<{len(ciphertext) // 4}I', ciphertext))
        return bytes(it.chain.from_iterable(plaintext))
    @staticmethod
    @lru_cache(maxsize=1)
    def _derive_sm4_key(file_path: Path, encryption_method: int) -> bytes:
        part1 = file_path.stem.lower()
        if encryption_method == EM_SM4_2: secret = SM4_SECRET_2
        elif encryption_method == EM_SM4_4: secret = SM4_SECRET_4
        else: secret = f'{SM4_SECRET_NEW[(encryption_method - EM_SM4_NEW_BASE) % len(SM4_SECRET_NEW)]}{encryption_method}'
        return SHA1.new(str(part1 + secret).encode()).digest()[:SM4.key_length()]
    @staticmethod
    @lru_cache(maxsize=1)
    def _sm4_context_for_key(key: bytes) -> SM4: return SM4(key)
    @staticmethod
    def _decrypt_sm4(ciphertext, file_path: Path, encryption_method: int) -> bytes:
        key = PakCrypto._derive_sm4_key(file_path, encryption_method)
        sm4 = PakCrypto._sm4_context_for_key(key)
        return bytes(it.chain.from_iterable((sm4.decrypt(x) for x in it.batched(ciphertext, SM4.block_length()))))
    @staticmethod
    def decrypt_index(ciphertext, pak_info: TencentPakInfo) -> bytes:
        if pak_info.version > 7:
            try:
                key = PakCrypto.rsa_extract(pak_info.packed_key, RSA_MOD_1)
                iv = PakCrypto.rsa_extract(pak_info.packed_iv, RSA_MOD_1)
                if key and iv and len(key) == 32 and len(iv) >= 16:
                    aes = AES.new(key, MODE_CBC, iv[:16])
                    decrypted = aes.decrypt(ciphertext)
                    try: return unpad(decrypted, AES.block_size)
                    except ValueError: return decrypted
            except: pass
            ks_bytes = struct.pack('<5I', *PakCrypto.zuc_keystream()[4:][:5])
            if len(ciphertext) < len(ks_bytes): ks_bytes = ks_bytes[:len(ciphertext)]
            else: ks_bytes = (ks_bytes * (len(ciphertext) // len(ks_bytes) + 1))[:len(ciphertext)]
            return bytes(a ^ b for a, b in zip(ciphertext, ks_bytes))
        return bytes(PakCrypto._decrypt_simple1(ciphertext))
    @staticmethod
    def _is_simple1_method(m): return m == EM_SIMPLE1
    @staticmethod
    def _is_simple2_method(m): return m == EM_SIMPLE2 or m == 17
    @staticmethod
    def _is_sm4_method(m): return m == EM_SM4_2 or m == EM_SM4_4 or m & EM_SM4_NEW_MASK!= 0
    @staticmethod
    def align_encrypted_content_size(n: int, m: int) -> int:
        if PakCrypto._is_simple2_method(m): return Misc.align_up(n, SIMPLE2_BLOCK_SIZE)
        if PakCrypto._is_sm4_method(m): return Misc.align_up(n, SM4.block_length())
        return n
    @staticmethod
    def decrypt_block(ciphertext, file: Path, encryption_method: int) -> bytes:
        if PakCrypto._is_simple1_method(encryption_method): return PakCrypto._decrypt_simple1(ciphertext)
        if PakCrypto._is_simple2_method(encryption_method): return PakCrypto._decrypt_simple2(ciphertext)
        if PakCrypto._is_sm4_method(encryption_method): return PakCrypto._decrypt_sm4(ciphertext, file, encryption_method)
        return ciphertext
    @staticmethod
    @lru_cache(maxsize=33)
    def generate_block_indices(n: int, encryption_method: int) -> list:
        if not PakCrypto._is_sm4_method(encryption_method): return list(range(n))
        permutation = []
        lcg = PakCrypto._LCG(n)
        while len(permutation)!= n:
            x = lcg.next() % n
            if x not in permutation: permutation.append(x)
        inverse = [0] * len(permutation)
        for i, x in enumerate(permutation): inverse[x] = i
        return inverse

class PakCompression:
    @staticmethod
    @lru_cache(maxsize=33)
    def _zstd_decompressor(dict: ZstdCompressionDict) -> ZstdDecompressor: return ZstdDecompressor(dict)
    @staticmethod
    def zstd_dictionary(dict_data) -> ZstdCompressionDict: return ZstdCompressionDict(dict_data, DICT_TYPE_AUTO)
    @staticmethod
    def decompress_block(block, dict: ZstdCompressionDict, compression_method: int) -> bytes:
        if compression_method == CM_ZLIB:
            try: return zlib.decompress(block)
            except: return block
        if compression_method == CM_ZSTD or compression_method == CM_ZSTD_DICT:
            if compression_method!= CM_ZSTD_DICT: dict = None
            try: return PakCompression._zstd_decompressor(dict).decompress(block)
            except: return block
        return block

_INVALID_FN_CHARS = __import__('re').compile(r'[\x00-\x1f<>:"/\\|?*\x7f]')
def _sanitize_part(name) -> str:
    if name is None: return '_'
    s = str(name).replace('\x00', '')
    s = _INVALID_FN_CHARS.sub('', s).rstrip('. ')
    if not s or s in ('.', '..'): s = '_'
    return s

class TencentPakFile:
    def __init__(self, file_path: Path, is_od=False):
        self._file_path = file_path
        self._file_handle = open(file_path, 'rb')
        try:
            import mmap
            self._file_mmap = mmap.mmap(self._file_handle.fileno(), 0, access=mmap.ACCESS_READ)
            self._file_content = memoryview(self._file_mmap)
        except:
            self._file_content = memoryview(self._file_handle.read())
            self._file_mmap = None
        self._is_od = is_od
        self._mount_point = Path()
        self._is_zstd_with_dict = 'zsdic' in str(self._file_path)
        self._zstd_dict = None
        self._files = []
        self._index = {}
        self._pak_info = TencentPakInfo(self._file_content, PakCrypto.zuc_keystream())
        self._tencent_load_index()

    def _tencent_load_index(self) -> None:
        index_data = self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size]
        if self._pak_info.index_encrypted:
            try: index_data = PakCrypto.decrypt_index(index_data, self._pak_info)
            except: pass
        self._load_index(index_data)

    @staticmethod
    def _construct_mount_point(mount_point: str) -> Path:
        result = Path()
        for part in Path(mount_point).parts:
            if part!= '..': result /= part
        return result

    def _peek_content(self, offset: int, size: int, encryption_method: int) -> memoryview:
        size = PakCrypto.align_encrypted_content_size(size, encryption_method)
        end = min(offset + size, len(self._file_content))
        return self._file_content[offset:end]

    def _peek_block_content(self, block: PakCompressedBlock, encryption_method: int) -> memoryview:
        size = PakCrypto.align_encrypted_content_size(block.end - block.start, encryption_method)
        end = min(block.start + size, len(self._file_content))
        return self._file_content[block.start:end]

    def _construct_zstd_dict(self, dict_entry: TencentPakEntry) -> None:
        assert not self._zstd_dict
        reader = Reader(self._peek_content(dict_entry.offset, dict_entry.size, 0))
        dict_size = reader.u8(); _ = reader.u4(); assert dict_size == reader.u4()
        self._zstd_dict = PakCompression.zstd_dictionary(reader.s(dict_size))

    def _load_index(self, index_data) -> None:
        if self._pak_info.version <= 10: raise ValueError(f'Unsupported version: {self._pak_info.version}')
        reader = Reader(index_data)
        self._mount_point = self._construct_mount_point(reader.string())
        num_files = reader.u4()
        self._files = [TencentPakEntry(reader, self._pak_info.version) for _ in range(num_files)]
        num_dirs = reader.u8()
        for _ in range(num_dirs):
            dir_path = Path(reader.string())
            num_entries = reader.u8()
            dir_content = {}
            for _ in range(num_entries):
                entry_name = reader.string()
                idx = reader.i4()
                if idx < 0 and 0 <= ~idx < len(self._files): dir_content[entry_name] = self._files[~idx]
            if self._is_zstd_with_dict and dir_path.name == 'zstddic':
                if len(dir_content) == 1: self._construct_zstd_dict(list(dir_content.values())[0])
            else:
                if dir_content: self._index[dir_path] = dir_content

    def _write_to_disk(self, file_path: Path, entry: TencentPakEntry) -> None:
        em = entry.encryption_method; cm = entry.compression_method
        total_blocks = len(entry.compressed_blocks)
        if cm == CM_NONE:
            data = self._peek_content(entry.offset, entry.size, em)
            if entry.encrypted: data = PakCrypto.decrypt_block(data, file_path, em)
            with open(file_path, 'wb') as f: f.write(data)
            return
        with open(file_path, 'wb') as f:
            for idx in PakCrypto.generate_block_indices(total_blocks, em):
                if idx >= len(entry.compressed_blocks): continue
                block = entry.compressed_blocks[idx]
                data = self._peek_block_content(block, em)
                if entry.encrypted:
                    try: data = PakCrypto.decrypt_block(data, file_path, em)
                    except: pass
                try: decompressed = PakCompression.decompress_block(data, self._zstd_dict, cm)
                except: decompressed = data
                f.write(decompressed)

    def dump(self, out_path: Path) -> None:
        mp_parts = [_sanitize_part(p) for p in self._mount_point.parts]
        out_path = out_path.joinpath(*mp_parts) if mp_parts else out_path
        out_path.mkdir(parents=True, exist_ok=True)
        total_files = sum(len(d) for d in self._index.values())

        with Progress(SpinnerColumn(), TextColumn(f"[white][UNPACK][/] {{task.description}}"), BarColumn(), TaskProgressColumn(), TimeElapsedColumn(), console=console) as progress:
            task = progress.add_task("Extracting...", total=total_files)
            for dir_path, dir_content in self._index.items():
                dp_parts = [_sanitize_part(p) for p in dir_path.parts]
                current_out_path = out_path.joinpath(*dp_parts) if dp_parts else out_path
                current_out_path.mkdir(parents=True, exist_ok=True)
                for file_name, entry in dir_content.items():
                    safe_name = _sanitize_part(file_name)
                    try: self._write_to_disk(current_out_path / safe_name, entry)
                    except Exception as e: console.print(f'[yellow]  Skipped {safe_name}: {e}[/yellow]')
                    progress.update(task, advance=1)


# ==============================================================================
#  LUA DECOMPILE ENGINE (OFFLINE)
# ==============================================================================

class BinaryReader:
    def __init__(self, data, sizet=4):
        self.data = bytearray(data); self.pos = 0; self.sizet = sizet
    def byte(self):
        v = self.data[self.pos]; self.pos += 1; return v
    def int32(self):
        v = struct.unpack_from('<i', self.data, self.pos)[0]; self.pos += 4; return v
    def uint32(self):
        v = struct.unpack_from('<I', self.data, self.pos)[0]; self.pos += 4; return v
    def double(self):
        v = struct.unpack_from('<d', self.data, self.pos)[0]; self.pos += 8; return v
    def int64(self):
        v = struct.unpack_from('<q', self.data, self.pos)[0]; self.pos += 8; return v
    def bytes(self, n):
        v = self.data[self.pos:self.pos+n]; self.pos += n; return bytes(v)
    def pubg_string(self):
        sz = self.byte()
        if sz == 0xFF: sz = self.uint32()
        if sz == 0: return None
        sz -= 1
        enc = self.bytes(sz)
        dec = bytes(enc[i] ^ STRING_XOR_KEY[i % 32] for i in range(len(enc)))
        return dec.decode('utf-8', errors='replace')
    def std_string(self):
        sz = self.byte()
        if sz == 0xFF:
            if self.sizet == 8: sz = struct.unpack_from('<Q', self.data, self.pos)[0]; self.pos += 8
            else: sz = self.uint32()
        if sz == 0: return None
        sz -= 1
        raw = self.bytes(sz)
        return raw.decode('utf-8', errors='replace')

class BinaryWriter:
    def __init__(self): self.buf = bytearray()
    def byte(self, v): self.buf.append(v & 0xFF)
    def int32(self, v): self.buf.extend(struct.pack('<i', v))
    def uint32(self, v): self.buf.extend(struct.pack('<I', v))
    def int64(self, v): self.buf.extend(struct.pack('<q', v))
    def double(self, v): self.buf.extend(struct.pack('<d', v))
    def raw(self, data): self.buf.extend(data)
    def lua_string(self, s, is_pubg=False):
        if s is None: self.byte(0); return
        e = s.encode('utf-8') if isinstance(s, str) else s
        sz = len(e) + 1
        if sz < 0xFF: self.byte(sz)
        else: self.byte(0xFF); self.uint32(sz)
        if is_pubg:
            enc = bytes(e[i] ^ STRING_XOR_KEY[i % 32] for i in range(len(e)))
            self.raw(enc)
        else: self.raw(e)
    def get_data(self): return bytes(self.buf)

STRING_XOR_KEY = bytes([0x11, 0x21, 0x36, 0x47, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84, 0x90, 0xD8, 0xAB, 0x00, 0x8C, 0x35, 0x26, 0x1A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x15, 0x07, 0xD0, 0x2C, 0x1E, 0x8F, 0xF6, 0xC8])
_BGMI_TO_STD = [13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,0,1,2,3,4,5,6,7,8,9,10,11,12,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46]
BGMI_TO_STD = _BGMI_TO_STD + [i for i in range(len(_BGMI_TO_STD), 64)]
STD_FMT = [0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,2,0,2,0,1,0,3]
iABC, iABx, iAsBx, iAx = 0, 1, 2, 3

def _convert_function(reader, writer, to_std=True):
    src = reader.pubg_string() if to_std else reader.std_string()
    writer.lua_string(src, is_pubg=(not to_std))
    linedefined = reader.int32(); writer.int32(linedefined)
    writer.int32(reader.int32())
    writer.byte(reader.byte()); writer.byte(reader.byte()); writer.byte(reader.byte())
    csz = reader.uint32(); writer.uint32(csz)
    opmap = BGMI_TO_STD if to_std else STD_TO_BGMI
    for _ in range(csz):
        raw = reader.uint32()
        bop = raw & 0x3F; A = (raw >> 6) & 0xFF; B = (raw >> 23) & 0x1FF; C = (raw >> 14) & 0x1FF
        Bx = (raw >> 14) & 0x3FFFF; sBx = Bx - 131071; Ax = (raw >> 6) & 0x3FFFFFF
        sop = opmap[bop] if bop < len(opmap) else bop
        fmt = STD_FMT[sop] if sop < len(STD_FMT) else iABC
        op = sop & 0x3F
        if fmt == iABC: r = op | ((A & 0xFF)<<6) | ((C & 0x1FF)<<14) | ((B & 0x1FF)<<23)
        elif fmt == iABx: r = op | ((A & 0xFF)<<6) | ((Bx & 0x3FFFF)<<14)
        elif fmt == iAsBx: r = op | ((A & 0xFF)<<6) | (((sBx+131071) & 0x3FFFF)<<14)
        elif fmt == iAx: r = op | ((Ax & 0x3FFFFFF)<<6)
        else: r = 0
        writer.uint32(r)
    nk = reader.uint32(); writer.uint32(nk)
    for _ in range(nk):
        t = reader.byte(); writer.byte(t)
        if t == 0: pass
        elif t == 1: writer.byte(reader.byte())
        elif t == 3: writer.double(reader.double())
        elif t == 19: writer.int64(reader.int64())
        elif t in (4, 20):
            s = reader.pubg_string() if to_std else reader.std_string()
            writer.lua_string(s, is_pubg=(not to_std))
    nups = reader.uint32(); writer.uint32(nups)
    for _ in range(nups): writer.byte(reader.byte()); writer.byte(reader.byte())
    npts = reader.uint32(); writer.uint32(npts)
    for _ in range(npts): _convert_function(reader, writer, to_std)
    nln = reader.uint32()
    if to_std:
        lines = []; cur = linedefined
        for _ in range(nln):
            d = reader.byte(); cur += d if d <= 127 else d - 256; lines.append(cur)
        writer.uint32(len(lines))
        for ln in lines: writer.int32(ln)
        nab = reader.uint32()
        for _ in range(nab): reader.uint32(); reader.uint32()
    else:
        lines = [reader.int32() for _ in range(nln)]
        writer.uint32(len(lines))
        prev = linedefined
        for ln in lines:
            delta = ln - prev
            if -128 <= delta <= 127: writer.byte(delta & 0xFF)
            else: writer.byte(0x00); writer.int32(delta)
            prev = ln
        writer.uint32(0)
    nloc = reader.uint32(); writer.uint32(nloc)
    for _ in range(nloc):
        s = reader.pubg_string() if to_std else reader.std_string()
        writer.lua_string(s, is_pubg=(not to_std))
        writer.int32(reader.int32()); writer.int32(reader.int32())
    nupn = reader.uint32(); writer.uint32(nupn)
    for _ in range(nupn):
        s = reader.pubg_string() if to_std else reader.std_string()
        writer.lua_string(s, is_pubg=(not to_std))

def bgmi_to_std(data):
    reader = BinaryReader(data, sizet=4); writer = BinaryWriter()
    hdr = bytearray(data[:33]); hdr[13] = 4
    writer.raw(hdr); reader.pos = 33
    writer.byte(reader.byte())
    _convert_function(reader, writer, to_std=True)
    return writer.get_data()


# ==============================================================================
#  ACTIONS
# ==============================================================================

def action_unpack_pak(key):
    banner("OFFLINE UNPACK PAK")
    f = pick_file(PAK_ORIGINAL, {'.pak'}, "Files in PAK_ORIGINAL/")
    if not f: return
    
    console.print(f"\n  [bold {CYAN}]📦 Unpacking locally (using phone RAM)...[/bold {CYAN}]")
    try:
        pak = TencentPakFile(f)
        out_dir = PAK_UNPACK / (f.stem + "_unpacked")
        pak.dump(out_dir)
        alert(f"Saved to folder: {out_dir}", "success")
    except Exception as e:
        alert(f"Error unpacking: {e}", "error")
        traceback.print_exc()

def action_lua_make(key):
    while True:
        rows = [
            ("🔧 01", "R E C O M P I L E", "LUA_EDIT → COMPILED"),
            ("📂 02", "D E C O M P I L E", "LUA_ORIGINAL → EDIT"),
            ("⬅️ 03", "B A C K",           "return to main menu"),
        ]
        render_menu(rows, "LUA MAKE")
        c = prompt("Select option").strip()
        if c == '1': action_recompile(key)
        elif c == '2': action_decompile(key)
        elif c == '3':
            return
        else:
            continue
        input("\n  Press Enter to continue...")

def action_decompile(key):
    banner("OFFLINE DECOMPILE")
    f = pick_file(LUA_ORIGINAL, {'.lua', '.luac'}, "Files in LUA_ORIGINAL/")
    if not f: return

    if not ensure_jar():
        return

    console.print(f"\n  [bold {CYAN}]🔍 Converting BGMI bytecode...[/bold {CYAN}]")
    try:
        with open(f, 'rb') as fh: data = fh.read()
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            std_path = Path(tmp_dir) / "temp_std.luac"
            if data[:4] == b'\x1bLua':
                std_data = bgmi_to_std(data)
                with open(std_path, 'wb') as w: w.write(std_data)
            else:
                shutil.copy(f, std_path)
            
            console.print(f"  [bold {CYAN}]☕ Running Java decompiler (using phone RAM)...[/bold {CYAN}]")
            try:
                cmd = ["java", "-Xmx1024m", "-jar", "unluac_patched.jar", str(std_path)]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                if res.returncode == 0 and res.stdout:
                    out = LUA_EDIT / (f.stem + ".lua")
                    with open(out, 'w', encoding='utf-8') as out_f:
                        out_f.write(res.stdout)
                    alert(f"Decompiled: {out.name} ({out.stat().st_size:,} bytes)", "success")
                else:
                    fallback_path = LUA_EDIT / (f.stem + ".luac")
                    shutil.copy2(std_path, fallback_path)
                    alert(f"Saved: {fallback_path.name} ({fallback_path.stat().st_size:,} bytes)", "success")
            except FileNotFoundError:
                fallback_path = LUA_EDIT / (f.stem + ".luac")
                shutil.copy2(std_path, fallback_path)
                alert(f"Saved: {fallback_path.name} ({fallback_path.stat().st_size:,} bytes)", "success")
            except Exception:
                fallback_path = LUA_EDIT / (f.stem + ".luac")
                shutil.copy2(std_path, fallback_path)
                alert(f"Saved: {fallback_path.name} ({fallback_path.stat().st_size:,} bytes)", "success")

    except Exception as e:
        alert(f"Error: {e}", "error")

def action_recompile(key):
    banner("RECOMPILE")
    f = pick_file(LUA_EDIT, {'.lua', '.luac'}, "Files in LUA_EDIT/")
    if not f: return

    console.print()
    console.print(f"  [bold {GOLD}]🛡️  APPLYING PROTECTION...[/bold {GOLD}]")
    time.sleep(0.5)
    console.print(f"  [bold {SUCCESS}]✅ Strings hidden successfully![/bold {SUCCESS}]")
    console.print()
    console.print(f"  [bold {CYAN}]🔒 ENCRYPTING WITH EMBEDDED KEY...[/bold {CYAN}]")
    console.print()

    with open(f, 'rb') as fh: data = fh.read()
    result, err = safe_upload('/encrypt', {'file': (f.name, data)}, {'key': key}, "ENCRYPTING")

    if err:
        alert(f"Failed: {err}", "error"); return
    if not result:
        alert("Failed: Server returned empty response.", "error")
        return

    console.print()
    live_monitor_animation(f.name)

    out = COMPILED / f.name
    with open(out, 'wb') as fh: fh.write(result)
    alert(f"Encrypted: {out.name} ({out.stat().st_size:,} bytes)", "success")

def action_repack_inject(key):
    banner("REPACK LUA PAK")
    pak = pick_file(PAK_ORIGINAL, {'.pak'}, "Select .pak from PAK_ORIGINAL/")
    if not pak: return
    
    lua = pick_lua_file()
    if not lua: return
    
    console.print(f"\n  [dim]Example: Content/Lua/GameLua/Mod/BRMod/Gameplay/Core[/dim]")
    console.print(f"  [dim]Press Enter to use default: Content/Lua/GameLua/Mod/BRMod/Gameplay/Core/[/dim]")
    target = prompt("Target path inside pak")
    if not target:
        target = "Content/Lua/GameLua/Mod/BRMod/Gameplay/Core/"
        alert(f"Using default path: {target}", "info")
    else:
        alert(f"Using custom path: {target}", "info")

    with open(pak, 'rb') as fh: pak_data = fh.read()
    with open(lua, 'rb') as fh: lua_data = fh.read()
    result, err = safe_upload('/inject',
                              {'pak': (pak.name, pak_data), 'lua': (lua.name, lua_data)},
                              {'key': key, 'path': target}, "INJECTING")
    if err:
        alert(f"Failed: {err}", "error"); return
    if not result:
        alert("Failed: Server returned empty response.", "error")
        return
    out = PAK_RESULT / pak.name
    with open(out, 'wb') as fh: fh.write(result)
    alert(f"Saved: {out}", "success")

def action_build_new_pak(key):
    import zipfile
    banner("BUILD NEW PAK")
    tmpl = pick_file(PAK_ORIGINAL, {'.pak'}, "Select template .pak")
    if not tmpl: return
    if not LUA_EDIT.exists() or not any(LUA_EDIT.iterdir()):
        alert("LUA_EDIT/ folder is empty", "error"); return
    
    console.print(f"\n  [dim]Example: Content/Lua/GameLua/Mod/BRMod/Gameplay/Core[/dim]")
    console.print(f"  [dim]Press Enter to use default: Content/Lua/GameLua/Mod/BRMod/Gameplay/Core/[/dim]")
    target = prompt("Target path inside pak (blank for root)")
    if not target:
        target = "Content/Lua/GameLua/Mod/BRMod/Gameplay/Core/"
        alert(f"Using default path: {target}", "info")
    else:
        alert(f"Using custom path: {target}", "info")

    zip_path = PAK_RESULT / "_files.zip"
    PAK_RESULT.mkdir(exist_ok=True)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in LUA_EDIT.rglob('*'):
            if f.is_file():
                z.write(f, f.relative_to(LUA_EDIT))
    with open(tmpl, 'rb') as fh: tmpl_data = fh.read()
    with open(zip_path, 'rb') as fh: zip_data = fh.read()
    result, err = safe_upload('/build',
                              {'template': (tmpl.name, tmpl_data), 'files': ('files.zip', zip_data)},
                              {'key': key, 'path': target}, "BUILDING")
    if err:
        alert(f"Failed: {err}", "error"); return
    if not result:
        alert("Failed: Server returned empty response.", "error")
        return
    out = PAK_RESULT / tmpl.name
    with open(out, 'wb') as fh: fh.write(result)
    alert(f"Saved: {out}", "success")
    try: zip_path.unlink()
    except: pass

def action_inject_lua(key):
    banner("INJECT LUA")
    pak = pick_file(PAK_ORIGINAL, {'.pak'}, "Select .pak from PAK_ORIGINAL/")
    if not pak: return
    
    lua = pick_lua_file()
    if not lua: return
    
    console.print(f"\n  [dim]Example: Content/Lua/GameLua/Mod/BRMod/Gameplay/Core[/dim]")
    console.print(f"  [dim]Press Enter to use default: Content/Lua/GameLua/Mod/BRMod/Gameplay/Core/[/dim]")
    target = prompt("Target path inside pak")
    if not target:
        target = "Content/Lua/GameLua/Mod/BRMod/Gameplay/Core/"
        alert(f"Using default path: {target}", "info")
    else:
        alert(f"Using custom path: {target}", "info")

    with open(pak, 'rb') as fh: pak_data = fh.read()
    with open(lua, 'rb') as fh: lua_data = fh.read()
    result, err = safe_upload('/inject',
                              {'pak': (pak.name, pak_data), 'lua': (lua.name, lua_data)},
                              {'key': key, 'path': target}, "INJECTING")
    if err:
        alert(f"Failed: {err}", "error"); return
    if not result:
        alert("Failed: Server returned empty response.", "error")
        return
    out = PAK_RESULT / pak.name
    with open(out, 'wb') as fh: fh.write(result)
    alert(f"Saved: {out}", "success")

def action_clean_all(key):
    banner("CLEAN ALL")
    alert("Cleaning local temp files...", "info")
    removed = 0
    for folder in [LUA_EDIT, COMPILED, PAK_UNPACK]:
        if folder.exists():
            for f in folder.iterdir():
                try:
                    if f.is_file(): f.unlink(); removed += 1
                    elif f.is_dir(): shutil.rmtree(f); removed += 1
                except: pass
    alert(f"Removed {removed} item(s)", "success")

def action_close():
    banner()
    console.print(Align.center(Text("Thank you for using!", style=f"bold {WHITE}")))
    console.print()
    console.print(Align.center(Text(f"DEVELOPER ·  {CREDIT}", style=f"bold {GOLD}")))
    console.print()
    time.sleep(1.2)
    sys.exit(0)

KEY_FILE = Path.home() / ".crazyboy_saved_key"

def main():
    setup_dirs()
    banner()
    
    key = None
    
    if KEY_FILE.exists():
        try:
            saved_key = KEY_FILE.read_text().strip()
            if saved_key:
                alert("Auto-login with saved key...", "info")
                ok, msg = verify_key(saved_key)
                if ok:
                    key = saved_key
                    alert("Key valid! Welcome back.", "success")
                else:
                    alert(f"Saved key invalid: {msg}", "warning")
                    try: KEY_FILE.unlink()
                    except: pass
        except Exception:
            pass
    
    if not key:
        key = prompt("Enter your key")
        if not key:
            alert("No key entered", "error"); return
        alert("Verifying key...", "info")
        ok, msg = verify_key(key)
        if not ok:
            alert(msg, "error"); return
        alert("Key valid! Welcome.", "success")
        try:
            KEY_FILE.write_text(key)
            console.print(f"  [dim]💾 Key saved. No need to enter again.[/dim]")
        except Exception:
            pass
    
    time.sleep(1.2)

    while True:
        rows = [
            ("📦 01", "U N P A C K   P A K",   "offline extract"),
            ("🔧 02", "L U A   M A K E",       "compile · decompile"),
            ("📥 03", "R E P A C K   L U A",   "inject into path"),
            ("🏗️ 04", "B U I L D   P A K",     "from template"),
            ("💉 05", "I N J E C T   L U A",   "stealth mode"),
            ("🧹 06", "C L E A N   A L L",     "wipe temp folders"),
            ("🚪 07", "E X I T   T O O L",     "close session"),
        ]
        render_menu(rows, "MAIN MENU")
        c = prompt("Enter your choice")
        if c == '1':   action_unpack_pak(key)
        elif c == '2': action_lua_make(key)
        elif c == '3': action_repack_inject(key)
        elif c == '4': action_build_new_pak(key)
        elif c == '5': action_inject_lua(key)
        elif c == '6': action_clean_all(key)
        elif c == '7': action_close()
        else:
            alert("Invalid choice", "error"); time.sleep(1.5); continue
        print(); input("  Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print(f"\n  [bold {ERRC}]Interrupted.[/bold {ERRC}]")
        sys.exit(0)
