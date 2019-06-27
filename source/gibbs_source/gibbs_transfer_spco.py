#!/usr/bin/env python
# -*- coding:utf-8 -*-
##########################################
#Gibbs sampling for training Place concept 
#Author Satoshi Ishibushi
#Editer Kazuya Asada (2017/09/29)

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
import scipy.stats as ss
#import mutual_information as mutual
from sklearn.preprocessing import normalize
import sklearn.cluster

#CNN_feature=1 #If you want to use vision of 4096 dimensions,you shold set 1.
start_time=time.time()
parser = argparse.ArgumentParser()
parser.add_argument( #"/googlenet_prob/"
    "Training_dataset_list",
    help="Input training directory."
)
parser.add_argument( #Out_put_dir="../result"+Out+repr(x)+"/per_"+repr(x)+"_iter_"+repr(iter+1)
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
    "--name_not",
    type=int,
    default=None,
    help="If you don't use name for environmet."
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
Traing_list = np.genfromtxt(args.Training_dataset_list , delimiter="\n", dtype="S") #directories of training dataset and test dataset

try:
    data_set_num=len(Traing_list)
except TypeError:
    Traing_list=np.array([Traing_list])
    data_set_num=1
Slide=int(args.slide)

vision_data_dir="/googlenet_prob/"  #directory where vision data exists
hyper_para=np.loadtxt("parameter/Hyper_Parameter_alpha/gibbs_trans_hyper_parameter_Taguchi2.txt",delimiter=" #",skiprows=2) #read hyper parameters
function_list=np.genfromtxt("../gibbs_dataset/dataset_path_txt/transfer_similar/function_dic.txt", delimiter="\n", dtype="S" ) #dictionary of function
name_list=np.genfromtxt("../gibbs_dataset/dataset_path_txt/transfer_similar/name_dic.txt", delimiter="\n", dtype="S" ) #dictionary of name
print("number of environment:"+repr(len(Traing_list)))

Stick_large_L=60 #number of concept upper limit in stick breaking process
Stick_large_R=60 #number of position distribution upper limit in stick breaking process
sigma_init = 100.0 #initial covariance value
iteration = 100 #number of iterarion
#cut_prob=0
test_num=args.test_num #index of test dataset

#========== read hyper parameters ===============
alpha_v = hyper_para[0] 
#alpha_f = hyper_para[1]
alpha_n = hyper_para[2]
kappa_0=hyper_para[3]
nu_0=hyper_para[4]
gamma = hyper_para[5]
gamma_0 = hyper_para[6]
beta = hyper_para[7]
vision_increment = hyper_para[8] 
function_increment = hyper_para[9]
name_increment = hyper_para[10]
psai_0 = np.matrix([[0.1,0.0,0.0,0.0],[0.0,0.1,0.0,0.0],[0.0,0.0,5.0,0.0],[0.0,0.0,0.0,5.0]])

def position_data_read_pass(directory,DATA_NUM,test_num): #read position data
    #Read only data not included in test_num
    all_position=[] 

    for i in range(DATA_NUM):

        if  (i in test_num)==False:
            f=directory+"/position/"+repr(i)+".txt"
            position=[] #(x,y,sin,cos)

            for line in open(f, 'r').readlines():
                data=line[:-1].split('\t')
                position +=[float(data[0].replace('\xef\xbb\xbf', ''))] #(x,y)
                position +=[float(data[1].replace('\r', ''))] #(sin,cos)

            all_position.append(position)

    return all_position

def vision_data_read_pass(directory,vision_increment,DATA_NUM,test_num): #read vision data
    #Read only data not included in test_num
    all_vision=[]

    for i in range(DATA_NUM):

        if  (i in test_num)==False:
            f=directory+repr(i)+".csv"
            vision=np.loadtxt(f,delimiter=",")
            
            try:
                vision=vision[:,0]
                vision=np.array(vision)

            except IndexError:
                pass

            vision = vision*vision_increment
            all_vision.append(vision)
    
    return all_vision

"""
def Function_data_read(directory,function_increment,DATA_NUM,test_num): #read function data
    #Read only data not included in test_num
    function_data_set=[] 

    for i in range(DATA_NUM):
        function_data=[0 for w in range(len(function_list))]

        if  (i in test_num)==False:
            try:
                file = directory+Function_data_dir+"function"+repr(i)+".txt"
                data=np.genfromtxt(file, delimiter=" ", dtype='S' )
                data_f = data.tolist() # EDITED 2017/10/29

                if isinstance(data_f, list) == False:
                    for w,dictionry in enumerate(function_list):
                        if data_f == dictionry:
                            function_data[w]+=function_increment

                else:
                    for d in data_f:
                        for w,dictionry in enumerate(function_list):
                            if d == dictionry:
                                function_data[w]+=function_increment    

            except IOError:
                pass

            function_data=np.array(function_data)
            function_data_set.append(function_data)

    return np.array(function_data_set)

"""

def Name_data_read(directory,name_increment,DATA_NUM,test_num,Name_data_dir): #read name data
    #Read only data not included in test_num
    name_data_set=[]

    for i in range(DATA_NUM):
        name_data=[0 for w in range(len(name_list))]

        if  (i in test_num)==False:
            try:
                file=directory+Name_data_dir+"word"+repr(i)+".txt"
                data=np.genfromtxt(file, delimiter=" ", dtype='S')
                data_n = data.tolist()

                if isinstance(data_n, list) == False:
                    for w,dictionry in enumerate(name_list):
                        if data_n == dictionry:
                            name_data[w]+=name_increment

                else:
                    for d in data_n:
                        for w,dictionry in enumerate(name_list):
                            if d == dictionry:
                                name_data[w]+=name_increment

            except IOError:
                pass

            name_data=np.array(name_data)
            name_data_set.append(name_data)

        else:
            print("test_data: "+repr(i))

    return np.array(name_data_set)

"""
def Name_data_read_cut(directory,name_increment,DATA_NUM,test_num,Name_data_dir):
    name_data_set=[]
    cut=cut_prob

    for i in range(DATA_NUM):
        name_data=[0 for w in range(len(name_list))]

        if  (i in test_num)==False:

            try:
                file=directory+Name_data_dir+"word"+repr(i)+".txt"
                data=np.genfromtxt(file, delimiter=" ", dtype='S' )

                if cut==1.0:
                    increment=name_increment
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
"""

def test_data_read(file,test_num): #read test data number
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

            print "Use test_data_read function"

        i+=1
        
    return test_data_num
    
def gibbs(Out,x): #gibbs sampling
    print "Start reading Data"

    vision_set=[]
    position_set=[]
    #function_set=[]
    name_set=[]
    C_t_set=[]
    r_t_set=[]
    G_set=[]
    pi_set=[]
    Sigma_set=[]
    Mu_set=[]
    data_num=[]
    G_0=nonpara_tool.stick_breaking(gamma_0,Stick_large_L)
    concept_num=Stick_large_L
    region_num=Stick_large_R
    MAP_X=[0 for e in range(data_set_num)]
    MAP_Y=[0 for e in range(data_set_num)]
    map_x=[0 for e in range(data_set_num)]
    map_y=[0 for e in range(data_set_num)]
    mu_0_set=[]

    for e,dir in enumerate(Traing_list):
        print "Reading ",dir," ..."
        
        if (e+1) < len(Traing_list): #directory where training name data exists
            Name_data_dir = "/name/per_100/"
            test_data_list=dir+"/test_num.txt"
            test_data_num=test_data_read(test_data_list,test_num)
            print("Training environmet:"+repr(e))

        else: #directory where test name data exists
            Name_data_dir = "/name/per_"+repr(x)+"/"
            test_data_list=dir+"/test_num.txt"
            test_data_num=test_data_read(test_data_list,test_num)
            print("Test environment: "+repr(e))

        #if args.vision==None: 
        vision_dir = dir+vision_data_dir #directory where vision data exists
        env_para = np.genfromtxt(dir+"/Environment_parameter.txt",dtype= None,delimiter =" ") #read environment parameter

        MAP_X[e] = float(env_para[0][1])  #Max x value of the map
        MAP_Y[e] = float(env_para[1][1])  #Max y value of the map
        map_x[e] = float(env_para[2][1]) #min x value of the map
        map_y[e] = float(env_para[3][1]) #min y value of the map

        map_center_x = ((MAP_X[e] - map_x[e])/2)+map_x[e]
        map_center_y = ((MAP_Y[e] - map_x[e])/2)+map_y[e]
        mu_0=np.array([map_center_x,map_center_y,0,0]) #initialize mu_0
        mu_0_set.append(mu_0)
        DATA_initial_index = int(env_para[5][1]) #initial data num
        DATA_last_index = int(env_para[6][1]) #last data num
        DATA_NUM =DATA_last_index - DATA_initial_index +1
        # env_para[4][1] (Number_of_place) is not used

        pose=np.array(position_data_read_pass(dir,DATA_NUM,test_data_num)) #read positon data
        position_set.append(pose)

        vision=np.array(vision_data_read_pass(vision_dir,vision_increment,DATA_NUM,test_data_num)) #read vision data
        vision_set.append(vision)

        """
        if args.function_not==e:
            print "In environment "+repr(e)+",name data is not used."
            function=[]

            for d in range(DATA_NUM):
                function_d=np.array([0.0 for k in range(len(function_list))])
                function.append(function_d)

        else:
            function=Function_data_read(dir,function_increment,DATA_NUM,test_data_num) #read function

        function_set.append(function)
        print sum(function)
        """

        if args.name_not==e:
            print "In environment "+repr(e)+",name data is not used."
            name=Name_data_read_cut(dir,name_increment,DATA_NUM,test_data_num,Name_data_dir) #read name data cut some data is cut (not used)

        else:
            name=Name_data_read(dir,name_increment,DATA_NUM,test_data_num,Name_data_dir) #read name data
            print "Use Name_data_read function"
    
        name_set.append(name)
        print(DATA_NUM, test_data_num)
        print sum(name)
        
        # EDITED 2017/11/02
        if len(test_data_num) > 1:
            DATA_NUM=DATA_NUM-len(test_data_num)

        Learnig_data_num=(DATA_last_index - DATA_initial_index +1)/Slide #Data number
        data_num.append(DATA_NUM)

        #gamma = 0.01
        G=np.random.dirichlet(G_0+gamma) #initialize G
        G_set.append(G)

        pi_e=[]
        for i in range(concept_num):
                pi=nonpara_tool.stick_breaking(beta,Stick_large_R) #initialize pi
                pi_e.append(pi)
        pi_set.append(pi_e)

        c_t=[1000 for n in xrange(DATA_NUM)] #initialize c_t
        C_t_set.append(c_t)

        r_t=[1000 for n in xrange(DATA_NUM)] #initialize r_t
        r_t_set.append(r_t)

        #initialize Mu
        Mu=[]
        kmeans=sklearn.cluster.KMeans(n_clusters=region_num, random_state=random.randint(1,100)).fit(pose)

        for j in range(region_num):
            index=int(random.uniform(0,DATA_NUM))
            p=kmeans.cluster_centers_[j]
            Mu.append(p)

        Mu=np.array(Mu)
        Mu_set.append(Mu)
        
        #initialize Sigma
        Sigma = np.array([[[sigma_init,0.0,0.0,0.0],[0.0,sigma_init,0.0,0.0],[0.0,0.0,sigma_init,0.0],[0.0,0.0,0.0,sigma_init]] for i in range(region_num)])
        Sigma_set.append(Sigma)

    VISION_DIM = len(vision_set[0][0]) #dimension of vision
    #FUNCTION_DIM =len(function_set[0][0]) #dimension of function
    NAME_DIM = len(name_set[0][0]) #dimension of name
    
    phi_v = np.array([[float(1.0)/VISION_DIM for i in range(VISION_DIM)] for j in range(concept_num)]) #initialize phi^v
    #phi_f = np.array([[float(1.0)/FUNCTION_DIM for i in range(FUNCTION_DIM)] for j in range(concept_num)]) #initialize phi^f
    phi_n = np.array([[float(1.0)/NAME_DIM for i in range(NAME_DIM)] for j in range(concept_num)]) #initialize phi^n
    region_choice = [dr for dr in range(region_num)] #[0,1,2,...,R-1]
    class_choice = [dc for dc in range(concept_num)] #[0,1,2,...,L-1]
    print("DATA_NUM: "+repr(data_num))

    for iter in xrange(iteration):
        print "iteration"+ repr(iter)  
        region_count = [[0.0 for i in range(region_num)] for j in range(data_set_num)] #array to store the number of position distributions (regions) in all environments
        class_count_e_set = [] #array to store the number of concepts in all environments

        for e in range(data_set_num): #for each environment

            #<<<<<<<<<< Latent variable (r_t, C_t) >>>>>>>>>>
            class_region_count = [[0.0 for i in range(region_num)] for j in range(concept_num)] #array to store the number of position distributions (regions) in environment e
            class_count_e = [0.0 for i in range(concept_num)] #array to store the number of concepts in environment e
            gauss_prob_set = np.zeros((region_num,data_num[e]),dtype=float) #array to store log(p(x_t|mu_{r_t},Sigma_{r_t})+p(r_t|pi_{C_t}))

            if iter==0:
                C_t = np.random.randint(concept_num,size=data_num[e]) #initialize C_t
            else:
                C_t = C_t_set[e]

            pi_e = np.array(pi_set[e])
            pi_data = np.array([pi_e[C_t[d]] for d in range(data_num[e])])
            pi_data = np.log(pi_data)

            for i in range(region_num):
                gauss_prob = ss.multivariate_normal.logpdf(position_set[e],Mu_set[e][i],Sigma_set[e][i])+pi_data[:,i] #caluculate log(p(x_t|mu_{r_t},Sigma_{r_t})+p(r_t|pi_{C_t}))
                gauss_prob_set[i] += gauss_prob

            gauss_prob_set = gauss_prob_set.T
            max_region = np.max(gauss_prob_set,axis=1)
            gauss_prob_set = gauss_prob_set - max_region[:,None]
            gauss_prob_set = np.exp(gauss_prob_set)
            sum_set = np.sum(gauss_prob_set,axis=1)
            gauss_prob_set = gauss_prob_set / sum_set[:,None]

            for d in xrange(0,data_num[e],Slide):
                r_t_set[e][d] = np.random.choice(region_choice,p=gauss_prob_set[d]) #sampling r_t
                region_count[e][r_t_set[e][d]] += 1.0
            r_t = r_t_set[e]

            phi_v_log = np.log(phi_v)
            phi_n_log = np.log(phi_n)
            #phi_f_log = np.log(phi_f)
            multi_prob_set = np.zeros((concept_num,data_num[e]),dtype=float) #array to store log(p(v_t|phi^v_{C_t})+p(n_t|phi^n_{C_t})+p(C_t|G))
            pi_data = np.array([pi_e.T[r_t[d]] for d in range(data_num[e])])
            pi_data = np.log(pi_data)
            G_log = np.log(G_set[e])
            
            for i in range(concept_num):
                vision_prob = vision_set[e].dot(phi_v_log[i])
                #function_prob = function_set[e].dot(phi_f_log[i])
                name_prob = name_set[e].dot(phi_n_log[i])
                #modal_prob = vision_prob+name_prob+function_prob+pi_data[:,i]
                modal_prob = vision_prob+name_prob+pi_data[:,i]
                modal_prob = modal_prob+G_log[i] 
                multi_prob_set[i] += modal_prob

            multi_prob_set = multi_prob_set.T
            max_concept = np.max(multi_prob_set,axis=1)
            multi_prob_set = multi_prob_set - max_concept[:,None]
            multi_prob_set = np.exp(multi_prob_set)
            sum_concept_set= np.sum(multi_prob_set ,axis=1)
            multi_prob_set = multi_prob_set / sum_concept_set[:,None]

            for d in xrange(0,data_num[e],Slide):
                C_t_set[e][d] = np.random.choice(class_choice,p=multi_prob_set[d]) #sampling C_t
                class_count_e[C_t_set[e][d]] += 1.0
                class_region_count[C_t_set[e][d]][r_t[d]] += 1.0

            #<<<<<<<<<< parameters of Gaussian distribution (Mu, Sigma) >>>>>>>>>>
            for r in xrange(region_num):
                pose_r=[]
                
                #========== calculating average ==========
                for d in xrange(data_num[e]):
                    if r_t_set[e][d] == r:
                        pose_r.append(position_set[e][d])
                        
                sum_pose = np.zeros(4) #([0.0,0.0,0.0,0.0])
                for i in xrange(len(pose_r)):
                    for j in xrange(4):
                        sum_pose[j] += pose_r[i][j]

                bar_pose=np.zeros(4) #([0.0,0.0,0.0,0.0])
                for i in xrange(4):
                    if sum_pose[i] != 0:		 	
                        bar_pose[i] = sum_pose[i]/len(pose_r)

			    #========== calculating Mu ==========
                Mu = (kappa_0*mu_0_set[e]+len(pose_r)*bar_pose)/(kappa_0+len(pose_r)) #Mu updated

                #========== calculating Matrix_R ==========
                bar_pose_matrix = np.matrix(bar_pose)
                Matrix_R = np.zeros([4,4])

                for i in xrange(len(pose_r)):
                    pose_r_matrix = np.matrix(pose_r[i])
                    Matrix_R += ((pose_r_matrix- bar_pose_matrix).T*(pose_r_matrix- bar_pose_matrix))

                #========== calculating Psai ==========
                ans = ((bar_pose_matrix - mu_0_set[e]).T * (bar_pose_matrix - mu_0_set[e]))*((kappa_0*len(pose_r))/(kappa_0+len(pose_r)))
                Psai = psai_0 + Matrix_R + ans #Psai updated
    		 	
    		 	#========== updating hyper parameter: Kappa,Nu ==========
                Kappa = kappa_0 + len(pose_r) #Kappa updated
                Nu = nu_0 + len(pose_r) #Nu updated

    		 	#========== sampling fron wishrt distribution ==========
                Sigma_set[e][r] = Prob_Cal.sampling_invwishartrand(Nu,Psai) #sampling Sigma
                Sigma_temp = Sigma_set[e][r]/Kappa
                Mu_set[e][r] = np.random.multivariate_normal(Mu,Sigma_temp) #sampling Mu

                if len(pose_r) == 0: #if no asigned data
                    p = np.array([random.uniform(map_x[e],MAP_X[e]),random.uniform(map_y[e],MAP_Y[e]),random.uniform(-1.0,1.0),random.uniform(-1.0,1.0)])
                    Mu_set[e][r] = p
                    Sigma_set[e][r] = np.array([[sigma_init,0.0,0.0,0.0],[0.0,sigma_init,0.0,0.0],[0.0,0.0,sigma_init,0.0],[0.0,0.0,0.0,sigma_init]])
            
            #<<<<<<<<<< local parameters of multinomial distribution (pi, G) >>>>>>>>>>
            for c in range(concept_num): 
                pi_set[e][c] = np.random.dirichlet(class_region_count[c]+beta) #sampling pi

            G_set[e] = np.random.dirichlet(class_count_e+(gamma*G_0)+50)+1e-100 #sampling G
            class_count_e_set.append(class_count_e)
	    
        #<<<<<<<<<< global parameters of multinomial distribution (phi^v, phi^n, G_0) >>>>>>>>>>
        total_vision_set = [] #array to store the number of vision (visual feature)
        #total_function_set = [] #array to store the number of fuction
        total_name_set = [] #array to store the number of name
        class_count = [0.0 for i in range(concept_num)] #array to store the number of concepts in all environments

        for c in xrange(concept_num):
            vision_c = []
            #function_c = []
            name_c = []

            for e in range(data_set_num):
                for d in xrange(data_num[e]):
                    if C_t_set[e][d] == c:
                        vision_c.append(vision_set[e][d])
                        #function_c.append(function_set[e][d])
                        name_c.append(name_set[e][d])
                        class_count[c] += 1.0

            total_vision = BoF.bag_of_feature(vision_c,VISION_DIM)
            total_vision_set.append(total_vision)
            total_vision = total_vision+alpha_v
            phi_v[c] = np.random.dirichlet(total_vision)+1e-100 #sampling phi_v

            """
            total_function = BoF.bag_of_feature(function_c,FUNCTION_DIM)
            total_function_set.append(total_function)
            total_function = total_function +alpha_f
            phi_f[c] = np.random.dirichlet(total_function)+1e-100 #sampling phi_f
            """

            total_name = BoF.bag_of_feature(name_c,NAME_DIM)
            total_name_set.append(total_name)
            total_name = total_name +alpha_n
            phi_n[c] = np.random.dirichlet(total_name)+1e-100 #sampling phi_n

            class_count[c] += gamma_0
            
            if len(vision_c) == 0:
                phi_v[c] = np.array([float(1.0)/VISION_DIM for i in range(VISION_DIM)])
                #phi_f[c] = np.array([float(1.0)/FUNCTION_DIM for i in range(FUNCTION_DIM)] )
                phi_n[c] = np.array([float(1.0)/NAME_DIM for i in range(NAME_DIM)] )

        G_0 = np.random.dirichlet(class_count) #sampling G_0

        if ((iter+1)%100)==0:
            C_num = 0 #C_num : Concept number
            for i in range(concept_num):
                if class_count[i]>gamma_0:
                    C_num += 1

            print "Class num:"+repr(C_num)+"\n"
            print region_count
            R_set=[0.0 for e in range(data_set_num)]
            for e in range(data_set_num):
                for r in range(region_num):
                    if region_count[e][r]>0:
                        R_set[e] +=1.0
            #========== Saving ==========
            print("--------------------------------------------")

            Out_put_dir = "gibbs_result/env_num_"+Out+"/per_"+repr(x)+"_iter_"+repr(iter+1)
            print(Out_put_dir)

            try:
                os.mkdir(Out_put_dir)
            except OSError:
                shutil.rmtree(Out_put_dir)
                os.mkdir(Out_put_dir)

            f=open("training_dataset",'w')
            for i,d in enumerate(Traing_list):
                w=repr(i)+":  "+d
                f.write(w)
            f.close()

            #saving finish time
            finish_time=time.time()- start_time
            f=open(Out_put_dir+"/time.txt","w")
            f.write("time:"+repr(finish_time)+" seconds.")
            f.close()
            f=open(Out_put_dir+"/training_dataset",'w')

            for i,d in enumerate(Traing_list):
                w=repr(i)+":  "+d+"\n"
                f.write(w)

            f.close()

            #====================saving environment parameter================================
            for i in range(data_set_num):
                os.mkdir(Out_put_dir+"/dataset"+repr(i))
                os.mkdir(Out_put_dir+"/dataset"+repr(i)+"/mu")
                os.mkdir(Out_put_dir+"/dataset"+repr(i)+"/sigma")
                os.mkdir(Out_put_dir+"/dataset"+repr(i)+"/region_name")
                os.mkdir(Out_put_dir+"/dataset"+repr(i)+"/region_function")
                np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/class.txt",C_t_set[i])
                np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/region.txt",r_t_set[i])
                np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/region_count.txt",region_count[i])
                np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/pi.csv",pi_set[i])
                np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/G.txt",G_set[i])
                np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/class_count_e.txt",class_count_e_set[i])
                np.savetxt(Out_put_dir+"/class_count.txt",class_count)
                f=open(Out_put_dir+"/dataset"+repr(i)+"/Parameter.txt","w")
                f.write("max_x_value_of_map: "+repr(MAP_X[i])+
                    "\nMax_y_value_of_map: "+repr(MAP_Y[i])+
                    "\nMin_x_value_of_map: "+repr(map_x[i])+
                    "\nMin_y_value_of_map: "+repr(map_y[i])+
                    "\nNumber_of_place: "+repr(concept_num)+
                    "\nData_num: "+repr(data_num[i])+
                    "\nSliding_data_parameter: "+repr(Slide)+
                    "\nNAME_dim: "+repr(NAME_DIM)+
                    "\nDataset: "+Traing_list[i]+
                    "\nEstimated_placeconcept_num: "+repr(C_num)+
                    "\nVision_dim: "+repr(VISION_DIM)+
                    #"\n Function_dim: "+repr(FUNCTION_DIM)+
                    "\nStick_breaking_process_max: "+repr(Stick_large_L)+
                    "\nVision_diric: "+repr(args.vision)+
                    "\nRegion_num: "+repr(R_set[i])+
                    "\nname_not: "+repr(args.name_not)+
                    "\nfunction_not: "+repr(args.function_not)+
                    #"\n name_prob: "+repr(cut_prob)+
                    "\ntest_num: "+repr(test_num)
                    )        
                f.close()

                f=open(Out_put_dir+"/dataset"+repr(i)+"/name_data_class.txt","w")
                for d in range(data_num[i]):
                    #w=sum(function_set[i][d])
                    if w>0:
                        f.write("data:"+repr(d)+" C_t:"+repr(C_t_set[i][d])+" r_t:"+repr(r_t_set[i][d])+"\n")
                f.close()
                #========Saving Gaussian distrbution===================
                for j in xrange(region_num):
                    np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/mu/gauss_mu"+repr(j)+".csv",Mu_set[i][j])
                    np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/sigma/gauss_sigma"+repr(j)+".csv",Sigma_set[i][j])
                
                #========Saving Probability of p(n_t|r_t), p(w_t|r_t)===================
                region_to_name_prob=np.array([0.0 for k in range(NAME_DIM)])
                #region_to_function_prob=np.array([0.0 for k in range(FUNCTION_DIM)])
                for r in range(region_num):
                    for c in range(concept_num):
                        prob=pi_set[i][c][r]
                        region_to_name_prob +=np.array(phi_n[c]*G_set[i][c]*prob)
                        #region_to_function_prob +=np.array(phi_f[c]*G_set[i][c]*prob)
                    np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/region_name/region_name"+repr(r)+".txt",region_to_name_prob)
                    #np.savetxt(Out_put_dir+"/dataset"+repr(i)+"/region_function/region_function"+repr(r)+".txt",region_to_function_prob)
            
            #====================saving concept parameter================================
            np.savetxt(Out_put_dir+"/phi_v.csv",phi_v)
            #np.savetxt(Out_put_dir+"/phi_f.csv",phi_f)
            np.savetxt(Out_put_dir+"/phi_n.csv",phi_n)
            np.savetxt(Out_put_dir+"/bag_of_vision.txt",total_vision_set)
            np.savetxt(Out_put_dir+"/bag_of_name.txt",total_name_set)
            #np.savetxt(Out_put_dir+"/bag_of_function.txt",total_function_set)

            f=open(Out_put_dir+"/hyper parameter.txt","w")
            f.write("alpha_v: "+repr(alpha_v)#+"\nalpha_f: "+repr(alpha_f)
                +("\nalpha_n: ")+repr(alpha_n)+("\ngamma_0: ")+repr(gamma_0)
                +("\nkappa_0: ")+repr(kappa_0)+("\nnu_0: ")+repr(nu_0)
                #+"\nmu_0: "+repr(mu_0)+"\npsai_0: "+repr(psai_0)+
                +"\ngamma: "+repr(gamma)+"\nbeta: "+repr(beta)
                +"\ninitial sigma: "+repr(sigma_init)+"\nsitck break limit: "+repr(Stick_large_L)
                +"\nvision_increment: "+repr(vision_increment)+"\nname_increment: "+repr(name_increment)
                +"\nfunction_increment: "+repr(function_increment)
                +"\npsai: ["+repr(psai_0[0][0])+"\n"+repr(psai_0[1][0])+"\n"+repr(psai_0[2][0])+"\n"+repr(psai_0[3][0])+"]"
                )
            f.close()
            
    print Name_data_dir 

if __name__ == "__main__":
    x=0 #percent given name x=0,7,14,21
    while x <= 21:
        gibbs(args.Output,x)
        x = x + 7
