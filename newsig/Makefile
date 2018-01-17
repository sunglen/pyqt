#Makefile for PYQT4 project

MAIN := newsig.py

#EXE := $(patsubst %.py, dist\\%.exe, $(MAIN))
EXE := $(patsubst %.py, %.exe, $(MAIN))

ELF := $(patsubst %.py, %, $(MAIN))

BUILD_DIR := build

DEL := rm -rf
PYUIC4 := pyuic4
PYRCC4 := pyrcc4
PYWRAP := pyinstaller

WRAPFLAGS := --hidden-import atexit
WRAPFLAGS += -F
WRAPFLAGS += -w
WRAPFLAGS += --distpath .

PYC := $(wildcard *.pyc)
SPEC := $(wildcard *.spec)

UI := $(wildcard *.ui)
QRC := $(wildcard *.qrc)

UIPY := $(patsubst %.ui, ui_%.py, $(UI))
QRCPY := $(patsubst %.qrc, qrc_%.py, $(QRC))

.PHONY: wrap ui clean

wrap: ui $(EXE)

%.exe: %.py
	$(PYWRAP) $(WRAPFLAGS) $<

ui: $(UIPY) $(QRCPY)

ui_%.py: %.ui
	$(PYUIC4) -o $@ $<

qrc_%.py: %.qrc
	$(PYRCC4) -o $@ $<

clean:
	$(DEL) $(EXE)
	$(DEL) $(UIPY)
	$(DEL) $(QRCPY)
	$(DEL) $(PYC)
	$(DEL) $(ELF)
	$(DEL) $(BUILD_DIR)
	$(DEL) $(SPEC)
