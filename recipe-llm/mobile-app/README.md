# Recipe LLM Mobile App (React Native)

A native iOS and Android app for Recipe LLM built with React Native.

## ⚠️ Important Note

**For most users, we recommend using the PWA (Progressive Web App) instead** - it's much easier to install and doesn't require development tools. See `../INSTALL_ON_IPHONE.md` for instructions.

This React Native app is for advanced users who want:
- A true native app experience
- App Store/Play Store distribution
- Offline functionality
- Native iOS/Android features

## Prerequisites

### Required Software

1. **Node.js** (v16 or higher)
   - Download from: https://nodejs.org

2. **Watchman** (Mac only)
   ```bash
   brew install watchman
   ```

3. **For iOS Development** (Mac only):
   - **Xcode** (latest version from Mac App Store)
   - **CocoaPods**:
     ```bash
     sudo gem install cocoapods
     ```

4. **For Android Development**:
   - **Android Studio** with Android SDK
   - **Java Development Kit (JDK)** 11 or higher

## Setup

### 1. Install Dependencies

```bash
cd mobile-app
npm install
```

### 2. Configure Your Server URL

**Edit `src/api/recipeLLM.js`:**

Change the `API_BASE_URL` to point to your Recipe LLM server:

```javascript
// For local development (use your computer's IP)
const API_BASE_URL = 'http://192.168.1.5:5000';

// For production (use your deployed server)
const API_BASE_URL = 'https://your-recipe-llm.onrender.com';
```

### 3. iOS Setup (Mac only)

```bash
cd ios
pod install
cd ..
```

## Running the App

### Start Your Recipe LLM Server First

**On your computer:**
```bash
cd ..
python src/web_app.py
```

Make sure the server is accessible at the URL you configured in step 2.

### Run on iOS

```bash
npm run ios
```

Or open `ios/RecipeLLM.xcworkspace` in Xcode and click Run.

### Run on Android

```bash
npm run android
```

Or open the `android` folder in Android Studio and click Run.

## Building for Production

### iOS

1. Open `ios/RecipeLLM.xcworkspace` in Xcode
2. Select your development team
3. Update bundle identifier
4. Archive and upload to App Store Connect

### Android

1. Generate a signing key
2. Configure `android/app/build.gradle`
3. Build release APK:
   ```bash
   cd android
   ./gradlew assembleRelease
   ```

## Features

- ✅ Native iOS and Android app
- ✅ Beautiful mobile UI
- ✅ Quick action buttons
- ✅ Real-time chat interface
- ✅ Loading indicators
- ✅ Error handling
- ✅ Optimized for mobile

## Troubleshooting

### "Cannot connect to server"

1. Check that your Recipe LLM server is running
2. Verify the `API_BASE_URL` in `src/api/recipeLLM.js`
3. Make sure your phone/emulator can reach the server
4. For iOS simulator, use your computer's IP, not localhost
5. For Android emulator, use `10.0.2.2` instead of localhost

### "Error installing pods"

```bash
cd ios
pod deintegrate
pod install
cd ..
```

### "Build failed" on iOS

1. Clean build folder: Xcode → Product → Clean Build Folder
2. Delete `ios/build` folder
3. Delete `Pods` folder and run `pod install` again

### "Build failed" on Android

1. Clean gradle: `cd android && ./gradlew clean`
2. Delete `android/.gradle` folder
3. Invalidate caches in Android Studio

## Configuration

### Changing the App Name

1. Edit `package.json` - change `"name"`
2. iOS: Edit `ios/RecipeLLM/Info.plist` - change `CFBundleDisplayName`
3. Android: Edit `android/app/src/main/res/values/strings.xml`

### Changing the App Icon

1. Create icons for all sizes (use https://www.appicon.co/)
2. iOS: Replace images in `ios/RecipeLLM/Images.xcassets/AppIcon.appiconset/`
3. Android: Replace images in `android/app/src/main/res/mipmap-*/`

### Changing Colors/Theme

Edit `src/App.js` - modify the `styles` object.

## Recommended Alternative

**For most users, we recommend the PWA (Progressive Web App) instead:**

Advantages of PWA:
- ✅ No development tools needed
- ✅ Install in 2 minutes
- ✅ Works on iPhone immediately
- ✅ Auto-updates
- ✅ No App Store approval needed

See `../INSTALL_ON_IPHONE.md` for PWA installation instructions.

**Use this React Native app if you:**
- Want to publish to App Stores
- Need offline functionality
- Want native device features
- Are comfortable with mobile development

## License

MIT License - See parent directory LICENSE.md

## Support

For issues:
- Check the main README.md
- See troubleshooting above
- Open a GitHub issue

Happy cooking! 👨‍🍳👩‍🍳
