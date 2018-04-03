'''
Created on 8. 8. 2017

@author: dmarkov004
'''

def IsNature(s):
    try:
        int(s)
    except ValueError:
        return False
    if int(float(s))>0:
        return True
    else:
        return False