# Using Spix


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
cmake -DSPIX_QT_MAJOR=6 -DCMAKE_PREFIX_PATH=/opt/Qt/6.8.0/gcc_64 ..
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
cd spix-script
python3 -m venv venv
source venv/bin/activate
pip install scikit-image numpy
python test.py

```

dann vorher dem starten 

