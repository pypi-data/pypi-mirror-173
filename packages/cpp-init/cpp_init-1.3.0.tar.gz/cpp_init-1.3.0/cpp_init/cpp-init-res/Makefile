CC = gcc
CXX = g++

PROJECT_NAME = {name}

ifeq ($(OS), Windows_NT)
RM = del
EXE = build\$(PROJECT_NAME){winext}
else
RM = rm
EXE = ./build/$(PROJECT_NAME){linext}
endif

FLAGS = -Iinclude {cloptions}
SRC = src/{sourcepath}
COMPILER = {compiler}

$(EXE): $(SRC)
	$(COMPILER) $(SRC) $(FLAGS) -o $(EXE)

test:
ifneq ($(OS), Windows_NT)
	chmod +x $(EXE)
endif
	$(EXE)

clean:
	$(RM) $(EXE)
