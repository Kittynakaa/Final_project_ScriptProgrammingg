# 🧪 System Quality Assurance & Testing (TEST.md)

โปรเจกต์ **ระบบแนะนำสีทาเล็บจากโทนผิว** มีการทดสอบทั้งแบบอัตโนมัติ (pytest)
และแบบ manual test cases เพื่อประกันคุณภาพ

ดูตารางเคสทดสอบฉบับเต็มที่: [`test_cases/TEST_CASES.md`](test_cases/TEST_CASES.md)

---

## 🚀 การรันชุดทดสอบอัตโนมัติ (Automated Unit Testing)

```bash
pytest          # รันทั้งหมด
pytest -v       # แสดงรายละเอียดรายเทส
```

### โมดูลทดสอบที่ผ่าน 100% (`tests/test_nail.py` — 15 เคส)
- การจำแนก undertone จากค่า ITA (cool / warm / neutral / unknown)
- การแปลงสี hex → BGR
- เครื่องมือแนะนำ: `suggest` (ปรับตามทรง/ความยาว), `search`, `filter_by_tag`, `sort`
- การลบรายการซ้ำ (dedupe)

## 🔍 การทดสอบด้วยมือ (Manual / Demo Testing)

| ประเภท | คำสั่ง / อินพุต | ผลที่คาดหวัง |
|--------|-----------------|--------------|
| Happy path | `python main.py hand.jpg oval medium` | แสดงโทนผิว + พาเลต + บันทึกไฟล์ |
| เปลี่ยนทรง | `python main.py hand.jpg stiletto long` | คำแนะนำอันดับ 1 เปลี่ยน |
| Validation | `python main.py hand.jpg abc xyz` | ใช้ค่าเริ่มต้น + แจ้งเตือน |
| ไฟล์ไม่พบ | `python main.py nofile.jpg` | "ไม่พบไฟล์รูป" ไม่ crash |
| ไฟล์ไม่ใช่รูป | `python main.py notes.txt` | "เปิดไฟล์รูปไม่ได้" ไม่ crash |
| Interrupt | กด Ctrl+C / Ctrl+D | "ปิดระบบอย่างปลอดภัย" |

## ✅ Definition of Done ด้านคุณภาพ
- ทุกฟีเจอร์มี unit test หรือ manual test case กำกับ
- ไม่มีกรณีที่โปรแกรม crash เป็น traceback จาก input ของผู้ใช้
- ชุดทดสอบอัตโนมัติต้องผ่าน 100% ก่อนเปิด Pull Request
