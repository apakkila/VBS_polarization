import os 
import glob


allOutFile =  glob.glob('./Ntuple*.*.out')
allOutFile.sort() # sort by name

jobsDone=[]
jobsNotDone=[]

for fileName in allOutFile:
  file = open(fileName,"r")

  lines = file.read()
  if "NtupleMaker::main()::DONE" in lines:
    jobsDone.append(fileName)
  else:
    jobsNotDone.append(fileName)

print("============================================")
print("                Jobs Done                   ")
print("============================================")

for jobs in jobsDone:
  print(jobs)

print("============================================")
print("                Jobs Still Not Done         ")
print("============================================")

for jobs in jobsNotDone:
  print(jobs)


print("========================================================")
print("                Checking last line of jobs  not done    ")
print("========================================================")

for jobs in jobsNotDone:
  print (jobs)
  os.system('tail -n 1 ' + jobs)
  print ("\n")

