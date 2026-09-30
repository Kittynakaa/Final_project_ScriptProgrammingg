# Sprint Result Report — Sprint 3

**Project Name:** ระบบแนะนำสีทาเล็บจากโทนผิว (Nail Color Recommender)
**Sprint:** 3 (Web Dashboard, Bilingual UI & GitHub Pages Deployment)
**Team Members:**
- Planner / Team Leader: _____________
- Coder: _____________
- Debugger: _____________

---

## 1. Sprint Progress Summary

- [x] พัฒนาหน้าเว็บแดชบอร์ด `index.html` — อัปโหลดรูป → วิเคราะห์ → แนะนำสีบนเบราว์เซอร์
- [x] พอร์ตอัลกอริทึม skin mask + ITA (CIE Lab) จาก Python มาเป็น JavaScript (ทำงาน client-side)
- [x] เชื่อม TheColorAPI ฝั่งเบราว์เซอร์เพื่อดึงชื่อสีจริง พร้อม Fallback
- [x] รองรับสองภาษา (TH/EN toggle) และออกแบบ UI สไตล์ Glassmorphism
- [x] ตั้ง CI (`.github/workflows/ci.yml`) รัน `pytest` อัตโนมัติทุกครั้งที่ push/PR
- [x] Deploy หน้าเว็บขึ้น GitHub Pages (`.github/workflows/static.yml`)
- [x] ทดสอบและส่งมอบโค้ดผ่าน Pull Request บน GitHub

**Overall status:** Sprint 3 เสร็จตามเป้าหมาย — ระบบใช้งานได้จริงบนเว็บโดยไม่ต้องติดตั้ง
โปรแกรม และมีระบบ CI/CD สมบูรณ์ สิ่งที่ยกไป Final Sprint: ปรับความแม่นยำการตรวจจับเล็บ
และต่อยอดฟีเจอร์ AI

## 2. Quality Assurance & Debugging Report

| Test Item | Input Used | Expected Result | Actual Result | Status |
|-----------|-----------|-----------------|---------------|--------|
| เว็บ: อัปโหลดรูป + วิเคราะห์ | รูปมือ + oval/medium | แสดงโทนผิว + พาเลต 6 ชุด | แสดงครบถูกต้อง | PASSED |
| เว็บ: ผลตรงกับ CLI | รูปเดียวกัน | undertone ตรงกับฝั่ง Python | ตรงกัน | PASSED |
| เว็บ: สลับภาษา TH/EN | กดปุ่มภาษา | เปลี่ยนข้อความทั้งหน้า | เปลี่ยนถูกต้อง | PASSED |
| เว็บ: เชื่อม API | โหลดชื่อสี | ได้ชื่อสีจาก TheColorAPI | ได้ชื่อสี (มี fallback) | PASSED |
| CI บน GitHub Actions | push โค้ด | รัน pytest อัตโนมัติผ่าน | ขึ้นเครื่องหมายถูกเขียว | PASSED |
| GitHub Pages Deploy | push เข้า main | เว็บออนไลน์เข้าถึงได้ | Deploy สำเร็จ | PASSED |

## 3. Weekly Retrospective (Wow! & Whoops!)

**Wow! (สิ่งที่ทำได้ดี)**
- ทำให้ระบบใช้งานได้จริงบนเว็บ ไม่ต้องติดตั้งอะไร ใครก็เปิดใช้ได้
- พอร์ตอัลกอริทึม ITA มาเป็น JavaScript ได้ผลตรงกับฝั่ง Python
- ระบบ CI/CD ทำงานอัตโนมัติครบวงจร (ทดสอบ + deploy)

**Whoops! (ปัญหาที่พบและแนวทางแก้)**
- GitHub Pages รันได้เฉพาะไฟล์ static (รัน Python ไม่ได้) → เขียนการวิเคราะห์ใหม่เป็น JavaScript ให้ทำงานในเบราว์เซอร์
- การเรียก API จากเบราว์เซอร์ติดเรื่องเครือข่ายบางครั้ง → ใส่ระบบ Fallback เหมือนฝั่ง Python
- โฟลเดอร์ `.github` เป็นไฟล์ซ่อน อัปโหลดผ่านการลากไฟล์ยาก → สร้างไฟล์ workflow ผ่านหน้าเว็บ GitHub โดยตรง

## 4. Repository / Pull Request

- Repository: `<ใส่ลิงก์ GitHub ของกลุ่ม>`
- Pull Request: `<ใส่ลิงก์ PR>`
- Live Web (GitHub Pages): `https://<ชื่อผู้ใช้>.github.io/<ชื่อ repo>/`
