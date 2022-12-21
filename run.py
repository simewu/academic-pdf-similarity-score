import fitz # install using: pip install PyMuPDF
import getopt
import os
import re
import sys

stats = {'words_added': 0, 'words_removed': 0, 'file1_word_count': 0, 'file2_word_count': 0, 'file1_most_used_words': '', 'file2_most_used_words': ''}

def terminal(cmd):
	return os.popen(cmd).read()

def wordDistribution(string, dictionarySize = 230):
	wordCount = 0
	wordDist = ''
	words = string.split()
	histogram = {}
	for word in words:
		word = word.lower()
		if len(word) == 0: continue
		match = re.search('[^a-z\-]*([a-z\-]+)[^a-z\-]*', word)
		if match is not None:
			wordCount += 1
			word = match.group(1)
			if dictionarySize is not None:
				if word not in histogram:
					histogram[word] = 1
				else:
					histogram[word] += 1

	if dictionarySize is not None:
		histogram = dict(sorted(histogram.items(), key=lambda item: item[1], reverse=True))
		keys = list(histogram.keys())
		if len(keys) > dictionarySize:
			keys = keys[0:dictionarySize]
		for word in keys:
			if len(wordDist) > 0: wordDist += ', '
			wordDist += word

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
		return ''

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
			pass
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

def generateWordList(fileName):
	file = open(fileName, 'r')
	dictionary = {}
	for line in file:
		if len(line.strip()) <= 1: continue
		dictionary[line.strip()] = True
	file.close()
	return dictionary


def similarity(fileName1 = None, fileName2 = None, verbose = True):
	global stats
	wordlist = generateWordList('academic_wordlist.txt')
	width, height = os.get_terminal_size()

	fileNames = []

	if fileName1 is None:
		print()
		print(color('white', 'cyan', ''.center(width)))
		print(color('white', 'cyan', 'Select the primary PDF file:'.center(width)))
		print(color('white', 'cyan', ''.center(width)))
		fileName1 = selectFile(r'.*\.pdf', r'', False)
		assert fileName1 is not None, 'Please select a valid file'
	fileNames.append(fileName1)


	if fileName2 is None:
		print(color('white', 'yellow', ''.center(width)))
		print(color('white', 'yellow', 'Select the baseline PDF file:'.center(width)))
		print(color('white', 'yellow', ''.center(width)))
		fileName2 = selectFile(r'.*\.pdf', r'', False)
		assert fileName2 is not None, 'Please select a valid file'
	fileNames.append(fileName2)

	for i, fileName in enumerate(fileNames):
		contents = ''
		with fitz.open(fileName) as doc:
			for page in doc:
				contents += page.get_text()

		# Restore any workd-breaks
		# First we search for any split words that need the a hyphen
		matches = re.findall(r'([A-Za-z0-9\.]+)-\n([A-Za-z0-9\.]+)', contents)
		for match in matches:
			word1 = match[0].lower()
			word2 = match[1].lower()
			if (word1 in wordlist and word2 in wordlist) or (word1 + '-' + word2) in wordlist:
				contents = contents.replace(match[0] + '-\n' + match[1], match[0] + '-' + match[1])
		# Then combine all auto-broken words
		contents = re.sub(r'-\n', '', contents)

		# Remove any extra spaces
		contents = re.sub(r'\s*\n\s*', '\n', contents)
		# Remove numbers without context
		contents = re.sub(r'\n([0-9\.\s]+\n)+', '\n', contents)
		# Remove author names on each page
		contents = re.sub(r'\n([A-Z\.]+ [A-Z][a-z]+,? )*and ([A-Z\.]+ [A-Z][a-z]+)\n', '\n', contents)
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

		# Fix other unicode characters
		contents = re.sub(r'[“”]', '"', contents)
		contents = re.sub(r'’', '\'', contents)

		file = open(f'file_{i + 1}.txt', 'w', encoding='utf8', errors='ignore')
		file.writelines(contents)
		file.close()

		stats[f'file{i + 1}_word_count'], stats[f'file{i + 1}_most_used_words'] = wordDistribution(contents)
		

	terminal('git diff --minimal --ignore-all-space --word-diff=porcelain --no-index --output file_diff.txt file_1.txt file_2.txt')
	differences = open('file_diff.txt', 'r', encoding='utf8', errors='ignore')
	diffStarted = False
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
		if line.startswith('-'):
			wordCount, _ = wordDistribution(line[1:], None)
			stats['words_removed'] += wordCount
			if verbose: print(color('red', 'black', line))

	baseline = stats['file2_word_count']
	added = stats['words_added']
	removed = stats['words_removed']
	if baseline != 0:
		similarity = 1 - (added + removed) / (baseline * 2)
	else: similarity = 0
	similarity *= 100

	if verbose:
		print()
		print(color('yellow', 'black', 'Most used words in primary paper: ') + stats['file1_most_used_words'])
		print()
		print(color('white', 'purple', ''.center(width)))
		print(color('yellow', 'purple', f'Primary file word count: {stats["file1_word_count"]}'.center(width)))
		print(color('yellow', 'purple', f'Baseline file word count: {stats["file2_word_count"]}'.center(width)))
		print(color('yellow', 'purple', f'Added words: {stats["words_added"]}'.center(width)))
		print(color('yellow', 'purple', f'Removed words: {stats["words_removed"]}'.center(width)))
		print(color('white', 'purple', ''.center(width)))
		print(color('red', 'purple', f'1 - (added + removed) / (baseline * 2)'.center(width)))
		print(color('white', 'purple', f'--------------------------------------'.center(width)))
		print(color('white', 'purple', f'Similarity score: {similarity}%'.center(width)))
		print(color('white', 'purple', f'--------------------------------------'.center(width)))
		print(color('white', 'purple', ''.center(width)))
	return similarity


if len(sys.argv) == 3:
	fileName1 = sys.argv[1]
	fileName2 = sys.argv[2]
	output = str(similarity(fileName1, fileName2, False)) + '%'
	print(output)
else:
	similarity()