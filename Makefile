#Makefile for PYQT4 project,
#another version
#usage: make ui
#generate exe or elf: make

MAIN := MainView.py

#EXE := $(patsubst %.py, dist\\%.exe, $(MAIN))
EXE := $(patsubst %.py, %.exe, $(MAIN))
ELF := $(patsubst %.py, %, $(MAIN))

PYC := $(wildcard *.pyc)
SPEC := $(wildcard *.spec)

BUILD_DIR := build

DEL := rm -rf
PYWRAP := pyinstaller

WRAPFLAGS := --hidden-import atexit
WRAPFLAGS += -F
#WRAPFLAGS += -w
WRAPFLAGS += --distpath .

EXTPYTHONPATH := -p d:\ext\Lib

.PHONY: wrap ui clean

wrap: ui $(EXE)

%.exe: %.py
	$(PYWRAP) $(WRAPFLAGS) $(EXTPYTHONPATH) $<

ui:
	make -C Views $@

clean:
	$(DEL) $(EXE)
	$(DEL) $(PYC)
	$(DEL) $(ELF)
	$(DEL) $(BUILD_DIR)
	$(DEL) $(SPEC)
	make -C Views $@
