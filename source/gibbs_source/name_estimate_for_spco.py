#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np 
import os
import sys
import math
from numpy.linalg import inv, cholesky
import scipy.stats as ss

# Check these dictionary!
name_list=np.loadtxt("../gibbs_dataset/dataset_path_txt/transfer_similar/name_dic_1DK.txt", delimiter="\n", dtype='S' )

def Multi_prob(data,phi): #log p(*|phi^*)
    phi +=1e-300
    phi_log=np.log(phi)
    prob = data.dot(phi_log.T)
    return prob

def normalize(probs): 
    prob_factor = 1.0 / sum(probs)
    return [prob_factor * p for p in probs]

def Name_data_read(file,name_increment): #read name data

    name_data=[0 for w in range(len(name_list))]
        
    #data=np.genfromtxt(file, delimiter="\n", dtype='S' )
    data=np.loadtxt(file, delimiter=' ', dtype='S' )

    data_l = data.tolist()
    
    if isinstance(data_l, list) == False:
        for w,dictionry in enumerate(name_list):
            if data_l == dictionry:
                name_data[w]+=name_increment
          
    else:
        for d in data_l:
            
            for w,dictionry in enumerate(name_list):
                
                if d == dictionry:
                    name_data[w]+=name_increment
                
                
    
    name_data=np.array(name_data)
    return name_data

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

result_dir=sys.argv[1] # result directory of gibbs sampling , example: gibbs_result/env_num_*
train_list=sys.argv[2] # text written dataset directories, example: ../gibbs_dataset/dataset_path_txt/transfer_similar/path_num*_X.txt
Training_list=np.genfromtxt(train_list , delimiter="\n", dtype='S' )
test_dataset_index=sys.argv[3] #index of test dataset   if path_num*, this is *
mute=1
test_num=0
best=1 #range of rank
#best=int(sys.argv[4])
out_put="name_estimate_value.txt" #Check file name!
name_out_put="estimate_sample_list.txt"
print("read dataset path")
print(Training_list)

per=0
max_per=20

try:
    data_set_num=len(Training_list) #number of trained rooms
except TypeError:
    Training_list=np.array([Training_list])
    data_set_num=1

while per <= max_per:

    parameter_dir = result_dir+"/per_"+repr(per)+"_iter_200/dataset"+repr(int(test_dataset_index))

    pi = np.loadtxt(parameter_dir+"/pi.csv") #read pi
    G = np.loadtxt(parameter_dir+"/G.txt") #read G
    mutual_info = np.loadtxt(parameter_dir+"/mutual_info.csv") #read mutual infomation I(n_t,C_t|Theta)

    region_num = len(pi[0])
    sigma_set = []
    mu_set = []
    region_count = np.loadtxt(parameter_dir+"/posdist_count.txt")

    for i in range(region_num):
        sigma = np.loadtxt(parameter_dir+"/sigma/gauss_sigma"+repr(i)+".csv") #read sigma
        mu = np.loadtxt(parameter_dir+"/mu/gauss_mu"+repr(i)+".csv") #read mu
        sigma_set.append(sigma)
        mu_set.append(mu)

    print(parameter_dir)


    try:
        phi_n=np.loadtxt(parameter_dir+"/../phi_n.csv") #read phi^n (for transfer learning model)
        phi_v=np.loadtxt(parameter_dir+"/../phi_v.csv") #read phi^n (for transfer learning model)
        #phi_f=np.loadtxt(parameter_dir+"/../phi_f.csv") 
        model_idx = 1 #index of transfer leaning model

    except IOError:
        phi_n=np.loadtxt(parameter_dir+"/../phi_n.csv") #read phi^n (for SpCoA)
        #phi_v=np.loadtxt(parameter_dir+"/phi_v_e.csv") #read phi^v (for SpCoA)
        #phi_f=np.loadtxt(parameter_dir+"/phi_f_e.csv")
        model_idx = 0 #index of SpCoA

    prob_n=normalize(np.sum(phi_n,axis=0))[0] 

    f_result=open(parameter_dir+"/"+out_put,'w')

    train_dir=Training_list[int(test_dataset_index)]

    if data_set_num < len(Training_list): 
        test_file=train_dir+"/test_num_all.txt"
    else: #read test number
        test_file=train_dir+"/test_num.txt"
    test_data_num=test_data_read(test_file,test_num)

    test_vision_set=[]
    test_pose_set=[]
    test_name_set=[]
    point_test_set=[]

    for i in test_data_num:
        
        test_vision=np.loadtxt(train_dir+"/googlenet_prob/"+repr(i)+".csv",delimiter=",") #read vision data
        test_vision_set.append(test_vision)

        f=train_dir+"/position/"+repr(i)+".txt"
        test_pose=[]
        for pos in open(f, 'r').readlines(): #read position data
            data=pos[:-1].split('\t') #sigverse
            #data=pos[:-1].split(' ')   #realworld
            a=data[0].replace('\xef\xbb\xbf', '') #sigverse
            #a=data[0].replace('\r', '')            #realworld
            b=data[1].replace('\r', '')
            test_pose.append(a)
            test_pose.append(b)    
        test_pose_set.append(test_pose)
        
        try:
            if (e+1) < len(Training_list):
                test_name=Name_data_read(train_dir+"/name/"+repr(per_num)+"/word"+repr(i)+".txt",1) # Check path!
            else:
                test_name=Name_data_read(train_dir+"/name/"+repr(per_num)+"/word"+repr(i)+".txt",1) # Check path!

            point_temp=[0.0 for k in range(len(name_list))]
            point_test_name=[0.0 for k in range(len(name_list))]
            index=np.argsort(point_temp)[::-1]
            for rank in range(2):
                point_test_name[index[rank]]=point_temp[index[rank]]
            point_test_set.append(point_test_name)
            test_name_set.append(test_name)
        except:
            test_name=[0 for w in range(len(name_list))]
            test_name=np.array(test_name)

            point_temp=[0.0 for k in range(len(name_list))]  
            point_test_name=[0.0 for k in range(len(name_list))]
            index=np.argsort(point_temp)[::-1]
            for rank in range(2):
                point_test_name[index[rank]]=point_temp[index[rank]]
            point_test_set.append(point_test_name)
            test_name_set.append(test_name)

    test_vision_set=np.array(test_vision_set)
    test_pose_set=np.array(test_pose_set)
    test_name_set=np.array(test_name_set)


    #========== estimate ==========
    gauss_prob_set=np.zeros((region_num,len(test_data_num)),dtype=float)
    for r in range(region_num):
        gauss_prob=ss.multivariate_normal.logpdf(test_pose_set,mu_set[r],sigma_set[r])    
        gauss_prob_set[r] += gauss_prob

    gauss_prob_set=gauss_prob_set.T
    max_region=np.max(gauss_prob_set,axis=1)
    gauss_prob_set=gauss_prob_set -max_region[:,None]
    gauss_prob_set=np.exp(gauss_prob_set)
    sum_set=np.sum(gauss_prob_set,axis=1)
    gauss_prob_set=gauss_prob_set / sum_set[:,None]

    for i in range(len(test_data_num)):
        class_prob=np.array([0.0 for k in range(len(pi))])
        for c in range(len(pi)):
            if model_idx == 1: #if transfer leaning model
                class_prob[c] += Multi_prob(test_vision_set[i],phi_v[c]) # * p(v_t|phi^v_c)
            class_prob[c] += math.log(G[c]) # * p(c|G)

            region_prob=0.0
            for r in range(region_num):
                if region_count[r]>0:
                    region_prob += pi[c][r]*gauss_prob_set[i][r] # * p(r|pi_c) * p(x_t|mu_r,sigma_r)

            if region_prob != 0.0:
                class_prob[c] += math.log(region_prob)

        max_c=np.argmax(class_prob)    
        class_prob-=class_prob[max_c]
        class_prob=np.exp(class_prob)    
        class_prob=normalize(class_prob)

        prob1_1=np.array([0.0 for k in range(len(name_list))]) #initialize p(n_t|v_t.x_t)

        for n in range(len(name_list)):
            for c in range(len(pi)):
                if mute==0:
                    prob1_1[n]+=class_prob[c]*phi_n[c][n] # * p(n_t|phi^n_c)
                else:
                    prob1_1[n]+=class_prob[c]*phi_n[c][n]*mutual_info[c][n] # * p(n_t|phi^n_c) * I(n_t,C_t) #default
        
        prob1_1=normalize(prob1_1)
        index=np.argsort(prob1_1)[::-1]
        prob1_1=np.sort(prob1_1)[::-1]
        #f_result.write("Data: "+repr(test_data_num[i])+"\n") #original

        point=0.0

        f_result.write(repr(test_data_num[i])+" ")
        for rank in range(best):
            #f_result.write(repr(rank)+": "+name_list[index[rank]]+" "+repr(prob1_1[rank])+"\n") #original
            #f_result.write(repr(test_data_num[i])+" "+name_list[index[rank]]+" "+repr(prob1_1[rank])+"\n") #original
            f_result.write(name_list[index[rank]]+" ")
                    
        # Edited 2017/11/20
        f_result.write("\n")
    f_result.close()

    per=per+5
