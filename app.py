import streamlit as st
import json
import os
from datetime import datetime
from auth import kullanici_kaydet, giris_yap

st.set_page_config(page_title="Okul Yöneticisi Eğitimi", layout="centered")

if "oturum" not in st.session_state:
    st.session_state["oturum"] = False
    st.session_state["kullanici"] = ""

st.title("📘 Okul Yöneticileri İçin Eğitim ve Değerlendirme Platformu")

menu = st.sidebar.selectbox("🔐 Menü", ["Giriş Yap", "Kayıt Ol"])

if menu == "Giriş Yap":
    kullanici = st.text_input("Kullanıcı Adı")
    sifre = st.text_input("Şifre", type="password")
    if st.button("Giriş"):
        if giris_yap(kullanici, sifre):
            st.success("Giriş başarılı!")
            st.session_state["oturum"] = True
            st.session_state["kullanici"] = kullanici
            st.experimental_rerun()
        else:
            st.error("Giriş bilgileri hatalı.")

elif menu == "Kayıt Ol":
    yeni_kullanici = st.text_input("Yeni Kullanıcı Adı")
    yeni_sifre = st.text_input("Yeni Şifre", type="password")
    if st.button("Kaydol"):
        if kullanici_kaydet(yeni_kullanici, yeni_sifre):
            st.success("Kayıt başarılı.")
        else:
            st.warning("Bu kullanıcı adı zaten kayıtlı.")

if st.session_state["oturum"]:
    st.success(f"👋 Hoş geldiniz, {st.session_state['kullanici']}")

    with open("konular.json", "r", encoding="utf-8") as f:
        konular = json.load(f)

    st.markdown("## 📚 Eğitim Modülleri")

    for konu in konular:
        with st.expander(f"🎓 {konu['baslik']}"):
            st.video(konu["video_url"])
            st.info(konu["aciklama"])
            if st.button(f"✅ Bu eğitimi tamamladım – {konu['baslik']}", key=konu["id"]):
                st.session_state["konu_id"] = konu["id"]
                st.session_state["konu_baslik"] = konu["baslik"]
                st.session_state["teste_basla"] = True
                st.experimental_rerun()

    if st.session_state.get("teste_basla", False):
        with open("sorular.json", "r", encoding="utf-8") as f:
            tum_sorular = json.load(f)

        secili_konu_id = st.session_state["konu_id"]
        secili_sorular = [s for s in tum_sorular if s["konu_id"] == secili_konu_id]

        st.subheader(f"📝 {st.session_state['konu_baslik']} Testi")
        cevaplar = []
        puan = 0

        for soru in secili_sorular:
            st.markdown(f"**{soru['soru']}**")
            secenek = st.radio("Seçiminiz:", soru["secenekler"], key=soru["id"])
            cevaplar.append((soru, secenek))

        if st.button("📊 Testi Bitir"):
            for soru, kullanici_cevabi in cevaplar:
                if kullanici_cevabi == soru["dogru_cevap"]:
                    puan += 1
            st.success(f"{len(secili_sorular)} soruda {puan} doğru yaptınız.")

            for soru, kullanici_cevabi in cevaplar:
                st.markdown("---")
                st.markdown(f"**Soru:** {soru['soru']}")
                if kullanici_cevabi == soru["dogru_cevap"]:
                    st.markdown("✅ Doğru")
                else:
                    st.markdown(f"❌ Yanlış - Doğru cevap: {soru['dogru_cevap']}")
                    st.markdown(f"📘 Geri Bildirim: {soru['geribildirim']}")
                    konu_url = next(k["video_url"] for k in konular if k["id"] == soru["konu_id"])
                    st.markdown(f"[🔁 Konuyu Tekrar İzle]({konu_url})")
