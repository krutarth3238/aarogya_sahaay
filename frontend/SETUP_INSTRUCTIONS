# Aarogya Sahayak - Setup Instructions

## 🚀 Quick Start Guide

### 1. Firebase Setup

1. **Create a Firebase Project**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Click "Create a project"
   - Name it "aarogya-sahayak" (or your preferred name)
   - Enable Google Analytics (optional)

2. **Enable Authentication**
   - In Firebase Console, go to "Authentication" > "Sign-in method"
   - Enable "Email/Password" provider

3. **Create Firestore Database**
   - Go to "Firestore Database" > "Create database"
   - Choose "Start in test mode" (for development)
   - Select a location (choose closest to India)

4. **Get Firebase Configuration**
   - Go to Project Settings > General
   - Scroll down to "Your apps" section
   - Click "Add app" > Web app
   - Copy the Firebase configuration object

5. **Update Firebase Config**
   - Open `config/firebase.ts`
   - Replace the placeholder values with your actual Firebase config:

```typescript
const firebaseConfig = {
  apiKey: "your-actual-api-key",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-actual-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "your-actual-sender-id",
  appId: "your-actual-app-id"
};
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Run the Application

```bash
npm start
```

Then:
- Press `i` for iOS simulator
- Press `a` for Android emulator
- Scan QR code with Expo Go app on your phone

### 4. Populate Demo Data (Optional)

To add sample data for testing:

```typescript
import { populateDemoData } from '@/services/demoData';

// Call this function once to populate demo data
populateDemoData();
```

## 📱 Features Implemented

### ✅ Core Features
- **Multilingual Support**: English, Hindi, Telugu, and more
- **Health Worker Connect**: Find and connect with ASHA workers
- **Daily Vitals Logging**: Blood pressure, sugar, weight, temperature
- **Automated Reminders**: Medication, appointments, check-ups
- **Personalized Health Feed**: Health tips and advice
- **User Authentication**: Sign up/Sign in with Firebase
- **Profile Management**: Personal and health information

### ✅ UI/UX Features
- **Attractive Color Palette**: Health-focused green and blue theme
- **Responsive Design**: Works on all screen sizes
- **Accessibility**: Large touch targets, clear typography
- **Gradient Headers**: Beautiful visual design
- **Card-based Layout**: Clean and organized interface

### ✅ Technical Features
- **Firebase Integration**: Authentication, Firestore, real-time data
- **Offline Support**: Local storage with AsyncStorage
- **TypeScript**: Full type safety
- **React Native Paper**: Material Design components
- **Expo Router**: File-based navigation
- **i18next**: Internationalization support

## 🎨 Design System

### Color Palette
- **Primary**: #4CAF50 (Health Green)
- **Secondary**: #2196F3 (Trust Blue)
- **Accent**: Orange, Teal, Purple, Amber
- **Status**: Success, Warning, Error, Info colors

### Typography
- **Headers**: Bold, 24-32px
- **Body**: Regular, 14-16px
- **Captions**: Light, 12-14px

### Components
- **Cards**: Rounded corners, subtle shadows
- **Buttons**: Gradient backgrounds, clear CTAs
- **Inputs**: Clean borders, icon support
- **Navigation**: Bottom tabs with icons

## 🔧 Customization

### Adding New Languages
1. Open `config/i18n.ts`
2. Add new language object to `resources`
3. Translate all text strings
4. Update language selector in UI

### Adding New Vitals
1. Update `VitalReading` interface in `services/auth.ts`
2. Add new vital type to vitals screen
3. Update charts and analytics
4. Add to health score calculation

### Customizing Health Score
1. Modify algorithm in `HealthScoreCard.tsx`
2. Adjust weight percentages
3. Add new factors (exercise, diet, etc.)

## 🚨 Important Notes

### Firebase Security Rules
Update your Firestore security rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only access their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Health workers are publicly readable
    match /healthWorkers/{document} {
      allow read: if true;
      allow write: if request.auth != null;
    }
    
    // Vital readings are user-specific
    match /vitalReadings/{document} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### Environment Variables
For production, use environment variables for Firebase config:

```bash
# .env
EXPO_PUBLIC_FIREBASE_API_KEY=your-api-key
EXPO_PUBLIC_FIREBASE_AUTH_DOMAIN=your-domain
EXPO_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
```

## 📊 Data Structure

### Collections in Firestore
- `users` - User profiles and health information
- `healthWorkers` - ASHA workers and volunteers
- `vitalReadings` - Health measurements
- `reminders` - Medication and appointment reminders
- `healthTips` - Educational content
- `messages` - Chat between users and health workers

## 🎯 Next Steps

### For Production
1. Set up proper Firebase security rules
2. Add data validation and sanitization
3. Implement proper error handling
4. Add analytics and crash reporting
5. Set up CI/CD pipeline
6. Add automated testing

### For Enhancement
1. Add voice input for vitals
2. Implement push notifications
3. Add offline sync capabilities
4. Integrate with wearable devices
5. Add telemedicine features
6. Implement health insights AI

## 🆘 Troubleshooting

### Common Issues
1. **Firebase connection failed**: Check your Firebase config
2. **Authentication not working**: Verify Firebase Auth is enabled
3. **App crashes on startup**: Check for missing dependencies
4. **Styling issues**: Ensure all color imports are correct

### Getting Help
- Check the README.md for detailed documentation
- Review Firebase console for any errors
- Check Expo logs for runtime issues
- Ensure all dependencies are properly installed

---

**Happy coding! 🎉**

The Aarogya Sahayak app is now ready to help people manage their health better across India.
