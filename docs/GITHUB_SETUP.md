# วิธีนำโปรเจกต์ขึ้น GitHub และเปิด Pull Request

โจทย์กำหนดให้ **ส่งมอบโค้ดผ่าน Pull Request** ทำตามขั้นตอนนี้ได้เลย

> ต้องติดตั้ง [Git](https://git-scm.com/downloads) และมีบัญชี GitHub ก่อน

## ขั้นที่ 1 — สร้าง Repository บน GitHub
1. เข้า github.com → **New repository**
2. ตั้งชื่อ เช่น `nail-color-recommender` → เลือก Public/Private ตามที่อาจารย์กำหนด
3. **อย่า** ติ๊ก "Add a README" (เพราะมีอยู่แล้ว) → **Create repository**

## ขั้นที่ 2 — อัปโหลดโค้ดครั้งแรก
เปิด Terminal ที่โฟลเดอร์โปรเจกต์ (ที่มี `main.py`) แล้วรัน:

```bash
git init
git add .
git commit -m "Initial commit: Nail Color Recommender (OOP, Sprint 1-2)"
git branch -M main
git remote add origin https://github.com/<ชื่อผู้ใช้>/nail-color-recommender.git
git push -u origin main
```

## ขั้นที่ 3 — ส่งงานผ่าน Pull Request (ทุก Sprint)

```bash
git checkout -b sprint-2
git add .
git commit -m "Sprint 2: image analysis, recommender, search/sort, file I/O"
git push -u origin sprint-2
```

จากนั้นเข้าหน้า repo บน GitHub → กด **Compare & pull request** → ใส่รายละเอียด
(ดึงจาก `docs/Sprint1.md`) → **Create pull request** → ให้เพื่อนรีวิว → **Merge**

## ขั้นที่ 4 — อัปเดตลิงก์ในเอกสาร
นำลิงก์ repo และ PR ไปใส่ใน `docs/Sprint1.md` (หัวข้อ 4) และตาราง Team Members
ใน `README.md`

## เกร็ด: เตรียม CI/CD (Final Sprint)
โปรเจกต์มีเทสต์ (`tests/test_nail.py`) พร้อมแล้ว เมื่อถึง Final Sprint สร้างไฟล์
`.github/workflows/ci.yml` ให้รัน `pytest` อัตโนมัติทุกครั้งที่ push ได้ทันที

> หมายเหตุ: โฟลเดอร์ `output/` (ภาพพาเลต + ประวัติ) ถูกตั้งให้ Git ไม่ track ไว้แล้ว
> ใน `.gitignore` เพราะเป็นไฟล์ที่โปรแกรมสร้างระหว่างใช้งาน
