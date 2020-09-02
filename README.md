# K2K
Although the paste command under the Linux system can merge files, the command cannot use one or more columns as keys to take the intersection or union of multiple files. K2K was developed for this reason.

K2K is available at [github](https://github.com/tianguolangzi/K2K)
and [PyPI](https://pypi.python.org/pypi/K2K).

# Install K2K

### pip
`pip install K2K`

### git 
```
git clone https://github.com/tianguolangzi/K2K.git
cd K2K/
python3 setup.py install
```

# User guide

The key is made up of the same columns.
### intersection
```
K2K A.txt B.txt C.txt.gz -k 1,2,3,4,5 -o 6 --sk --so
K2K A.txt B.txt C.txt.gz -k 1-5 -o 6 --sk --so 
```

#### union
```
K2K A.txt B.txt C.txt.gz -k 1-5 -o 6 --sk --so  --do U
```

When taking the union, you can set the default value through the ‘-r’ parameter
```
K2K A.txt B.txt C.txt.gz -k 1-5 -o 6 --sk --so  --do U  -r -
```

The key is made up of the different columns.
```
K2K A.txt B.txt C.txt.gz -k '1,3;2,3;3,4' -o 6  --so 
```
At the same time, the output columns are not the same.

```
K2K A.txt B.txt C.txt.gz -k '1,3;2,3;3,4' -o '4,5;5,6;5,6' 
```