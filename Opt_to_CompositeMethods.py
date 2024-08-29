import os
import shutil
import glob

base_dir = os.getcwd()


def Create_CM(method):
    
    f = open('run_all_gjfs_series.sh', 'r')
    filecontents = f.readlines()
    f.close()

    if method == 'CBS-QB3':
        filecontents[6] = f"#SBATCH --job-name={method.split('-')[0]}-Full\n"
    else:
        filecontents[6] = f'#SBATCH --job-name={method}-Full\n'

    f = open('run_all_gjfs_series.sh', 'w')
    f.writelines(filecontents)
    f.close()

    f = open(GJF_File, 'r')
    filecontents = f.readlines()
    f.close()

    filecontents[2] = f'%chk={GJF_File.split(".")[0]}.chk\n'
    
    if GJF_File.startswith('TS'):
        filecontents[3] = f'#opt=(calcall,tight,ts) freq {method} maxdisk=500GB int=ultrafine\n'
    else:
        filecontents[3] = f'#opt=(calcall,tight) freq {method} maxdisk=500GB int=ultrafine\n'
        
    if filecontents[4] != '\n':
        del filecontents[4]

    f = open(GJF_File, 'w')
    f.writelines(filecontents)
    f.close()
    

for root, dirs, files in os.walk('.', topdown=False):
    for dir in dirs:
        if dir == 'Optimization':    
            Opt_Path = os.path.abspath(os.path.join(root,dir))
            Parent_Dir = os.path.abspath(root)
            
            print(Parent_Dir)
            
            os.chdir(Opt_Path)
            
            for iter_dir in os.listdir():
                if os.path.isdir(iter_dir):
                    Opt_Path = os.path.abspath(os.path.join(Opt_Path,iter_dir))
                    os.chdir(Opt_Path)
                    break

            GJF_File = glob.glob('*.gjf')[0]
            SH_File  = glob.glob('*.sh')[0]

            os.chdir(Parent_Dir)
            
            if 'Composite Methods' in str(os.listdir()):
                print("Composite Methods Dir Found!")
            else:
                os.mkdir('Composite Methods')
                os.mkdir('Composite Methods/CBS-QB3')
                os.mkdir('Composite Methods/G4')
                                
                CBS_Path = os.path.abspath(os.path.join(Parent_Dir, 'Composite Methods/CBS-QB3'))
                G4_Path = os.path.abspath(os.path.join(Parent_Dir, 'Composite Methods/G4'))

                shutil.copy(os.path.join(Opt_Path, GJF_File), CBS_Path)
                shutil.copy(os.path.join(Opt_Path, SH_File ), CBS_Path)
                
                shutil.copy(os.path.join(Opt_Path, GJF_File), G4_Path)
                shutil.copy(os.path.join(Opt_Path, SH_File ), G4_Path)

                os.chdir(CBS_Path)
                Create_CM(method='CBS-QB3')

                os.chdir(G4_Path)
                Create_CM(method='G4')
            
            os.chdir(base_dir)                                        


print("Done!")