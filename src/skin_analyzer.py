"""
SkinAnalyzer (Business Logic Layer)
===================================
ประมวลผลภาพเพื่อ (1) หาบริเวณผิว (skin mask) และ (2) ประเมินโทนผิว (undertone)
ด้วยค่า ITA (Individual Typology Angle) ใน CIE Lab color space
"""

import math
import cv2 as cv
import numpy as np


class SkinAnalyzer:
    # ช่วงสีผิวใน YCrCb (ปรับได้ตามสภาพแสง/กล้อง)
    YCRCB_LOWER = np.array([0, 133, 77], dtype=np.uint8)
    YCRCB_UPPER = np.array([255, 173, 127], dtype=np.uint8)

    # เกณฑ์แบ่ง undertone จากค่า ITA
    ITA_COOL = 28
    ITA_WARM = 10
    MIN_SKIN_PIXELS = 500

    def skin_mask(self, bgr):
        """สร้าง mask บริเวณผิวด้วย threshold YCrCb + morphology + เลือกก้อนใหญ่สุด"""
        ycrcb = cv.cvtColor(bgr, cv.COLOR_BGR2YCrCb)
        mask = cv.inRange(ycrcb, self.YCRCB_LOWER, self.YCRCB_UPPER)

        # ทำความสะอาด: เปิด (ลบ noise) แล้วปิด (อุดรูโหว่)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel, iterations=2)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel, iterations=2)

        # เลือก connected component ที่ใหญ่ที่สุด (สันนิษฐานว่าเป็นมือ)
        num, labels, stats, _ = cv.connectedComponentsWithStats(mask, connectivity=8)
        if num > 1:
            areas = stats[1:, cv.CC_STAT_AREA]
            largest = 1 + int(np.argmax(areas))
            mask = np.where(labels == largest, 255, 0).astype(np.uint8)
        return mask

    def estimate_undertone(self, bgr, skin_mask):
        """
        ประเมิน undertone (cool / warm / neutral) จากค่าเฉลี่ยใน Lab
        คืนค่า (tone, ITA). ถ้าพิกเซลผิวน้อยเกินไปคืน ('unknown', 0.0)
        """
        m = skin_mask > 0
        if int(m.sum()) < self.MIN_SKIN_PIXELS:
            return "unknown", 0.0

        lab = cv.cvtColor(bgr, cv.COLOR_BGR2Lab)
        L = lab[..., 0][m].mean() * (100 / 255.0)   # ปรับสเกล L* เป็น 0-100
        b = (lab[..., 2][m].mean() - 128)           # b*: เหลือง(+)/น้ำเงิน(-)

        ita = math.degrees(math.atan2((L - 50), b if abs(b) > 1e-3 else 1e-3))
        tone = self.classify_ita(ita)
        return tone, ita

    @classmethod
    def classify_ita(cls, ita):
        """แปลงค่า ITA เป็นชื่อ undertone"""
        if ita >= cls.ITA_COOL:
            return "cool"
        elif ita <= cls.ITA_WARM:
            return "warm"
        return "neutral"

    def analyze(self, bgr):
        """สะดวก: คืน (mask, tone, ita) ในครั้งเดียว"""
        mask = self.skin_mask(bgr)
        tone, ita = self.estimate_undertone(bgr, mask)
        return mask, tone, ita
