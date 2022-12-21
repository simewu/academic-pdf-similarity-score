# Compute the Similarity Between PDFs
This program takes in two PDF files (preferrably academic papers), converts them into file_1.txt and file_2.txt, then uses:

```
git diff --minimal --ignore-all-space --word-diff=porcelain --no-index --output file_diff.txt file_1.txt file_2.txt
```

to compare the words in each file. The similarity score percentage is computed with:

```
similarity = 1 - (words_added + words_removed) / (initial_word_count * 2)
```

## Usage
To use UI to select the PDF files with a verbose and pretty-printed output, including the word differences and the most occuring words, use:
```
python3 run.py
```
or double-click run.bat for Windows users.

---

To automate computing the similarity and only print the similarity score (for usage by a machine) use:
```
python3 run.py file1.pdf file2.pdf
```

## Example output:
> python3 run.py
> 
> Select the primary PDF file:
> 
> > File 1  -  example_paper_1_bitcoin.pdf
> > 
> > File 2  -  example_paper_2_ethereum.pdf
> 
> Please select a file (1 to 2): 1
> 
> 
> Select the baseline PDF file:
> 
> > File 1  -  example_paper_1_bitcoin.pdf
> > 
> > File 2  -  example_paper_2_ethereum.pdf
> 
> Please select a file (1 to 2): 2
> 
> [WORD DIFF]
> 
> Most used words in primary paper: [MOST COMMON WORDS]
> 
> 
> > Primary file word count: 3441
> > 
> > Baseline file word count: 13446
> > 
> > Added words: 12956
> > 
> > Removed words: 2951
> > 
> > 1 - (added + removed) / (baseline * 2)
> > 
> > \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-
> > 
> > Similarity score: 40.84857950319798%
> > 
> > \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-
> > 

## Additionally
For researchers, consider using the contents from file_1.txt (the primary PDF) to further analyze your document.
