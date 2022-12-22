# Compute the Similarity Between Two PDFs
Services like [crossref](https://www.crossref.org/services/similarity-check/) offer a similarity tool to compare the contents of two manuscripts, returning a percentage of how similar one is to another. However, these tools are closed-source, and often require a membership. Free online tools may steal your manuscript, and can be inaccurate.

This open-source tool computes the similarity just like crossref, but is freely accessible to use by anyone. It takes in two PDF files (preferrably academic papers), and converts them into file_1.txt and file_2.txt, then uses:

```
git diff --minimal --ignore-all-space --word-diff=porcelain --no-index --output file_diff.txt file_1.txt file_2.txt
```

to compare the words in each file. The similarity percentage does the same as crossref by computing:

```
similarity = similar_words / initial_word_count
```

## Usage
To use UI to select the PDF files with a verbose and pretty-printed output, including the word differences and the most occuring words, use:
```
python3 run.py
```
(Windows users can double-click run.bat).

To automate computing the similarity and only output the similarity score (for automation and usage by a machine) use:
```
python3 run.py file1.pdf file2.pdf
```

## Example output:
> python3 run.py example_paper_1_bitcoin.pdf example_paper_2_ethereum.pdf
> 
> > 14.45993031358885%
> 
> python3 run.py
> 
> Select the baseline PDF file:
> 
> > File 1  -  example_paper_1_bitcoin.pdf
> > 
> > File 2  -  example_paper_2_ethereum.pdf
> 
> Please select a file (1 to 2): 1
> 
> 
> Select the primary PDF file:
> 
> > File 1  -  example_paper_1_bitcoin.pdf
> > 
> > File 2  -  example_paper_2_ethereum.pdf
> 
> Please select a file (1 to 2): 2
> 
> [WORD DIFF]
> 
> Most used words in primary paper: the, to, a, of, and, block, is, hash, z, be, in, it, transaction, p, by, that, transactions, for, as, nodes, with, chain, on, an, can, attacker, if, network, we, q, proof-of-work, will, are, not, blocks, he, one, honest, owner, -, from, they, k, without, but, this, public, key, new, s, tx, need, all, probability, system, would, has, each, timestamp, trusted, cpu, than, value, problem, them, longest, only, at, more, coin, next, or, after, coins, time, nonce, up, merkle, payments, party, using, proof, power, long, majority, were, any, verify, have, work, node, prev, sender, peer-to-peer, electronic, solution, still, make, their, information, could, mint, double, which, its, back, when, number, working, incentive, root, header, privacy, digital, third, into, while, trust, model, must, payment, other, server, previous, first, such, get, before, once, change, then, catch, branch, his, linking, poisson, i, w, signatures, required, double-spending, generate, effort, parties, enough, based, there, accepted, no, control, payee, every, running, way, our, item, average, until, added, per, accept, some, amount, computer, security, made, being, pages, directly, financial, propose, cannot, redoing, messages, broadcast, basis, what, works, possible, since, increases, off, two, protect, order, secure, money, sign, later, confirm, single, history, received, needs, signature, private, hashed, zero, bits, been, also, many, exponentially, finds, broadcasts, spent, consider, keep, may, receive, case, becomes, longer, do, reach, starts, circulation, containing, rules, him
> 
> 
> > Baseline file word count: 3444
> > 
> > Primary file word count: 13446
> > 
> > Added words: 12948
> > 
> > Removed words: 2946
> > 
> > Similar words: 498
> > 
> > 
> > max(similar/primary, similar/baseline)
> > 
> > \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-
> > 
> > Similarity score: 14.45993031358885%
> > 
> > \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-
> > 

## Additionally
For researchers, consider using the contents from file_2.txt (the primary PDF) to further analyze the document.
