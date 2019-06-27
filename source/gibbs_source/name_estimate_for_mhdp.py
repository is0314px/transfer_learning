#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
import os
import sys
import math
from numpy.linalg import inv, cholesky

name_list=np.genfromtxt("../gibbs_dataset/dataset_path_txt/transfer_similar/name_dic.txt", delimiter="\n", dtype="S" )

def Multi_prob(data,phi):
    phi +=1e-300
    phi_log=np.log(phi)
    prob = data.dot(phi_log.T)
    return prob

def normalize(probs):
    prob_factor = 1.0 / sum(probs)
    return [prob_factor * p for p in probs]

def test_data_read(file,test_num):
    i=0
    test_data_num=[]
    for line in open(file, 'r').readlines():

        if i==test_num:
            num=line[:-1].split(',')

            for n in num:
                try:
                    test_data_num.append(int(n))
                except ValueError:
                    pass
        i+=1

    return test_data_num

result_dir=sys.argv[1] # trained data path
train_list=sys.argv[2] # txt written dir path
training_list=np.genfromtxt(train_list , delimiter="\n", dtype='S' )
test_dataset_index=sys.argv[3] #index of test dataset   #0
test_num=0
best=1 #range of rank
#best=sys.argv[4]
out_put="name_estimate_value.txt"
print("read dataset path")
print(training_list)

per=0
max_per=21

training_list=np.array([training_list])

while per <= max_per:

    parameter_dir=result_dir+"/per_"+repr(per)+"_iter_100/dataset"+repr(int(test_dataset_index))#+"/"
    train_dir = training_list[int(test_dataset_index)]
    G=np.loadtxt(parameter_dir+"/G.txt")
    mutual_info=np.loadtxt(parameter_dir+"/mutual_info.csv")
    class_count=np.loadtxt(parameter_dir+"/class_count_e.txt")

    try:
        phi_n=np.loadtxt(parameter_dir+"/phi_n_e.csv")
        phi_v=np.loadtxt(parameter_dir+"/phi_v_e.csv")
        #phi_f=np.loadtxt(parameter_dir+"/phi_f_e.csv")
    except IOError:
        phi_n=np.loadtxt(parameter_dir+"/../phi_n.csv")
        phi_v=np.loadtxt(parameter_dir+"/../phi_v.csv")
        #phi_f=np.loadtxt(parameter_dir+"/../phi_f.csv")

    prob_n=normalize(np.sum(phi_n,axis=0))[0]
    f_result=open(parameter_dir+"/"+out_put,'w')
    test_file=train_dir+"/test_num.txt"
    test_data_num=test_data_read(test_file,test_num)

    for i in test_data_num:

        test_vision=np.loadtxt(train_dir+"/googlenet_prob/"+repr(i)+".csv",delimiter=",") #read vision data

        #========== estimate ==========
        class_prob=np.array([0.0 for k in range(len(G))])

        for c in range(len(G)):
            class_prob[c] +=Multi_prob(test_vision,phi_v[c]) # * p(v_t|phi^v_c)
            class_prob[c] +=math.log(G[c]) # * p(c|G)

        max_c =np.argmax(class_prob)
        class_prob -=class_prob[max_c]
        class_prob=np.exp(class_prob)
        class_prob=normalize(class_prob)
        prob1_1=np.array([0.0 for k in range(len(name_list))])

        for n in range(len(name_list)):
            for c in range(len(G)):
                if class_count[c]>0:
                    prob1_1[n]+= class_prob[c]*phi_n[c][n]*mutual_info[c][n] # * p(n_t|phi^n_c) * I(n_t,C_t)
                
        prob1_1=normalize(prob1_1)
        index=np.argsort(prob1_1)[::-1]
        prob1_1=np.sort(prob1_1)[::-1]
        #f_result.write("Data: "+repr(i)+"\n") #original
        #print "Data: "+repr(i)
        point=0.0

        f_result.write(repr(i)+" ")
        for rank in range(int(best)):
            #f_result.write(repr(i)+": "+name_list[index[rank]]+" "+repr(prob1_1[rank])+" ")
            f_result.write(name_list[index[rank]]+" ")
        f_result.write("\n")

    f_result.close()

    per=per+7


