# coding: utf-8
# Copyright (c) 2016-2020 Kun Zhang
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Author: Kun Zhang <tianguolangzi@gmail.com>

import sys,gzip
import argparse
from collections import defaultdict
__version__=1.0
__infor__='Combine multiple files based on the same key consisting of one or more columns'

def getParser():
    parser = argparse.ArgumentParser(
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    description='''K2KS.\n{} '''.format(__infor__), 
                                    epilog='''useage: \n\tK2K  test/*unix.txt -k 1-5 -o 6-8 --so --sk -r -  >test.test''')
    parser.add_argument('--version', action = 'version', version = '{}'.format(__version__))
    parser.add_argument('files', nargs = '*', help = 'files' )
    parser.add_argument('--so',action='store_true',default=False,help = "Use this parameter when the columns to be output from each file are the same. Then use the -o parameter, just fill in the columns that need to be output once.")
    parser.add_argument('--sk',action='store_true',default=False,help = "When the columns of each file to form the key are the same, use this parameter, and then use the -k parameter, you only need to specify the column to form the key once.")
    parser.add_argument('-k',nargs = '*',help = "The columns that make up the key in each file are separated by commas, consecutive columns are connected by dashes, and different files are separated by semicolons.")
    parser.add_argument('-o',nargs = '*',help = "The columns to be output in each file are separated by commas, consecutive columns are connected by dashes, and different files are separated by semicolons.")
    parser.add_argument('--do',choices=['I','U'],default='I',help="The file merging method is to take intersection or union. U stands for union, I stands for intersection.")
    parser.add_argument('-r',default="-",help="When taking the union, what symbol is used to replace the default value.")
    parser.add_argument('--OF', default = '\t', help = 'field separator')
    parser.add_argument('--OFS',default = '\t', help = 'output field separator')
    return parser


def readFile(File,KeyIndex,OF,OutIndex,Replace):

    A1=gzip.open(File,"rt") if File[-3:] == '.gz' else open(File,"r")
    KeyDict=defaultdict(lambda:"\t".join([Replace]*len(OutIndex)))
    for line in A1.readlines():
        if "#" == line[0]:continue
        if line == '\n':continue
        tmp = line.strip().split(OF)
        Key = "\t".join([ tmp[i] for i in KeyIndex ])
        Con = "\t".join([ tmp[i] for i in OutIndex ])
        KeyDict[Key] = Con
    A1.close()
    return KeyDict


def getIndexList(Index):
    tmp=[]
    tmp1=[]
    tmp2=[]
    for i in Index:
        tmp.extend(i.replace(' ','').split(","))
    tmp1= [i for i in tmp if i not in tmp1]
    for i in tmp1:
        if i =="":continue
        if "-" not in i :
            tmp2.append(int(i)-1)
        else:
            l,m=list(map(int,i.split("-")))
            for j in range(l,m+1):
                tmp2.append(j-1)
    return tmp2


def K2K(Files,KeyIndexDict,OutIndexDict,Replace,OF,UI):
    ConDict    = {}
    KeySetDict = {}
    for f in Files:
        ConDict[f]    = readFile(f,KeyIndexDict[f],OF,OutIndexDict[f],Replace)
        KeySetDict[f] = set(ConDict[f].keys())
    if UI == 'U':
        KeySet = KeySetDict[Files[0]]
        for f in Files[1:]:
            KeySet = KeySet | KeySetDict[f]
    elif UI == 'I':
        KeySet = KeySetDict[Files[0]]
        for f in Files[1:]:
            KeySet = KeySet & KeySetDict[f]
    return KeySet,ConDict


def main():
    parser  = getParser()
    args    = parser.parse_args()
    if len(args.files) <= 1:
        print('ERROR. At least two input files are required.')
        sys.exit(1)
    Files   =   args.files
    OF      =   args.OF
    OFS     =   args.OFS
    so      =   args.so
    sk      =   args.sk
    UI      =   args.do
    Replace =   args.r
    
    
    # if args.header is None:
        # args.header =   ('0,'*len(Files))[:-1]
        # Header  =   getIndexList(args.header)
    # else:
        # Header  =   getIndexList(args.header)
        # if len(Header)<len(Files):
            # Header  =   Header+[Header[0]]*(len(Files)-len(Header))
    # Header          =   [h+1 for h in Header]
    KeyIndexDict    =   {}
    OutIndexDict    =   {}
    if sk:
        KeyIndex    =   getIndexList(args.k)
        for f in Files:
            KeyIndexDict[f] = KeyIndex
    else:
        AllIndex    =   " ".join(args.k).split(';')
        if len(AllIndex) != len(Files):
            print('ERROR. The number of files'+str(len(Files))+'is not equal to the number of -k.'+str(len(AllIndex)))
            sys.exit(1)
        else:
            for f,tmpIndex in zip(Files,AllIndex):
                KeyIndexDict[f] =  getIndexList([tmpIndex])

    if so:
        OutIndex    =   getIndexList(args.o)
        for f in Files:
            OutIndexDict[f] =   OutIndex
    else:
        AllIndex    =   " ".join(args.o).split(';')
        if len(AllIndex) != len(Files):
            print('ERROR. The number of files'+str(len(Files))+'is not equal to the number of -o.'+str(len(AllIndex)))
            sys.exit(1)
        else:
            for f,tmpIndex in zip(Files,AllIndex):
                OutIndexDict[f] =   getIndexList([tmpIndex])


    KeySet,ConDict  =   K2K(Files,KeyIndexDict,OutIndexDict,Replace,OF,UI)
    for k in KeySet:
        print(k + OFS + OFS.join([ConDict[f][k]  for f  in Files]))

if __name__ == '__main__':
    main()
