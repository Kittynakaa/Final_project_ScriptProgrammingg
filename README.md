# 💅 ระบบแนะนำสีทาเล็บจากโทนผิว (Nail Color Recommender)

โปรเจกต์รายวิชา **CP352301 Script Programming** — Final Project
แอปพลิเคชันวิเคราะห์ภาพมือ/เล็บด้วย **Computer Vision (OpenCV)** เพื่อประเมิน
โทนผิว (undertone) แล้วแนะนำพาเลตสีทาเล็บที่เข้ากับผู้ใช้ ตามโทนผิว ทรงเล็บ
และความยาวเล็บ พัฒนาด้วย Python เชิงวัตถุ (OOP) สถาปัตยกรรมแบบ 3 ชั้น

---

## 1. ภาพรวมและคุณค่า (Problem & Value)

การเลือกสีทาเล็บให้เข้ากับสีผิวเป็นเรื่องที่คนส่วนใหญ่ตัดสินใจยากและมักลองผิดลองถูก
ระบบนี้ช่วยให้:

- **ตัดสินใจง่ายขึ้น** — วิเคราะห์โทนผิวจากรูปถ่ายให้อัตโนมัติ (cool / warm / neutral)
- **เฉพาะบุคคล** — คำแนะนำปรับตามทรงเล็บและความยาวเล็บที่เลือก
- **เห็นภาพ** — แสดงพาเลตสีเป็นภาพจริงและบันทึกผลไว้ดูย้อนหลังได้

## 2. หลักการทำงาน (How it works)

1. **ตรวจจับผิว (Skin Mask)** — แปลงภาพเป็น YCrCb แล้ว threshold ช่วงสีผิว
   ทำ morphology และเลือกก้อนที่ใหญ่ที่สุด (สันนิษฐานว่าเป็นมือ)
2. **ประเมินโทนผิว (Undertone)** — แปลงเป็น CIE Lab แล้วคำนวณค่า
   **ITA (Individual Typology Angle)** เพื่อจำแนกเป็น cool / warm / neutral
3. **แนะนำสี (Rule-based)** — จับคู่โทนผิว + ทรง + ความยาวเล็บ กับ "กฎ" ที่เก็บ
   ในไฟล์ JSON เพื่อคืนพาเลตสีที่เหมาะสม (สูงสุด 6 ชุด)
4. **แสดงผล & บันทึก** — วาดภาพพาเลตและบันทึกประวัติผลการวิเคราะห์ลงไฟล์

## 3. ฟีเจอร์หลัก (Features)

- วิเคราะห์โทนผิวจากรูปภาพด้วย OpenCV (CIE Lab / ITA)
- แนะนำพาเลตสีแบบ rule-based ปรับตามทรง/ความยาวเล็บ
- **ค้นหา / กรองตามแท็ก / เรียงลำดับ** คำแนะนำ
- ระบบเป็นแบบ **data-driven** — แก้สี/เพิ่มกฎได้ในไฟล์ `data/palette_rules.json` โดยไม่ต้องแตะโค้ด
- บันทึกภาพพาเลต (.png) และประวัติผลการวิเคราะห์ (.json)
- จัดการข้อผิดพลาด (ไฟล์ไม่พบ/ไม่ใช่รูป/พิกเซลผิวน้อย ฯลฯ) โดยไม่ crash
- **รันได้ทั้งบนเครื่อง (CLI) และบน Google Colab (GUI)**

## 4. สถาปัตยกรรม (3-Layer Architecture)

| ชั้น (Layer) | หน้าที่ | ไฟล์ |
|--------------|---------|------|
| Presentation | CLI: รับ input, แสดงผล, จัดการข้อผิดพลาด | `src/cli.py` |
| Business Logic | วิเคราะห์ผิว, ประเมินโทน, แนะนำสี, เชื่อม API, โมเดลข้อมูล | `src/skin_analyzer.py`, `src/recommender.py`, `src/api_client.py`, `src/models.py` |
| Data Access | อ่านกฎพาเลต, บันทึกประวัติ, วาด/บันทึกภาพ | `src/data_store.py`, `src/palette_renderer.py` |

```
Presentation (NailApp / CLI)
        │
        ▼
Business Logic (SkinAnalyzer · NailRecommender · Suggestion/AnalysisResult)
        │
        ▼
Data Access (DataStore · PaletteRenderer) ──► palette_rules.json · history.json · palette_*.png
```

## 5. เทคโนโลยีที่ใช้ (Tech Stack)

- **Python 3.x** + OOP / โครงสร้างแบบโมดูล
- **OpenCV** (ประมวลผลภาพ, color space), **NumPy** (คำนวณเมทริกซ์)
- **requests** + **TheColorAPI** (External API ดึงชื่อสีจริง)
- **Pillow / Matplotlib** (แสดงผลและวาดภาพ)
- **pytest** (ชุดทดสอบอัตโนมัติ)
- เวอร์ชัน Colab เพิ่ม: **ipywidgets** (GUI), **pillow-heif** (รองรับไฟล์ .HEIC)

## 6. โครงสร้างโปรเจกต์

```
nail-color-recommender/
├── main.py                     # จุดเริ่มต้น (CLI, รันนอก Colab ได้)
├── requirements.txt
├── README.md
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── models.py               # Suggestion, AnalysisResult
│   ├── data_store.py           # DataStore (โหลดกฎ/บันทึกประวัติ)
│   ├── skin_analyzer.py        # SkinAnalyzer (skin mask + undertone/ITA)
│   ├── recommender.py          # NailRecommender (suggest/search/filter/sort)
│   ├── palette_renderer.py     # PaletteRenderer (วาด/บันทึกภาพพาเลต)
│   ├── api_client.py           # ColorApiClient (เชื่อม External API + Fallback)
│   └── cli.py                  # NailApp (Presentation Layer)
├── data/
│   └── palette_rules.json      # กฎพาเลตสี (data-driven)
├── tests/
│   └── test_nail.py            # ชุดทดสอบอัตโนมัติ (15 เคส)
├── notebook/
│   └── nail_colab.ipynb        # เวอร์ชัน GUI บน Google Colab
├── output/                     # ผลลัพธ์ (ภาพพาเลต + ประวัติ)
└── docs/
    ├── PLAN.md
    ├── Sprint1.md
    └── GITHUB_SETUP.md
```

## 7. วิธีติดตั้งและรัน (Getting Started)

```bash
git clone <URL ของ repository>
cd nail-color-recommender
pip install -r requirements.txt

# โหมดโต้ตอบ (ถาม path รูป + ทรง + ความยาว)
python main.py

# หรือระบุค่าเลย: python main.py <path รูป> <ทรง> <ความยาว>
python main.py hand.jpg oval medium
```

ผลลัพธ์: คำแนะนำพาเลตทางหน้าจอ + ภาพพาเลตใน `output/` + ประวัติใน `output/history.json`

> เวอร์ชัน GUI: เปิด `notebook/nail_colab.ipynb` บน Google Colab แล้วกดรัน
> (อัปโหลดรูปผ่านปุ่มและเลือกทรง/ความยาวจาก dropdown)

## 8. การทดสอบ (Testing)

```bash
pytest            # หรือ  python -m pytest
```

ครอบคลุมการจำแนก undertone (ITA), การแปลงสี hex→BGR และเครื่องมือแนะนำ
(suggest / search / filter / sort)

## 9. สมาชิกในทีมและการหมุนเวียนบทบาท (Role Rotation Matrix)

เพื่อให้สมาชิกทุกคนได้ฝึกครบทั้ง 3 บทบาทหลัก (**Planner / Architect**,
**Coder / Dev**, **Debugger / QA & DevOps**) มีการหมุนเวียนบทบาทในแต่ละ Sprint

| สมาชิก | รหัสนักศึกษา | Sprint 1 | Sprint 2 | Sprint 3 | Final |
| :--- | :---: | :---: | :---: | :---: | :---: |
| ชาคริต อ่วมอ่ำ | 663380555-8 | Planner | Coder | Debugger | Planner |
| อภิสรา นครสุข | 663380578-6 | Coder | Debugger | Planner | Coder |
| เมธาวี สิทธิชัยเนตร | 663380372-6 | Coder | Debugger | Planner | Coder |
| สาริษฐ์ บุตรช่วง | 663380365-3 | Debugger | Planner | Coder | Debugger |


## 10. ฟีเจอร์และสถานะการพัฒนา (Features & Status)

### 🟢 ทำเสร็จแล้ว (Sprint 1–2)
- วิเคราะห์โทนผิวจากภาพด้วย OpenCV (skin mask + ITA ใน CIE Lab)
- แนะนำพาเลตสีแบบ rule-based ปรับตามทรง/ความยาวเล็บ (data-driven จาก JSON)
- **เชื่อม External API (TheColorAPI)** ดึงชื่อสีจริงมาเสริมพาเลต พร้อมระบบ Fallback เมื่อ API ล่ม
- ค้นหา / กรองตามแท็ก / เรียงลำดับคำแนะนำ
- บันทึกภาพพาเลต (.png) และประวัติผลวิเคราะห์ (.json)
- Exception handling ครบ (ไฟล์ไม่พบ/ไม่ใช่รูป/Ctrl+C/Ctrl+D)
- ชุดทดสอบอัตโนมัติ 17 เคส (ผ่าน 100%) + CI รัน pytest ทุก push/PR
- **หน้าเว็บแดชบอร์ด (`index.html`)** — อัปโหลดรูปแล้ววิเคราะห์+แนะนำสีในเบราว์เซอร์ (client-side), สองภาษา TH/EN, ดีไซน์ Glassmorphism
- **Deploy ขึ้น GitHub Pages อัตโนมัติ** (`.github/workflows/static.yml`)

### 🟡 ตามแผน (Roadmap — Final)
- ปรับความแม่นยำการตรวจจับ "เล็บ" ให้แยกจากผิวได้ดีขึ้น, เก็บ Edge Cases เพิ่ม
- ต่อยอด AI: virtual try-on ทาสีบนเล็บจริง / โมเดลจำแนกโทนผิว-ทรงเล็บอัตโนมัติ

### 🌐 เว็บเดโม (GitHub Pages)
เมื่อเปิด GitHub Pages แล้ว เข้าได้ที่: `https://<ชื่อผู้ใช้>.github.io/<ชื่อ repo>/`
### 11. ## 📅 แผนการทำงานภาพรวม (3 Sprints Roadmap)

### Sprint 1: Core System Foundation & OOP CLI Architecture
* **เป้าหมาย:** สร้างรากฐานสถาปัตยกรรมเชิงวัตถุ (OOP) แบบ 3 เลเยอร์ และ CLI Interface ที่รับ input อย่างปลอดภัย
* **รายละเอียดงาน:**
  - `src/models.py` : โมเดลข้อมูลหลัก `Suggestion`, `AnalysisResult`
  - `src/cli.py` & `main.py` : หน้าต่างปฏิสัมพันธ์ Command Line Interface (2 โหมด) พร้อม Input Validation
  - Exception Handling : ไฟล์ไม่พบ / ไฟล์ไม่ใช่รูป / Ctrl+C / Ctrl+D
  - `docs/PLAN.md` : กำหนดขอบเขตงานและ Definition of Done

### Sprint 2: Image Analysis, Recommender & File I/O
* **เป้าหมาย:** วิเคราะห์ภาพเพื่อประเมินโทนผิว แนะนำสีแบบ rule-based และจัดเก็บข้อมูลถาวร
* **รายละเอียดงาน:**
  - `src/skin_analyzer.py` : ตรวจจับผิว (YCrCb + morphology) และประเมินโทนผิวด้วยค่า ITA ใน CIE Lab
  - `src/recommender.py` : แนะนำสีแบบ rule-based + ค้นหา/กรอง/เรียง (data-driven จาก `data/palette_rules.json`)
  - `src/palette_renderer.py` : วาดและบันทึกภาพพาเลตสีเป็นไฟล์ `.png`
  - `src/data_store.py` : โหลดกฎพาเลต และบันทึกประวัติผลวิเคราะห์ลง `output/history.json`
  - `tests/test_nail.py` : ชุดทดสอบระบบอัตโนมัติ (Automated pytest — 15 เคส ผ่าน 100%)
  - `docs/LEARNINGLOG.md` : บันทึกการใช้ AI อย่างรับผิดชอบ (Gen AI Prompt Logs)

### Sprint 3: Accuracy Tuning, Web Dashboard & GitHub Pages Deployment
* **เป้าหมาย:** ปรับความแม่นยำการตรวจจับ พัฒนาหน้าเว็บ และระบบส่งมอบงานอัตโนมัติ
* **รายละเอียดงาน:**
  - ปรับความแม่นยำการแยกบริเวณ "เล็บ" ออกจากผิว และเก็บ Edge Cases เพิ่ม
  - `index.html` : หน้าเว็บแดชบอร์ดอัปโหลดรูปและแสดงพาเลตสีที่แนะนำ (Sprint 3)
  - `.github/workflows/ci.yml` : ระบบ CI/CD รัน `pytest` อัตโนมัติทุกครั้งที่ push/PR
  - ต่อยอด AI : virtual try-on ทาสีบนเล็บจริง หรือโมเดลจำแนกโทนผิว/ทรงเล็บ


## 12. เอกสารประกอบโครงการ (Project Docs)

| ไฟล์ | เนื้อหา |
|------|---------|
| [`docs/PLAN.md`](docs/PLAN.md) | ขอบเขตงาน + Definition of Done |
| [`docs/Sprint1.md`](docs/Sprint1.md) | รายงานผล Sprint (QA + Retrospective) |
| [`docs/FLOWCHART.md`](docs/FLOWCHART.md) | แผนภาพสถาปัตยกรรม (Mermaid) |
| [`docs/LEARNINGLOG.md`](docs/LEARNINGLOG.md) | บันทึกการใช้ AI อย่างรับผิดชอบ |
| [`docs/GITHUB_SETUP.md`](docs/GITHUB_SETUP.md) | วิธีขึ้น GitHub + เปิด Pull Request |
| [`TEST.md`](TEST.md) · [`test_cases/TEST_CASES.md`](test_cases/TEST_CASES.md) | การทดสอบและเคสทดสอบ |
| [`CHANGELOG.md`](CHANGELOG.md) | ประวัติการเปลี่ยนแปลงตาม Sprint |
