import os

base_dir = os.getcwd()

for root, dirs, files in os.walk('.', topdown=False):
    for dir in dirs:
        JobPath = os.path.join(root,dir)
        if 'Gau' in str(os.listdir(JobPath)):
            JobAbsPath = os.path.abspath(JobPath)
            print(JobAbsPath)

print("Gau file paths printed!")
