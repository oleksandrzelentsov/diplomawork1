CMD=javac
DEST=bin
OPTS=-d $(DEST)
SRC=src

all: compile run

compile: $(SRC) $(DEST)
	find -name *.java | xargs $(CMD) $(OPTS)

clean:
	find -name *.class | xargs rm

run: $(DEST)/com/termsclient/Main.class
	java -cp $(DEST) com.termsclient.Main
