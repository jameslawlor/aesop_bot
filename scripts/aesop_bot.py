import random
import string
import numpy as np
import pronouncing

def clean_text(text):
    translator= str.maketrans('','',string.punctuation) # remove punctuation
    text = [line.translate(translator) for line in text]
    text = [line.strip().lower() for line in text] #lwrcase and strip
    return text

def markov_model(text_input, n):
    """
    N-gram Markov model, takes in corpus and returns dict of n-grams
    """
    dic = {}
    for i in range(len(text_input) - n):
        gram = tuple(text_input[i:i+n])
        next_word = text_input[i+n]
        if gram not in dic:
            dic[gram] = [next_word]
        else:
            dic[gram].append(next_word)
    return dic

def remove_true_aesop_lines(true_lines, pairs_of_lyrics):
    true_aesop = " ".join(true_lines)
    lst = []
    for pair in pairs_of_lyrics:
        l1 = pair[0]
        l2 = pair[1]
        if (l1 not in true_aesop) and (l2 not in true_aesop):
            lst.append(pair)
    return lst

def clean_pairs(list_of_pairs):
    lst = []
    for pair in list_of_pairs:
        [l1, l2] = pair
        l1 = l1.capitalize().replace(' i ', ' I ')
        l2 = l2.capitalize().replace(' i ', ' I ')
        l1 = l1 + ","
        l2 = l2 + '.'
        lst.append([l1,l2])
    return lst

def find_rhyming_pairs(list_of_lines):
	banned_words = ['i','we','a','my','by','is','and',
					'he','she','the','to','your','or','an','you']
	rhyming_pairs = []
	for line1 in list_of_lines:
		for line2 in list_of_lines:
			first_ending_word = line1[-1]
			second_ending_word = line2[-1]
			if line2 != line1:
				if second_ending_word in pronouncing.rhymes(first_ending_word):
					if (first_ending_word not in banned_words) and\
                        (second_ending_word not in banned_words): 
						l1 = " ".join(line1)
						l2 = " ".join(line2)
						rhyming_pairs.append([l1,l2])
	return rhyming_pairs

def generate_lyrics(model, iters):
	
	# Generate new lyrics
	generated_lines = []
	
	for i in range(iters):
		line = random.choice(list(model.keys()))
		current_word = line
		initial_line_length = len(line)
		desired_line_length = random.choice(range(6,10))
		while len(line) < desired_line_length:
			candidates = model[current_word]
			next_word = np.random.choice(candidates)
			line = line + (next_word,)
			current_word = line[-2:]
		generated_lines.append(line)
	
	return generated_lines


if __name__ == '__main__':

	lyrics_source = random.choice(['ROCK', 'BOT'])

	lyrics_source = 'ROCK'
	lyrics_source = 'BOT'

	corpus = open("../data/aesop_corpus.txt","r").readlines()
	text = clean_text(corpus)

	if lyrics_source == 'BOT':
		blob = " ".join(text).split()
		dic = markov_model(blob, 2)
		bot_lyrics = generate_lyrics(dic, 100)
		rhyming_lyric_pairs = find_rhyming_pairs(bot_lyrics)
		rhyming_lyric_pairs = remove_true_aesop_lines(text, rhyming_lyric_pairs)
		rhyming_lyric_pairs = clean_pairs(rhyming_lyric_pairs)
		lyrics = random.choice(rhyming_lyric_pairs)
	else:
		rhyming_aesop_pairs = []
		for ix in range(len(text[:-1])):
			line1 = text[ix]
			line2 = text[ix+1]
			if (len(line1) > 0) and (len(line2) > 0):
				first_ending_word = text[ix].split()[-1]
				second_ending_word = text[ix+1].split()[-1]
				if second_ending_word in pronouncing.rhymes(first_ending_word):
					rhyming_aesop_pairs.append([line1,line2])
		rhyming_aesop_pairs = clean_pairs(rhyming_aesop_pairs)
		lyrics = random.choice(rhyming_aesop_pairs)

	print("{}: \n {}".format(lyrics_source,lyrics))
