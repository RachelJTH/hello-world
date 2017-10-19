import nltk
# nltk.download()

sentence = "DNA damage response, signal transduction by p53 class mediator resulting in cell cycle arrest"
tokens = nltk.word_tokenize(sentence)
# print tokens

tagged = nltk.pos_tag(tokens)
# print tagged

entities = nltk.chunk.ne_chunk(tagged)
# print entities
