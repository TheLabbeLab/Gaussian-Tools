import os

base_dir = os.getcwd()

for root, dirs, files in os.walk('.', topdown=False):
    for dir in dirs:
        JobPath = os.path.join(root,dir)
        if 'slurm' not in str(os.listdir(JobPath)) and 'run_all_gjfs_series.sh' in os.listdir(JobPath):
            JobAbsPath = os.path.abspath(JobPath)
            os.chdir(JobAbsPath)
            os.system('dos2unix run_all_gjfs_series.sh')
            FireJobs = 'sbatch run_all_gjfs_series.sh'
            os.system(FireJobs)
            os.chdir(base_dir)

print("Fired all Jobs!")
