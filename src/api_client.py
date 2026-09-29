"""
ColorApiClient (Business Logic Layer — External API Gateway)
============================================================
เชื่อมต่อ External API: TheColorAPI (https://www.thecolorapi.com) — ฟรี ไม่ต้องมี API key
ส่งโค้ดสี hex ไปเพื่อขอ "ชื่อสีจริง" มาเสริมคำแนะนำพาเลต

หลัก Defensive Programming: ถ้า API ล่ม/ไม่มีเน็ต/timeout จะใช้ชื่อสีสำรอง
(Fallback) แทน โปรแกรมจึงไม่ล่ม 100%
"""

import requests

# ชื่อสีสำรอง (Fallback) สำหรับโค้ดสีที่ใช้ในพาเลต เผื่อ API เรียกไม่ได้
FALLBACK_COLOR_NAMES = {
    "#C3C7FF": "Periwinkle", "#EDEBFF": "Lavender Mist", "#FFB3D1": "Cotton Candy",
    "#9AD0F5": "Baby Blue", "#FFFFFF": "White", "#BFC6D1": "Silver Grey",
    "#E6E6FA": "Lavender", "#FFB6C1": "Light Pink", "#98FF98": "Mint Green",
    "#40E0D0": "Turquoise", "#8B0000": "Dark Red", "#0F52BA": "Sapphire",
    "#C0C0C0": "Silver", "#4B0082": "Indigo", "#800080": "Purple",
    "#F2C6A0": "Peach", "#E8A87C": "Caramel", "#B8860B": "Dark Goldenrod",
    "#FFD700": "Gold", "#6B8E23": "Olive Drab", "#4B5320": "Army Green",
    "#B22222": "Firebrick", "#FFA07A": "Light Salmon", "#FFDB58": "Mustard",
    "#CC5500": "Burnt Orange", "#FF7F50": "Coral", "#FFDAB9": "Peach Puff",
    "#808000": "Olive", "#F5E6DC": "Nude", "#E3C4B5": "Rose Beige",
    "#C00021": "Crimson", "#8B0016": "Dark Crimson", "#FDF5F8": "Snow Pink",
    "#E2D7FF": "Pale Lilac", "#FF0000": "Red", "#800020": "Burgundy",
    "#000080": "Navy", "#50C878": "Emerald", "#483C32": "Taupe",
    "#F5CBA7": "Apricot", "#FADBD8": "Blush", "#36454F": "Charcoal",
    "#808080": "Grey", "#F2EFEA": "Ivory", "#FBE9E7": "Seashell",
    "#FFE0B2": "Light Apricot", "#000000": "Black", "#2E2A2A": "Jet Black",
    "#D4AF37": "Metallic Gold",
}


class ColorApiClient:
    BASE_URL = "https://www.thecolorapi.com/id"

    def __init__(self, timeout=5):
        self.timeout = timeout
        self.last_source = None  # "api" หรือ "fallback" — ไว้บอกผู้ใช้ว่าดึงจากไหน

    def get_color_name(self, hex_code):
        """
        คืนชื่อสีของโค้ด hex — พยายามดึงจาก API ก่อน ถ้าไม่สำเร็จใช้ fallback
        """
        hx = "#" + hex_code.lstrip("#").upper()
        try:
            resp = requests.get(self.BASE_URL,
                                 params={"hex": hx.lstrip("#")},
                                 timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            name = data.get("name", {}).get("value")
            if name:
                self.last_source = "api"
                return name
        except Exception:
            pass  # เงียบไว้แล้วไป fallback (Defensive)

        self.last_source = "fallback"
        return FALLBACK_COLOR_NAMES.get(hx, hx)

    def enrich_palette(self, palette):
        """รับลิสต์โค้ดสี hex → คืนลิสต์ (hex, ชื่อสี)"""
        return [(hx, self.get_color_name(hx)) for hx in palette]
