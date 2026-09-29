"""
NailRecommender (Business Logic Layer)
======================================
เครื่องมือแนะนำสีทาเล็บแบบ rule-based
- รับ undertone + ทรงเล็บ + ความยาวเล็บ -> คืนลิสต์คำแนะนำ (Suggestion)
- โหลด "กฎ" จากไฟล์ JSON (data-driven) จึงแก้สี/เพิ่มกฎได้โดยไม่แตะโค้ด
- รองรับการ ค้นหา / กรอง / เรียงลำดับ คำแนะนำ
"""

from .models import Suggestion

VALID_SHAPES = ["round", "oval", "almond", "square", "squoval", "stiletto"]
VALID_LENGTHS = ["short", "medium", "long"]


class NailRecommender:
    def __init__(self, rules, max_results=6):
        self.rules = rules
        self.max_results = max_results

    def _build(self, dict_list):
        return [Suggestion(d["palette"], d["tags"], d["note"]) for d in dict_list]

    def suggest(self, undertone, nail_shape, nail_length):
        """สร้างลิสต์คำแนะนำตาม undertone + ทรง + ความยาว (สูงสุด max_results, ลบซ้ำแล้ว)"""
        base = self.rules["undertone"].get(undertone,
                                           self.rules["undertone"]["neutral"])
        recs = self._build(base)

        sl = self.rules["shape_length"]
        # ปรับคำแนะนำเพิ่มตามทรง/ความยาวเล็บ
        if nail_shape in ["round", "short"] or nail_length == "short":
            # เล็บสั้น -> ขึ้นก่อน เพื่อให้คำแนะนำที่เหมาะกับความยาวแสดงจริงใน 6 อันดับแรก
            recs = self._build([sl["micro_french"]]) + recs
        elif nail_shape in ["oval", "almond"]:
            recs = self._build([sl["oval_almond"]]) + recs
        elif nail_shape in ["square", "squoval"]:
            recs = self._build([sl["square"]]) + recs
        else:  # stiletto / long
            recs = self._build([sl["long"]]) + recs

        return self._dedupe(recs)[:self.max_results]

    # ---------- ค้นหา / กรอง / เรียง ----------
    def search(self, suggestions, keyword):
        """ค้นหาคำแนะนำจากคำ (ในแท็กหรือคำอธิบาย)"""
        return [s for s in suggestions if s.has_tag(keyword)]

    def filter_by_tag(self, suggestions, tag):
        """กรองเฉพาะคำแนะนำที่มีแท็กตรงเป๊ะ"""
        tag = tag.lower()
        return [s for s in suggestions if tag in [t.lower() for t in s.tags]]

    def sort_by_palette_size(self, suggestions, descending=True):
        """เรียงคำแนะนำตามจำนวนสีในพาเลต"""
        return sorted(suggestions, key=lambda s: len(s.palette), reverse=descending)

    @staticmethod
    def _dedupe(suggestions):
        seen, uniq = set(), []
        for s in suggestions:
            if s.key() not in seen:
                seen.add(s.key())
                uniq.append(s)
        return uniq
