# Sprint Result Report — Sprint 1 & 2

**Project Name:** ระบบแนะนำสีทาเล็บจากโทนผิว (Nail Color Recommender)
**Sprint:** 1 (CLI & OOP Foundation) + 2 (Image Analysis & Core Features)
**Team Members:**
- Planner : ชาคริต อ่วมอ่ำ 
- Coder: อภิสรา นครสุข
- Coder: เมธาวี สิทธิชัยเนตร 
- Debugger: สาริษฐ์ บุตรช่วง

---

## 1. Sprint Progress Summary

**Sprint 1 — Front-End (CLI)**
- [x] กำหนดขอบเขตงานและ Definition of Done ใน `PLAN.md`
- [x] ออกแบบโครง CLI (โหมดโต้ตอบ + โหมดระบุอาร์กิวเมนต์)
- [x] รับค่าและตรวจสอบความถูกต้อง (ทรง/ความยาวต้องอยู่ในตัวเลือก, ตรวจ path รูป)
- [x] จัดการข้อผิดพลาด: ไฟล์ไม่พบ, ไฟล์ไม่ใช่รูป, กด Ctrl+C / Ctrl+D

**Sprint 2 — Back-End (Image Analysis & Core Features)**
- [x] ออกแบบเป็น OOP: `SkinAnalyzer`, `NailRecommender`, `DataStore`, `PaletteRenderer`, `Suggestion`, `AnalysisResult`, `NailApp`
- [x] ตรวจจับผิว (YCrCb + morphology + largest component)
- [x] ประเมินโทนผิวด้วยค่า ITA ใน CIE Lab (cool / warm / neutral)
- [x] แนะนำสีแบบ rule-based ปรับตามทรง/ความยาวเล็บ
- [x] ค้นหา / กรองตามแท็ก / เรียงลำดับคำแนะนำ
- [x] ทำระบบเป็น data-driven: โหลดกฎพาเลตจาก `palette_rules.json`
- [x] เชื่อม External API (TheColorAPI) ดึงชื่อสีจริง พร้อม Defensive Fallback เมื่อ API ล่ม
- [x] File I/O: บันทึกภาพพาเลต (.png) และประวัติผลวิเคราะห์ (.json)
- [x] แยกเวอร์ชัน CLI (รันนอก Colab) ออกจากเวอร์ชัน GUI (Colab) เพื่อกันเดโมพัง
- [x] สร้างชุดทดสอบอัตโนมัติ (`tests/test_nail.py`, 15 เคส)
- [x] ทดสอบและส่งมอบโค้ดผ่าน Pull Request บน GitHub

**Overall status:** Sprint 1–2 เสร็จตามเป้าหมาย ระบบวิเคราะห์ภาพและแนะนำสี
ทำงานครบ End-to-End สิ่งที่ยกไป Sprint ถัดไป: (1) ปรับความแม่นยำการตรวจจับ
บริเวณเล็บ (แยกจากผิว) (2) ตั้ง CI/CD รันเทสต์อัตโนมัติบน GitHub Actions
(3) ต่อยอดฟีเจอร์ AI (เช่น virtual try-on หรือโมเดลจำแนกโทนผิว)

## 2. Quality Assurance & Debugging Report

| Test Item | Input Used | Expected Result | Actual Result | Status |
|-----------|-----------|-----------------|---------------|--------|
| จำแนก undertone (cool) | ITA = 40 | คืน "cool" | ได้ "cool" | PASSED |
| จำแนก undertone (warm) | ITA = 5 | คืน "warm" | ได้ "warm" | PASSED |
| จำแนก undertone (neutral) | ITA = 20 | คืน "neutral" | ได้ "neutral" | PASSED |
| ภาพไม่มีผิว | ภาพดำล้วน | คืน "unknown" ไม่ crash | ได้ "unknown" | PASSED |
| แปลงสี hex→BGR | "#FF0000" | (0, 0, 255) | ถูกต้อง | PASSED |
| แนะนำสี (ทรง oval) | warm/oval/medium | ombré ขึ้นก่อน | อันดับ 1 คือ ombré | PASSED |
| แนะนำสี (เล็บสั้น) | neutral/square/short | มี micro-French แสดง | แสดงใน 6 อันดับ | PASSED |
| ค้นหาคำแนะนำ | keyword "pastel" | คืนเฉพาะที่มี pastel | ถูกต้อง | PASSED |
| กรองตามแท็ก | tag "cool" | คืนเฉพาะแท็ก cool | ถูกต้อง | PASSED |
| เรียงตามจำนวนสี | ชุดคำแนะนำ | เรียงมาก→น้อย | ถูกต้อง | PASSED |
| รูปไม่พบ | path ที่ไม่มีจริง | แจ้งเตือน ไม่ crash | "ไม่พบไฟล์รูป: ..." | PASSED |
| กด Ctrl+C / Ctrl+D | โหมดโต้ตอบ | ปิดอย่างปลอดภัย | "ปิดระบบอย่างปลอดภัย" | PASSED |
| pipeline เต็ม (E2E) | รูป + oval/medium | ได้คำแนะนำ + บันทึกไฟล์ | ทำงานครบ บันทึก .png/.json | PASSED |
| เชื่อม External API | เรียก TheColorAPI ด้วย hex | ได้ชื่อสีจริง | ดึงชื่อสีสำเร็จ (เช่น Periwinkle) | PASSED |
| API ล่ม/ไม่มีเน็ต | ตัดการเชื่อมต่อ | ใช้ชื่อสีสำรอง ไม่ crash | fallback ทำงานถูกต้อง | PASSED |
| Unit tests | `pytest` | ทุกเคสผ่าน | 17 passed | PASSED |

## 3. Weekly Retrospective (Wow! & Whoops!)

**Wow! (สิ่งที่ทำได้ดี)**
- นำ Computer Vision (skin mask + ITA ใน Lab) มาผูกกับระบบแนะนำแบบ rule-based
  ได้ครบเป็น pipeline เดียว
- ทำระบบเป็น data-driven (กฎอยู่ในไฟล์ JSON) แก้/เพิ่มสีได้โดยไม่แตะโค้ด
- แยกเวอร์ชัน CLI ที่รันได้ทุกที่ ออกจากเวอร์ชัน GUI บน Colab — ลดความเสี่ยงตอนสาธิต

**Whoops! (ปัญหาที่พบและแนวทางแก้)**
- โค้ดเดิมเป็นสคริปต์ใน Colab ก้อนเดียว ผูกกับ `google.colab` และ `ipywidgets`
  → refactor เป็นคลาส OOP แยก 3 เลเยอร์ และทำ CLI ที่ไม่พึ่ง Colab
- โค้ดเดิม "ไม่ได้บันทึกผลลัพธ์" ลงไฟล์เลย → เพิ่ม DataStore บันทึกภาพพาเลต + ประวัติ
- คำแนะนำสำหรับเล็บสั้น (micro-French) ถูกต่อท้ายจึงโดนตัดออกจาก 6 อันดับแรกเสมอ
  → ย้ายให้ขึ้นก่อน คำแนะนำที่เหมาะกับความยาวเล็บจึงแสดงจริง
- การจัดการข้อผิดพลาดตอนเปิดรูปมีน้อย → เพิ่มการตรวจ path/ชนิดไฟล์และ Exception Handling

## 4. Repository / Pull Request

- Repository: `<ใส่ลิงก์ GitHub ของกลุ่ม>`
- Pull Request: `<ใส่ลิงก์ PR>`
