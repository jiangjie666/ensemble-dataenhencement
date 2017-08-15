#coding=utf-8 
       
import os
import caffe 
import numpy as np 
root='/home/liuyun/caffe/'   #��Ŀ¼ 
deploy=root + 'examples/DR_grade/deploy.prototxt'    #deploy�ļ� 
caffe_model=root + 'models/DR/model1/DRnet_iter_40000.caffemodel'  #ѵ���õ� caffemodel 
 
 
import os
dir = root+'examples/DR_grade/test_512/'
filelist=[]
filenames = os.listdir(dir)
for fn in filenames:
   fullfilename = os.path.join(dir,fn)
   filelist.append(fullfilename)
 
 
# img=root+'data/DRIVE/test/60337.jpg'   #����ҵ�һ�Ŵ���ͼƬ 
 
def Test(img):
      
    net = caffe.Net(deploy,caffe_model,caffe.TEST)   #����model��network 
       
    #ͼƬԤ�������� 
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})  #�趨ͼƬ��shape��ʽ(1,3,28,28) 
    transformer.set_transpose('data', (2,0,1))    #�ı�ά�ȵ�˳����ԭʼͼƬ(28,28,3)��Ϊ(3,28,28) 
    #transformer.set_mean('data', np.load(mean_file).mean(1).mean(1))    #��ȥ��ֵ��ǰ��ѵ��ģ��ʱû�м���ֵ������Ͳ��� 
    transformer.set_raw_scale('data', 255)    # ���ŵ���0��255��֮�� 
    transformer.set_channel_swap('data', (2,1,0))   #����ͨ������ͼƬ��RGB��ΪBGR 
       
    im=caffe.io.load_image(img)                   #����ͼƬ 
    net.blobs['data'].data[...] = transformer.preprocess('data',im)      #ִ���������õ�ͼƬԤ�������������ͼƬ���뵽blob�� 
       
    #ִ�в��� 
    out = net.forward() 
       
    labels = np.loadtxt(labels_filename, str, delimiter='\t')   #��ȡ��������ļ� 
    prob= net.blobs['prob'].data[0].flatten() #ȡ�����һ�㣨prob������ĳ�����ĸ���ֵ������ӡ,'prob'Ϊ���һ�������
    print prob 
    order=prob.argsort()[4]  #������ֵ����ȡ�����ֵ���ڵ���� ,9ָ���Ƿ�Ϊ0-9ʮ�� 
    #argsort()�����Ǵ�С�������� 
    print 'the class is:',labels[order]   #�������ת���ɶ�Ӧ��������ƣ�����ӡ 
    f=file("/home/liuyun/caffe/examples/DR_grade/label.txt","a+")
    f.writelines(img+' '+labels[order]+'\n')
 
labels_filename = root +'examples/DR_grade/DR.txt'    #��������ļ��������ֱ�ǩת����������� 
 
for i in range(0, len(filelist)):
    img= filelist[i]
    Test(img)
