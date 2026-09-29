"""
NailApp (Presentation Layer)
============================
ส่วนติดต่อผู้ใช้แบบ Command Line — รันได้ทุกที่ (ไม่ผูกกับ Google Colab)
รับ path รูปเล็บ + ทรง + ความยาว -> วิเคราะห์ -> แสดงคำแนะนำ + บันทึกผล

ใช้ได้ 2 แบบ:
  1) โหมดโต้ตอบ:      python main.py
  2) ระบุอาร์กิวเมนต์: python main.py <image_path> <shape> <length>
"""

import os
import cv2 as cv

from .data_store import DataStore
from .skin_analyzer import SkinAnalyzer
from .recommender import NailRecommender, VALID_SHAPES, VALID_LENGTHS
from .palette_renderer import PaletteRenderer
from .api_client import ColorApiClient
from .models import AnalysisResult

MAX_WIDTH = 900  # ย่อรูปให้กว้างสุดเท่านี้เพื่อความเร็ว


class NailApp:
    def __init__(self):
        self.store = DataStore()
        self.analyzer = SkinAnalyzer()
        self.recommender = NailRecommender(self.store.load_rules())
        self.renderer = PaletteRenderer()
        self.api = ColorApiClient()  # External API: ดึงชื่อสีจริงจาก TheColorAPI

    # ---------- helper: รับค่าอย่างปลอดภัย ----------
    @staticmethod
    def _choose(prompt, options, default):
        raw = input(f"{prompt} {options} [{default}]: ").strip().lower()
        if raw == "":
            return default
        if raw in options:
            return raw
        print(f"  ⚠️ '{raw}' ไม่อยู่ในตัวเลือก ใช้ค่าเริ่มต้น '{default}' แทน")
        return default

    def _load_image(self, path):
        """อ่านรูปจากไฟล์ + ย่อขนาด; โยน error ที่สื่อความหมายถ้าอ่านไม่ได้"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"ไม่พบไฟล์รูป: {path}")
        img = cv.imread(path, cv.IMREAD_COLOR)
        if img is None:
            raise ValueError(f"เปิดไฟล์รูปไม่ได้ (ไฟล์อาจไม่ใช่รูปภาพ): {path}")
        if img.shape[1] > MAX_WIDTH:
            scale = MAX_WIDTH / img.shape[1]
            img = cv.resize(img, (MAX_WIDTH, int(img.shape[0] * scale)))
        return img

    # ---------- ขั้นตอนวิเคราะห์หลัก ----------
    def analyze(self, image_path, nail_shape, nail_length, save_history=True):
        """รันทั้งกระบวนการ 1 ครั้ง -> คืน AnalysisResult"""
        img = self._load_image(image_path)

        mask, tone, ita = self.analyzer.analyze(img)
        suggestions = self.recommender.suggest(tone, nail_shape, nail_length)

        result = AnalysisResult(
            image_name=os.path.basename(image_path),
            undertone=tone, ita=ita,
            nail_shape=nail_shape, nail_length=nail_length,
            suggestions=suggestions,
        )

        # บันทึกภาพพาเลตสรุป (Output)
        palette_img = self.store._output_path(
            f"palette_{os.path.splitext(result.image_name)[0]}.png")
        self.renderer.save_summary(suggestions, palette_img)
        self._last_palette_path = palette_img

        if save_history:
            self.store.save_analysis(result)
        return result

    # ---------- แสดงผล ----------
    def _print_result(self, result):
        print("\n==========================================")
        print("   💅 ผลวิเคราะห์และคำแนะนำสีทาเล็บ")
        print("==========================================")
        print(f"📷 ไฟล์: {result.image_name}")
        print(f"🎨 โทนผิวรอบเล็บ (Undertone): {result.undertone}  (ITA ≈ {result.ita:.1f})")
        print(f"💅 ทรงเล็บ: {result.nail_shape} | ความยาว: {result.nail_length}")
        print("------------------------------------------")
        print(f"🎨 คำแนะนำพาเลต/สไตล์ (สูงสุด {self.recommender.max_results}):")
        for i, s in enumerate(result.suggestions, 1):
            # เชื่อม External API เพื่อดึงชื่อสีจริงของแต่ละโค้ดสีในพาเลต
            named = self.api.enrich_palette(s.palette)
            colors_txt = ", ".join(f"{hx} ({name})" for hx, name in named)
            print(f"  {i}. {s.note}")
            print(f"     สี: {colors_txt}")
            print(f"     tags={s.tags}")
        print("------------------------------------------")
        src = "TheColorAPI (ออนไลน์)" if self.api.last_source == "api" else "ข้อมูลสำรอง (fallback)"
        print(f"🌐 แหล่งชื่อสี: {src}")
        print(f"🖼️  บันทึกภาพพาเลตไว้ที่: {self._last_palette_path}")

    # ---------- โหมดโต้ตอบ ----------
    def run(self, argv=None):
        argv = argv or []
        try:
            if len(argv) >= 1:
                image_path = argv[0]
                nail_shape = argv[1] if len(argv) >= 2 else "oval"
                nail_length = argv[2] if len(argv) >= 3 else "medium"
            else:
                print("=== 💅 ระบบแนะนำสีทาเล็บจากโทนผิว ===")
                image_path = input("พิมพ์ path ของรูปเล็บ: ").strip().strip('"')
                nail_shape = self._choose("เลือกทรงเล็บ", VALID_SHAPES, "oval")
                nail_length = self._choose("เลือกความยาว", VALID_LENGTHS, "medium")

            result = self.analyze(image_path, nail_shape, nail_length)
            self._print_result(result)

        except (FileNotFoundError, ValueError) as e:
            print(f"❌ {e}")
        except (KeyboardInterrupt, EOFError):
            raise  # ส่งต่อให้ main.py ปิดโปรแกรมอย่างสุภาพ
        except Exception as e:  # กันพังจากกรณีที่คาดไม่ถึง
            print(f"❌ เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")
