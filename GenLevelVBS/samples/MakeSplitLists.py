import itertools
import os
import glob

def chunks(l, n):
  """Yield successive n-sized chunks from l."""
  for i in range(0, len(l), n):
    yield l[i:i + n]

def main(txtFileName, nGroupFiles=10):
  listOfTxtFiles = glob.glob(txtFileName+".txt")

  for txtFile in listOfTxtFiles:
    sampleName = txtFile.replace(".txt","")
    with open(txtFile) as f:
      files = f.read().splitlines()
      filesChunks = list(chunks(files,nGroupFiles))
      i=0
      for fileChunk in filesChunks:
        txtFileSplitName = sampleName+"_part"+str(i)+".txt"
        fOut = open(txtFileSplitName, "w")
        for line in fileChunk:
          # write line to output file
          fOut.write(line + "\n")
        fOut.close()
        i += 1

if __name__ == "__main__":

  txtFiles=[
    ("USER_Run3Summer22DR_GENSIMRECO_BX0_SingleNeutrino_E-10_gun",25),
    ("USER_Run3Summer22DR_GENSIMRECO_SingleNeutrino_E-10_gun",25),
  ]

  for txtFile in txtFiles:
    main(txtFile[0],txtFile[1])

