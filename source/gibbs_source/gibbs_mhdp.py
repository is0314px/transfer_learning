#!/usr/bin/env python
# -*- coding:utf-8 -*-
##########################################
#Gibbs sampling for training Place concept 
#Author Satoshi Ishibushi
#Editer Kazuya Asada (2017/10/13)

#-==========================================-

##########################################
import argparse
import numpy as np
import random
import string
import sys
import glob
import re
import math
import os
from numpy.linalg import inv, cholesky
from scipy.stats import chi2
import time
sys.path.append("lib/")
import BoF
import Prob_Cal
import Multi
import file_read as f_r
import nonpara_tool
import shutil

#CNN_feature=1 #If you want to use vision of 4096 dimensions,you shold set 1.
start_time=time.time()

parser = argparse.ArgumentParser()
parser.add_argument(
    "Training_dataset_list",
    help="Input training directory."
)
parser.add_argument(#result save location: Out_put_dir="../LDA_result"+args.Output+"_iter_"+repr(iter+1)
    "Output",
    help="Output directory."
)
parser.add_argument(
    "--slide",
    default=1,
    help="Sliding num for reading training data."
)
parser.add_argument(
    "--vision",
    type=str,
    default=None,
    help="vision_dirc"
)
parser.add_argument(
    "--iteration",
    type=int,
    default=1000,
    help="iteration"

)
parser.add_argument(
    "--word_not",
    type=int,
    default=None,
    help="If you don't use word for environmet."

)
parser.add_argument(
    "--function_not",
    type=int,
    default=None,
    help="If you don't use function description for environmet."

)
parser.add_argument(
    "--test_num",
    type=int,
    default=1,
    help="If you don't use function description for environmet."

)

args = parser.parse_args() 
Traing_list=np.genfromtxt(args.Training_dataset_list , delimiter="\n", dtype='S' ) #Traing_list:roomで取得したのデータセットがあるパス

try:
    data_set_num=len(Traing_list)
except TypeError:
    Traing_list=np.array([Traing_list])
    data_set_num=1

Slide=int(args.slide) #sampling interval
vision_data_dir="/googlenet_prob/" #Check File Path!

hyper_para=np.loadtxt("parameter/Hyper_Parameter_alpha/gibbs_mhdp_lda_hyper_parameter_Taguchi.txt",delimiter=" #",skiprows=2) #Check File Path! ハイパーパラメータを記載したtxt
Stick_large_L=60 #max concept number

#read hyper parameters
alpha_v = hyper_para[0]
alpha_n = hyper_para[2]
gamma = hyper_para[5]
gamma_0 = hyper_para[6]
vision_increment = hyper_para[8] 
word_increment = hyper_para[10]
iteration = 100
cut_prob=0
test_num=args.test_num

name_list=np.genfromtxt("../gibbs_dataset/dataset_path_txt/transfer_similar/name_dic.txt", delimiter="\n", dtype="S" )

def vision_data_read_pass(directory,S,DATA_NUM,test_num): #read vision data
    all_vision=[]

    for i in range(DATA_NUM):
        if  (i in test_num)==False:
            f=directory+repr(i)+".csv" #~/googlenet_prob/*.csv
            vision=np.loadtxt(f,delimiter=",")
            try:
                vision=vision[:,0]
                vision=np.array(vision)

            except IndexError:
                pass
            
            vision=vision*S
            all_vision.append(vision)

    return all_vision

def Name_data_read(directory,word_increment,DATA_NUM,test_num, Name_data_dir): #read name data
    name_data_set=[]
    
    for i in range(DATA_NUM):
        name_data=[0 for w in range(len(name_list))]

        if  (i in test_num)==False:
            try:
                file=directory+Name_data_dir+"word"+repr(i)+".txt" 
                data=np.genfromtxt(file, delimiter=" ", dtype='S')
                data_n = data.tolist() # EDITED 2017/10/29
                if isinstance(data_n, list) == False:
                    for w,dictionry in enumerate(name_list):
                        if data_n == dictionry:
                            name_data[w]+=word_increment
                else:
                    for d in data_n:
                        for w,dictionry in enumerate(name_list):
                            if d == dictionry:
                                name_data[w]+=word_increment
            except IOError:
                pass
            name_data=np.array(name_data)
            name_data_set.append(name_data)
        else:
            print("test data: "+repr(i))
    return np.array(name_data_set)


def Name_data_read_cut(directory,word_increment,DATA_NUM,test_num,Name_data_dir): #read name data
    name_data_set=[]
    cut=cut_prob
    for i in range(DATA_NUM):
        name_data=[0 for w in range(len(name_list))]
        if  (i in test_num)==False:
            try:
                file=directory+Name_data_dir+"word"+repr(i)+".txt" 
                data=np.genfromtxt(file, delimiter=" ", dtype='S' )
                
                if cut==1.0:
                    increment=word_increment
                    cut=cut_prob
                else:
                    increment=0.0
                    cut +=cut_prob
                
                try:
                    for d in data:
                        
                        for w,dictionry in enumerate(name_list):
                            if d == dictionry:
                                name_data[w]+=increment

                except TypeError:
                    
                    for w,dictionry in enumerate(name_list):
                        if d == dictionry:
                            name_data[w]+=increment
            except IOError:
                pass
            name_data=np.array(name_data)
            name_data_set.append(name_data)

    return np.array(name_data_set)

def test_data_read(file,test_num):#read test data number
    i=1 #if i=1, read test number
    test_data_num=[]
    for line in open(file, 'r').readlines():
        
        if i==test_num:
            num=line[:-1].split(',') # delete "\n"
            
            for n in num:
                try:
                    test_data_num.append(int(n))
                except ValueError:
                    pass

        i+=1
    return test_data_num


def gibbs(Out,x):
    vision_set=[]
    name_set=[]
    C_t_set=[]
    G_set=[]
    data_num=[]
    G_0=nonpara_tool.stick_breaking(gamma_0,Stick_large_L) 
    concept_num=Stick_large_L

    for e,dir in enumerate(Traing_list):
        print "Reading ",dir," ..."

        test_data_list=dir+"/test_num.txt" #text written test data number
        test_data_num=test_data_read(test_data_list,test_num)

        #if args.vision==None: 
        vision_dir = dir+vision_data_dir #PATH+/googlenet_prob/
        env_para = np.genfromtxt(dir+"/Environment_parameter.txt",dtype= None,delimiter =" ") #read environment parameter of room e

        DATA_initial_index = int(env_para[5][1]) #Initial data num
        DATA_last_index = int(env_para[6][1]) #Last data num
        DATA_NUM = DATA_last_index - DATA_initial_index +1 #learning data number

        vision=np.array(vision_data_read_pass(vision_dir,vision_increment,DATA_NUM,test_data_num)) #read vision data
        vision_set.append(vision)

        Name_data_dir="/name/per_"+repr(x)+"/"
        if args.word_not!=None:
            print "In environment "+repr(e)+",word data is not used."
            name=Name_data_read_cut(dir,word_increment,DATA_NUM,test_data_num,Name_data_dir) #read name data

        else:
            name=Name_data_read(dir,word_increment,DATA_NUM,test_data_num,Name_data_dir) #read name data
        
        name_set.append(name)
        print("read name veator = "+repr(sum(name)))

        # EDITED 2017/11/02
        if len(test_data_num) > 1:#if test data exist
            DATA_NUM=DATA_NUM-len(test_data_num)

        Learnig_data_num=(DATA_last_index - DATA_initial_index +1)/Slide #learning data number
        data_num.append(DATA_NUM)
        
        G=nonpara_tool.stick_breaking(gamma_0,Stick_large_L) #initialize G
        G_set.append(G)

        c_t=[1000 for n in xrange(DATA_NUM)] #initialize c_t
        C_t_set.append(c_t)
    
    #get dimension of information
    VISION_DIM = len(vision_set[0][0])
    NAME_DIM = len(name_set[0][0])

    #initialize phi^v, phi^n
    phi_v_e = np.array([[[float(1.0)/VISION_DIM for i in range(VISION_DIM)] for j in range(concept_num)] for k in range(data_set_num)])
    phi_n_e=np.array([[[float(1.0)/NAME_DIM for i in range(NAME_DIM)] for j in range(concept_num)] for k in range(data_set_num)])

    class_choice=[dc for dc in range(concept_num)] #[0,1,...,L-1]
    print("data number:"+repr(data_num))
    
    for iter in xrange(iteration):

        print "iteration"+ repr(iter)
        class_count=[0.0 for i in range(concept_num)]
        class_count_e_set=[]
        total_vision_e_set=[]
        total_name_e_set=[]
        
        for e in range(data_set_num):

            class_count_e=[0.0 for i in range(concept_num)]      
            phi_v_log=np.log(phi_v_e[e])
            phi_n_log=np.log(phi_n_e[e])        
            multi_prob_set=np.zeros((concept_num,data_num[e]),dtype=float)

            G_log=np.log(G_set[e])

            for i in range(concept_num):
                vision_prob=vision_set[e].dot(phi_v_log[i])
                name_prob=name_set[e].dot(phi_n_log[i])
                modal_prob=vision_prob+name_prob
                modal_prob=modal_prob+G_log[i] 
                multi_prob_set[i] +=modal_prob

            multi_prob_set =multi_prob_set.T
            max_concept =np.max(multi_prob_set,axis=1)
            multi_prob_set = multi_prob_set - max_concept[:,None]
            multi_prob_set =np.exp(multi_prob_set)
            sum_concept_set=np.sum(multi_prob_set ,axis=1)
            multi_prob_set = multi_prob_set / sum_concept_set[:,None]

            for d in xrange(0,data_num[e],Slide):
                C_t_set[e][d] =np.random.choice(class_choice,p=multi_prob_set[d]) #sampling C_t
                class_count_e[C_t_set[e][d]]+= 1.0
            
            temp_vision_e_set=[]
            temp_name_e_set=[]

            for c in xrange(concept_num):
                vision_e_c=[] 
                name_e_c=[]

                for d in xrange(data_num[e]):
                    if C_t_set[e][d]==c:
                        vision_e_c.append(vision_set[e][d])
                        name_e_c.append(name_set[e][d])
                        class_count[c] += 1.0 
                
                total_vision_e = BoF.bag_of_feature(vision_e_c,VISION_DIM)
                temp_vision_e_set.append(total_vision_e)
                total_vision_e = total_vision_e+alpha_v
                phi_v_e[e][c] = np.random.dirichlet(total_vision_e)+ 1e-100 #sampling phi_v

                total_name_e=BoF.bag_of_feature(name_e_c,NAME_DIM)
                temp_name_e_set.append(total_name_e)
                total_name_e=total_name_e +alpha_n
                phi_n_e[e][c]=np.random.dirichlet(total_name_e) #sampling phi_n

            total_vision_e_set.append(temp_vision_e_set)
            total_name_e_set.append(temp_name_e_set)

            G_set[e]=np.random.dirichlet(class_count_e+gamma)+ 1e-100 #sampling G
            class_count_e_set.append(class_count_e)
        
        if ((iter+1)%100)==0: #save every 100 iteration
            C_num=[0 for e in range(data_set_num)]
            for e in range(data_set_num):
                for i in range(concept_num):
                    if class_count_e[i]>0:
                        C_num[e] +=1


            print "Class num:"+repr(C_num)+"\n"

            #================Saving=====================
            Out_put_dir = "gibbs_result/mhdp_lda/per_"+repr(x)+"_iter_"+repr(iter+1)
            
            try:
                os.mkdir(Out_put_dir)
            except OSError:
                shutil.rmtree(Out_put_dir)
                os.mkdir(Out_put_dir)
                
            f=open(Out_put_dir+"/training dataset",'w')
            for i,d in enumerate(Traing_list): 
                w=repr(i)+":  "+d+"\n"
                f.write(w)
            f.close()

            #saving finish time
            finish_time=time.time()- start_time
            f=open(Out_put_dir+"/time.txt","w")
            f.write("time:"+repr(finish_time)+" seconds.") 
            f.close()

            #====================saving environment parameter================================
            for i in range(data_set_num):
                os.mkdir(Out_put_dir+"/dataset"+repr(i)) #save to ~/dataset*

                np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/class.txt",C_t_set[i])
                np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/G.txt",G_set[i])
                np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/phi_v_e.csv",phi_v_e[i])
                np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/phi_n_e.csv",phi_n_e[i])
                np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/class_count_e.txt",class_count_e_set[e])
                np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/total_name_e.txt",total_name_e_set[i])
                np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/total_vision_e.csv",total_vision_e_set[i])

                f=open(Out_put_dir+"/dataset"+repr(i)+"/Parameter.txt","w") #save to ~/dataset*/Parameter.txt
                f.write("\nNumber_of_place: "+repr(concept_num)+
                    "\nData_num: "+repr(data_num[i])+
                    "\nSliding_data_parameter: "+repr(Slide)+
                    "\nNAME_dim: "+repr(NAME_DIM)+
                    "\nDataset: "+Traing_list[i]+
                    "\nEstimated_placeconcept_num: "+repr(C_num[i])+
                    "\nVision_dim: "+repr(VISION_DIM)+
                    "\nStick_breaking_process_max: "+repr(Stick_large_L)+
                    "\nVision_diric: "+repr(args.vision)+
                    "\nword_not: "+repr(args.word_not)+
                    "\nword_prob: "+repr(cut_prob)+
                    "\ntest_num: "+repr(test_num)
                    )           
                f.close()
                
            #====================saving concept parameter================================
            f=open(Out_put_dir+"/hyper parameter.txt","w") #save to ~/hyper parameter.txt
            f.write("alpha_v: "+repr(alpha_v)
                +("\nalpha_n: ")+repr(alpha_n)
                +("\ngamma_0: ")+repr(gamma_0)+"\ngamma: "+repr(gamma)
                +"\nsitck break limit: "+repr(Stick_large_L)
                +"\nvision_increment: "+repr(vision_increment)+"\nword_increment: "+repr(word_increment)
                )
            f.close()


if __name__ == '__main__':
    x=0 #percent given name x= 0,7,14,21
    while x <= 21:
        gibbs(args.Output,x)
        x = x + 7