import os
import glob

base_dir = os.getcwd()

for root, dirs, files in os.walk('.', topdown=False):
    for dir in dirs:            
        dirPath = os.path.join(root,dir)
        AbsDirPath = os.path.abspath(dirPath)

        os.chdir(AbsDirPath)

        if 'slurm' in str(os.listdir(AbsDirPath)):

            slurmFile = glob.glob('slurm-*')
            
            if len(slurmFile) > 1:
                print('\n')
                print("Multiple Slurm File Exist!")
                print(AbsDirPath)
                print('\n')
            
            f = open(slurmFile[0], 'r')
            filecontents = f.readlines()
            f.close()

            if len(filecontents) > 0:

                if "DUE TO TIME LIMIT" in filecontents[0]:
                    print(AbsDirPath)
                
        os.chdir(base_dir)