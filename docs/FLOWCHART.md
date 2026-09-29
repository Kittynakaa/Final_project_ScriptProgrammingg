# System Architecture & Workflow Flowchart

แผนภาพการไหลของข้อมูลของ **ระบบแนะนำสีทาเล็บจากโทนผิว (Nail Color Recommender)**
แสดงการทำงานร่วมกันของ Presentation Layer (CLI), Business Logic Layer และ
Data Access Layer ตามหลัก Separation of Concerns

```mermaid
graph TD
    User([ผู้ใช้ / CLI]) -->|1. path รูป + ทรง + ความยาว| CLI[NailApp Controller]

    subgraph Presentation Layer
        CLI
    end

    subgraph Business Logic Layer
        CLI -->|2. ส่งภาพ| Skin[SkinAnalyzer]
        Skin -->|2a. skin mask YCrCb + morphology| Skin
        Skin -->|2b. ITA ใน CIE Lab| Tone{{undertone: cool/warm/neutral}}
        Tone -->|3. โทน + ทรง + ความยาว| Rec[NailRecommender]
        Rec -->|3a. โหลดกฎ| Rules[(palette_rules.json)]
        Rec -->|4. คำแนะนำสูงสุด 6 ชุด| CLI
        CLI -->|4a. ขอชื่อสีจริง| Api[ColorApiClient]
        Api -->|GET hex| Ext[TheColorAPI ภายนอก]
        Ext -->|ชื่อสี JSON| Api
        Api -.->|Fallback เมื่อ API ล่ม| CLI
    end

    subgraph Data Access Layer
        CLI -->|5. บันทึกประวัติ| Store[DataStore]
        Store -->|เขียน| Hist[(output/history.json)]
        CLI -->|6. วาดพาเลต| Render[PaletteRenderer]
        Render -->|บันทึกภาพ| PNG[(output/palette_*.png)]
    end

    CLI -->|7. แสดงผล + ไฟล์ที่บันทึก| User
```

## คำอธิบายลำดับการทำงาน

1. ผู้ใช้ระบุ path รูปมือ พร้อมทรงเล็บและความยาวเล็บ (ผ่าน CLI)
2. `SkinAnalyzer` ตรวจจับบริเวณผิว (YCrCb + morphology + เลือกก้อนใหญ่สุด)
   แล้วประเมินโทนผิวด้วยค่า ITA ใน CIE Lab → cool / warm / neutral
3. `NailRecommender` โหลดกฎจาก `palette_rules.json` แล้วจับคู่โทนผิว + ทรง +
   ความยาว เพื่อสร้างคำแนะนำ (สูงสุด 6 ชุด, ลบรายการซ้ำ)
4. `DataStore` บันทึกผลการวิเคราะห์ลง `output/history.json` (Data Persistence)
5. `PaletteRenderer` วาดแถบสีพาเลตและบันทึกเป็น `output/palette_*.png`
6. `NailApp` แสดงผลทางหน้าจอและบอกตำแหน่งไฟล์ที่บันทึก

> GitHub แสดงผลบล็อก ```mermaid``` เป็นแผนภาพอัตโนมัติเมื่อเปิดไฟล์นี้บนเว็บ
