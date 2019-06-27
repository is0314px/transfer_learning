#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
import sys

def test_data_read(file,test_num):#read number of test data
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

if __name__ == "__main__":
    result_dir = sys.argv[1] #result path of gibbs sampling , example: gibbs_result/env_num_*
    test_dataset_index = sys.argv[2] #index of test dataset   if path_num*, this is *
    name_list=np.loadtxt("../gibbs_dataset/dataset_path_txt/transfer_similar/name_dic_1DK.txt", delimiter="\n", dtype="S" )
    dataset_dir=sys.argv[3] #dataset directory saved in result_dir
    test_num_txt = dataset_dir+"/test_num.txt"
    label_dir = dataset_dir+"/name_label"

    per=0
    max_per=20

    while per <= max_per:
        estimated_txt = result_dir+"/per_"+repr(per)+"_iter_200/dataset"+repr(int(test_dataset_index))+"/name_estimate_value.txt"
        test_num=0
        test_data_num=test_data_read(test_num_txt,test_num) #read test data number
        
        label_name=[]
        for test_data_index in test_data_num:
            temp=np.loadtxt(label_dir+"/word"+repr(test_data_index)+".txt", delimiter="\n", dtype="S" ) #read label name data
            label_name.append(temp)

        read_estimated_txt=np.loadtxt(estimated_txt, delimiter=" ", dtype="S" ) #read estimated name data

        N=0 #0,1,2,3,..., all label number
        cnt=0 #count matching number
        est_name_num = [0 for i in range(len(name_list))]
        label_name_num = [0 for i in range(len(name_list))]
        prob_k = [0 for i in range(len(name_list))]

        for estimated_name in read_estimated_txt:
            if str(estimated_name[1]) in str(label_name[N]): #if estimated name matched to label name, cnt is incremented
                cnt += 1

            for k, names in enumerate(name_list):
                if names == str(estimated_name[1]):
                    est_name_num[k] += 1
                if names in str(label_name[N]):
                    label_name_num[k] += 1
            
            N=N+1
        
        chance_prob = 0
        for k in range(len(name_list)):
            prob_k[k]=(float(est_name_num[k])/float(N))*(float(label_name_num[k])/float(N))
            chance_prob += prob_k[k]
        
        accuracy=float(cnt)/float(N)
        kappa=(accuracy-chance_prob)/(1-chance_prob) #caluculae kappa statistic

        print("per:"+repr(per))
        print("kappa_statistic = "+repr(kappa))

        file = open(result_dir+'/kappa_statistic.txt','a')
        file.write(repr(per)+"%: "+repr(kappa)+'\n')
        file.close()

        per=per+5




    

