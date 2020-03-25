import random
# class ProbTree:

    # def __init__(self):
        # self.l = []
        # self.total = 0 

    # def add(self, item):
        # self.total += 1
        # self.l.append(item)
        # # self.total += 1
        # # if item in self.d:
            # # self.d[item] += 1
        # # else:
            # # self.d[item] = 1

    # def __str__(self):
        # return "|| dict: " + str(self.l) + " total items: " + str(self.total) + " ||"

# process file into probability sequences
PUNCTUATION = {"\"", "-", ",", ".", "(", ")", "!", "?", " "}

f = open("./corpus.txt", "r")
lines = f.read().split("\n")

def process(s):
    """
    given a string, process it into a list such that:
    it is split on spaces,
    and punctuations are on thier own
    """
    ans = []
    current_sampling = ""
    for i in range(len(s)):
        if s[i] in PUNCTUATION:
            if current_sampling != "":
                ans.append(current_sampling) 
                current_sampling = ""
            #also add in non-space punctuation
            if s[i] != " ":
                ans.append(s[i])
        else:
            current_sampling += s[i]
    if current_sampling:
        ans.append(current_sampling)
    return ans

def generate_links(lines, n):
    starting_words = []
    word_links = dict()
    for line in lines:
        line = process(line) 
        if len(line) > n:
            starting_words.append(tuple(line[i] for i in range(n)))
        
        for ind, word in enumerate(line):
            endpoint = min(ind + n, len(line))
            word_grouping = tuple(line[j] for j in range(ind, endpoint))
            if word_grouping in word_links:
                if ind + n < len(line):
                    word_links[word_grouping].append(line[ind + n])
                else:
                    word_links[word_grouping].append("\n")
            else:
                word_links[word_grouping] = []
                if ind + n < len(line):
                    word_links[word_grouping].append(line[ind + n])
                else:
                    word_links[word_grouping].append("\n")
    return starting_words, word_links

starting_words, word_links = generate_links(lines, 3)
# for word in word_links:
    # print(str(word) + " : " + str(word_links[word]))

def generate_sentence(wl, sw):
    rand = random.randrange(len(sw))
    gen_word = sw[rand]
    sentence = ""
    for word in gen_word[:-1]:
        sentence += word + " "
    while not gen_word[-1] == "\n":
        sentence += gen_word[-1] + " "
        next_word_list = wl[gen_word]
        # print(gen_word)
        # print(next_word_list)
        rand = random.randrange(len(next_word_list))
        gen_word = (*(gen_word[1:]), next_word_list[rand])
    return sentence

for i in range(30):
    print(generate_sentence(word_links, starting_words))
