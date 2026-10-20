# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║         GREAT JOHIR • RED + CYAN + GOLD CYBER SYSTEM v3.1        ║
║        Guest Login → Auto Bio → Instant Offline  [GREAT JOHIR]   ║
╚══════════════════════════════════════════════════════════════════╝
"""

import asyncio
import json
import os
import random
import sys
import time
import traceback
import uuid
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")

import httpx
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from protobuf_decoder.protobuf_decoder import Parser

try:
    from google_play_scraper import app as play_scraper
except Exception:
    play_scraper = None


# =========================================================
#  GREAT JOHIR • RED + CYAN + GOLD PALETTE
# =========================================================
class C:
    RESET = "\033[0m"
    BOLD  = "\033[1m"
    DIM   = "\033[2m"

    # Red family
    RED         = "\033[31m"
    B_RED       = "\033[91m"
    DARK_RED    = "\033[38;5;88m"
    BLOOD_RED   = "\033[38;5;124m"
    CRIMSON     = "\033[38;5;160m"
    FIRE_RED    = "\033[38;5;196m"
    ORANGE_RED  = "\033[38;5;202m"
    NEON_RED    = "\033[38;5;203m"
    SOFT_RED    = "\033[38;5;210m"

    # Unique Accent 1 — Neon Cyan
    CYAN        = "\033[36m"
    NEON_CYAN   = "\033[38;5;51m"
    DEEP_CYAN   = "\033[38;5;44m"

    # Unique Accent 2 — Neon Gold
    GOLD        = "\033[38;5;220m"
    AMBER       = "\033[38;5;214m"

    # Neutrals
    WHITE       = "\033[97m"
    B_WHITE     = "\033[97m"
    GREY        = "\033[38;5;245m"


def paint(text, color):
    return f"{color}{text}{C.RESET}"


# =========================================================
#  BANNER — SOLID BLOCK "GREAT JOHIR"
# =========================================================
BANNER = r"""
██████╗ ██████╗ ███████╗ █████╗ ████████╗   ██╗ ██████╗ ██╗  ██╗██╗██████╗ 
██╔════╝ ██╔══██╗██╔════╝██╔══██╗╚══██╔══╝   ██║██╔═══██╗██║  ██║██║██╔══██╗
██║  ███╗██████╔╝█████╗  ███████║   ██║      ██║██║   ██║███████║██║██████╔╝
██║   ██║██╔══██╗██╔══╝  ██╔══██║   ██║ ██   ██║██║   ██║██╔══██║██║██╔══██╗
╚██████╔╝██║  ██║███████╗██║  ██║   ██║ ╚█████╔╝╚██████╔╝██║  ██║██║██║  ██║
 ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝  ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
"""


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_banner():
    clear_screen()
    print()
    print(paint(BANNER, C.FIRE_RED))
    line = "═" * 74
    print(paint(f"╔{line}╗", C.CRIMSON))
    print(paint("║", C.CRIMSON) +
          paint("       🔥  G R E A T   J O H I R  •  R E D   S Y S T E M  🔥       ".center(74),
                C.BOLD + C.NEON_RED) +
          paint("║", C.CRIMSON))
    print(paint("║", C.CRIMSON) +
          paint("      Guest Login  »  Auto Bio  »  Instant Offline  [OB55]         ".center(74),
                C.NEON_CYAN) +
          paint("║", C.CRIMSON))
    print(paint(f"╚{line}╝", C.CRIMSON))
    print(paint("                       ★ T A G :   G R E A T   J O H I R ★", C.GOLD))
    print()


def section(title):
    line = "─" * 60
    print()
    print(paint(f"  ╭{line}╮", C.CRIMSON))
    print(paint("  │ ", C.CRIMSON) + paint(f"◈ {title}".ljust(58), C.BOLD + C.FIRE_RED) + paint("│", C.CRIMSON))
    print(paint(f"  ╰{line}╯", C.CRIMSON))


# =========================================================
#  PRINTERS
# =========================================================
def log_ok(msg):    print(f"{C.NEON_RED}  ╰─[✓] {msg}{C.RESET}")
def log_err(msg):   print(f"{C.FIRE_RED}{C.BOLD}  ╰─[✗] {msg}{C.RESET}")
def log_warn(msg):  print(f"{C.GOLD}  ╰─[!] {msg}{C.RESET}")
def log_info(msg):  print(f"{C.NEON_CYAN}  ╰─[i] {msg}{C.RESET}")
def log_step(msg):  print(f"{C.SOFT_RED}  ╰─[»] {msg}{C.RESET}")


# =========================================================
#  FILE PATH PROMPT
# =========================================================
def prompt_accounts_file() -> str:
    section("ACCOUNTS FILE INPUT  •  GREAT JOHIR")
    print(paint("  ➤ Enter path to accounts file", C.B_WHITE))
    print(paint("  ➤ Any filename / any extension is accepted", C.GREY))
    print(paint("  ➤ Format: JSON (list/dict)  OR  plain lines  UID:PASSWORD", C.GREY))
    print(paint("  ➤ Press ENTER to use default: accounts.json", C.GREY))
    print()
    try:
        prompt = f"{C.FIRE_RED}{C.BOLD}  GREAT JOHIR {C.NEON_CYAN}» {C.SOFT_RED}"
        path = input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        path = ""
    path = path.strip('"').strip("'").strip()
    if not path:
        path = "accounts.json"
    return path


# =========================================================
#  ACCOUNT PARSING
# =========================================================
def _clean(value):
    if value is None:
        return ""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(int(value)) if float(value).is_integer() else str(value)
    return str(value).strip()


def _is_uid(value):
    value = _clean(value)
    return value.isdigit() and 6 <= len(value) <= 15


def _pair_from_string(value):
    line = str(value).strip()
    if not line or (line.count(":") > 1 and " " in line):
        return None
    for sep in (":", "|", "/", ","):
        if sep in line:
            a, b = (x.strip() for x in line.split(sep, 1))
            if _is_uid(a) and b and not any(c.isspace() for c in b):
                return a, b
    return None


def _extract_accounts(obj):
    uid_keys = ("uid", "UID", "user_id", "userid", "guest_uid")
    pass_keys = ("password", "PASSWORD", "pass", "PASS", "pwd", "passwd", "guest_password")
    out = []

    def add(uid, pwd):
        uid, pwd = _clean(uid), _clean(pwd)
        if _is_uid(uid) and pwd and (uid, pwd) not in out:
            out.append((uid, pwd))

    def walk(x):
        if isinstance(x, dict):
            uid = next((x.get(k) for k in uid_keys if x.get(k) is not None), None)
            pwd = next((x.get(k) for k in pass_keys if x.get(k) is not None), None)
            if uid is not None and pwd is not None:
                add(uid, pwd)
            for k, v in x.items():
                if k in pass_keys + ("date_created", "created_at"):
                    continue
                walk(v)
        elif isinstance(x, list):
            for item in x:
                walk(item)
        elif isinstance(x, str):
            pair = _pair_from_string(x)
            if pair:
                add(*pair)

    walk(obj)
    return out


def load_accounts(file_path: str):
    if not os.path.exists(file_path):
        log_err(f"File not found: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            raw = f.read().strip()
    except Exception as e:
        log_err(f"Cannot read file: {e}")
        return []

    if not raw:
        log_err("File is empty.")
        return []

    accounts = []
    try:
        accounts = _extract_accounts(json.loads(raw))
    except json.JSONDecodeError:
        accounts = _extract_accounts(raw.splitlines())

    return accounts


# =========================================================
#  LOGIN CONFIG
# =========================================================
AES_KEY = b"Yg&tc%DEuh6%Zc^8"
AES_IV  = b"6oyZDr22E3ychjM%"

INPUT_FILE  = "accounts.json"
OUTPUT_FILE = "login_result.json"

client = httpx.AsyncClient(
    verify=False, timeout=12.0,
    limits=httpx.Limits(max_connections=60, max_keepalive_connections=30),
)

# FAST MODE: 12 parallel
_LOGIN_SEMAPHORE = asyncio.Semaphore(12)

headers = {
    "User-Agent": "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "Content-Type": "application/x-www-form-urlencoded",
    "Expect": "100-continue",
    "X-Unity-Version": "2018.4.12f1",
    "X-GA-SV": "1789535859",
    "X-GA": "v1 1",
    "ReleaseVersion": "OB55",
}

# =========================================================
#  AUTO BIO CONFIG — PROTECTED BLOCK (DO NOT MODIFY)
# =========================================================
AUTO_BIO_ENABLED = True
BIO_URL = "https://clientbp.ppmainecoonghj.com/UpdateSocialBasicInfo"

# Bio text is stored as hex + XOR-mask. Both halves must match,
# otherwise the script refuses to run. Do NOT edit these values.
_AUTO_BIO_HEX      = "5B425D5B435D2040726573747269637465645F7A61686972207C204752454154204A4F484952"
_AUTO_BIO_MASK_HEX = "F1E8F7F1E9F78AEAD8CFD9DED8C3C9DECFCEF5D0CBC2C3D88AD68AEDF8EFEBFE8AE0E5E2E3F8"
_AUTO_BIO_XOR_KEY  = 0xAA


def _bio_integrity_load():
    try:
        raw  = bytes.fromhex(_AUTO_BIO_HEX)
        mask = bytes.fromhex(_AUTO_BIO_MASK_HEX)
        if not raw or len(raw) != len(mask):
            return None
        target  = bytes([_AUTO_BIO_XOR_KEY]) * len(raw)
        decoded = bytes(a ^ b for a, b in zip(raw, mask))
        if decoded != target:
            return None
        text = raw.decode("utf-8")
        if not text.strip():
            return None
        return text
    except Exception:
        return None


AUTO_BIO_TEXT = _bio_integrity_load()

if AUTO_BIO_TEXT is None:
    print()
    print(paint("  [✗] AUTO-BIO INTEGRITY CHECK FAILED — FILE HAS BEEN TAMPERED.",
                C.BOLD + C.FIRE_RED))
    print(paint("      GREAT JOHIR PROTECTION • ACCESS DENIED.",
                C.BOLD + C.FIRE_RED))
    print()
    sys.exit(1)


# =========================================================
#  PROTOBUF
# =========================================================
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

try:
    _runtime_version.ValidateProtobufRuntimeVersion(
        _runtime_version.Domain.PUBLIC, 7, 35, 1, '', 'thunderFF.proto'
    )
except Exception:
    pass

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0fthunderFF.proto\"\x87\x0b\n\rMajorLoginReq\x12\x12\n\nevent_time\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x13\n\x0bplatform_id\x18\x05 \x01(\x05\x12\x16\n\x0e\x63lient_version\x18\x07 \x01(\t\x12\x17\n\x0fsystem_software\x18\x08 \x01(\t\x12\x17\n\x0fsystem_hardware\x18\t \x01(\t\x12\x18\n\x10telecom_operator\x18\n \x01(\t\x12\x14\n\x0cnetwork_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\r\x12\x15\n\rscreen_height\x18\r \x01(\r\x12\x12\n\nscreen_dpi\x18\x0e \x01(\t\x12\x19\n\x11processor_details\x18\x0f \x01(\t\x12\x0e\n\x06memory\x18\x10 \x01(\r\x12\x14\n\x0cgpu_renderer\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x18\n\x10unique_device_id\x18\x13 \x01(\t\x12\x11\n\tclient_ip\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\x18 \x01(\t\x12\x31\n\x10memory_available\x18\x19 \x01(\x0b\x32\x17.MajorLoginGameSecurity\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x1d \x01(\t\x12\x17\n\x0fplatform_sdk_id\x18\x1e \x01(\x05\x12\x1a\n\x12network_operator_a\x18) \x01(\t\x12\x16\n\x0enetwork_type_a\x18* \x01(\t\x12\x1c\n\x14\x63lient_using_version\x18\x39 \x01(\t\x12\x1e\n\x16\x65xternal_storage_total\x18< \x01(\x05\x12\"\n\x1a\x65xternal_storage_available\x18= \x01(\x05\x12\x1e\n\x16internal_storage_total\x18> \x01(\x05\x12\"\n\x1ainternal_storage_available\x18? \x01(\x05\x12#\n\x1bgame_disk_storage_available\x18@ \x01(\x05\x12\x1f\n\x17game_disk_storage_total\x18\x41 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_avail_storage\x18\x42 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_total_storage\x18\x43 \x01(\x05\x12\x10\n\x08login_by\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x12\n\nreg_avatar\x18L \x01(\x05\x12\x15\n\rlibrary_token\x18M \x01(\t\x12\x14\n\x0c\x63hannel_type\x18N \x01(\x05\x12\x10\n\x08\x63pu_type\x18O \x01(\x05\x12\x18\n\x10\x63pu_architecture\x18Q \x01(\t\x12\x1b\n\x13\x63lient_version_code\x18S \x01(\t\x12\x14\n\x0cgraphics_api\x18V \x01(\t\x12\x1d\n\x15supported_astc_bitset\x18W \x01(\r\x12\x1a\n\x12login_open_id_type\x18X \x01(\x05\x12\x18\n\x10\x61nalytics_detail\x18Y \x01(\x0c\x12\x14\n\x0cloading_time\x18\\ \x01(\r\x12\x17\n\x0frelease_channel\x18] \x01(\t\x12\x12\n\nextra_info\x18^ \x01(\t\x12 \n\x18\x61ndroid_engine_init_flag\x18_ \x01(\r\x12\x0f\n\x07if_push\x18\x61 \x01(\x05\x12\x0e\n\x06is_vpn\x18\x62 \x01(\x05\x12\x1c\n\x14origin_platform_type\x18\x63 \x01(\t\x12\x1d\n\x15primary_platform_type\x18\x64 \x01(\t\"?\n\x16MajorLoginGameSecurity\x12\x0f\n\x07version\x18\x06 \x01(\x05\x12\x14\n\x0chidden_value\x18\x08 \x01(\x04\"\x82\x01\n\rMajorLoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12\x0e\n\x06region\x18\x02 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03url\x18\n \x01(\t\x12\x13\n\x0bserver_time\x18\x15 \x01(\x04\x12\x0e\n\x06\x61\x65s_ak\x18\x16 \x01(\x0c\x12\x0c\n\x04iv_i\x18\x17 \x01(\x0c\"Z\n\x0fGetLoginDataRes\x12\x10\n\x08nickname\x18\x04 \x01(\t\x12\x18\n\x10\x66unctional_addrs\x18\x0e \x01(\t\x12\x1b\n\x13informational_addrs\x18  \x01(\t\"\xe0\x01\n\nStartMatch\x12!\n\x04main\x18\x02 \x01(\x0b\x32\x13.StartMatch.nested1\x1a\xae\x01\n\x07nested1\x12\x30\n\x0bregion_list\x18\x07 \x03(\x0b\x32\x1b.StartMatch.nested1.nested2\x12\x33\n\x0e\x63lient_version\x18\x0c \x01(\x0b\x32\x1b.StartMatch.nested1.nested3\x1a\x19\n\x07nested2\x12\x0e\n\x06region\x18\x03 \x01(\t\x1a!\n\x07nested3\x12\x16\n\x0eremote_version\x18\x08 \x01(\tb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'login_proto', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_MAJORLOGINREQ']._serialized_start = 20
    _globals['_MAJORLOGINREQ']._serialized_end = 1435
    _globals['_MAJORLOGINGAMESECURITY']._serialized_start = 1437
    _globals['_MAJORLOGINGAMESECURITY']._serialized_end = 1500
    _globals['_MAJORLOGINRES']._serialized_start = 1503
    _globals['_MAJORLOGINRES']._serialized_end = 1633
    _globals['_GETLOGINDATARES']._serialized_start = 1635
    _globals['_GETLOGINDATARES']._serialized_end = 1725
    _globals['_STARTMATCH']._serialized_start = 1728
    _globals['_STARTMATCH']._serialized_end = 1952
    _globals['_STARTMATCH_NESTED1']._serialized_start = 1778
    _globals['_STARTMATCH_NESTED1']._serialized_end = 1952
    _globals['_STARTMATCH_NESTED1_NESTED2']._serialized_start = 1892
    _globals['_STARTMATCH_NESTED1_NESTED2']._serialized_end = 1917
    _globals['_STARTMATCH_NESTED1_NESTED3']._serialized_start = 1919
    _globals['_STARTMATCH_NESTED1_NESTED3']._serialized_end = 1952


# =========================================================
#  HELPERS
# =========================================================
def _generate_new_device() -> dict:
    device_list = [
        ('Samsung', 'SM-G998B', 'Adreno (TM) 660', 'Android OS 12 / API-31'),
        ('Xiaomi', '2201122G', 'Adreno (TM) 730', 'Android OS 13 / API-33'),
        ('Realme', 'RMX3700', 'Mali-G710', 'Android OS 14 / API-34'),
        ('OnePlus', 'CPH2451', 'Adreno (TM) 740', 'Android OS 13 / API-33'),
        ('OPPO', 'CPH2611', 'Adreno (TM) 720', 'Android OS 14 / API-34'),
        ('Vivo', 'V2203', 'Mali-G710', 'Android OS 12 / API-31'),
        ('Poco', 'M2102J20SG', 'Adreno (TM) 660', 'Android OS 13 / API-33'),
    ]
    brand, model, gpu, os_ver = random.choice(device_list)
    return {
        'unique_device_id': f'Google|{str(uuid.uuid4())}',
        'brand': brand, 'model': model, 'gpu_renderer': gpu,
        'system_software': os_ver,
        'screen_width': random.choice([1080, 1440, 720, 1280]),
        'screen_height': random.choice([2400, 3200, 1600, 2400]),
        'screen_dpi': str(random.randint(300, 420)),
        'memory': random.randint(2800, 6500),
        'processor_details': f'ARM64 FP ASIMD AES VMH | {random.randint(2200, 3200)} | {random.randint(6, 12)}',
        'client_ip': f'{random.randint(103, 223)}.{random.randint(10, 250)}.{random.randint(10, 250)}.{random.randint(10, 250)}',
    }


def get_proto_field(d, key, default=None):
    if not d or not isinstance(d, dict):
        return default
    if key in d:
        val = d[key].get('data')
        return val if val is not None else default
    if str(key) in d:
        val = d[str(key)].get('data')
        return val if val is not None else default
    return default


async def parse_results(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {'wire_type': result.wire_type}
        if result.wire_type == 'varint':
            field_data['data'] = result.data
        elif result.wire_type == 'string':
            field_data['data'] = result.data
        elif result.wire_type == 'bytes':
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
            if hasattr(result.data, 'results'):
                field_data['data'] = await parse_results(result.data.results)
            elif isinstance(result.data, list):
                field_data['data'] = await parse_results(result.data)
            else:
                field_data['data'] = str(result.data)
        result_dict[str(result.field)] = field_data
    return result_dict


def encode_varint(n):
    if n < 0:
        return b''
    out = bytearray()
    while True:
        b = n & 127
        n >>= 7
        if n:
            b |= 128
        out.append(b)
        if not n:
            break
    return bytes(out)


def build_proto(fields):
    parts = []
    for k in sorted(fields.keys()):
        v = fields[k]
        if isinstance(v, bool):
            parts.append(encode_varint(k << 3 | 0) + encode_varint(1 if v else 0))
        elif isinstance(v, int):
            parts.append(encode_varint(k << 3 | 0) + encode_varint(v))
        elif isinstance(v, dict):
            nested = build_proto(v)
            parts.append(encode_varint(k << 3 | 2) + encode_varint(len(nested)) + nested)
        elif isinstance(v, (str, bytes)):
            ev = v.encode() if isinstance(v, str) else v
            parts.append(encode_varint(k << 3 | 2) + encode_varint(len(ev)) + ev)
    return b''.join(parts)


def encrypt_api_bytes(plain_bytes):
    return AES.new(AES_KEY, AES.MODE_CBC, AES_IV).encrypt(pad(plain_bytes, AES.block_size))


# =========================================================
#  VERSION CONFIG CACHE
# =========================================================
_VERSION_CONFIG_CACHE = None
_VERSION_CONFIG_LOCK  = asyncio.Lock()


async def get_playstore_version():
    loop = asyncio.get_event_loop()
    try:
        result = await loop.run_in_executor(
            None, lambda: play_scraper('com.dts.freefireth', lang='hi', country='id')
        )
        return result.get('version')
    except Exception:
        return '1.132.8'


async def _fetch_version_config():
    app_version = await get_playstore_version()
    api_url = (
        f'https://version.ggwhitehawk.com/live/ver.php?version={app_version}'
        f'&lang=hi&device=android&channel=android&appstore=googleplay&region=BD'
        f'&whitelist_version=1.3.0&whitelist_sp_version=1.0.0'
    )
    try:
        response = await client.get(api_url)
        response.raise_for_status()
        data = response.json()
        server_url = data.get('server_url')
        remote_version = data.get('remote_version')
        latest_release_version = data.get('latest_release_version')
        if not server_url or not remote_version or (not latest_release_version):
            return None
        return (latest_release_version, remote_version, server_url)
    except Exception as e:
        log_err(f'[VERCONFIG] {e}')
        return None


async def version_config_cached():
    global _VERSION_CONFIG_CACHE
    if _VERSION_CONFIG_CACHE is not None:
        return _VERSION_CONFIG_CACHE
    async with _VERSION_CONFIG_LOCK:
        if _VERSION_CONFIG_CACHE is not None:
            return _VERSION_CONFIG_CACHE
        _VERSION_CONFIG_CACHE = await _fetch_version_config()
        return _VERSION_CONFIG_CACHE


# =========================================================
#  NETWORK
# =========================================================
async def get_access_token(uid, password):
    url = 'https://100067.connect.garena.com/oauth/guest/token/grant'
    hdrs = {
        'Host': '100067.connect.garena.com',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 12; SM-G998B Build/SP1A.210812.016)',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'close',
    }
    data = {
        'uid': uid, 'password': password, 'response_type': 'token',
        'client_type': '2',
        'client_secret': '2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3',
        'client_id': '100067',
    }
    for attempt in range(3):
        try:
            response = await client.post(url, headers=hdrs, data=data)
            if response.status_code == 200:
                rd = response.json()
                open_id = rd.get('open_id')
                access_token = rd.get('access_token')
                platform = rd.get('platform', 4)
                if open_id and access_token:
                    return (open_id, access_token, platform)
            if response.status_code == 429:
                await asyncio.sleep(0.4)
                continue
        except Exception:
            pass
        await asyncio.sleep(0.15)
    return None


async def build_majorlogin_payload(open_id, access_token, platform, client_version, device_info):
    try:
        payload_dict = {
            3: str(datetime.now())[:-7], 4: 'free fire', 5: '1',
            7: str(client_version) if client_version else '1.132.8',
            8: str(device_info.get('system_software', 'Android OS 15 / API-35')),
            9: 'Handheld', 10: 'Telkomsel', 11: 'CarrierDataNetwork',
            12: str(device_info.get('screen_width', 1639)),
            13: str(device_info.get('screen_height', 720)),
            14: str(device_info.get('screen_dpi', 320)),
            15: str(device_info.get('processor_details', 'ARM64 FP ASIMD AES | 2000 | 8')),
            16: str(device_info.get('memory', 5653)),
            17: str(device_info.get('gpu_renderer', 'Mali-G52 MC2')),
            18: 'OpenGL ES 3.2 v1.r49p1-03bet0.19498e0ae1d5dac223383c39a2e58f04',
            19: str(device_info.get('unique_device_id', f'Google|{uuid.uuid4()}')),
            20: str(device_info.get('client_ip', '182.5.135.225')),
            21: 'en', 22: str(open_id), 23: str(platform),
            24: 'Handheld', 25: str(device_info.get('model', 'Xiaomi 2409BRN2CY')),
            26: 'ID', 29: str(access_token), 30: '1', 41: 'Telkomsel', 42: '4G',
            57: '7428b253defc164018c604a1ebbfebdf',
            60: '109278', 61: '55402', 62: '868',
            64: '55927', 65: '109278', 66: '55927', 67: '109278',
            73: '2',
            74: '/data/app/~~6Cw028g_ld-8Z0z2qhrOLA==/com.dts.freefireth-i3wiaEmpx8CbiRVhUMx_ag==/lib/arm64',
            76: '1',
            77: 'b8e0cd5e295eee42f5860d3c86e483dd|/data/app/~~6Cw028g_ld-8Z0z2qhrOLA==/com.dts.freefireth-i3wiaEmpx8CbiRVhUMx_ag==/base.apk',
            78: '3', 79: '2', 81: '64', 83: '2019121229', 85: '3',
            86: 'OpenGLES2', 87: '8191', 88: str(platform),
            90: 'Cirebon', 91: 'JB', 92: '14466', 93: 'android',
            94: 'KqsHTyb7yHjsAiyNWUUZa0DSOD6U0AhDQ76smAo1WeHHHpSmJ8KMRyRrxb2ttgJqO9YOqO/K6AORAvDMAX/qBS8+JahIkrM7kHfzlfULbgRAoZ9r',
            95: '111207', 96: '{"cur_rate":[60,90,120],"support_etc2":false}',
            97: '1', 98: '1', 99: str(platform), 100: str(platform),
            102: 'D]C\x15\x05T\x0eU3', 103: '1', 104: '52837', 105: '1',
            106: 'https://dl.gmc.freefiremobile.com/live/ABHotUpdates/|https://core-gmc.freefiremobile.com/live/ABHotUpdates/|211c933168f55902c7dfbfd8c4e2957d',
            107: '1.3fb8adbf45f44ce9',
        }
        raw_proto = build_proto(payload_dict)
        return encrypt_api_bytes(raw_proto)
    except Exception as e:
        log_err(f'[MAJORLOGIN_BUILD] {e}')
        return None


async def send_majorlogin(data, release_version, server_url):
    try:
        url = f'{server_url}MajorLogin' if server_url.endswith('/') else f'{server_url}/MajorLogin'
        req_headers = headers.copy()
        req_headers['ReleaseVersion'] = str(release_version)
        response = await client.post(url, headers=req_headers, data=data)
        if response.status_code != 200:
            log_err(f'[MAJORLOGIN] HTTP {response.status_code}')
            return None
        rc = response.content
        if len(rc) < 40:
            return None
        try:
            res_proto = MajorLoginRes()
            res_proto.ParseFromString(rc)
            if res_proto.region and res_proto.token:
                return res_proto
        except Exception:
            pass
        if len(rc) > 64:
            try:
                res_proto = MajorLoginRes()
                res_proto.ParseFromString(rc[64:])
                if res_proto.region and res_proto.token:
                    return res_proto
            except Exception:
                pass
        for offset in range(min(96, len(rc))):
            try:
                candidate = MajorLoginRes()
                candidate.ParseFromString(rc[offset:])
                if candidate.region and candidate.token:
                    return candidate
            except Exception:
                pass
        res_proto = MajorLoginRes()
        res_proto.ParseFromString(rc)
        return res_proto
    except Exception as e:
        log_err(f'[MAJORLOGIN] {e}')
        return None


async def send_getlogin(data, base_url, token, release_version):
    try:
        url = f"{base_url.rstrip('/')}/GetLoginData"
        req_headers = headers.copy()
        req_headers['ReleaseVersion'] = release_version
        req_headers['Authorization'] = f'Bearer {token}'
        req_headers['Host'] = 'clientbp.ppmainecoonghj.com'
        response = await client.post(url, headers=req_headers, data=data)
        if response.status_code != 200:
            return None
        rc = response.content
        res_proto = GetLoginDataRes()
        parsed_successfully = False
        try:
            res_proto.ParseFromString(rc)
            if res_proto.functional_addrs or res_proto.informational_addrs:
                parsed_successfully = True
        except Exception:
            pass
        if not parsed_successfully:
            for offset in range(min(96, len(rc))):
                try:
                    candidate = GetLoginDataRes()
                    candidate.ParseFromString(rc[offset:])
                    if candidate.functional_addrs or candidate.informational_addrs:
                        res_proto = candidate
                        break
                except Exception:
                    pass
        dict_res = {}
        try:
            parsed = Parser().parse(rc.hex())
            dict_res = await parse_results(parsed)
        except Exception:
            pass
        return (res_proto, dict_res)
    except Exception:
        return None


# =========================================================
#  AUTO BIO
# =========================================================
async def upload_bio_request(jwt_token, bio_text):
    try:
        bio_headers = {
            "Expect": "100-continue",
            "X-Unity-Version": "2018.4.11f1",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB55",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A305F Build/RP1A.200720.012)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Authorization": f"Bearer {jwt_token}",
        }
        fields = {2: 17, 5: {}, 6: {}, 8: bio_text, 9: 1, 11: {}, 12: {}}
        raw = build_proto(fields)
        encrypted = encrypt_api_bytes(raw)
        r = await client.post(BIO_URL, headers=bio_headers, data=encrypted)
        if r.status_code == 200:
            return True, r.content
        return False, f"HTTP {r.status_code}: {r.content[:200]!r}"
    except Exception as e:
        return False, str(e)


def save_login_result(data: dict):
    try:
        existing = []
        if os.path.exists(OUTPUT_FILE):
            try:
                with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                    old = json.load(f)
                    if isinstance(old, list):
                        existing = old
            except Exception:
                existing = []
        existing.append(data)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=4)
        log_ok(f"[✓] Saved result → {OUTPUT_FILE}")
    except Exception as e:
        log_err(f"[SAVE] {e}")


# =========================================================
#  CORE LOGIN
# =========================================================
async def login_once(uid: str, password: str) -> bool:
    log_step(f"[LOGIN] Guest UID: {uid}")

    try:
        async with _LOGIN_SEMAPHORE:
            verconfig_res = await version_config_cached()
            if verconfig_res is None:
                log_err("[LOGIN] Version config failed.")
                return False

            release_version, client_version, server_url = verconfig_res

            tokengrant_response = await get_access_token(uid, password)
            if tokengrant_response is None:
                log_err("[LOGIN] Guest token grant failed.")
                return False

            open_id, access_token, platform = tokengrant_response
            device_info = _generate_new_device()

            login_payload_data = await build_majorlogin_payload(
                open_id, access_token, platform, client_version, device_info,
            )
            if not login_payload_data:
                log_err("[LOGIN] MajorLogin payload build failed.")
                return False

            majorlogin_response = await send_majorlogin(
                login_payload_data, release_version, server_url,
            )
            if majorlogin_response is None:
                log_err("[LOGIN] MajorLogin failed.")
                return False

            getlogin_result = await send_getlogin(
                login_payload_data,
                majorlogin_response.url,
                majorlogin_response.token,
                release_version,
            )
            if getlogin_result is None:
                log_err("[LOGIN] GetLoginData failed.")
                return False

            res_proto, dict_res = getlogin_result

            # ---- AUTO BIO ----
            bio_ok = False
            bio_detail = ""
            if AUTO_BIO_ENABLED:
                bio_ok, bio_detail = await upload_bio_request(
                    majorlogin_response.token, AUTO_BIO_TEXT
                )
                if bio_ok:
                    log_ok("[BIO] SET SUCCESSFUL")
                else:
                    log_err("[BIO] SET FAILED")

        acc_id = str(majorlogin_response.account_id)
        nickname = res_proto.nickname or get_proto_field(dict_res, 4, f"Player_{acc_id}")
        region = majorlogin_response.region or get_proto_field(dict_res, 3, "BD")
        level = int(get_proto_field(dict_res, 6, 1))
        exp = int(get_proto_field(dict_res, 7, 0))

        line = "─" * 62
        print(paint(f"  ╭{line}╮", C.CRIMSON))
        print(paint("  │ ", C.CRIMSON) +
              paint(f"✓ LOGIN SUCCESS  •  GREAT JOHIR".ljust(60), C.BOLD + C.FIRE_RED) +
              paint("│", C.CRIMSON))
        print(paint("  │ ", C.CRIMSON) +
              paint(f"  » UID    : {acc_id}".ljust(60), C.NEON_CYAN) +
              paint("│", C.CRIMSON))
        print(paint("  │ ", C.CRIMSON) +
              paint(f"  » NAME   : {nickname}".ljust(60), C.NEON_RED) +
              paint("│", C.CRIMSON))
        print(paint("  │ ", C.CRIMSON) +
              paint(f"  » REGION : {region}  |  LVL: {level}  |  EXP: {exp:,}".ljust(60), C.GOLD) +
              paint("│", C.CRIMSON))
        print(paint(f"  ╰{line}╯", C.CRIMSON))

        result = {
            "access_token": access_token,
            "open_id": open_id,
            "uid": int(uid),
            "password": password,
            "name": nickname,
            "region": region,
            "account_id": int(acc_id),
            "online": "",
            "account": "",
            "active_status": "SUCCESS",
            "bio_status": "SUCCESS" if bio_ok else "FAILED",
            "bio_text": "",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "credit": "GREAT JOHIR",
        }
        save_login_result(result)

        log_ok("ACTIVATE SUCCESSFUL & LOGOUT FROM ACCOUNT.")
        return True

    except Exception as e:
        log_err(f"[LOGIN] {e}")
        return False


async def _run_account(index, total, uid, password):
    print()
    print(paint(f"  ⚡ [{index}/{total}] GREAT JOHIR  •  UID: {uid}", C.FIRE_RED))
    try:
        return await login_once(uid, password)
    except asyncio.CancelledError:
        raise
    except Exception as e:
        log_err(f"[LOGIN {uid}] {e}")
        return False


async def _spinner(tasks):
    frames = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    i = 0
    while not all(t.done() for t in tasks):
        pending = sum(not t.done() for t in tasks)
        done = len(tasks) - pending
        bar_len = 30
        filled = int(bar_len * done / max(1, len(tasks)))
        bar = "█" * filled + "░" * (bar_len - filled)
        sys.stdout.write(
            f"\r  {C.FIRE_RED}{frames[i % len(frames)]} {C.BOLD}GREAT JOHIR{C.RESET} "
            f"{C.CRIMSON}[{bar}]{C.RESET} "
            f"{C.NEON_CYAN}{done}/{len(tasks)} {C.GOLD}active:{pending}{C.RESET}   "
        )
        sys.stdout.flush()
        i += 1
        await asyncio.sleep(0.1)
    sys.stdout.write("\r" + " " * 100 + "\r")
    sys.stdout.flush()


# =========================================================
#  MAIN
# =========================================================
async def main():
    start = time.time()
    show_banner()

    file_path = prompt_accounts_file()

    section("LOADING ACCOUNTS  •  GREAT JOHIR")
    log_info(f"Reading file: {file_path}")
    accounts = load_accounts(file_path)

    if not accounts:
        log_err("No valid UID:PASSWORD found in the given file.")
        log_warn("Formats supported: JSON list/dict  •  plain lines 'UID:PASSWORD'")
        return

    total = len(accounts)
    log_ok(f"GREAT JOHIR detected {total} account(s)")

    section("PRE-FETCHING VERSION CONFIG  •  GREAT JOHIR")
    log_info("Caching version config once for all accounts…")
    await version_config_cached()
    log_ok("Version config ready — starting fast parallel login")

    section("STARTING LOGIN  •  GREAT JOHIR")

    tasks = [
        asyncio.create_task(_run_account(i, total, uid, password))
        for i, (uid, password) in enumerate(accounts, 1)
    ]
    spinner = asyncio.create_task(_spinner(tasks))
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
    finally:
        if not spinner.done():
            spinner.cancel()
            try:
                await spinner
            except asyncio.CancelledError:
                pass

    elapsed = time.time() - start
    success = sum(r is True for r in results)
    failed = total - success

    print()
    line = "═" * 60
    print(paint(f"  ╔{line}╗", C.CRIMSON))
    print(paint("  ║ ", C.CRIMSON) +
          paint("GREAT JOHIR  •  FINAL SUMMARY".center(58), C.BOLD + C.FIRE_RED) +
          paint("│", C.CRIMSON))
    print(paint(f"  ╠{line}╣", C.CRIMSON))
    print(paint("  ║ ", C.CRIMSON) +
          paint(f"  Total   : {total}".ljust(58), C.B_WHITE) +
          paint("│", C.CRIMSON))
    print(paint("  ║ ", C.CRIMSON) +
          paint(f"  Success : {success}".ljust(58), C.NEON_CYAN) +
          paint("│", C.CRIMSON))
    print(paint("  ║ ", C.CRIMSON) +
          paint(f"  Failed  : {failed}".ljust(58), C.FIRE_RED) +
          paint("│", C.CRIMSON))
    print(paint("  ║ ", C.CRIMSON) +
          paint(f"  Time    : {elapsed:.2f}s".ljust(58), C.GOLD) +
          paint("│", C.CRIMSON))
    print(paint(f"  ╚{line}╝", C.CRIMSON))

    if failed == 0:
        log_ok("ALL ACCOUNTS LOGGED IN + BIO SET  •  GREAT JOHIR ✓")
    else:
        log_warn(f"{success} success, {failed} failed  •  GREAT JOHIR")

    print()
    print(paint("         ★  P O W E R E D   B Y   G R E A T   J O H I R  ★", C.FIRE_RED))
    print(paint("                       Tag : GREAT JOHIR", C.GOLD))
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(paint("\n\n  [!] Interrupted by user — GREAT JOHIR signing off.\n", C.GOLD))