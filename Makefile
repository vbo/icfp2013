PROJECT_DIR=./fast_solver

INCLUDES_DIR=$(PROJECT_DIR)
INCLUDES=$(wildcard $(INCLUDES_DIR)/*.h)
SOURCES=$(wildcard $(PROJECT_DIR)/*.c)
EXE_SOURCE=$(PROJECT_DIR)/evaluate.c
EXE=evaluate.exe
LIB_SOURCES=$(filter-out $(EXE_SOURCE),$(SOURCES))
GCC=gcc
LIB=./lib/libbvsolve.so
#PYTHON_INCLUDES_DIR=/usr/include/python2.7

.PHONY: all lib exe
lib: $(LIB)
exe: $(EXE)
all: $(EXE) $(LIB)


$(EXE): $(LIB_SOURCES) $(INCLUDES) $(SOURCES)
	$(GCC) -Wall -O0 $(LIB_SOURCES) $(EXE_SOURCE) -I$(INCLUDES_DIR) -o $@

$(LIB): $(LIB_SOURCES) $(INCLUDES)
	$(GCC) -Wall -O2 --shared $(LIB_SOURCES) -I$(INCLUDES_DIR) -o $(LIB)
