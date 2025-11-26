# How to Install Recipe LLM as an App on Your iPhone

This guide shows you how to install Recipe LLM on your iPhone so it works like a real app!

---

## 📱 Method 1: Progressive Web App (PWA) - EASIEST!

This method turns the web app into an iPhone app. **No App Store needed!**

### Step 1: Start the Server on Your Computer

**On your Mac/Windows/Linux computer:**

1. Open Terminal (Mac) or Command Prompt (Windows)
2. Navigate to the recipe-llm folder:
   ```bash
   cd /path/to/the-book-of-secret-knowledge/recipe-llm
   ```
3. Install dependencies (first time only):
   ```bash
   pip install -r requirements.txt
   pip install Pillow
   ```
4. Generate icons (first time only):
   ```bash
   python generate_icons.py
   ```
5. Set your API key:
   ```bash
   export OPENAI_API_KEY='your-key-here'
   ```
6. Start the server:
   ```bash
   python src/web_app.py
   ```

### Step 2: Find Your Computer's IP Address

**On the same computer, open a NEW terminal:**

**Mac/Linux:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Windows:**
```cmd
ipconfig
```

Look for your local IP address (usually looks like `192.168.1.5` or `10.0.0.5`)

### Step 3: Install on iPhone

1. **Make sure your iPhone is on the SAME WiFi network as your computer**

2. **Open Safari** on your iPhone (must be Safari, not Chrome)

3. **Go to the URL:**
   ```
   http://YOUR-IP-ADDRESS:5000
   ```
   Example: `http://192.168.1.5:5000`

4. **Tap the Share button** (the square with an arrow pointing up) at the bottom of Safari

5. **Scroll down and tap "Add to Home Screen"**

6. **Give it a name** (default is "Recipe LLM")

7. **Tap "Add"** in the top right

8. **Done!** 🎉 You now have a Recipe LLM app icon on your home screen!

### Using Your New App

- **Tap the icon** on your home screen
- It opens **fullscreen** like a real app
- Works exactly like the web version
- **Your computer must be on** and running the server

---

## 🌐 Method 2: Cloud Deployment - Use ANYWHERE!

Deploy to a cloud service so you can use it anywhere without your computer.

### Option A: Deploy to Render (Free)

1. **Create a Render account:** https://render.com

2. **Create a `render.yaml` file** (already included if you used the provided file)

3. **Push to GitHub** (already done)

4. **Connect to Render:**
   - Go to render.com dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect and deploy

5. **Set environment variables:**
   - Add your `OPENAI_API_KEY` in the Render dashboard

6. **Get your URL:**
   - Render gives you a URL like: `https://recipe-llm.onrender.com`

7. **Install on iPhone:**
   - Open that URL in Safari on your iPhone
   - Tap Share → "Add to Home Screen"
   - Now it works anywhere with internet!

### Option B: Deploy to Railway (Free)

Similar to Render:
1. Sign up at https://railway.app
2. Connect GitHub repo
3. Add environment variables
4. Get your permanent URL
5. Install as PWA on iPhone

---

## 📦 Method 3: React Native App (Advanced)

For a true native iOS app, you can create a React Native version.

### Prerequisites
- Mac computer (required for iOS development)
- Xcode installed
- Node.js and npm installed

See `mobile-app/README.md` for full instructions on building the React Native version.

---

## 🔧 Troubleshooting

### "Can't connect" on iPhone
- ✅ Check both devices are on the same WiFi
- ✅ Check the IP address is correct
- ✅ Make sure the server is running on your computer
- ✅ Try turning off any VPN on your computer
- ✅ Check firewall isn't blocking port 5000

### "Add to Home Screen" doesn't show app features
- ✅ Make sure you're using Safari (not Chrome)
- ✅ Icons should load automatically
- ✅ If not, regenerate icons: `python generate_icons.py`

### App icon is missing
- ✅ Make sure icons were generated: `ls static/icons/`
- ✅ Regenerate if needed: `python generate_icons.py`
- ✅ Restart the web server

### Want to use without computer on?
- ✅ Use Method 2 (Cloud Deployment)
- ✅ Deploy to Render or Railway
- ✅ Works from anywhere!

---

## 🎨 Customizing the App Icon

Want a custom icon?

1. **Use an icon generator:** https://www.pwabuilder.com/imageGenerator
   - Upload your custom icon image
   - Download the generated pack
   - Replace files in `static/icons/`

2. **Or create manually:**
   - Create PNG files for each size: 72, 96, 128, 144, 152, 192, 384, 512
   - Name them: `icon-72x72.png`, `icon-96x96.png`, etc.
   - Put them in `static/icons/`

3. **Restart the server** and reinstall the PWA on your iPhone

---

## ✨ Features When Installed as App

- ✅ **Fullscreen** - No browser UI
- ✅ **Home Screen Icon** - Quick access
- ✅ **Splash Screen** - Professional loading
- ✅ **Works Offline** - Basic functionality (after first load)
- ✅ **Fast Loading** - Cached resources
- ✅ **Notifications** - Can add push notifications later

---

## 💡 Tips

1. **Bookmark the IP address** in Safari for easy access
2. **Use cloud deployment** for best experience
3. **Add a static IP** to your computer so the address doesn't change
4. **Use port forwarding** if you want to access from outside your network (advanced)

---

## 🚀 Next Steps

Once installed:
- Ask for any recipe
- Get cooking tips
- Substitute ingredients
- Adapt recipes for dietary needs
- Scale recipes up or down

Enjoy your AI cooking assistant! 👨‍🍳👩‍🍳

---

## Need Help?

- Check the main README.md for more info
- See QUICKSTART.md for basic usage
- Open an issue on GitHub if you have problems
