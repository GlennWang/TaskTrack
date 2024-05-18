## Setup and Run

1. Create a virtual environment:
   
   ```
   python -m venv myenv
   ```

2. Activate the virtual environment:
   
   - Windows:
     
     ```
     myenv\Scripts\activate
     ```
   
   - macOS/Linux:
     
     ```
     source myenv/bin/activate
     ```

3. Install dependencies:
   
   ```
   pip install -r requirements.txt
   ```

4. cd app
   
   ```
   cd app
   ```

5. Start the Flask app:
   
   ```
   python app.py
   ```

# Pyinstaller

1. Normal:

```
PyInstaller --add-data="./vuedist;vuedist" --add-data="extensions.py;." -n TaskTrack -i ./vuedist/tasks.ico app.py --onefile
```

2. noconsole:

```
PyInstaller --add-data="./vuedist;vuedist" --add-data="extensions.py;." -n TaskTrack --noconsole -i ./vuedist/tasks.ico app.py --onefile
```

note：You need to exclude your project folder from Windows virus check
