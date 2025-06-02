import streamlit as st
import json
import os
from datetime import datetime

# Eğitim konularını yükle
with open("konular.json", "r", encoding="utf-8") as f:
    konular = json.load(f)

# Soruları yükle
with open("sorular.json", "r", encoding="utf-8") as f:
    tum_sorular = json.load(f)

PUANLAR_DOSYASI = "puanlar.json"

def puani_kaydet(kullanici_adi, konu_id, puan, toplam):
    if os.path.exists(PUANLAR_DOSYASI):
        with open(PUANLAR_DOSYASI, "r", encoding="utf-8") as f:
            puanlar = json.load(f)
    else:
        puanlar = {}

    if kullanici_adi not in puanlar:
        puanlar[kullanici_adi] = []

    puanlar[kullanici_adi].append({
        "tarih": datetime.today().strftime("%Y-%m-%d"),
        "konu": konu_id,
        "puan": puan,
        "toplam": toplam
    })

    with open(PUANLAR_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(puanlar, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="Eğitim ve Test Uygulaması", layout="centered")

st.title("📘 Konu Tabanlı Eğitim ve Değerlendirme")

# Kullanıcı girişi (isteğe bağlı)
kullanici_adi = st.text_input("İsminizi giriniz", max_chars=30)
if not kullanici_adi:
    st.warning("Devam etmek için lütfen isminizi giriniz.")
    st.stop()

# Eğitim içeriğini seçtir
konu_basliklari = [k["baslik"] for k in konular]
secili_baslik = st.selectbox("📚 Bir eğitim konusunu seçin:", konu_basliklari)

# Seçilen konunun detaylarını getir
secili_konu = next(k for k in konular if k["baslik"] == secili_baslik)

st.video(secili_konu["video_url"])
st.markdown(f"**Açıklama:** {secili_konu['aciklama']}")

if st.button("🎓 Eğitimi Tamamladım, Teste Başla"):
    st.session_state["konu_id"] = secili_konu["id"]
    st.session_state["konu_baslik"] = secili_konu["baslik"]
    st.session_state["teste_basla"] = True

# Test modülü
if st.session_state.get("teste_basla", False):
    st.markdown("---")
    st.subheader(f"📝 {st.session_state['konu_baslik']} Testi")

    secili_konu_id = st.session_state["konu_id"]
    sorular = [s for s in tum_sorular if s["konu_id"] == secili_konu_id]

    puan = 0
    cevaplar = []

    for soru in sorular:
        st.write(f"**{soru['soru']}**")
        secenek = st.radio("Seçiminiz:", soru["secenekler"], key=soru["id"])
        cevaplar.append((soru, secenek))

    if st.button("📊 Testi Bitir"):
        for soru, kullanici_cevabi in cevaplar:
            if kullanici_cevabi == soru["dogru_cevap"]:
                puan += 1

        st.success(f"{len(sorular)} soruda {puan} doğru yaptınız.")
        puani_kaydet(kullanici_adi, secili_konu_id, puan, len(sorular))

        for soru, kullanici_cevabi in cevaplar:
            st.markdown("---")
            st.markdown(f"**Soru:** {soru['soru']}")
            if kullanici_cevabi == soru["dogru_cevap"]:
                st.markdown("✅ Doğru")
            else:
                st.markdown(f"❌ Yanlış - Doğru cevap: {soru['dogru_cevap']}")
                st.markdown(f"📘 **Geri Bildirim:** {soru['geribildirim']}")
                st.markdown(f"[🔁 Konuyu Tekrar İzle]({secili_konu['video_url']})")
