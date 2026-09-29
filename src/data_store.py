"""
DataStore (Data Access Layer)
=============================
รับผิดชอบการอ่าน/เขียนไฟล์ทั้งหมด:
- โหลดกฎพาเลตสีจาก palette_rules.json (ระบบเป็นแบบ data-driven แก้สี/กฎได้โดยไม่แตะโค้ด)
- บันทึก/อ่านประวัติผลการวิเคราะห์ (Data Persistence)
"""

import json
import os


class DataStore:
    def __init__(self, data_dir="data", output_dir="output"):
        self.data_dir = data_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _data_path(self, filename):
        return os.path.join(self.data_dir, filename)

    def _output_path(self, filename):
        return os.path.join(self.output_dir, filename)

    # ---------- โหลดกฎพาเลต ----------
    def load_rules(self, filename="palette_rules.json"):
        """อ่านกฎพาเลตจากไฟล์ JSON; ถ้าอ่านไม่ได้ ให้ยกข้อผิดพลาดที่สื่อความหมาย"""
        try:
            with open(self._data_path(filename), "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"ไม่พบไฟล์กฎพาเลต: {self._data_path(filename)}")
        except json.JSONDecodeError as e:
            raise ValueError(f"ไฟล์กฎพาเลตไม่ใช่ JSON ที่ถูกต้อง: {e}")

    # ---------- ประวัติผลการวิเคราะห์ ----------
    def load_history(self, filename="history.json"):
        try:
            with open(self._output_path(filename), "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_analysis(self, result, filename="history.json"):
        """เพิ่มผลการวิเคราะห์ 1 รายการลงไฟล์ประวัติ"""
        history = self.load_history(filename)
        history.append(result.to_dict())
        with open(self._output_path(filename), "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        return self._output_path(filename)
