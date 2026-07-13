DOCX=DSG-TM-001_Digital_StarGate.docx

word:
	pandoc README.md SUMMARY.md chapters/*.md appendices/*.md -o $(DOCX) --toc

clean:
	rm -f $(DOCX)
