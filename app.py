import streamlit as st
import json
from datetime import datetime
import os

# JSON dosyalarını yükle
with open("sorular.json", "r", encoding="utf-8") as f:
    sorular = json.load(f)

PUANLAR_DOSYASI = "puanlar.json"

def puani_kaydet(kullanici_adi, puan, toplam):
    if os.path.exists(PUANLAR_DOSYASI):
        with open(PUANLAR_DOSYASI, "r", encoding="utf-8") as f:
            puanlar = json.load(f)
    else:
        puanlar = {}

    if kullanici_adi not in puanlar:
        puanlar[kullanici_adi] = []

    puanlar[kullanici_adi].append({
        "tarih": datetime.today().strftime("%Y-%m-%d"),
        "puan": puan,
        "toplam": toplam
    })

    with open(PUANLAR_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(puanlar, f, ensure_ascii=False, indent=2)

# Arayüz
st.title("🏫 Okul Yöneticileri İçin Çevik Liderlik ve Kriz Yönetimi Testi")

kullanici_adi = st.text_input("Lütfen adınızı girin:", key="kullanici_adi")

if kullanici_adi:
    puan = 0
    cevaplar = []

    for soru in sorular:
        st.subheader(soru["soru"])
        cevap = st.radio("Seçiminiz:", soru["secenekler"], key=soru["id"])
        cevaplar.append((soru, cevap))

    if st.button("Testi Bitir ve Puanımı Göster"):
        for soru, kullanici_cevabi in cevaplar:
            if kullanici_cevabi == soru["dogru_cevap"]:
                puan += 1
        st.success(f"🎉 {len(sorular)} soruda {puan} doğru cevabınız var.")
        puani_kaydet(kullanici_adi, puan, len(sorular))

        for soru, kullanici_cevabi in cevaplar:
            st.markdown("---")
            st.markdown(f"**Soru:** {soru['soru']}")
            if kullanici_cevabi == soru["dogru_cevap"]:
                st.markdown("✅ Doğru")
            else:
                st.markdown(f"❌ Yanlış - Doğru cevap: {soru['dogru_cevap']}")
            st.markdown(f"**Geri Bildirim:** {soru['geribildirim']}")

        # Puan geçmişi gösterimi
        with open(PUANLAR_DOSYASI, "r", encoding="utf-8") as f:
            puanlar = json.load(f)
        st.markdown("---")
        st.subheader("📈 Geçmiş Puanlarınız")
        for kayit in puanlar[kullanici_adi][-5:]:
            st.write(f"{kayit['tarih']}: {kayit['puan']} / {kayit['toplam']}")
