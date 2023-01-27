import argparse
#argparse module used to link command line interface input to the program
from nltk.tokenize import sent_tokenize, word_tokenize
# tokenize the file into sentences and sentences into words
from nltk.corpus import stopwords
#it removes the stopwords from sentences
from string import punctuation
# access the punctuation from the string
from nltk.probability import FreqDist
#frequency distribution records the number of times each values (i.e. count the frequency of each word)
from heapq import nlargest
#used to find the n largest elements from an iterable,
from collections import defaultdict
#to create a dict which does not have any key , it automatically generates a key during the iteration.

def main():
	args = parse_arguments()
	content = read_file(args.filepath)
	content = sanitize_input(content)

	sent_tokens, word_tokens = tokenize_content(content)
	sent_ranks = score_tokens(sent_tokens, word_tokens)
	print(summarize(sent_ranks, sent_tokens, args.length))

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('filepath', help='File name of text to summarize')
	parser.add_argument('-l', '--length', default=4, help='No. of sentences to return')
	args = parser.parse_args()
	return args
"""Argument Parser :
argparse.ArgumentParser : container for argument specifications.

 ArgumentParser.add_argument() method attaches individual argument specifications to the parser.
 
 ArgumentParser.parse_args() method runs the parser and places the extracted data. 
 It takes arguments passed to the script and convert into an object so it can easily accessed and used within script.
 """
def read_file(path):
	try: # Exception handling in file
		with open(path, 'r') as f:
			return f.read()
	except IOError as e:
		print('File could not be located')
		# Path of file is given as input and open file in read mode

def sanitize_input(data):
	replace = {
		ord('\f') : ' ',
		ord('\t') : ' ',
		ord('\n') : ' ',
		ord('\r') : None
	}
	return data.translate(replace)
"""In this method tab , new line , mathematical problem or curly braces replace by whitespace and none value to reduce the size of file"""

def tokenize_content(content):

	stop_words = set(stopwords.words('english') + list(punctuation))
	#set of English stop words from the NLTK library and punctuation marks
	words = word_tokenize(content.lower())
	#tokenizes the content into a list of words and converts all words to lowercase
	return (sent_tokenize(content), [word for word in words if word not in stop_words])
#returns a tuple containing the list of sentences using the "sent_tokenize" function and the list of words without any stop words

def score_tokens(sent_tokens, word_tokens):
	word_freq = FreqDist(word_tokens) #create a frequency distribution of the words in word_tokens
	rank = defaultdict(int) #generate a defaultdict does not any key , later sentences from sent_tokens becomes the key of dictionary
	#create a dictionary keys are the indices of the sentences in sent_tokens and the values are initially set to 0.
	for i, sent in enumerate(sent_tokens):#iterates through the list of words in the sentence
		for  word in word_tokenize(sent.lower()):# tokenize the sentences into words and coverts into lowercase
			if word in word_freq: #checks if each word exists in the word_freq
				rank[i] += word_freq[word] # if yes then increment the values of corresponding keys

	return rank

def summarize(ranks, sentences, length):
# here ranks= sent_rank= score_tokens = rank dictionary

	if int(length) > len(sentences): #if the length of expected summary is greater than the exact length of file then
		print('You requested more sentences in the summary than there are in the text.')
		return ''

	else:
		indices = nlargest(int(length), ranks, key=ranks.get) #nlargest will return the indices of the length highest-scoring sentences in ranks based on the values of the ranks dictionary.
		final_summary = [sentences[j] for j in indices] #iterates over the elements in the indices list, and for each element j, it selects the sentence from the sentences list that has an index equal to j and adds it to the final_summary list.
		return ' '.join(final_summary) #Finally, it joins the selected sentences together with a space and returns the summary as a single string.



if __name__ == '__main__':
	main()