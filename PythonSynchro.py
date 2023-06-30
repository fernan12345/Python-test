import sys
import time
import os
import hashlib
import shutil
import stat

ARGUMENTS = 5

def log(log_path, message):
      #Write in the log file that we give as parameter
      now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
      with open(log_path, "a") as f:
            f.write("[" +now+ "] "+message+"\n")

#function utilized for calculate and compare hashing
def file_hashing_compare(fileoriginal, filesynchro):
      equal = False
      #File 1
      hasher1 = hashlib.md5()
      afile1 = open(fileoriginal, 'rb')
      buf1 = afile1.read()
      a = hasher1.update(buf1)
      md5_a=(str(hasher1.hexdigest()))
      #File 2
      hasher2 = hashlib.md5()
      afile2 = open(filesynchro, 'rb')
      buf2 = afile2.read()
      b = hasher2.update(buf2)
      md5_b=(str(hasher2.hexdigest()))
      #Compare md5
      if(md5_a==md5_b):
            equal = True
            print(fileoriginal+ " y " +filesynchro+ " son iguales")

      return equal

def compareHashFolder(original_folder, synchro_folder):
      #get all files of the folder in the original folder
      files = os.listdir(original_folder)
      #get all files in the folder of the synchro folder
      files_backup = os.listdir(synchro_folder)
      #Compare the 2 list of elements of the folders
      if len(files) != len(files_backup):
            return False
      for file in files:
            if file in files_backup:
                  if file_hashing_compare(original_folder+"/"+file, synchro_folder+"/"+file) != True:
                        return False
            else:
                  return False
      return True



#Function utilized to do the synchronization
def synchronize ():
      print ("synchronizing")
      original_files = os.listdir(original_folder_path)
      synchronized_files =os.listdir(synchronized_folder_path)

      #Loop for remove the files that doesnt exist in the original folder anymore
      for filesynchro in synchronized_files:
            exist = False
            print (filesynchro)
            for file in original_files:
                  #If they are 2 folders we compare with the folder method of comparison
                  if( os.path.isdir(synchronized_folder_path+"/"+filesynchro) and os.path.isdir(original_folder_path+"/"+file) ):
                        exist = compareHashFolder(original_folder_path+"/"+file,synchronized_folder_path+"/"+filesynchro)
                  #If they are 2 files, we compare with the file method of comparison
                  elif (os.path.isfile(synchronized_folder_path+"/"+filesynchro) and os.path.isfile(original_folder_path+"/"+file)):
                         exist = file_hashing_compare(original_folder_path+"/"+file, synchronized_folder_path+"/"+filesynchro)
                  #If both files/folders are exactly the same, we break the loop as no more comparison are needed, saving computing time
                  if exist == True:
                        break
            #In case the file/folder  exist in the synchro folder but doesnt exist in the original folder, we delete it   
            if exist == False:
                  log(log_file_path, "The file/folder "+filesynchro+" doesnt exist or its not equal in the original folder.Deleting it")
                  #If it is a file, we delete it with the file deleting function
                  if ( os.path.isfile(synchronized_folder_path+"/"+filesynchro) ):
                        os.remove(synchronized_folder_path+"/"+filesynchro)
                  # Or we delete it with the directory deleting function if it is a directory
                  elif( os.path.isdir(synchronized_folder_path+"/"+filesynchro) ):
                        shutil.rmtree(synchronized_folder_path+"/"+filesynchro, ignore_errors=True)

      #Loop for check if the files in original already exist in synchro, and if not, copy them.
      for file in original_files:
            equal = False
            for filesynchro in synchronized_files:
                  #If they are 2 folders we compare with the folder method of comparison
                  if( os.path.isdir(synchronized_folder_path+"/"+filesynchro) and os.path.isdir(original_folder_path+"/"+file) ):
                        equal = compareHashFolder(original_folder_path+"/"+file,synchronized_folder_path+"/"+filesynchro)
                  #If they are 2 files, we compare with the file method of comparison
                  elif (os.path.isfile(synchronized_folder_path+"/"+filesynchro) and os.path.isfile(original_folder_path+"/"+file)):
                         equal = file_hashing_compare(original_folder_path+"/"+file, synchronized_folder_path+"/"+filesynchro)
                  #If both files/folders are exactly the same, we break the loop as no more comparison are needed, saving computing time
                  if equal == True:
                        break
            #In case the file/folder doesnt exist in the synchro folder, we copy the filde/folder into it
            if equal == False:
                  log(log_file_path,"The file "+file+" doesnt exist in the synchro folder. We copy it")
                  if ( os.path.isfile(original_folder_path+"/"+file) ):
                        shutil.copyfile(original_folder_path+"/"+file,synchronized_folder_path+"/"+file)

                  elif( os.path.isdir(original_folder_path+"/"+file) ):
                        shutil.copytree(original_folder_path+"/"+file,synchronized_folder_path+"/"+file, dirs_exist_ok=True)



      return 0







exit = 0
if len(sys.argv) != ARGUMENTS:
        print("Number of arguments is (including the executing python file command)",len(sys.argv), "which its not ", ARGUMENTS)
        print("remember that the arguments must be: original folder, synchronized folder, synchronization interval and log file path")
        print("If you need to use more arguments for any reason, you can modify ARGUMENT variable to fit the new number")
     
else:
    original_folder_path = sys.argv[ARGUMENTS-4] #Path of the original folder
    synchronized_folder_path = sys.argv[ARGUMENTS-3] #Path of the original folder
    syncro_interval = sys.argv[ARGUMENTS-2] #Number of seconds between synchronizations
    log_file_path = sys.argv[ARGUMENTS-1] #Log file path

    while exit == 0:
          synchronize()
          time.sleep(int(syncro_interval))


