#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np 
import argparse
import os
import sys
import math
from numpy.linalg import inv, cholesky
import glob
import re
import shutil
#import pypr.clustering.gmm as gmm

parameter_dir = sys.argv[1] #test dataset directory
env_num = sys.argv[2] #test dataset index (test data number) example:if env_num_0, this is 0

name_dic = np.loadtxt("../gibbs_dataset/dataset_path_txt/transfer_similar/name_dic_1LDK.txt", delimiter="\n", dtype='S' )

dir = "../gibbs_dataset/similar/dataset_B/1LDK_9" 
name_data_dir = "/name_label/"
position_data_dir = "/position/"
name_dir = dir + name_data_dir
position_dir = dir + position_data_dir

global_dist_num = 7
local_dist_num = 1
dist_num = global_dist_num + local_dist_num
N = 30
DATA_NUM =  N * dist_num

def Multi_prob(data,phi): #log p(*|phi^*)
    phi += 1e-300
    #phi_log = np.log(phi)
    phi_log = phi
    prob = data.dot(phi_log.T)
    return prob

position_list = [[] for w in range(len(name_dic))]


#=========== make label position ==========
for i in range(DATA_NUM):

    name_file = name_dir + "word" + repr(i) + ".txt"
    name = np.loadtxt(name_file, delimiter=" ", dtype='S')
    name_list = name.tolist()

    position_file = position_dir + repr(i) + ".txt"
    position = []

    for line in open(position_file, 'r').readlines():
        #for similar
        data=line[:-1].split('\t')
        position += [float(data[0].replace('\xef\xbb\xbf', ''))]
    
        #for realworld
        #data=line[:-1].split(' ')
        #position +=[float(data[0].replace('\r', ''))]
        position += [float(data[1].replace('\r', ''))]
    

    if(i >= 0 and i <= 14) or (i >=120 and i <= 134):
        position_list[0].append(position)
    if(i >= 15 and i <= 29) or (i >= 135 and i <= 149):
        position_list[1].append(position)
    if(i >= 30 and i <= 44) or (i >= 150 and i <= 164):
        position_list[2].append(position)
    if(i >= 45 and i <= 59) or (i >= 165 and i <= 179):
        position_list[3].append(position)
    if(i >= 60 and i <= 74) or (i >= 180 and i <= 194):
        position_list[4].append(position)
    if(i >= 75 and i <= 89) or (i >= 195 and i <= 209):
        position_list[5].append(position)
    if(i >= 90 and i <= 104) or (i >= 210 and i <= 224):
        position_list[6].append(position)
    if(i >= 105 and i <= 119) or (i >= 225 and i <= 239):
        position_list[7].append(position)


label_pos = []
for idx in range(dist_num):
    x_ave = 0
    y_ave = 0
    for m in range(N):
        x_ave = x_ave + position_list[idx][m][0]
        y_ave = y_ave + position_list[idx][m][1]
    
    x_ave = x_ave / N
    y_ave = y_ave / N
    label_pos.append([x_ave,y_ave])


per = 0
PER = 5
MAX_PER = 20

while per <= MAX_PER:
    
    per_dir = '/per_'+repr(int(per))+'_iter_200/dataset'+repr(int(env_num))
    result_env = np.genfromtxt(parameter_dir+per_dir+"/Parameter.txt",delimiter=": ",dtype='S')#read parameter text of test dataset
    train_dir = result_env[7][1]
    train_env = np.genfromtxt(train_dir+"/Environment_parameter.txt",delimiter=" ",dtype='S')#read environmet parameter 
    data_num = int(train_env[6][1])-int(train_env[5][1])+1

    #========== read estimated parameters of test data ==========
    try:
        phi_n = np.loadtxt(parameter_dir+per_dir+"/phi_n_e.csv")

    except IOError:
        phi_n = np.loadtxt(parameter_dir+per_dir+"/../phi_n.csv")

    pi = np.loadtxt(parameter_dir+per_dir+"/pi.csv")
    G = np.loadtxt(parameter_dir+per_dir+"/G.txt")
    region_num = len(pi[0])
    sigma_set = []
    mu_set = []

    for i in range(region_num):
        sigma = np.loadtxt(parameter_dir+per_dir+"/sigma/gauss_sigma"+repr(i)+".csv")
        mu = np.loadtxt(parameter_dir+per_dir+"/mu/gauss_mu"+repr(i)+".csv")
        sigma_set.append(sigma)
        mu_set.append(mu)
    
    file = open(parameter_dir+'/cost.txt','a')

    sum_global = 0
    sum_local = 0

    #========== estimate position and evaluate cost ==========
    name_vector = np.array([1,0,0,0,0,0,0,0,0]) #read correct name label of test data and make vector having elements of name
    idx = 0

    prob_rt = [0.0 for i in xrange(len(pi[0]))]

    for r in xrange(len(pi[0])):
        for c in xrange(len(G)):
            prob = Multi_prob(name_vector,phi_n[c])*G[c]*pi[c][r] #p(n_t|phi^n_c)*p(c|G)*p(r|pi_c)
            prob_rt[r] += prob

    r_t = np.argmax(prob_rt) #choose r_t

    cost = ((label_pos[idx][0] - mu_set[r_t][0])**2) + ((label_pos[idx][1] - mu_set[r_t][1])**2) #x[0]:axis-X, x[1]:axis-Z
    cost = cost**0.5 #caluculate cost

    print("玄関　　　："+repr(cost))
    file.write(repr(per)+"% 玄関　　　："+repr(cost)+'\n')
    sum_global += cost

    #=========================================================
    name_vector = np.array([0,1,0,0,0,0,0,0,0]) #read correct name label of test data and make vector having elements of name
    idx = 7

    prob_rt = [0.0 for i in xrange(len(pi[0]))]

    for r in xrange(len(pi[0])):
        for c in xrange(len(G)):
            prob = Multi_prob(name_vector,phi_n[c])*G[c]*pi[c][r] #p(n_t|phi^n_c)*p(c|G)*p(r|pi_c)
            prob_rt[r] += prob

    r_t = np.argmax(prob_rt) #choose r_t

    cost = ((label_pos[idx][0] - mu_set[r_t][0])**2) + ((label_pos[idx][1] - mu_set[r_t][1])**2) #x[0]:axis-X, x[1]:axis-Z
    cost = cost**0.5 #caluculate cost

    print("トイレ　　："+repr(cost))
    file.write(repr(per)+"% トイレ　　："+repr(cost)+'\n')
    sum_global += cost

    #=========================================================
    name_vector = np.array([0,0,1,0,0,0,0,0,0]) #read correct name label of test data and make vector having elements of name
    idx = 1

    prob_rt = [0.0 for i in xrange(len(pi[0]))]

    for r in xrange(len(pi[0])):
        for c in xrange(len(G)):
            prob = Multi_prob(name_vector,phi_n[c])*G[c]*pi[c][r] #p(n_t|phi^n_c)*p(c|G)*p(r|pi_c)
            prob_rt[r] += prob

    r_t = np.argmax(prob_rt) #choose r_t

    cost = ((label_pos[idx][0] - mu_set[r_t][0])**2) + ((label_pos[idx][1] - mu_set[r_t][1])**2) #x[0]:axis-X, x[1]:axis-Z
    cost = cost**0.5 #caluculate cost

    print("寝室　　　："+repr(cost))
    file.write(repr(per)+"% 寝室　　　："+repr(cost)+'\n')
    sum_global += cost

    #=========================================================
    name_vector = np.array([0,0,0,1,0,0,0,0,0]) #read correct name label of test data and make vector having elements of name
    idx = 6

    prob_rt = [0.0 for i in xrange(len(pi[0]))]

    for r in xrange(len(pi[0])):
        for c in xrange(len(G)):
            prob = Multi_prob(name_vector,phi_n[c])*G[c]*pi[c][r] #p(n_t|phi^n_c)*p(c|G)*p(r|pi_c)
            prob_rt[r] += prob

    r_t = np.argmax(prob_rt) #choose r_t

    cost = ((label_pos[idx][0] - mu_set[r_t][0])**2) + ((label_pos[idx][1] - mu_set[r_t][1])**2) #x[0]:axis-X, x[1]:axis-Z
    cost = cost**0.5 #caluculate cost

    print("風呂　　　："+repr(cost))
    file.write(repr(per)+"% 風呂　　　："+repr(cost)+'\n')
    sum_global += cost

    #=========================================================
    name_vector = np.array([0,0,0,0,1,0,0,0,0]) #read correct name label of test data and make vector having elements of name
    idx = 2

    prob_rt = [0.0 for i in xrange(len(pi[0]))]

    for r in xrange(len(pi[0])):
        for c in xrange(len(G)):
            prob = Multi_prob(name_vector,phi_n[c])*G[c]*pi[c][r] #p(n_t|phi^n_c)*p(c|G)*p(r|pi_c)
            prob_rt[r] += prob

    r_t = np.argmax(prob_rt) #choose r_t

    cost = ((label_pos[idx][0] - mu_set[r_t][0])**2) + ((label_pos[idx][1] - mu_set[r_t][1])**2) #x[0]:axis-X, x[1]:axis-Z
    cost = cost**0.5 #caluculate cost

    print("リビング　："+repr(cost))
    file.write(repr(per)+"% リビング　："+repr(cost)+'\n')
    sum_global += cost

    #=========================================================
    name_vector = np.array([0,0,0,0,0,1,0,0,0]) #read correct name label of test data and make vector having elements of name
    idx = 3

    prob_rt = [0.0 for i in xrange(len(pi[0]))]

    for r in xrange(len(pi[0])):
        for c in xrange(len(G)):
            prob = Multi_prob(name_vector,phi_n[c])*G[c]*pi[c][r] #p(n_t|phi^n_c)*p(c|G)*p(r|pi_c)
            prob_rt[r] += prob

    r_t = np.argmax(prob_rt) #choose r_t

    cost = ((label_pos[idx][0] - mu_set[r_t][0])**2) + ((label_pos[idx][1] - mu_set[r_t][1])**2) #x[0]:axis-X, x[1]:axis-Z
    cost = cost**0.5 #caluculate cost

    print("ダイニング："+repr(cost))
    file.write(repr(per)+"% ダイニング："+repr(cost)+'\n')
    sum_global += cost

    #=========================================================
    name_vector = np.array([0,0,0,0,0,0,1,0,0]) #read correct name label of test data and make vector having elements of name
    idx = 4

    prob_rt = [0.0 for i in xrange(len(pi[0]))]

    for r in xrange(len(pi[0])):
        for c in xrange(len(G)):
            prob = Multi_prob(name_vector,phi_n[c])*G[c]*pi[c][r] #p(n_t|phi^n_c)*p(c|G)*p(r|pi_c)
            prob_rt[r] += prob

    r_t = np.argmax(prob_rt) #choose r_t

    cost = ((label_pos[idx][0] - mu_set[r_t][0])**2) + ((label_pos[idx][1] - mu_set[r_t][1])**2) #x[0]:axis-X, x[1]:axis-Z
    cost = cost**0.5 #caluculate cost

    print("キッチン　："+repr(cost))
    file.write(repr(per)+"% キッチン　："+repr(cost)+'\n')
    sum_global += cost

    #=========================================================
    name_vector = np.array([0,0,0,0,0,0,0,1,0]) #read correct name label of test data and make vector having elements of name
    idx = 5

    prob_rt = [0.0 for i in xrange(len(pi[0]))]

    for r in xrange(len(pi[0])):
        for c in xrange(len(G)):
            prob = Multi_prob(name_vector,phi_n[c])*G[c]*pi[c][r] #p(n_t|phi^n_c)*p(c|G)*p(r|pi_c)
            prob_rt[r] += prob

    r_t = np.argmax(prob_rt) #choose r_t

    cost = ((label_pos[idx][0] - mu_set[r_t][0])**2) + ((label_pos[idx][1] - mu_set[r_t][1])**2) #x[0]:axis-X, x[1]:axis-Z
    cost = cost**0.5 #caluculate cost

    print("洗面所　　："+repr(cost))
    file.write(repr(per)+"% 洗面所　　："+repr(cost)+'\n')
    sum_global += cost

    #=========================================================
    name_vector = np.array([0,0,0,0,0,0,0,0,1]) #read correct name label of test data and make vector having elements of name
    idx = 1

    prob_rt = [0.0 for i in xrange(len(pi[0]))]

    for r in xrange(len(pi[0])):
        for c in xrange(len(G)):
            prob = Multi_prob(name_vector,phi_n[c])*G[c]*pi[c][r] #p(n_t|phi^n_c)*p(c|G)*p(r|pi_c)
            prob_rt[r] += prob

    r_t = np.argmax(prob_rt) #choose r_t

    cost = ((label_pos[idx][0] - mu_set[r_t][0])**2) + ((label_pos[idx][1] - mu_set[r_t][1])**2) #x[0]:axis-X, x[1]:axis-Z
    cost = cost**0.5 #caluculate cost

    print("田口　　　："+repr(cost))
    file.write(repr(per)+"% 田口　　　："+repr(cost)+'\n')
    sum_local += cost


    ave_global = sum_global / global_dist_num
    ave_local = sum_local / local_dist_num

    print("global cost："+repr(ave_global))
    print("local cost ："+repr(ave_local))
    print(" ")

    file.write(repr(per)+"% global cost："+repr(ave_global)+'\n')
    file.write(repr(per)+"% local cost ："+repr(ave_local)+'\n')
    file.write('\n')
    file.close()

    per = per + PER

                            