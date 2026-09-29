"""
Domain Models (Business Logic Layer)
====================================
โครงสร้างข้อมูลหลักของระบบแนะนำสีทาเล็บ
"""

from datetime import datetime


class Suggestion:
    """คำแนะนำพาเลตสี 1 ชุด (โค้ดสี + แท็กสไตล์ + คำอธิบาย)"""

    def __init__(self, palette, tags, note):
        self.palette = list(palette)   # ลิสต์โค้ดสี hex เช่น ["#C3C7FF", "#EDEBFF"]
        self.tags = list(tags)         # แท็กสไตล์ เช่น ["pastel", "cool"]
        self.note = note               # คำอธิบายภาษาไทย

    def has_tag(self, keyword):
        """คืน True ถ้าแท็กหรือคำอธิบายมีคำค้น (ไม่สนตัวพิมพ์เล็ก/ใหญ่)"""
        keyword = keyword.lower()
        if keyword in self.note.lower():
            return True
        return any(keyword in t.lower() for t in self.tags)

    def key(self):
        """คีย์เอกลักษณ์สำหรับลบรายการซ้ำ"""
        return tuple(self.palette) + tuple(self.tags)

    def to_dict(self):
        return {"palette": self.palette, "tags": self.tags, "note": self.note}

    def __repr__(self):
        return f"Suggestion(note={self.note!r}, palette={self.palette})"


class AnalysisResult:
    """ผลการวิเคราะห์ 1 ครั้ง (สำหรับแสดงผลและบันทึกประวัติ)"""

    def __init__(self, image_name, undertone, ita, nail_shape, nail_length,
                 suggestions, timestamp=None):
        self.image_name = image_name
        self.undertone = undertone
        self.ita = ita
        self.nail_shape = nail_shape
        self.nail_length = nail_length
        self.suggestions = suggestions          # ลิสต์ของ Suggestion
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "image_name": self.image_name,
            "undertone": self.undertone,
            "ita": round(self.ita, 2),
            "nail_shape": self.nail_shape,
            "nail_length": self.nail_length,
            "suggestions": [s.to_dict() for s in self.suggestions],
        }
