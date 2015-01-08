#!/usr/bin/python 

b'You need Python 2.6 or later.'

import sys
import os
import tempfile
import errno
import re


gold_dir = ''
system_dir = ''

def create_tmp_folder():
    tmp_folder = tempfile.mkdtemp() 
    try:
        os.makedirs(tmp_folder)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(tmp_folder):
            pass
        else: raise
    return tmp_folder

tmp_folder = create_tmp_folder()

if len(sys.argv) > 3:
    ord = 1
else:
    ord = 0

if (ord):
    gold_dir = sys.argv[2]
    system_dir = sys.argv[3]
else:
    gold_dir = sys.argv[1]
    system_dir = sys.argv[2]

fscore = 0.0
total = 0
for file in os.listdir(gold_dir):
    f = open(gold_dir+'/'+file,'r')
    out = open(tmp_folder+'/gold-'+file,'w')
    for i, line in enumerate(f):
        if i == 0:
            continue
        out.write(line)
    length = i
    total += length
    f.close()
    out.close()
    if not os.path.isfile(system_dir+'/'+file):
        print "No answer file found " + system_dir+'/'+file
        print "Skipping the evaluation of it. Fscore set at 0"
        continue
    f = open(system_dir+'/'+file,'r')
    out = open(tmp_folder+'/sys-'+file,'w')
    for i, line in enumerate(f):
        if i == 0:
            continue
        out.write(line)
    f.close()
    out.close()
        
    if (ord):
        command = 'python evaluation_timeline_ord.py '+tmp_folder+' gold-'+file +' sys-'+file
        os.system(command)
    else:
        command = 'python evaluation_timeline.py '+tmp_folder+' gold-'+file +' sys-'+file
        os.system(command)
    f = open(tmp_folder+'/tmp.out','r')
    for line in f:
        if line.strip()=='':
            continue
        print 'FSCORE:'+line.strip()+'\t'+file
        fscore += float(line.strip())*length
fmicro = fscore/total
print "MICRO-FSCORE:"+str(fmicro)
command = 'rm -rf '+tmp_folder    
os.system(command)
