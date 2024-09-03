import os

run_shell_script = """#!/bin/bash
#SBATCH --partition=amilan
#SBATCH --qos=normal
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --time=24:00:00
#SBATCH --job-name=m062x
#SBATCH --account=ucb273_peak2
#SBATCH --mail-type=ALL
#SBATCH --mail-user=prsh1291@colorado.edu

module purge
module load gaussian/g16_c.02

# Always specify a scratch directory on a fast storage space (not /home or /projects!)
export GAUSS_SCRDIR="$(pwd)"

FILES=*.gjf
for f in $FILES
do
 DATE=$(date +"%Y-%m-%d")
 name=$(echo "$f" | cut -f 1 -d ".")
 LogName="${name}_${DATE}"
 g16 <$name.gjf> $LogName.log
 echo "Processing $name file..."
done

date
"""

for root, dirs, files in os.walk('.', topdown=False):
    for file in files:
        if file.endswith('.gjf'):
            print(file)
            if file.startswith('TS'):
                filepath = os.path.join(root, file)
                print(filepath)
                f = open(filepath, 'r')
                filecontents = f.readlines()
                f.close()
                # print(filecontents[0:7])
                filecontents[0] = '%nprocshared=32\n'
                filecontents[1] = '%mem=100GB\n'
                filecontents[2] = f'%chk={file.split(".")[0]}.chk\n'
                filecontents[3] = f'#opt=(calcall,tight,ts) freq m062x/cc-pvtz maxdisk=500GB int=ultrafine\n'
                filecontents.pop(4)
                filecontents[4] = '\n'
                filecontents[5] = 'Gaussian input prepared by Pray Shah\n'
                # print(filecontents[0:7])
                f = open(filepath, 'w')
                f.writelines(filecontents)
                f.close()
                filepath = os.path.join(root, 'run_all_gjfs_series.sh')
                f = open(filepath, 'w')
                f.writelines(run_shell_script)
                f.close()

            else:
                filepath = os.path.join(root, file)
                print(filepath)
                f = open(filepath, 'r')
                filecontents = f.readlines()
                f.close()
                # print(filecontents[0:7])
                filecontents[0] = '%nprocshared=32\n'
                filecontents[1] = '%mem=100GB\n'
                filecontents[2] = f'%chk={file.split(".")[0]}.chk\n'
                filecontents[3] = f'#opt=(calcall,tight) freq m062x/cc-pvtz maxdisk=500GB int=ultrafine\n'
                filecontents[4] = '\n'
                filecontents[5] = 'Gaussian input prepared by Pray Shah\n'
                # print(filecontents[0:7])
                f = open(filepath, 'w')
                f.writelines(filecontents)
                f.close()
                filepath = os.path.join(root, 'run_all_gjfs_series.sh')
                f = open(filepath, 'w')
                f.writelines(run_shell_script)
                f.close()


