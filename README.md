# WG Testing Repo


Welcome to the testing repository for **Wiggle Games**. This repository contains the essential components for the development and testing of games developed for WiggleGames.com. Here, you’ll find code, test scripts, and documentation to help you get started. It's not that hard, really.

# Running a game

You'll need Python installed because well the games are written in Python. If we want to run them on a website then they need to be written in Javascript, which is less easy on the brain. 

Attempts to convert the code can be found in the ```web-ports``` folder. Games will be converted to web code then released on WiggleGames.com, unless it is web native.

## Install Python on Windows

### Step 1: Download Installer
1. Go to the [Python website](https://www.python.org/downloads/).
2. Click "Download Python" for your version.

### Step 2: Run the Installer
1. Locate the downloaded file and double-click it.
2. **Check** "Add Python to PATH."
3. Click "Install Now."

### Step 3: Verify Installation
1. Open Command Prompt (`Win + R`, type `cmd`).
2. Run:

   ```bash
   python --version

You'll want to also install the requirements in the requiurements.txt file. You usually use "pip" in the terminal to download packages.

ex.
"pip install pygame"

Once that's finished all you need to do is run the file.
```python ./main.py```

## License

This repository is licensed under the MIT License.
