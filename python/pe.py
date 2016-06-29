import pefile
import os,string,shutil,re

PEfile_Path = r"E:\test\test.exe"
pe = pefile.PE(PEfile_Path)

print PEfile_Path
print pe