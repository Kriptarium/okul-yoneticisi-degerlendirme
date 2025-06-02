import streamlit as st
import json
from datetime import datetime
import os
from auth import kullanici_kaydet, giris_yap

st.set_page_config(page_title="Okul Yöneticisi Eğitimi", layout="centered")

# Oturum başlat
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
        else:
            st.error("Giriş bilgileri hatalı.")

elif menu == "Kayıt Ol":
    yeni_kullanici = st.text_input("Yeni Kullanıcı Adı")
    yeni_sifre = st.text_input("Yeni Şifre", type="password")
    if st.button("Kaydol"):
        if kullanici_kaydet(yeni_kullanici, yeni_sifre):
            st.success("Kayıt başarılı. Artık giriş yapabilirsiniz.")
        else:
            st.warning("Bu kullanıcı adı zaten kayıtlı.")

# Eğitim/Test ekranı
if st.session_state["oturum"]:
    st.success(f"👋 Hoş geldiniz, {st.session_state['kullanici']}")
    st.markdown("---")
    st.markdown("Devam etmek için lütfen eğitim modülünü başlatın...")

    # Buradan sonra konular.json + sorular.json üzerinden eğitim ve test akışı entegre edilir
