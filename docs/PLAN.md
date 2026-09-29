# PLAN.md — แผนโครงการ

**โปรเจกต์:** ระบบแนะนำสีทาเล็บจากโทนผิว (Nail Color Recommender)
**รายวิชา:** CP352301 Script Programming — Final Project

---

## 1. สเปกความต้องการ (Project Scope)

พัฒนาแอปพลิเคชันที่วิเคราะห์ภาพมือ/เล็บด้วย Computer Vision เพื่อประเมินโทนผิว
(undertone) แล้วแนะนำพาเลตสีทาเล็บที่เหมาะสม โดยคำแนะนำปรับตามโทนผิว ทรงเล็บ
และความยาวเล็บ ระบบต้องบูรณาการแนวคิดที่เรียนมา: OOP, โครงสร้างแบบโมดูล,
การประมวลผลภาพ, File I/O + การจัดเก็บข้อมูลถาวร (JSON), การค้นหา/กรอง/เรียงข้อมูล
และ Exception Handling

## 2. ขอบเขตการทำงาน (Functional Scope)

**อินพุต:** รูปภาพมือ/เล็บ + ทรงเล็บ (round/oval/almond/square/squoval/stiletto)
+ ความยาว (short/medium/long)

**กระบวนการ:**
1. ตรวจจับบริเวณผิว (skin mask) ด้วย YCrCb + morphology
2. ประเมินโทนผิวด้วยค่า ITA ใน CIE Lab → cool / warm / neutral
3. แนะนำพาเลตสีแบบ rule-based (ปรับตามทรง/ความยาว) สูงสุด 6 ชุด
4. รองรับการค้นหา/กรอง/เรียงลำดับคำแนะนำ

**เอาต์พุต:** คำแนะนำพาเลตทางหน้าจอ + ภาพพาเลต (.png) + ประวัติผลวิเคราะห์ (.json)

## 3. สถาปัตยกรรม (Architecture)

แบ่งเป็น 3 เลเยอร์ตามหลัก Separation of Concerns

- **Presentation Layer** — `NailApp` (CLI): รับ input, validation, แสดงผล
- **Business Logic Layer** — `SkinAnalyzer`, `NailRecommender`, `Suggestion`, `AnalysisResult`
- **Data Access Layer** — `DataStore` (โหลดกฎ/บันทึกประวัติ), `PaletteRenderer` (วาด/บันทึกภาพ)

**หมายเหตุการออกแบบ:** กฎพาเลตเก็บในไฟล์ JSON (data-driven) และแยกส่วน
วิเคราะห์ภาพออกจากส่วนแสดงผล เพื่อให้เปลี่ยนหน้าจอ (CLI ↔ GUI/Web) ได้โดยไม่แตะ Logic

## 4. แผนการพัฒนาแบบ Iterative (Sprint Plan)

| Sprint | จุดเน้น | รายละเอียด |
|--------|---------|-----------|
| Sprint 1 | Front-End (CLI) | โครงรับ input, validation, จัดการข้อผิดพลาด |
| Sprint 2 | Back-End | ประมวลผลภาพ (skin/undertone), แนะนำสี, ค้นหา/กรอง/เรียง, File I/O |
| Sprint 3 | Full-Stack | ปรับความแม่นยำการตรวจจับ, จัดการ State, Edge Cases |
| Final | DevOps & AI | Automated Testing, CI/CD (GitHub Actions), ต่อยอด AI |

## 5. บทบาทในทีม (Roles)

- **Planner / Team Leader** — วางสเปก, กำหนด Definition of Done, จัดทำเอกสาร,
  ออกแบบกฎ Undertone → Palette (Color Mapping)
- **Coder** — พัฒนา pipeline ประมวลผลภาพและ recommender ตามสถาปัตยกรรม
- **Debugger** — ทดสอบ Edge Cases, จัดการ Exception, เขียนเทสต์, เปิด Pull Request

## 6. เครื่องมือ (Tools)

Python 3.x · OpenCV · NumPy · Pillow · Matplotlib · pytest · Git/GitHub
(เวอร์ชัน Colab: ipywidgets, pillow-heif)

## 7. Definition of Done (DoD)

ฟีเจอร์หนึ่งถือว่า "เสร็จ" เมื่อ:

- [ ] ทำงานได้ตามความต้องการ (requirement)
- [ ] ตรวจสอบและจัดการอินพุตที่ไม่ถูกต้อง (ไฟล์ไม่พบ/ไม่ใช่รูป/ค่าไม่อยู่ในตัวเลือก)
- [ ] จัดการข้อผิดพลาดอย่างเหมาะสม ไม่ crash เป็น traceback
- [ ] โค้ดเป็นไปตามโครงสร้างแบบโมดูล/OOP ของโครงการ
- [ ] ข้อมูลที่จำเป็นถูกจัดเก็บอย่างถูกต้อง (บันทึกภาพพาเลต + ประวัติ)
- [ ] มีชุดทดสอบสำหรับฟังก์ชันสำคัญ
- [ ] ทำงานผ่านส่วนติดต่อที่ตั้งใจไว้ (CLI และ/หรือ GUI บน Colab)
- [ ] มีเอกสารกำกับเมื่อจำเป็น
- [ ] ทดสอบและส่งมอบโค้ดผ่าน **Pull Request** บน GitHub
