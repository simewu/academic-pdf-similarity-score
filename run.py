#!/usr/bin/python3

from unidecode import unidecode # Install using: pip install Unidecode
import fitz # Install using: pip install PyMuPDF
import getopt
import importlib.machinery
import math
import os
import re
import sys

# Attempt to repair word-breaks, fix paragraphs, white-space, and normalize strange symbols
improveFormatting = True

supportsColor = importlib.machinery.SourceFileLoader('supportsColor','supports-color-python/supports_color/__init__.py').load_module()
useTerminalColors = supportsColor.supportsColor.stdout

# Gets filled with data values as the script runs
stats = {'similar_words': 0, 'words_added': 0, 'words_removed': 0, 'file1_word_count': 0, 'file2_word_count': 0, 'file1_most_used_words': '', 'file2_most_used_words': ''}

# Call an os command
def terminal(cmd):
	return os.popen(cmd).read()

# Clear the terminal
def clearTerminal():
	if os.name == 'nt':
		terminal('cls')
	else:
		terminal('clear')

# Get the number of words, and the distribution of [dictionarySize] words in a given string
def wordDistribution(string, dictionarySize = 100):
	wordCount = 0
	wordDist = ''
	words = string.split()
	histogram = {}
	for word in words:
		word = word.lower().strip()
		prevWord = ''
		while(word != prevWord):
			prevWord = word
			symbols = '!"#&\'()*+,-./0123456789:;<=>?@[\\]^_\\`{|}~ '
			if len(word) > 0 and word[-1] in symbols: word = word[:-1]
			if len(word) > 0 and word[0] in symbols: word = word[1:]
		if len(word) == 0: continue
		wordCount += 1
		if dictionarySize is not None:
			if word not in histogram:
				histogram[word] = 1
			else:
				histogram[word] += 1

	if dictionarySize is not None:
		histogram = dict(sorted(histogram.items(), key=lambda item: item[1], reverse=True))
		keys = list(histogram.keys())
		if dictionarySize > 0 and len(keys) > dictionarySize:
			keys = keys[0:dictionarySize]
		for word in keys:
			if histogram[word] == 1: break
			if len(wordDist) > 0: wordDist += ', '
			wordDist += word
			wordDist += color('purple', 'black', ' (' + str(histogram[word]) + ')')

	return wordCount, wordDist

# Given two regular expressions, list the files that match/don't match it, and ask the user to select from them
def selectFile(inclusionRegex, exclusionRegex = '', subdirs = False):
	files = []
	if subdirs:
		for (dirpath, dirnames, filenames) in os.walk('.'):
			for file in filenames:
				path = os.path.join(dirpath, file)
				if path[:2] == '.\\': path = path[2:]
				if bool(re.match(inclusionRegex, path)) and not bool(re.match(exclusionRegex, path)):
					files.append(path)
	else:
		for file in os.listdir(os.curdir):
			if os.path.isfile(file) and bool(re.match(inclusionRegex, file)):
				files.append(file)
	print()
	if len(files) == 0:
		print(f'No files were found that match "{inclusionRegex}"')
		print()
		return None

	for i, file in enumerate(files):
		print('  ' + color('cyan', 'black', f'File {i + 1}  -  ') + color('yellow', 'black', file))
	print()

	selection = None
	while selection is None:
		try:
			i = int(input(f'Please select a file (1 to {len(files)}): '))
		except KeyboardInterrupt:
			sys.exit()
		except:
			return None
		if i > 0 and i <= len(files):
			selection = files[i - 1]
	print()
	return selection

# Change the color of text in the terminal
# Leaving the forground or background blank will reset the color to its default
# Providing a message will return the colored message (reset to default afterwards)
# If it's not working for you, be sure to call os.system('cls') before modifying colors
# Usage:
# - print(color('black', 'white', 'Inverted') + ' Regular')
# - print(color('black', 'white') + 'Inverted' + color() + ' Regular')
def color(foreground = '', background = '', message = ''):
	if not useTerminalColors: return message
	fg = {
		'red': '1;31',
		'green': '1;32',
		'yellow': '1;33',
		'blue': '1;34',
		'purple': '1;35',
		'cyan': '1;36',
		'white': '1;37',
		'black': '0;30',
		'gray': '1;30'
	}
	bg = {
		'red': ';41m',
		'green': ';42m',
		'yellow': ';43m',
		'blue': ';44m',
		'purple': ';45m',
		'cyan': ';46m',
		'white': ';47m',
		'black': ';48m'
	}
	if foreground not in fg or background not in bg: return '\033[0m' # Reset
	color = f'\033[0m\033[{ fg[foreground.lower()] }{ bg[background.lower()] }'
	if message == '': return color
	else: return f'{ color }{ str(message) }\033[0m'

# Given a file full of words, return a dictionary for the words
def generateWordList(fileName):
	file = open(fileName, 'r')
	dictionary = {}
	for line in file:
		if len(line.strip()) <= 1: continue
		dictionary[line.strip()] = True
	file.close()
	return dictionary

# Compute the similarity between two files
def similarity(fileName1 = None, fileName2 = None, verbose = True):
	global stats
	wordlist = generateWordList('academic_wordlist.txt')
	if verbose:
		width, height = os.get_terminal_size()

	fileNames = []
	while fileName1 is None or len(fileName1) == 0:
		print(color('white', 'yellow', ''.center(width)))
		print(color('white', 'yellow', 'Select the baseline PDF/TXT file:'.center(width)))
		print(color('white', 'yellow', ''.center(width)))
		fileName1 = selectFile(r'.*\.(pdf|txt)', r'', False)
		assert fileName1 is not None, 'No file was selected. Please make sure that there is a PDF or text file in the directory of this script.'
	fileNames.append(fileName1)


	while fileName2 is None or len(fileName2) == 0:
		print()
		print(color('white', 'cyan', ''.center(width)))
		print(color('white', 'cyan', 'Select the primary PDF/TXT file:'.center(width)))
		print(color('white', 'cyan', ''.center(width)))
		fileName2 = selectFile(r'.*\.(pdf|txt)', r'', False)
		assert fileName2 is not None, 'No file was selected. Please make sure that there is a PDF or text file in the directory of this script.'

	fileNames.append(fileName2)

	for i, fileName in enumerate(fileNames):
		contents = ''
		numWords = 0
		if fileName.endswith('.txt'):
			with open(fileName, 'r', encoding='utf8', errors='ignore') as file:
				contents = file.read()
		else:
			with fitz.open(fileName) as doc:
				for page in doc:
					try:
						page.clean_contents(sanitize=True)
						numWords += len(page.get_text_words())
						contents += page.get_text()
					except AttributeError:
						page._cleanContents()
						numWords += len(page.getTextWords())
						contents += page.getText()

		if improveFormatting:
			# Optimize until it cannot optimize any further
			prev_contents = ''
			while prev_contents != contents:
				# Restore any word-breaks
				# First we search for any split words that need the a hyphen
				matches = re.findall(r'([A-Za-z0-9\.]+)-\n([A-Za-z0-9\.]+)', contents)
				for match in matches:
					word1 = match[0].lower().rstrip()
					word2 = match[1].lower().lstrip()
					if (word1 in wordlist and word2 in wordlist) or (word1 + '-' + word2) in wordlist:
						contents = contents.replace(match[0] + '-\n' + match[1], match[0] + '-' + match[1])
				# Then combine all auto-broken words
				contents = re.sub(r'-\n', '', contents)
				contents = re.sub(r'([a-zA-Z])\s*-\s*([a-zA-Z])', '\\1-\\2', contents)
				# Remove any extra spaces
				contents = re.sub(r'\s*\n\s*', '\n', contents)
				# Remove numbers without context
				#contents = re.sub(r'\n([0-9\.\s]+\n)+', '\n', contents)
				# Remove author names on each page
				#contents = re.sub(r'\n([A-Z\.]+ [A-Z][a-z]+,? )*and ([A-Z\.]+ [A-Z][a-z]+)\n', '\n', contents)
				contents = re.sub(r'Electronic copy available at: .*', '', contents)
				contents = re.sub(r'Authorized licensed use limited to: .*', '', contents)
				# Restore mid-sentence breaks
				contents = re.sub(r'(\b[a-z\-]+)\n', '\\1 ', contents)
				contents = re.sub(r'\n([a-z\-]+)', ' \\1', contents)
				contents = re.sub(r'(\. [A-Z][a-z\-]*)\n', '\\1 ', contents)
				contents = re.sub(r'([\.:,=])\n', '\\1 ', contents)
				contents = re.sub(r'([0-9])\n', '\\1 ', contents)
				contents = re.sub(r'\n\.', '.', contents)
				# Merge any titles together
				contents = re.sub(r'([A-Z][a-z\-]*)\n([A-Z][a-z\-]*)', '\\1 \\2', contents)
				contents = re.sub(r'([A-Z][a-z\-]*)\n', '\\1: ', contents)
				contents = re.sub(r'\n([A-Z][a-z\-]*)', ': \\1', contents)
				# Remove any double spaces
				contents = re.sub(r' {2,}', ' ', contents)
				# Fix/normalize other unicode characters
				contents = unidecode(contents)

				prev_contents = contents

		file = open(f'file_{i + 1}.txt', 'w', encoding='utf8', errors='ignore')
		file.writelines(contents)
		file.close()

		stats[f'file{i + 1}_word_count'], stats[f'file{i + 1}_most_used_words'] = wordDistribution(contents)

		if verbose:
			if numWords == 0: numWords = stats[f'file{i + 1}_word_count']
			print('Number of words:', numWords, 'after optimization:', stats[f'file{i + 1}_word_count'])
			print()

	terminal('git diff --minimal --ignore-all-space --word-diff=porcelain --no-index file_1.txt file_2.txt > file_diff.txt')
	differences = open('file_diff.txt', 'r', encoding='utf8', errors='ignore')
	diffStarted = False
	numDiffLines = 0
	for line in differences:
		line = line.strip()
		if not diffStarted:
			if line.startswith('@@') and line.endswith('@@'):
				diffStarted = True
			continue

		if line.startswith('+'):
			wordCount, _ = wordDistribution(line[1:], None)
			stats['words_added'] += wordCount
			if verbose: print(color('green', 'black', line))
		elif line.startswith('-'):
			wordCount, _ = wordDistribution(line[1:], None)
			stats['words_removed'] += wordCount
			if verbose: print(color('red', 'black', line))
		else:
			if line == '~': continue
			wordCount, _ = wordDistribution(line, None)
			stats['similar_words'] += wordCount
			if verbose: print(color('white', 'black', line))
		numDiffLines += 1

	baseline = stats['file1_word_count']
	primary = stats['file2_word_count']
	#added = stats['words_added']
	#removed = stats['words_removed']
	similar = stats['similar_words']
	if numDiffLines == 0:
		similar = max(baseline, primary)

	if primary != 0 and baseline != 0:
		similarity = max(similar / primary, similar / baseline)
	else:
		similarity = 0

	if verbose:
		similarity_color = ''
		if math.ceil(similarity * 100) == 0:
			similarity_color = 'light blue'
		elif math.ceil(similarity * 100) <= 24:
			similarity_color = 'dark blue'
		elif math.ceil(similarity * 100) <= 49:
			similarity_color = 'yellow'
		elif math.ceil(similarity * 100) <= 74:
			similarity_color = 'orange'
		else:
			similarity_color = 'red'
		similarity_str = f' Similarity score: {math.ceil(similarity * 100)}% ({similarity} = {similarity_color}) '
		print(color('yellow', 'black', 'Most used words in the primary paper: ') + stats['file1_most_used_words'])
		print()
		print(color('white', 'purple', ''.center(width)))
		print(color('yellow', 'purple', f'Baseline file word count: {stats["file1_word_count"]}'.center(width)))
		print(color('yellow', 'purple', f'Primary file word count: {stats["file2_word_count"]}'.center(width)))
		print(color('yellow', 'purple', f'Added words: {stats["words_added"]}'.center(width)))
		print(color('yellow', 'purple', f'Removed words: {stats["words_removed"]}'.center(width)))
		print(color('yellow', 'purple', f'Similar words: {stats["similar_words"]}'.center(width)))
		print(color('white', 'purple', ''.center(width)))
		print(color('cyan', 'purple', f'similarity = max(similar/primary, similar/baseline)'.center(width)))
		print(color('white', 'purple', ('-' * len(similarity_str)).center(width)))
		print(color('white', 'purple', similarity_str.center(width)))
		print(color('white', 'purple', ('-' * len(similarity_str)).center(width)))
		print(color('white', 'purple', ''.center(width)))
		print(color('purple', 'black', f'Decrease similarity by scrolling up and reducing the white/similar words in the diff'.center(width)))
	return similarity

if len(sys.argv) == 3:
	fileName1 = sys.argv[1]
	fileName2 = sys.argv[2]
	output = str(similarity(fileName1, fileName2, False))
	print(output)
else:
	clearTerminal()
	similarity()