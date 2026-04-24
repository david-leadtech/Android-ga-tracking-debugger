# 📊 Android GA Debugger GUI

> 🇪🇸 Looking for the Spanish version? [Click here](README.es.md)

A desktop tool that lets you inspect Firebase/Google Analytics logs from connected Android devices using `adb logcat`.

## 🧰 Main Features

- Intuitive **Tkinter** GUI
- Visualizes:
  - Events (`Logging event`)
  - User properties (`Setting user property`)
  - Consent data (`Setting storage consent`)
- Multi-language support (🇪🇸 Spanish, 🇺🇸 English)
- Log search and navigation
- ADB and device connection checks

---

## 📦 Requirements

- Python 3.7+
- ADB (Android Debug Bridge)
- OS: Windows, Linux, or macOS

---

## ⚙️ Installation

### 1. Clone or download this repo

```bash
git clone https://github.com/david-leadtech/Android-ga-tracking-debugger.git
cd Android-ga-tracking-debugger
```

### 2. Install Python dependencies

No external packages required – uses only standard Python libraries.

### 3. Install ADB

#### ✅ Quick way (recommended)

Download **platform-tools** from the official site:

📎 https://developer.android.com/tools/releases/platform-tools

#### 🔧 Windows

1. Unzip into a folder like `C:\platform-tools`
2. Add it to your system `PATH`:
   - Control Panel > System > Advanced system settings > Environment Variables
   - Edit `PATH` and add `C:\platform-tools`

#### 🔧 macOS / Linux

```bash
# Extract the zip
unzip platform-tools-latest-*.zip

# Move it globally (optional)
sudo mv platform-tools /opt/

# Add to PATH (in ~/.bashrc, ~/.zshrc, etc.)
export PATH=$PATH:/opt/platform-tools
```

Then check:

```bash
adb version
```

---

## 🚀 Run the App

```bash
python main.py
```

The program will auto-check:

- If ADB is installed
- If an Android device/emulator is connected

---

## 🌐 Languages

You can switch between English and Spanish in the `Languages` menu.

---

## 📂 Project Structure

The project follows a Model-View-Controller (MVC) architecture to ensure a clear separation of concerns.

- main.py: The main entry point of the application. It initializes and runs the Controller.

- src/: Contains the core source code.

  - model.py: The Model, which manages the application's state and data logic.

  - view.py: The View, which builds and manages the Tkinter GUI.

  - adb_manager.py: A dedicated module to handle all communications with ADB.

  - log_parser.py: Handles the parsing of logcat lines.

  - config_manager.py: Manages user configuration.

  - i18n.py: Handles internationalization (translations).

- assets/: Contains static files like icons and images.

- locales.json: Stores the translation strings for multi-language support.

- config.json: Stores the user's configuration, such as the selected language.

- `tests/`: Unit tests (for example, log line parsing).

- `requirements-dev.txt`: Optional dev dependencies (e.g. pytest) for contributors and CI.



---

## Development

### Running tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

---

## Releases

Versioning follows `__version__` in `main.py`. The first GitHub release for this fork is **`v1.0.0`** (current baseline). After new work lands on `main`, bump the version and tag **`v1.1.0`**, etc. See [CHANGELOG.md](CHANGELOG.md) and [docs/RELEASES.md](docs/RELEASES.md); pushing a `v*.*.*` tag runs the Release workflow.

---

## Repository

This project is developed and released from **david-leadtech/Android-ga-tracking-debugger** only. Clone and open issues there.

If your local `origin` still points elsewhere, run:

```bash
git remote set-url origin https://github.com/david-leadtech/Android-ga-tracking-debugger.git
```

See [docs/REPO.md](docs/REPO.md) for details.

---

## 👨‍💻 Author

Original tool by **Alejandro Reinoso** (see `LICENSE.txt`).  
🔗 [LinkedIn](https://www.linkedin.com/in/alejandroreinosogomez/)  
📬 [Contact](https://alejandroreinoso.com/contacto/?utm_source=ga_android_debugger)
