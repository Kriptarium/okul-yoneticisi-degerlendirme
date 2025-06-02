import json
import hashlib
import os

KULLANICI_DOSYASI = "kullanicilar.json"

def sifre_hashle(sifre):
    return hashlib.sha256(sifre.encode()).hexdigest()

def kullanici_kaydet(kullanici_adi, sifre):
    if os.path.exists(KULLANICI_DOSYASI):
        with open(KULLANICI_DOSYASI, "r", encoding="utf-8") as f:
            kullanicilar = json.load(f)
    else:
        kullanicilar = {}

    if kullanici_adi in kullanicilar:
        return False

    kullanicilar[kullanici_adi] = sifre_hashle(sifre)

    with open(KULLANICI_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(kullanicilar, f, ensure_ascii=False, indent=2)

    return True

def giris_yap(kullanici_adi, sifre):
    if not os.path.exists(KULLANICI_DOSYASI):
        return False

    with open(KULLANICI_DOSYASI, "r", encoding="utf-8") as f:
        kullanicilar = json.load(f)

    sifre_hash = sifre_hashle(sifre)
    return kullanicilar.get(kullanici_adi) == sifre_hash
