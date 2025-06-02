import streamlit as st
import json
import os
from datetime import datetime
from auth import kullanici_kaydet, giris_yap

# Kullanıcı ilerlemesi dosyası
def ilerleme_kaydet(kullanici, konu_id):
    dosya = "ilerleme.json"
    if os.path.exists(dosya):
        with open(dosya, "r", encoding="utf-8") as f:
            veriler = json.load(f)
    else:
        veriler = {}

    if kullanici not in veriler:
        veriler[kullanici] = []

    if konu_id not in veriler[kullanici]:
        veriler[kullanici].append(konu_id)

    with open(dosya, "w", encoding="utf-8") as f:
        json.dump(veriler, f, ensure_ascii=False, indent=2)

def ilerleme_al(kullanici):
    dosya = "ilerleme.json"
    if os.path.exists(dosya):
        with open(dosya, "r", encoding="utf-8") as f:
            veriler = json.load(f)
            return veriler.get(kullanici, [])
    return []

st.set_page_config(page_title="Okul Yöneticisi Eğitimi", layout="centered")

# Oturum değişkenlerini tanımla
if "oturum" not in st.session_state:
    st.session_state["oturum"] = False
if "kullanici" not in st.session_state:
    st.session_state["kullanici"] = ""
if "teste_basla" not in st.session_state:
    st.session_state["teste_basla"] = False
if "konu_id" not in st.session_state:
    st.session_state["konu_id"] = None
if "konu_baslik" not in st.session_state:
    st.session_state["konu_baslik"] = None

st.title("📘 Okul Yöneticileri İçin Eğitim ve Değerlendirme Platformu")

menu = st.sidebar.selectbox("🔐 Menü", ["Giriş Yap", "Kayıt Ol"])

if menu == "Giriş Yap":
    kullanici = st.text_input("Kullanıcı Adı")
    sifre = st.text_input("Şifre", type="password")
    if st.button("Giriş"):
        if kullanici and sifre:
            if giris_yap(kullanici, sifre):
                st.success("Giriş başarılı!")
                st.session_state["oturum"] = True
                st.session_state["kullanici"] = kullanici
                st.rerun()
            else:
                st.error("Giriş bilgileri hatalı veya kullanıcı bulunamadı.")
        else:
            st.warning("Lütfen kullanıcı adı ve şifre giriniz.")

elif menu == "Kayıt Ol":
    yeni_kullanici = st.text_input("Yeni Kullanıcı Adı")
    yeni_sifre = st.text_input("Yeni Şifre", type="password")
    if st.button("Kaydol"):
        if yeni_kullanici and yeni_sifre:
            if kullanici_kaydet(yeni_kullanici, yeni_sifre):
                st.success("Kayıt başarılı. Giriş yapabilirsiniz.")
            else:
                st.warning("Bu kullanıcı adı zaten kayıtlı.")
        else:
            st.warning("Lütfen kullanıcı adı ve şifre giriniz.")

if st.session_state["oturum"]:
    st.success(f"👋 Hoş geldiniz, {st.session_state['kullanici']}")

    with open("konular.json", "r", encoding="utf-8") as f:
        konular = json.load(f)

    st.sidebar.markdown("## 📚 Eğitim Modülleri")
    kullanici_ilerleme = ilerleme_al(st.session_state["kullanici"])
    for k in konular:
        if k["id"] in kullanici_ilerleme:
            k["baslik"] += " ✅"
    konu_basliklari = [k["baslik"] for k in konular]
    secilen_konu = st.sidebar.selectbox("Eğitim modülünü seçin", konu_basliklari)

    secili_konu = next((k for k in konular if k["baslik"] == secilen_konu), None)
    if secili_konu:
        st.header(f"🎓 {secili_konu['baslik']}")
        st.video(secili_konu["video_url"])
        st.info(secili_konu["aciklama"])
        if st.button("✅ Bu eğitimi tamamladım"):
            st.session_state["konu_id"] = secili_konu["id"]
            st.session_state["konu_baslik"] = secili_konu["baslik"]
            ilerleme_kaydet(st.session_state["kullanici"], secili_konu["id"])
            st.session_state["teste_basla"] = True
            st.rerun()

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
