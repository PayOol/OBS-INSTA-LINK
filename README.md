# 🚀 OBS Insta-Link: Instant PC-to-Mobile Transfer

**Transfer your OBS recordings to your Smartphone via QR Code instantly. No Cloud. No Cables.**

![OBS Script](https://img.shields.io/badge/OBS-Script-black?style=flat-square&logo=obs-studio)
![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 😫 The Problem
You just recorded a great clip on OBS. Now you want to post it on TikTok, Instagram Reels, or send it via WhatsApp.
But... you have to upload it to Google Drive (slow), wait, open your phone, download it (slow), and save it. **It kills the creative flow.**

## ✨ The Solution: Insta-Link
**Insta-Link** is a lightweight Python script for OBS Studio.
1. **Record** your video.
2. Click **Stop Recording**.
3. A **QR Code** automatically pops up on your OBS scene.
4. **Scan it** with your phone to download the video immediately over your local Wi-Fi.

✅ **Zero Internet Speed required** (Local Transfer)
✅ **Auto-Hide** (QR Code hides while recording)
✅ **Force Download** (Works on Android & iOS Safari)
✅ **100% Free & Open Source**

---

## ☕ Support the Project
This script is free to use. If it saves you time in your content creation workflow, consider buying me a coffee!

[**>>> CLICK HERE TO SUPPORT (Donation) <<<**](https://payool.mychariow.shop/prd_t2vk4y)

---

## ⚙️ Prerequisites (Read Carefully)

OBS Studio requires a specific version of Python to run scripts. **Even if you have Python installed, please follow this step.**

1. **Download Python 3.10 (Embeddable Package)**
   [Click here to download Python 3.10.11 (Zip)](https://www.python.org/ftp/python/3.10.11/python-3.10.11-embed-amd64.zip)
   *(Note: Newer versions like 3.12+ might crash OBS scripts).*

2. **Install**
   - Create a folder named `OBS-Python` on your `C:` drive (e.g., `C:\OBS-Python`).
   - Extract **all files** from the Zip into this folder.

3. **Link to OBS**
   - Open OBS Studio.
   - Go to **Tools** > **Scripts** > **Python Settings** tab.
   - Click **Browse** and select your `C:\OBS-Python` folder.
   - *Status should say: "Loaded Python Version 3.10".*

---

## 📥 Installation

1. **Download the Script**
   Download the `obs_insta_link.py` file from this repository.

2. **Load Script in OBS**
   - Go to **Tools** > **Scripts**.
   - Click the **+** button.
   - Select `obs_insta_link.py`.

3. **Create the QR Source**
   - In your OBS Scene, add a new Source: **Image**.
   - Name it exactly: `QR_Share` (Case sensitive).
   - *Note: You can change this name later in the Script Properties if needed.*
   - Select a placeholder image (it will be replaced automatically).

---

## 🎬 How to Use

1. **Start Recording:** The `QR_Share` image will automatically **hide**.
2. **Stop Recording:** Wait 1 or 2 seconds. The `QR_Share` image will **appear** with a fresh QR Code.
3. **Scan:** Open your phone camera, scan the code, and accept the download.

---

## 🔧 Troubleshooting / FAQ

**Q: The QR Code does not appear.**
A: Check the "Script Log" button in the Scripts window.
- If it says *"Source not found"*: Make sure your Image source is named correctly (`QR_Share`).
- If it says *"Python not loaded"*: Re-read the Prerequisites section.

**Q: My phone cannot connect (Timeout).**
A:
1. Your PC and Phone must be on the **same Wi-Fi network**.
2. **Windows Firewall:** The first time you run it, Windows will ask for permission. You must check **"Private Networks"** and **"Allow"**. If you missed this, check your Firewall settings.

**Q: iOS (iPhone) Specifics**
A: Safari will ask *"Do you want to download...?"*. Click Yes.
The video will be saved in the **Files App** (Downloads folder), not directly in the Photos Gallery. To save it to Photos: Open Files App > Open Video > Share Icon > Save Video.

---

## 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

**Author:** PayOol™
