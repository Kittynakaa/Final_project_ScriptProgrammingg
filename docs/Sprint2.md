# Sprint Result Report — Sprint 2

**Project Name:** ระบบแนะนำสีทาเล็บจากโทนผิว (Nail Color Recommender)
**Sprint:** 2 (Back-End — Image Analysis, Recommender, External API & File I/O)
**Team Members:**
- Planner : สาริษฐ์ บุตรช่วง
- Coder:  ชาคริต อ่วมอ่ำ 
- Debugger: เมธาวี สิทธิชัยเนตร 
- Debugger:  อภิสรา นครสุข
---

## 1. Sprint Progress Summary

- [x] พัฒนา `SkinAnalyzer` ตรวจจับบริเวณผิว (YCrCb + morphology + เลือกก้อนใหญ่สุด)
- [x] ประเมินโทนผิวด้วยค่า ITA ใน CIE Lab จำแนกเป็น cool / warm / neutral
- [x] พัฒนา `NailRecommender` แนะนำสีแบบ rule-based ปรับตามทรง/ความยาวเล็บ
- [x] ทำระบบเป็น data-driven: โหลดกฎพาเลตจาก `data/palette_rules.json`
- [x] เพิ่มการค้นหา / กรองตามแท็ก / เรียงลำดับคำแนะนำ
- [x] File I/O: บันทึกภาพพาเลต (.png) และประวัติผลวิเคราะห์ (`output/history.json`)
- [x] เชื่อม External API (TheColorAPI) ดึงชื่อสีจริง พร้อมระบบ Defensive Fallback
- [x] เขียนชุดทดสอบอัตโนมัติด้วย pytest (17 เคส ผ่าน 100%)
- [x] ทดสอบและส่งมอบโค้ดผ่าน Pull Request บน GitHub

**Overall status:** Sprint 2 เสร็จตามเป้าหมาย — ระบบวิเคราะห์ภาพและแนะนำสีทำงานครบ
End-to-End พร้อมบันทึกข้อมูลและเชื่อม API สิ่งที่ยกไป Sprint ถัดไป: พัฒนาเป็นหน้าเว็บ

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
| ค้นหา / กรอง / เรียง | keyword, tag, จำนวนสี | คืนผลถูกต้อง | ถูกต้องทั้งหมด | PASSED |
| File I/O | ชำระผลวิเคราะห์ | บันทึกลง history.json | บันทึกสำเร็จ | PASSED |
| เชื่อม External API | เรียก TheColorAPI ด้วย hex | ได้ชื่อสีจริง | ได้ชื่อสี (เช่น Periwinkle) | PASSED |
| API ล่ม / ไม่มีเน็ต | ตัดการเชื่อมต่อ | ใช้ชื่อสีสำรอง ไม่ crash | fallback ทำงานถูกต้อง | PASSED |
| Unit tests | `pytest` | ทุกเคสผ่าน | 17 passed | PASSED |

## 3. Weekly Retrospective (Wow! & Whoops!)

**Wow! (สิ่งที่ทำได้ดี)**
- นำ Computer Vision (skin mask + ITA ใน Lab) มาผูกกับระบบแนะนำแบบ rule-based ได้ครบเป็น pipeline เดียว
- ทำระบบ data-driven (กฎอยู่ในไฟล์ JSON) แก้/เพิ่มสีได้โดยไม่แตะโค้ด
- เชื่อม External API สำเร็จ พร้อมระบบสำรองที่ทำให้แอปไม่ล่ม

**Whoops! (ปัญหาที่พบและแนวทางแก้)**
- คีย์ของ dict ถูกบันทึกเป็น string ใน JSON → แก้ด้วยการแปลงกลับเป็น `int` ตอนโหลด
- คำแนะนำสำหรับเล็บสั้น (micro-French) ถูกต่อท้ายจึงโดนตัดออกจาก 6 อันดับแรก → ย้ายให้แสดงลำดับต้น
- API อาจล่ม/ไม่มีเน็ต → เพิ่ม Defensive Fallback ใช้ชื่อสีสำรอง

## 4. Repository / Pull Request

- Repository: `<ใส่ลิงก์ GitHub ของกลุ่ม>`
- Pull Request: `<ใส่ลิงก์ PR>`
