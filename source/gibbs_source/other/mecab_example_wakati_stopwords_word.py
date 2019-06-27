#!/usr/bin/env python
#coding:utf-8
import MeCab
import os
import glob
import re
import codecs

# http://hivecolor.com/id/86
# テキストマイニングの前処理。名詞抽出、ストップワード除去

'''
def extractKeyword(text):
	u"""textを形態素解析して、名詞のみのリストを返す"""
	tagger = MeCab.Tagger()
	encoded_text = text.encode('utf-8')
	node = tagger.parseToNode(encoded_text).next
	keywords = []
	while node:
		if node.feature.split(",")[0] == "名詞":
			keywords.append(node.surface)
		node = node.next
	return keywords

def splitDocument(documents):
	u"""文章集合を受け取り、名詞のみ空白区切りの文章にして返す"""
	splitted_documents = []
	for d in documents:
		keywords = extractKeyword(d)
		splitted_documents.append(' '.join(keywords))
	return splitted_documents

def removeStoplist(documents, stoplist):
	u"""ストップワードを取り除く"""
	stoplist_removed_documents = []
	for document in documents:
		words = []
		for word in document.lower().split():
			if word not in stoplist:
				words.append(word)
		stoplist_removed_documents.append(words)
	return stoplist_removed_documents

def getTokensOnce(all_tokens):
	u"""一回しか出現しない単語を返す"""
	tokens_once = set([])
	for word in set(all_tokens):
		if all_tokens.count(word) == 1:
			tokens_once.add(word)
	return tokens_once

def removeTokensOnce(documents, tokens_once):
	u"""一回しか出現しない単語を取り除く"""
	token_removed_documents = []
	for document in documents:
		words = []
		for word in document:
			if word not in tokens_once:
				words.append(word)
		token_removed_documents.append(words)
	return token_removed_documents'''

if __name__ == "__main__":
	DATA_NUM = 400
	mt = MeCab.Tagger("-Owakati")
	
	output_path = "/home/emlab/Caffe/SIGVerse3Log/0920_10room/10rooms_edits0921Kobayashi/wakati_words_functions_room010/words" # check output path
	
	input_path = "/home/emlab/Caffe/SIGVerse3Log/0920_10room/10rooms_edits0921Kobayashi/words_functions_room010/words" # check input path
	
	stoplist = set("ここ これ と この です いい し します ます する は の て に また を が で 。".split()) # 通常の文字列でよい
	for i in range(DATA_NUM):
		#word=[0 for n in range(word_class)]
		#signal=("word"+repr(i)+".txt") in file
		signal = os.path.isfile(input_path + "/word%03d.txt"%i)
		
		if signal==True:
			f=codecs.open(input_path + "/word%03d.txt"%i,"r","utf-8")
			data=f.read()
			line=data.split("\n")
			f.close()
			f_out = open(output_path + "/word%03d.txt"%i,"w")
			for k in range(len(line)):
				text = mt.parse(line[k].encode("utf-8"))
				words = []
				for word in text.split():
					if word not in stoplist:
						#words.append(word)
						f_out.write(word)
						f_out.write(" ")
			#f_out.write(str(words))
			f_out.close()
		else:
			pass
	
	"""print 'raw_documents:'
	for d in raw_documents:
		print d
	print ''

	# 空白区切りの文字列を入れるリスト
	splitted_documents = splitDocument(raw_documents)

	print 'splitted_documents:'
	for d in splitted_documents:
		print d
	print ''

	stoplist = set('プレ ハザード'.split()) # 通常の文字列でよい
	print 'stoplist:'
	for s in stoplist:
		print s,
	print '\n'

	# ストップワードを除いた二重リスト
	stoplist_removed_documents = removeStoplist(splitted_documents, stoplist)

	print 'stoplist_removed_documents:'
	for t in stoplist_removed_documents:
		for w in t:
			print w,
		print ''
	print ''

	# 全ての単語を重複ありで含むリスト
	all_tokens = sum(stoplist_removed_documents, [])

	print 'all_tokens:'
	for t in all_tokens:
		print t,
	print '\n'

	# 一回しかでてこない単語のみを持つセット
	tokens_once = getTokensOnce(all_tokens)

	print 'tokens_once:'
	for t in tokens_once:
		print t,
	print '\n'

	# 一回しかでてこない単語を除いた最終的なテキスト
	preprocessed_documents = removeTokensOnce(stoplist_removed_documents, tokens_once)

	print 'preprocessed_documents:'
	for d in preprocessed_documents:
		for w in d:
			print w,
		print ''
		"""
