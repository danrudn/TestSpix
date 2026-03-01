# General

Automated testing framework for Qt/QML applications using Spix and Python.

## Install 
## 1. install dependency anyrpc

```
git clone https://github.com/sgieseking/anyrpc
cd anyrpc
mkdir build
cd build
cmake .. -DBUILD_WITH_LOG4CPLUS=OFF
make
sudo make install  # install in /usr/local/lib...
```

## 2. build spix for using the lib in qmake project

```
mkdir -p libs/spix/build/
cd libs/spix/build/

# DSPIX_QT_MAJOR=5 for QT 5.15
cmake -DSPIX_QT_MAJOR=6 \
-DSPIX_BUILD_EXAMPLES=OFF \
-DCMAKE_INSTALL_PREFIX=../install \
-DCMAKE_PREFIX_PATH=~/Qt/6.10.2/gcc_64 ..
cmake --build .
sudo cmake --install .

```

## 3. add spix to .pro 

```
# Add Spix here 
SPIX_PREFIX = $$PWD/libs/spix/install
SPIX_INCDIR = $$SPIX_PREFIX/include
SPIX_LIBDIR = $$SPIX_PREFIX/lib

INCLUDEPATH += $$SPIX_INCDIR
LIBS += -L$$SPIX_LIBDIR \
        -lSpixCore \
        -lSpixQtQuick

# Linux runtime path
QMAKE_RPATHDIR += $$SPIX_LIBDIR
```


## 4. install python dependencies for image compare
```
# 1. Venv erstellen (einmalig)
python3 -m venv venv

# 2. venv sourcen
source venv/bin/activate

# 3. Dependencies installieren aus pyproject.toml
pip install -e .

```



## Architecture

```
┌─────────────────────────┐         ┌──────────────────────────┐
│  Test Machine (Python)  │         │  Qt Application          │
│                         │         │                          │
│  • Python 3.12          │  RPC    │  • TestSpix (Qt 6.10)    │
│  • test scripts         │────────▶│  • Spix (XML-RPC Server) │
│  • scikit-image         │  :9000  │  • Port 9000             │
│  • NO Spix needed       │         │  • anyrpc library        │
└─────────────────────────┘         └──────────────────────────┘
```

**Key Concept:** XML-RPC is an open standard protocol. The test machine only needs Python with standard libraries - Spix server runs inside the Qt application.

---



## Dependencies

### Qt App
- **Spix** (libs/spix/) - Qt/QML automation framework
  - Provides XML-RPC server
  - QML tree navigation
  - Screenshot capabilities
  - Property access
- **anyrpc** (libs/spix/) - XML-RPC implementation

### Test Scripts (Python)
- **Python 3.12+**
- **xmlrpc.client** (standard library)
- **scikit-image** - for SSIM-based image comparison
- **numpy** - numerical operations

---



## Project Structure

```
TestSpix/
├── main.cpp                          # Qt app entry point + Spix integration
├── main.qml, Page1.qml, ...          # QML UI files
├── viewcontroller.cpp/h              # State machine controller
├── statechart.scxml                  # Qt State Machine definition
├── libs/
│   ├── spix/                         # Spix testing framework (git submodule)
│   └── anyrpc/                       # XML-RPC library (git submodule)
├── spix_script/
│   ├── pyproject.toml                # Python dependencies
│   ├── script_stateScreenshotCheck/  # Screenshot-based tests
│   │   ├── test.py                   # Main test script
│   │   ├── images_reference/         # Reference screenshots
│   │   └── images_test/              # Test output screenshots
│   └── script_propertyTreeCheck/     # QML tree-based tests
│       ├── record.py                 # Record reference snapshots
│       ├── test.py                   # Run tests
│       ├── qml_tree_utils.py         # Tree dump/compare utilities
│       ├── json_reference/           # Reference QML trees
│       └── json_test/                # Test output trees
└── doc/
    └── README.md                     # This file
```

---



## Testing Approaches

### 1. Screenshot-Based Testing (`script_stateScreenshotCheck/`)
Compares visual output using SSIM (Structural Similarity Index).

**Pros:**
- ✅ Catches visual regressions
- ✅ Tests rendering output

**Cons:**
- ⚠️ Sensitive to anti-aliasing, font rendering
- ⚠️ Requires threshold (0.9999) instead of exact match

**Use case:** Visual regression testing, layout verification

---

### 2. QML Tree-Based Testing (`script_propertyTreeCheck/`)
Compares complete QML object hierarchy as JSON.

**How it works:**
1. C++ recursively dumps QML tree to JSON
2. Stored in dynamic property `_qmlTreeJson`
3. Python reads via Spix `getStringProperty()`
4. Simple JSON equality comparison

**Pros:**
- ✅ Deterministic (no rendering variations)
- ✅ Fast comparison
- ✅ Detects property changes, structure changes

**Cons:**
- ⚠️ Doesn't catch visual rendering issues
- ⚠️ Large JSON files for complex UIs

**Use case:** State verification, property validation, structure tests

---



## Usage

### Run Tests

#### Screenshot Tests:
```bash
cd spix_script/script_stateScreenshotCheck
source ../venv/bin/activate
python3 test.py
```

#### QML Tree Tests:

**Record reference snapshots (first time or after intentional changes):**
```bash
cd spix_script/script_propertyTreeCheck
source ../venv/bin/activate
python3 record.py  # Creates json_reference/*.json
```

**Run tests:**
```bash
python3 test.py  # Compares current state to json_reference/
```

---



## How It Works

### Custom Command Handler (main.cpp)

```cpp
server.setGenericCommandHandler([&viewController, mainWindow](std::string command, std::string payload) {
    if (command == "gotoPage1") {
        viewController.gotoPage1();
    } else if (command == "dumpQmlTree") {
        QJsonObject tree = dumpQmlObject(mainWindow, 50);
        QJsonDocument doc(tree);
        QString jsonString = doc.toJson(QJsonDocument::Compact);
        mainWindow->setProperty("_qmlTreeJson", jsonString);
    }
});
```

### Python Test Script

```python
import xmlrpc.client
server = xmlrpc.client.ServerProxy('http://localhost:9000')

# Navigate
server.command("gotoPage2", "")

# Read state
state = server.getStringProperty("mainWindow/rootItem", "state")

# Dump QML tree
server.command("dumpQmlTree", "")
tree_json = server.getStringProperty("mainWindow", "_qmlTreeJson")
tree = json.loads(tree_json)
```

---



## Key Implementation Details

### XML-RPC Communication
- **Standard HTTP-based protocol** (port 9000)
- Spix provides server, Python provides client
- Commands are async (void return), property reads are sync

### QML Tree Dumping
**Process Flow:**

1. **Python sends command** via XML-RPC:
   ```python
   server.command("dumpQmlTree", "")
   ```

2. **Qt receives command** in custom handler (main.cpp):
   - Handler calls `dumpQmlObject(mainWindow, 50)`
   - Recursively traverses QObject hierarchy via `QMetaObject`
   - For each object: reads objectName, className, properties
   - Serializes to JSON format

3. **Store result** as dynamic property on mainWindow:
   ```cpp
   mainWindow->setProperty("_qmlTreeJson", jsonString);
   ```

4. **Python reads property** via Spix:
   ```python
   tree_json = server.getStringProperty("mainWindow", "_qmlTreeJson")
   tree = json.loads(tree_json)
   ```

**Technical Details:**
- **Recursive traversal** of QObject hierarchy
- **Special handling** for `QQuickWindow` (only dumps contentItem to avoid duplicates)
- **Properties captured:** objectName, className, all simple types (string, int, bool, double)
- **Max depth:** 50 levels (configurable)
- **Data transfer:** Via dynamic QObject property (C++ only, not exposed to QML)

---



## License

See individual component licenses:
- Spix: MIT License (libs/spix/LICENSE.txt)
- anyrpc: MIT License (libs/anyrpc/license)