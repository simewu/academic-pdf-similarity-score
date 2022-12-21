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
To automate computing the similarity and only output the similarity score (for usage by a machine) use:
```
python3 run.py example_paper_1_bitcoin.pdf example_paper_2_ethereum.pdf
```

## Example output:
> python3 run.py file1.pdf file2.pdf
> 
> > 40.84857950319798%
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
> Most used words in primary paper: the, to, a, of, and, block, is, z, hash, be, in, it, transaction, p, by, that, transactions, for, as, nodes, with, chain, on, an, can, attacker, if, network, we, proof-of-work, q, will, are, not, blocks, he, one, honest, owner, from, they, k, without, but, this, public, key, new, s, tx, need, all, -, probability, system, would, has, each, timestamp, trusted, cpu, than, value, problem, them, longest, only, at, more, coin, next, or, after, coins, time, nonce, up, merkle, payments, party, using, proof, power, long, majority, were, any, verify, have, work, node, prev, sender, peer-to-peer, electronic, solution, still, make, their, information, could, mint, double, which, its, back, when, number, working, incentive, root, header, privacy, digital, third, into, while, trust, model, must, payment, other, server, previous, first, such, get, before, once, change, then, catch, branch, his, linking, poisson, i, w, signatures, required, double-spending, generate, effort, parties, enough, based, there, accepted, no, control, payee, every, running, way, our, item, average, until, added, per, accept, some, amount, computer, security, made, being, pages, directly, financial, propose, cannot, redoing, messages, broadcast, basis, what, works, possible, since, increases, off, two, protect, order, secure, money, sign, later, confirm, single, history, received, needs, signature, private, hashed, zero, bits, been, also, many, exponentially, finds, broadcasts, spent, consider, keep, may, receive, case, becomes, longer, do, reach, starts, circulation, containing, rules, him, own, tree, should, verification, place, see, invalid, inputs, never, ever
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
For researchers, consider using the contents from file_2.txt (the primary PDF) to further analyze the document.
