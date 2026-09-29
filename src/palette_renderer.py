"""
PaletteRenderer (Presentation helper)
=====================================
วาดแถบสีจากโค้ด hex และบันทึกภาพสรุปคำแนะนำเป็นไฟล์ .png
ใช้ตัวอักษร ASCII (โค้ดสี hex) บนภาพเพื่อให้แสดงผลได้โดยไม่ต้องพึ่งฟอนต์ไทย
(คำอธิบายภาษาไทยจะพิมพ์ทางหน้าจอ CLI แทน)
"""

import cv2 as cv
import numpy as np


class PaletteRenderer:
    @staticmethod
    def hex_to_bgr(hx):
        """แปลง #RRGGBB -> (B, G, R)"""
        hx = hx.lstrip("#")
        r = int(hx[0:2], 16)
        g = int(hx[2:4], 16)
        b = int(hx[4:6], 16)
        return (b, g, r)

    @classmethod
    def render_row(cls, palette, width=480, height=70):
        """คืน numpy image (BGR) ของแถบสี 1 แถวจากลิสต์ hex"""
        row = np.ones((height, width, 3), dtype=np.uint8) * 255
        n = max(len(palette), 1)
        sw = width // n
        for i, hx in enumerate(palette):
            x0 = i * sw
            x1 = width if i == n - 1 else (i + 1) * sw
            row[:, x0:x1] = cls.hex_to_bgr(hx)
            # เขียนโค้ดสีกำกับ (ตัวอักษรสีตัดกับพื้นหลัง)
            b, g, r = cls.hex_to_bgr(hx)
            luminance = 0.299 * r + 0.587 * g + 0.114 * b
            text_color = (0, 0, 0) if luminance > 140 else (255, 255, 255)
            cv.putText(row, hx.upper(), (x0 + 8, height - 22),
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv.LINE_AA)
        return row

    @classmethod
    def save_summary(cls, suggestions, out_path, width=480):
        """
        รวมแถบสีของทุกคำแนะนำเป็นภาพเดียวแล้วบันทึกเป็นไฟล์
        คืน path ของไฟล์ที่บันทึก
        """
        row_h, gap, label_h = 70, 14, 26
        block = label_h + row_h + gap
        canvas = np.ones((block * len(suggestions) + gap, width, 3),
                         dtype=np.uint8) * 255
        y = gap
        for idx, s in enumerate(suggestions, 1):
            cv.putText(canvas, f"{idx})", (6, y + 18),
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (30, 30, 30), 2, cv.LINE_AA)
            row = cls.render_row(s.palette, width=width - 40, height=row_h)
            canvas[y + label_h:y + label_h + row_h, 40:40 + row.shape[1]] = row
            y += block
        cv.imwrite(out_path, canvas)
        return out_path
