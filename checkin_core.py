"""
签到核心功能 - 从原始Python脚本提取的核心逻辑
适配Android Kivy应用
"""

import requests
import json
import time
import base64
from urllib.parse import quote

# ======================== 配置 ========================
BASE_URL = "https://xsfw.gsupl.edu.cn"
CONTEXT_PATH = "/xsfw"
CRYPTO_KEY = "***"
APPID = "5405362541914944"
APPNAME = "swmzncqapp"

# API 端点
LOGIN_API = f"{BASE_URL}/xsfw/sys/emapfunauth/loginValidate.do"
LOGIN_PAGE = f"{BASE_URL}/xsfw/sys/swmzncqapp/*default/index.do?wxType=1"

# 应用初始化 API
API_GET_ROLES = f"{BASE_URL}/xsfw/sys/swpubapp/NewMobileAPIController/getUserRoles.do"
API_SET_ROLE = f"{BASE_URL}/xsfw/sys/swpubapp/NewMobileAPIController/setAppRole.do"
API_GET_MENU = f"{BASE_URL}/xsfw/sys/swpubapp/NewMobileAPIController/getMenuInfo.do"

# 签到 API
API_GET_KQ_INFO = f"{BASE_URL}/xsfw/sys/swmzncqapp/kqController/getKqInfo.do"
API_ADD_KQ_INFO = f"{BASE_URL}/xsfw/sys/swmzncqapp/kqController/addKqInfo.do"
API_GET_KQLS = f"{BASE_URL}/xsfw/sys/swmzncqapp/kqController/getKqlsList.do"


# ======================== 纯 Python AES-128-ECB 实现 ========================
# 来自原始脚本，略作简化

_SBOX = bytes([
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
])

_RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]


def _xtime(a: int) -> int:
    """GF(2^8) 乘法：乘以 0x02"""
    return ((a << 1) ^ (0x1b if a & 0x80 else 0)) & 0xff


def _pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    """PKCS#7 填充"""
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)


def _key_expansion(key: bytes) -> bytes:
    """AES-128 密钥扩展：16 字节密钥 → 176 字节轮密钥"""
    w = [0] * 44
    
    # 前 4 个字直接从密钥取
    for i in range(4):
        w[i] = int.from_bytes(key[4 * i:4 * i + 4], 'big')

    for i in range(4, 44):
        temp = w[i - 1]
        if i % 4 == 0:
            temp = ((temp << 8) | (temp >> 24)) & 0xffffffff
            temp = (_SBOX[(temp >> 24) & 0xff] << 24 |
                    _SBOX[(temp >> 16) & 0xff] << 16 |
                    _SBOX[(temp >> 8) & 0xff] << 8 |
                    _SBOX[temp & 0xff])
            temp ^= (_RCON[i // 4 - 1] << 24)
        w[i] = w[i - 4] ^ temp

    expanded = bytearray(176)
    for i, word in enumerate(w):
        expanded[4 * i] = (word >> 24) & 0xff
        expanded[4 * i + 1] = (word >> 16) & 0xff
        expanded[4 * i + 2] = (word >> 8) & 0xff
        expanded[4 * i + 3] = word & 0xff
    return bytes(expanded)


def _sub_bytes(state: bytearray) -> None:
    """SubBytes 变换（原地）"""
    for i in range(16):
        state[i] = _SBOX[state[i]]


def _shift_rows(state: bytearray) -> None:
    """ShiftRows 变换（原地，列主序）"""
    state[1], state[5], state[9], state[13] = state[5], state[9], state[13], state[1]
    state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6]
    state[3], state[7], state[11], state[15] = state[15], state[3], state[7], state[11]


def _mix_columns(state: bytearray) -> None:
    """MixColumns 变换（原地）"""
    for col in range(4):
        i = col * 4
        a0, a1, a2, a3 = state[i], state[i + 1], state[i + 2], state[i + 3]

        t0 = _xtime(a0)
        t1 = _xtime(a1)
        t2 = _xtime(a2)
        t3 = _xtime(a3)

        state[i] = t0 ^ t1 ^ a1 ^ a2 ^ a3
        state[i + 1] = a0 ^ t1 ^ t2 ^ a2 ^ a3
        state[i + 2] = a0 ^ a1 ^ t2 ^ t3 ^ a3
        state[i + 3] = t0 ^ a0 ^ a1 ^ a2 ^ t3


def _add_round_key(state: bytearray, expanded_key: bytes, round_num: int) -> None:
    """AddRoundKey 变换（原地）"""
    offset = round_num * 16
    for i in range(16):
        state[i] ^= expanded_key[offset + i]


def _aes_encrypt_block(block: bytes, expanded_key: bytes) -> bytes:
    """AES-128 加密单个 16 字节块"""
    state = bytearray(block)

    _add_round_key(state, expanded_key, 0)

    for r in range(1, 10):
        _sub_bytes(state)
        _shift_rows(state)
        _mix_columns(state)
        _add_round_key(state, expanded_key, r)

    _sub_bytes(state)
    _shift_rows(state)
    _add_round_key(state, expanded_key, 10)

    return bytes(state)


def aes_encrypt_ecb(plain_bytes: bytes, key: str) -> str:
    """
    AES-128-ECB-PKCS7 加密
    参数:
        plain_bytes: 明文字节
        key:         密钥字符串（16 字节）
    返回:
        Base64 编码的密文字符串
    """
    key_bytes = key.encode('utf-8')
    padded = _pkcs7_pad(plain_bytes, 16)
    expanded_key = _key_expansion(key_bytes)

    encrypted = bytearray()
    for i in range(0, len(padded), 16):
        encrypted += _aes_encrypt_block(padded[i:i + 16], expanded_key)

    return base64.b64encode(bytes(encrypted)).decode('utf-8')


class CheckinBot:
    """签到机器人 - 适配Android版本"""
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S901U) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.6099.144 Mobile Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
        })
        self.logged_in = False
        self.app_initialized = False
        self.kq_info = None
        self.role_id = None
        self.login_referer = None
    
    def aes_encrypt(self, plain_text: str) -> str:
        """AES加密（适配Android）"""
        return aes_encrypt_ecb(plain_text.encode('utf-8'), CRYPTO_KEY)
    
    def _post_api(self, url: str, params: dict = None) -> dict:
        """API POST请求"""
        if params is None:
            params = {}
        
        body = "data=" + quote(json.dumps(params, ensure_ascii=False))
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/plain, */*",
            "Referer": self.login_referer or LOGIN_PAGE,
        }
        
        try:
            resp = self.session.post(url, data=body, headers=headers, timeout=30)
            if resp.status_code == 200 and resp.text:
                return resp.json()
            return {}
        except Exception as e:
            print(f"API请求错误: {e}")
            return {}
    
    def login(self) -> bool:
        """登录"""
        try:
            # 访问登录页
            r = self.session.get(LOGIN_PAGE, allow_redirects=True, timeout=30)
            self.login_referer = r.url
            
            # 加密凭据
            login_data = {
                "userName": self.aes_encrypt(self.username),
                "password": self.aes_encrypt(self.password),
                "isWeekLogin": "false"
            }
            
            resp = self.session.post(
                LOGIN_API,
                data=login_data,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": r.url,
                    "Origin": BASE_URL,
                },
                timeout=30
            )
            
            result = resp.json()
            if result.get("validate") == "success":
                self.logged_in = True
                return True
            return False
        except Exception as e:
            print(f"登录错误: {e}")
            return False
    
    def init_app(self) -> bool:
        """初始化应用"""
        try:
            # 获取用户角色
            result = self._post_api(API_GET_ROLES, {"APPID": APPID})
            if result.get("code") != "0":
                return False
            
            roles = result.get("data", [])
            if not roles:
                return False
            
            self.role_id = roles[0].get("ROLEID", "")
            
            # 设置应用角色
            result = self._post_api(API_SET_ROLE, {
                "APPID": APPID,
                "APPNAME": APPNAME,
                "ROLEID": self.role_id,
            })
            if result.get("code") != "0":
                return False
            
            # 获取菜单权限
            result = self._post_api(API_GET_MENU, {"APPNAME": APPNAME})
            if result.get("code") != "0":
                return False
            
            self.app_initialized = True
            return True
        except Exception as e:
            print(f"应用初始化错误: {e}")
            return False
    
    def get_kq_info(self) -> dict:
        """获取考勤信息（适配Android）"""
        try:
            result = self._post_api(API_GET_KQ_INFO)
            if result.get("code") == "0":
                self.kq_info = result.get("data", {})
                return self.kq_info
            return {}
        except Exception as e:
            print(f"获取考勤信息错误: {e}")
            return {}
    
    def do_checkin(self, longitude: float = None, latitude: float = None,
                   address: str = None, location_index: int = 0) -> dict:
        """执行签到（适配Android）"""
        try:
            if not self.kq_info:
                return {"success": False, "msg": "未获取考勤信息"}
            
            config = self.kq_info.get("CONFIG_INFO", {})
            qd = self.kq_info.get("QD_INFO", {})
            dd_list = self.kq_info.get("DD_LIST", [])
            is_qj = self.kq_info.get("IS_QJ", False)
            
            # 检查前置条件
            if is_qj:
                return {"success": True, "msg": "已请假", "skip": True}
            
            if qd.get("hasQd") and not qd.get("hasQdhcq"):
                return {"success": True, "msg": "已签到", "skip": True}
            
            if not dd_list:
                return {"success": False, "msg": "无签到地点"}
            
            # 确定坐标
            if longitude is None or latitude is None:
                idx = max(0, min(location_index, len(dd_list) - 1))
                chosen = dd_list[idx]
                longitude = float(chosen.get("JDZB", 0))
                latitude = float(chosen.get("WDZB", 0))
                address = address or chosen.get("QDDD", f"签到点{idx+1}")
            
            if address is None:
                address = f"GPS({longitude},{latitude})"
            
            # 提交签到
            params = {
                "KQWZXX": address,
                "JDZB": str(longitude),
                "WDZB": str(latitude),
            }
            
            result = self._post_api(API_ADD_KQ_INFO, params)
            
            if result.get("code") == "0":
                return {"success": True, "msg": "签到成功", "data": result.get("data")}
            else:
                msg = result.get("msg", "未知错误")
                return {"success": False, "msg": msg, "raw": result}
        except Exception as e:
            print(f"签到错误: {e}")
            return {"success": False, "msg": f"签到错误: {str(e)}"}
    
    def get_history(self, limit: int = 5) -> list:
        """获取签到历史"""
        try:
            result = self._post_api(API_GET_KQLS, {
                "pageNumber": "1",
                "pageSize": str(limit * 2)
            })
            if result.get("code") == "0":
                data = result.get("data", {})
                rows = data.get("rows", data) if isinstance(data, dict) else []
                if isinstance(rows, list):
                    return rows[:limit]
            return []
        except Exception as e:
            print(f"获取历史错误: {e}")
            return []