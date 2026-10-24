# ULTIMATE QUIZ — Android

Android version of ULTIMATE QUIZ with Slovak and Czech multiple-choice quizzes.

- App name: **ULTIMATE QUIZ**
- APK filename: **ULTIMATE-QUIZ-Android.apk**
- Version: **1.0.0**

## Build APK using GitHub Actions

1. Upload `main.py`, `quizzes.json`, `buildozer.spec`, and the `.github/workflows/build-android.yml` workflow to the root of your GitHub repository. Keep the `.github/workflows` folder structure.
2. Open the repository's **Actions** tab and choose **Build Android APK**.
3. Click **Run workflow** and wait for the workflow to finish successfully.
4. Open the completed workflow run. Under **Artifacts**, download `ULTIMATE-QUIZ-Android`.
5. Extract the downloaded ZIP to get `ULTIMATE-QUIZ-Android.apk`.

This workflow builds a debug APK for testing. It is not a signed Google Play release build.
