import streamlit as st
import json
from datetime import datetime
import os
from auth import kullanici_kaydet, giris_yap

st.set_page_config(page_title="Çevik Liderlik Testi", layout="centered")

# Kullanıcı oturumu
if "oturum" not in st.session_state:
    st.session_state["oturum"] = False
    st.session_state["kullanici"] = ""

st.title("🔐 Giriş / Kayıt")

menu = st.sidebar.selectbox("Menü", ["Giriş Yap", "Kayıt Ol"])

if menu == "Giriş Yap":
    kullanici = st.text_input("Kullanıcı Adı")
    sifre = st.text_input("Şifre", type="password")

    if st.button("Giriş"):
        if giris_yap(kullanici, sifre):
            st.success("Giriş başarılı.")
            st.session_state["oturum"] = True
            st.session_state["kullanici"] = kullanici
        else:
            st.error("Giriş başarısız.")

elif menu == "Kayıt Ol":
    yeni_kullanici = st.text_input("Yeni Kullanıcı Adı")
    yeni_sifre = st.text_input("Yeni Şifre", type="password")
    if st.button("Kayıt"):
        if kullanici_kaydet(yeni_kullanici, yeni_sifre):
            st.success("Kayıt başarılı. Şimdi giriş yapabilirsiniz.")
        else:
            st.warning("Bu kullanıcı zaten kayıtlı.")

# Test ekranı
if st.session_state["oturum"]:
    st.markdown(f"👋 Hoş geldin **{st.session_state['kullanici']}**")
    st.markdown("---")

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
        st.success(f"{len(sorular)} soruda {puan} doğru cevabınız var.")
        puani_kaydet(st.session_state["kullanici"], puan, len(sorular))

        for soru, kullanici_cevabi in cevaplar:
            st.markdown("---")
            st.markdown(f"**Soru:** {soru['soru']}")
            if kullanici_cevabi == soru["dogru_cevap"]:
                st.markdown("✅ Doğru")
            else:
                st.markdown(f"❌ Yanlış - Doğru cevap: {soru['dogru_cevap']}")
            st.markdown(f"**Geri Bildirim:** {soru['geribildirim']}")

        # Geçmiş puanları göster
        if os.path.exists(PUANLAR_DOSYASI):
            with open(PUANLAR_DOSYASI, "r", encoding="utf-8") as f:
                puanlar = json.load(f)
            if st.session_state["kullanici"] in puanlar:
                st.markdown("---")
                st.subheader("📈 Geçmiş Puanlarınız")
                for kayit in puanlar[st.session_state["kullanici"]][-5:]:
                    st.write(f"{kayit['tarih']}: {kayit['puan']} / {kayit['toplam']}")
