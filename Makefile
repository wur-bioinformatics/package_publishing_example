all: assignment.md
	pandoc --pdf-engine=xelatex --from=gfm -o assignment.pdf assignment.md

clean:
	rm -f workshop.pdf
