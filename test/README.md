### This is readme file
---
#### Set up
###### Abby:
Supporting packages are listed in "package.json" file, when running reactive running commands,
it will set up the environment automatically.

Related running packages needed:
    First try to go over steps in this website for setting up:
        https://reactnative.dev/docs/environment-setup
    Include but not limit with:
        node, watchman, JDK, Android Studio, npx(npm), (cocoapods, gradle)
    Check the export path if you are using mac

Other related testing set ups on my laptop (Android Studio):
Virtual Device:
    Pixel 2 API 29, Android 10.0, x86
SDK:
    Android SDK Platform 29
    Sources for Android 29
    Google Play Intel x86 Atom System Image
SDK Tools:
    Android Emulator
    Android SDK Platform-Tools
    Android SDK Build-Tools 32-rc1:
        31.0.0
        30.0.2
        29.0.2
---
#### Running commands
###### Abby:
    1. Start your device, either real android device or virtual device
    I start mine in Android Studio
    2. Go to the project folder(terminal), using the command "npm start -c",
    this will install and set up almost everything and ready to emulate the app
    (Check http://localhost:19002/ for more information)
    3. The app should be lunched by Expo Go
---
#### Coding & implementation
###### Abby:
Assign different pages in main js file: App.js
All page files stored in screens folder
Pics stored in assets folder
outline style sheets of these stored in components
any helper functions stored in helpers folder







