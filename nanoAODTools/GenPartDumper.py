#! /usr/bin/env python3
# Sources:
#   https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/python/genparticles_cff.py
#   https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/NanoAOD/plugins/LHETablesProducer.cc
from datamodel import Collection
#from PhysicsTools.NanoAODTools.postprocessing.tools import hasbit
import datamodel as datamodel
datamodel.statusflags['isHardPrompt'] = datamodel.statusflags['isPrompt'] + datamodel.statusflags['fromHardProcess'] 

def hasAncestor(part,pdgId):
  if part.moth:
    if abs(part.moth.pdgId) == pdgId:
      return True
    elif part.moth.moth:
      return hasAncestor(part.moth,pdgId)
    else:
      return False
  else:
    return False

def getFinalCopy(part):
  desc = None
  for dau in part.daughters:
    if dau.pdgId == part.pdgId: 
      desc = dau
      break
  return getFinalCopy(desc) if desc else part


def getFirstCopy(part):
  parent = None
  if part.mother != None and part.mother.pdgId == part.pdgId:
    parent = part.mother
  return getFirstCopy(parent) if parent else part

def hasMother(part,pdgId):
  if abs(part.moth.pdgId) == pdgId:
    return True
  else:
    return False

def getprodchain(part,genparts=None,event=None,decay=-1):
  """Print production chain recursively."""
  chain = "%3s"%(part.pdgId)
  # chain = "%3s (%s) "%(part.pdgId, part._index)
  imoth = part.genPartIdxMother
  while imoth>=0:
    if genparts is not None:
      moth = genparts[imoth]
      # chain = "%3s -> "%(moth.pdgId)+chain
      chain = "%3s (%2s) -> "%(moth.pdgId, moth._index)+chain
      imoth = moth.genPartIdxMother
    elif event is not None:
      # chain = "%3s -> "%(event.GenPart_pdgId[imoth])+chain
      chain = "%3s (%2s) -> "%(event.GenPart_pdgId[imoth], moth._index)+chain
      imoth = event.GenPart_genPartIdxMother[imoth]
  if genparts is not None and decay>0:
    chain = chain[:-3] # remove last particle
    chain += getdecaychain(part,genparts,indent=len(chain),depth=decay-1)
  return chain


def getdecaychain(part,genparts,indent=0,depth=999):
  """Print decay chain recursively."""
  chain   = "%3s"%(part.pdgId)
  # chain = "%3s (%s) "%(part.pdgId, part._index)
  imoth   = part._index
  ndaus   = 0
  indent_ = len(chain)+indent
  for idau in range(imoth+1,genparts._len): 
    dau = genparts[idau]
    if dau.genPartIdxMother==imoth: # found daughter
      if ndaus>=1:
        chain += '\n'+' '*indent_
      if depth>=2:
        chain += " -> "+getdecaychain(dau,genparts,indent=indent_+4,depth=depth-1)
      else: # stop recursion
        # chain += " -> %3s"%(dau.pdgId)
        chain += " -> %3s (%3s)"%(dau.pdgId, dau._index)
      ndaus += 1
  return chain

# DUMPER MODULE
class GenPartDumper():
  def __init__(self):
    self.nleptonic = 0
    self.ntauonic  = 0
    self.nevents   = 0

  def setupGenParts(self,particles):

    for i, particle in enumerate(particles):
      particle.daughters = []
      particle.mother = None
      particle.mothPdgId = 0

    for i, particle in enumerate(particles):
      if particle.genPartIdxMother >= 0 and particle.genPartIdxMother < particles._len:
        particle.mothPdgId = particles[particle.genPartIdxMother].pdgId
        particle.mother = particles[particle.genPartIdxMother]
        particles[particle.genPartIdxMother].daughters.append(particle)

  def analyze(self, event, particles):
    """Dump gen information for each gen particle in given event."""
    print("\n%s Event %s %s"%('-'*10,event.event,'-'*70))
    self.nevents += 1
    leptonic = False
    tauonic = False
    bosons = [ ]
    taus = [ ]
    #particles = Collection(event,'LHEPart')
    print(" \033[4m%7s %7s %7s %7s %7s %7s %7s %7s %8s %9s %10s  \033[0m"%(
      "index","pdgId","moth","mothId","dR","pt","eta","status","prompt","taudecay","last copy"))
    for i, particle in enumerate(particles):
      mothidx  = particle.genPartIdxMother
      eta      = max(-999,min(999,particle.eta))
      prompt   = particle.statusflag('isPrompt') #hasbit(particle.statusFlags,0)
      taudecay = particle.statusflag('isTauDecayProduct') #hasbit(particle.statusFlags,2)
      lastcopy = particle.statusflag('isLastCopy') #hasbit(particle.statusFlags,13)
      #ishardprompt = particle.statusflag('isHardPrompt')
      if 0<=mothidx<particles._len:
        moth    = particles[mothidx]
        mothpid = moth.pdgId
        mothdR  = max(-999,min(999,particle.DeltaR(moth))) #particle.p4().DeltaR(moth.p4())
        print(" %7d %7d %7d %7d %7.2f %7.2f %7.2f %7d %8s %9s %10s"%(
          i,particle.pdgId,mothidx,mothpid,mothdR,particle.pt,eta,particle.status,prompt,taudecay,lastcopy))
      else:
        print(" %7d %7d %7s %7s %7s %7.2f %7.2f %7d %8s %9s %10s"%(
          i,particle.pdgId,"","","",particle.pt,eta,particle.status,prompt,taudecay,lastcopy))
      if lastcopy:
        if abs(particle.pdgId) in [11,13,15]:
          leptonic = True
          if abs(particle.pdgId)==15:
            tauonic = True
            taus.append(particle)
        elif abs(particle.pdgId) in [23,24]:
          bosons.append(particle)
    for boson in bosons: # print production chain
      print("Boson production:")
      print(getprodchain(boson,particles,decay=2))
    for tau in taus: # print decay chain
      print("Tau decay:")
      print(getdecaychain(tau,particles))
    if leptonic:
      self.nleptonic += 1
    if tauonic:
      self.ntauonic += 1

  def endJob(self):
    print('\n'+'-'*96)
    if self.nevents>0:
      print("  %-10s %4d / %-4d (%4.1f%%)"%('Tauonic: ',self.ntauonic, self.nevents,100.0*self.ntauonic/self.nevents))
      print("  %-10s %4d / %-4d (%4.1f%%)"%('Leptonic:',self.nleptonic,self.nevents,100.0*self.nleptonic/self.nevents))
    print("%s Done %s\n"%('-'*10,'-'*80))