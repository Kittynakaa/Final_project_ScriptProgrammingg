"""
ระบบแนะนำสีทาเล็บจากโทนผิว (Nail Color Recommender)
===================================================
CP352301 Script Programming — Final Project

วิเคราะห์โทนผิวรอบเล็บจากรูปภาพ (OpenCV, CIE Lab / ITA) แล้วแนะนำพาเลตสีทาเล็บ
ตามโทนผิว + ทรงเล็บ + ความยาวเล็บ

รันด้วย:
    python main.py                                  # โหมดโต้ตอบ
    python main.py hand.jpg oval medium             # ระบุค่าเลย
"""

import sys
from src.cli import NailApp


def main():
    app = NailApp()
    app.run(sys.argv[1:])


if __name__ == "__main__":
    # [Error Resilience] กัน crash เมื่อผู้ใช้กด Ctrl+C / Ctrl+D
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\n👋 ได้รับสัญญาณหยุดการทำงาน — ปิดระบบอย่างปลอดภัย")
