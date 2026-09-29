# Test Cases — ระบบแนะนำสีทาเล็บจากโทนผิว

ตารางเคสทดสอบฉบับเต็ม (Automated + Manual) ผลล่าสุด: **ผ่านทั้งหมด**

## A. Automated Unit Tests (`pytest`, 15 เคส)

| # | เคสทดสอบ | อินพุต | ผลที่คาดหวัง | สถานะ |
|---|----------|--------|--------------|-------|
| A1 | classify ITA (cool) | ITA = 40 | "cool" | PASSED |
| A2 | classify ITA (warm) | ITA = 5 | "warm" | PASSED |
| A3 | classify ITA (neutral) | ITA = 20 | "neutral" | PASSED |
| A4 | undertone เมื่อไม่มีผิว | ภาพดำล้วน + mask ว่าง | "unknown" | PASSED |
| A5 | hex→BGR (ขาว) | "#FFFFFF" | (255,255,255) | PASSED |
| A6 | hex→BGR (แดง) | "#FF0000" | (0,0,255) | PASSED |
| A7 | hex→BGR ไม่มี # | "000000" | (0,0,0) | PASSED |
| A8 | suggest คืนไม่เกิน max | cool/almond/long | ≤ 6 รายการ | PASSED |
| A9 | oval → ombré ขึ้นก่อน | warm/oval/medium | อันดับ 1 มี tag "ombre" | PASSED |
| A10 | เล็บสั้น → micro-French | neutral/square/short | มี micro-French ใน 6 อันดับ | PASSED |
| A11 | undertone unknown → fallback | unknown/stiletto/long | มีคำแนะนำ ไม่ crash | PASSED |
| A12 | search คำค้น | keyword "pastel" | คืนเฉพาะที่มี pastel | PASSED |
| A13 | filter ตามแท็ก | tag "cool" | คืนเฉพาะแท็ก cool | PASSED |
| A14 | sort ตามจำนวนสี | ชุดคำแนะนำ | เรียงมาก→น้อย | PASSED |
| A15 | dedupe รายการซ้ำ | 2 รายการเหมือนกัน | เหลือ 1 | PASSED |

## B. Manual / Integration Test Cases

| # | เคสทดสอบ | ขั้นตอน | ผลที่คาดหวัง | สถานะ |
|---|----------|---------|--------------|-------|
| B1 | Happy path (E2E) | `python main.py hand.jpg oval medium` | แสดงโทน+ITA, พาเลต 6 ชุด, บันทึก .png/.json | PASSED |
| B2 | เปลี่ยนทรง/ความยาว | `python main.py hand.jpg stiletto long` | คำแนะนำอันดับ 1 เปลี่ยนเป็น statement 3D | PASSED |
| B3 | Input Validation | `python main.py hand.jpg abc xyz` | ใช้ค่าเริ่มต้น (oval/medium) + แจ้งเตือน | PASSED |
| B4 | ไฟล์รูปไม่พบ | `python main.py nofile.jpg` | "❌ ไม่พบไฟล์รูป" ไม่ crash | PASSED |
| B5 | ไฟล์ไม่ใช่รูป | `python main.py notes.txt` | "❌ เปิดไฟล์รูปไม่ได้" ไม่ crash | PASSED |
| B6 | ยกเลิกกลางคัน | กด Ctrl+C / Ctrl+D | "👋 ปิดระบบอย่างปลอดภัย" | PASSED |
| B7 | Data Persistence | รันหลายครั้ง แล้วเปิด history.json | มีบันทึกครบทุกครั้ง | PASSED |

## หมายเหตุ
- เตรียมรูปมือจริง (เช่น `hand.jpg`) ไว้ในโฟลเดอร์โปรเจกต์ก่อนรัน B1–B3, B7
- เคส B4–B6 ใช้แสดงความทนทานต่อข้อผิดพลาด (Error Resilience) ในวันนำเสนอ
