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
import pypr.clustering.gmm as gmm

parameter_dir=sys.argv[1] #test dataset directory
env_num=sys.argv[2] #test dataset index (test data number) example:if env_num_*, this is *

name_list=np.genfromtxt("../gibbs_dataset/dataset_path_txt/transfer_similar/name_dic.txt", dtype="S" )

def Name_data_read(file,word_increment): #read name of test data
    
    name_data=[0 for w in range(len(name_list))]
    
    data=np.genfromtxt(file, delimiter=" ", dtype="S" )
    word_increment=1
    
    try:
        for d in data:
            data_n = d.tolist()
            if isinstance(data_n, list) == False:
                for w,dictionry in enumerate(name_list):
                    if data_n == dictionry:
                        name_data[w]+=word_increment
            else:
                for dd in data_n:
                    for w,dictionry in enumerate(name_list):
                        if dd == dictionry:
                            name_data[w]+=word_increment
        
    except TypeError:
        
        for w,dictionry in enumerate(name_list):
            if data == dictionry:
                name_data[w]+=word_increment
    
    return np.array(name_data)

def Multi_prob(data,phi): #log p(*|phi^*)
    phi +=1e-300
    #phi_log=np.log(phi)
    phi_log=phi
    prob = data.dot(phi_log.T)
    return prob

def position_data_read_pass(directory,DATA_NUM,test_num): #read position data
    #Read only data not included in test_num
    all_position=[] 

    for i in range(DATA_NUM):
            
        f=directory+"/position/"+repr(i)+".txt"
        position=[] #(x,y,sin,cos)

        for line in open(f, 'r').readlines():
            data=line[:-1].split('\t')
            position +=[float(data[0].replace('\xef\xbb\xbf', ''))]
            position +=[float(data[1].replace('\r', ''))]

        all_position.append(position)

    return all_position

def position_data_read(name_vector,train_dir, data_num): #read correct positions of test data and read index of the positions
    position_set=[]
    index_set=[]
    for d in range(data_num):
        file=train_dir+"/name_label/word"+repr(d)+".txt"
        data=Name_data_read(file,20) 
        check =15
        for k in range(len(name_vector)):
            if name_vector[k]>0 and name_vector[k]!=data[k]:
                check=0
        if check==1:
            f=open(train_dir+"/position/"+repr(d)+".txt")
            pose = f.readlines()
            
            data=pose[0].split("\t")
            
            test_pose=[float(data[0].replace('\xef\xbb\xbf', '')),float(data[1].replace('\r\n', ''))] #(x,y)

            position_set.append(test_pose)
            index_set.append(d)

    return position_set,index_set

def test_data_read(file,test_num): #read number of test data
    i=0
    test_data_num=[]
    for line in open(file, 'r').readlines(): # 0,1,2,3,8,9,...
        
        if i==test_num: # line's row number == test_num
            num=line[:-1].split(',') # make number list and delete \n  [0,1,2,3,8,9]
            for n in num:
                try:
                    test_data_num.append(int(n))
                except ValueError:
                    pass
        i+=1
    
    return test_data_num

per=0
max_per=21

while per <= max_per:

    per_dir='/per_'+repr(int(per))+'_iter_100/dataset'+repr(int(env_num))

    result_env=np.genfromtxt(parameter_dir+per_dir+"/Parameter.txt",delimiter=": ",dtype='S')#read parameter text of test dataset
    train_dir=result_env[8][1]
    train_env=np.genfromtxt(train_dir+"/Environment_parameter.txt",delimiter=" ",dtype='S')#read environmet parameter 
    data_num=int(train_env[6][1])-int(train_env[5][1])+1

    #========== read estimated parameters of test data ==========
    try:
        phi_n=np.loadtxt(parameter_dir+per_dir+"/phi_n_e.csv")

    except IOError:
        phi_n=np.loadtxt(parameter_dir+per_dir+"/../phi_n.csv")

    pi=np.loadtxt(parameter_dir+per_dir+"/pi.csv")
    G=np.loadtxt(parameter_dir+per_dir+"/G.txt")
    region_num=len(pi[0])
    sigma_set=[]
    mu_set=[]

    for i in range(region_num):
        sigma=np.loadtxt(parameter_dir+per_dir+"/sigma/gauss_sigma"+repr(i)+".csv")
        mu=np.loadtxt(parameter_dir+per_dir+"/mu/gauss_mu"+repr(i)+".csv")
        sigma_set.append(sigma)
        mu_set.append(mu)

    test_num=0
    test_file=train_dir+"/test_num.txt" #text written test data number
    test_data_num=test_data_read(test_file,test_num) #read test data number
    pose=np.array(position_data_read_pass(train_dir,data_num,test_data_num)) #read correct position data

    #========== estimate position and evaluate cost ==========
    p_num=0
    cost_sum=0
    for p in test_data_num:

        name_vector=Name_data_read(train_dir+"/name_label/word"+repr(p)+".txt",20) #read correct name label of test data and make vector having elements of name

        prob_rt=[0.0 for i in xrange(len(pi[0]))]

        for r in xrange(len(pi[0])):
            for c in xrange(len(G)):
                #prob = np.log(Multi_prob(name_vector,phi_n[c]))
                #prob = prob + np.log(G[c])
                #prob = prob + np.log(pi[c][r])
                #prob_rt[r] += prob
                prob = Multi_prob(name_vector,phi_n[c])*G[c]*pi[c][r] #p(n_t|phi^n_c)*p(c|G)*p(r|pi_c)
                prob_rt[r] += prob
                
        #print(np.exp(prob_rt))
        #print(prob_rt/(sum(prob_rt))

        r_t = np.argmax(prob_rt) #choose r_t

        cost=((pose[p][0]-mu_set[r_t][0])**2)+((pose[p][1]-mu_set[r_t][1])**2) #x[0]:axis-X, x[1]:axis-Z
        cost=cost**0.5 #caluculate cost

        cost_sum+=cost
        p_num+=1

    cost_ave=cost_sum/p_num

    print("per"+repr(int(per))+": cost="+repr(float(cost_ave)))

    per=per+7


