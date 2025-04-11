# 🎤 VoiceSpy — Real-Time Discord Voice Channel Auditor  

**Track, log, and analyze voice channel activity effortlessly.** VoiceSpy is a Python Discord bot that monitors voice channels in real-time, recording user joins/leaves with timestamps and exporting data directly to Google Sheets.  

## ✨ Features  

- **🔍 Real-Time Monitoring** – Instantly logs voice channel activity (join/leave events).  
- **📊 Google Sheets Integration** – Automatically exports data to your spreadsheet.  
- **⚡ Nextcord-Powered** – Built with Python 3.13 and Nextcord for stability.  
- **📝 Detailed Logs** – Records usernames, Discord IDs, timestamps, and actions.  
- **🛠️ Minimal Setup** – Easy configuration with slash commands.  

## 🛠️ Setup  

1. **Invite the Bot**  
   - Grant `View Channels` and `Send Messages` permissions.  
2. **Configure Google Sheets API**  
   - Set up credentials via the [Google Sheets API guide](https://developers.google.com/sheets/api).  
3. **Run the Bot**  
   ```sh
   pip install -r requirements.txt
   python main.py
   ```  

## 📜 Command List  

| Command | Description |  
|---------|-------------|  
| `/addvoice [channel]` | Starts tracking a voice channel. |  
| `/removevoice [channel]` | Stops tracking a voice channel. |  

## 🤖 Self-Hosting  

Clone the repo, install dependencies, and configure your `.env` file:  

```sh
git clone https://github.com/pristordev/voicespy.git
cd VoiceSpy
python -m pip install -r requirements.txt
```  

## 📄 License  
MIT © [pristordev] – Free and open-source.  

---

🚀 **Need help?** Open an Issue or contact me on Discord!  

---

⭐ **Enjoy VoiceSpy?** Give the repo a star to support development!  

---
