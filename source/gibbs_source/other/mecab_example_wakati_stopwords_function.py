#!/usr/bin/env python
#coding:utf-8
import MeCab
import os
import glob
import re
import codecs

# http://hivecolor.com/id/86
# テキストマイニングの前処理。名詞抽出、ストップワード除去

if __name__ == "__main__":
	DATA_NUM = 400
	mt = MeCab.Tagger("-Owakati")
	
	output_path = "/home/emlab/Caffe/SIGVerse3Log/0919_10room/10rooms_edits0919/wakati_words_functions_room010/functions" # check output path
	
	input_path = "/home/emlab/Caffe/SIGVerse3Log/0919_10room/10rooms_edits0919/words_functions_room010/functions" # check input path
	
	stoplist = set("お ご ここ これ と この です いい し します ます する は の て に また を が で 。".split()) # 通常の文字列でよい
	for i in range(DATA_NUM):
		#word=[0 for n in range(word_class)]
		#signal=("word"+repr(i)+".txt") in file
		signal = os.path.isfile(input_path + "/function%03d.txt"%i)
		
		if signal==True:
			f=codecs.open(input_path + "/function%03d.txt"%i,"r","utf-8")
			data=f.read()
			line=data.split("\n")
			f.close()
			f_out = open(output_path + "/function%03d.txt"%i,"w")
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

