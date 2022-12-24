# Compute the Similarity Between PDFs
Services like [crossref](https://www.crossref.org/services/similarity-check/) offer a similarity tool to compare the contents of two manuscripts, returning a percentage of how similar one is to another. However, these tools are closed-source, and often require a membership. Free online tools may steal your manuscript, and can be inaccurate.

This open-source tool computes the similarity just like crossref, but is freely accessible to use by anyone. It takes in two PDF files (preferrably academic papers), and converts them into file_1.txt and file_2.txt, then uses:

```console
git diff --minimal --ignore-all-space --word-diff=porcelain --no-index --output file_diff.txt file_1.txt file_2.txt
```

to compare the words in each file. The similarity percentage does the same as crossref by computing:

```python
similarity = similar_words / initial_word_count
```

## Usage
To use the UI to select the PDF files with a verbose and pretty-printed output, including the word differences and the most occuring words, use:
```console
python3 run.py
```
(Windows users can double-click run.bat).

To automate computing the similarity and only output the similarity score (for usage by a machine) use:
```console
python3 run.py file1.pdf file2.pdf
```

## Example output:
```
> python3 run.py example_1_bitcoin_nakamoto.pdf example_2_bitcoin_wright.pdf
0.8582677165354331

> python3 run.py

Select the baseline PDF/TXT file:
  File 1  -  example_1_bitcoin_nakamoto.pdf
  File 2  -  example_2_bitcoin_wright.pdf
  File 3  -  file_1.txt
  File 4  -  file_2.txt
Please select a file (1 to 2): 1

Select the primary PDF/TXT file:
  File 1  -  example_1_bitcoin_nakamoto.pdf
  File 2  -  example_2_bitcoin_wright.pdf
  File 3  -  file_1.txt
  File 4  -  file_2.txt
Please select a file (1 to 2): 2

Bitcoin: A Peer-to-Peer Electronic Cash System
-Satoshi Nakamoto satoshin@gmx.com www.bitcoin.org
+Dr Craig S Wright craigswright@acm.org Charles Sturt University
Abstract. A purely peer-to-peer version of electronic cash would allow online payments to be sent directly from one party to another without
+the burdens of
going through a financial institution. [...]

Most used words in the primary paper: the (241), to (119), [...]

Baseline file word count: 3429
Primary file word count: 3476
Added words: 68
Removed words: 21
Similar words: 2943

similar/primary: 0.846662830840046
similar/baseline: 0.8582677165354331
similarity = max(similar/primary, similar/baseline)
--------------------------------------------------
 Similarity score: 86% (0.8582677165354331 = red) 
--------------------------------------------------
Decrease similarity by scrolling up and reducing the white/similar words in the diff
```

## Additionally
For researchers, consider using the contents from file_2.txt (the primary PDF) to further analyze the document, e.g., Microsoft Word has some text analysis tools under Review --> Editor, and Grammarly can catch typos.
