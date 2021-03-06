#!/usr/bin/python

#SYNTAX: ./3daptamers.py SEQ folder returnDNA sectruct
#BEWARE: SOME TRIPLE SPACES ARE NEEDED AND MUST NOT BE REPLACED BY TABS ! 

from sys import *
from os import system, chdir, getcwd

if argc<5:
	print "SYNTAX: ./3daptamers.py SEQ folder returnDNA sectruct"
	exit(0)

a = 0
ncycles = int(argv[5])

def progress(string):
	avancement = open("progress.txt", "a")
	avancement.writelines([string+'\n'])
	avancement.close()

def console(string):
	print "----------------------------------------------------------------------------------------"
	print string
	print "----------------------------------------------------------------------------------------"

# Path definition
console("Path definitions")
userdir = "~/aptamers"
exportcmd = "export ROSETTA=%s/Rosetta ; export ROSETTA3=%s/Rosetta/main/source ; export RNA_TOOLS=$ROSETTA/tools/rna_tools; python $RNA_TOOLS/sym_link.py ; export PATH=$PATH:$RNA_TOOLS/bin/export PYTHONPATH=$PYTHONPATH:$RNA_TOOLS/bin/ ;"%(userdir, userdir)
path = '%s/%s'%(userdir, argv[2])

while path != getcwd():
	try:
		chdir(path)
	except OSError:
		a += system('mkdir %s'%path)
		if a:
			progress('!Unable to create task directory on server')
			exit(1)

avancement = open("progress.txt", "w")
avancement.writelines(["1\n"])
avancement.close()

try:
	from Bio.Seq import Seq
	from Bio.Alphabet import IUPAC
	from Bio import SeqIO
	from Bio.SeqRecord import SeqRecord
except ImportError as e:
	progress('!Import error: %s'%e)
	exit(1)

# Transcribe in RNA
if 'T' in argv[1]:
	console("Transcription in RNA")
	progress('2')
	sequ = Seq( argv[1] , IUPAC.unambiguous_dna).transcribe()
else:
	sequ = Seq( argv[1] , IUPAC.unambiguous_dna)

# Save in FASTA format (aptamer.fa)
console("Saving in FASTA format")
progress('3')
rec1 = SeqRecord( seq=sequ , id="aptamer" , name='aptamer1', description='Sequence ADN')
try:
	SeqIO.write( rec1 , "aptamer.fa", "fasta")
except:
	e = exc_info()[0]
	progress("!FASTA saving error: %s" % e )
	exit(1)


#Searching for the secondary structure
if len(argv[4]) != len(sequ):
	console("Searching for the secondary structure")
	progress('4')
	a += system("RNAfold < aptamer.fa -o dotbracket")
	if a:
		progress('!RNAfold error')
		exit(1)
	try:
		fichier = open("dotbracket_aptamer.fold", "r")
		data = fichier.readlines()
		fichier.close()
		primaire = data[0][:-1]
		secondaire = data[1][0:len(primaire)]
		fichier = open("aptamer.dtb", "w")
		fichier.writelines([secondaire+'\n'])
		fichier.close()
		a += system("rm dotbracket_aptamer.fold")
	except IOError:
		progress('!No dotbracket_aptemer.fold file created')
		exit(1)
else:
	try:
		fichier = open("aptamer.dtb", "w")
		fichier.writelines([argv[4]+'\n'])
		fichier.close()
	except IOError:
		progress('!No aptamer.dtb file written')
		exit(1)


# Finding known helix in sequence
console("Identifying helixes")
progress('5')
print "%s/aptamer.dtb %s/aptamer.fa"%(path, path)
a += system(exportcmd+"python $RNA_TOOLS/job_setup/helix_preassemble_setup.py -secstruct %s/aptamer.dtb -fasta %s/aptamer.fa"%(path, path))
if a:
	progress('!No CMDLINES file created')
	exit(1)
a += system("chmod +x %s/CMDLINES"%path)

fichier = open("CMDLINES", "r")
data = fichier.readlines()
option = data[-1][2:-1]
N = -1
for word in option.split():
	if "helix" in word: N+=1
fichier.close()

# preprocessing ==> Predict the helixN.out 
console("Preprocessing helixes")
progress('6')
a += system(exportcmd+"/bin/bash %s/CMDLINES"%path)
if a:
	progress('!Unable to run CMDLINES')
	exit(1)

# computation
console("Computation (this may take a while)")
progress('7')
a += system(exportcmd+"$ROSETTA3/bin/rna_denovo.linuxgccrelease -fasta %s/aptamer.fa -secstruct_file %s/aptamer.dtb -fixed_stems -tag aptamer -working_res 1-%d -cycles %d -ignore_zero_occupancy false -include_neighbor_base_stacks  -minimize_rna false"%(path, path, len(primaire), ncycles)+option)
if a:
	progress('!Computation failed')
	exit(1)

exit(0)

#minimization
console("Minimization")
progress('8')

a += system(exportcmd+"$RNA_TOOLS/job_setup/parallel_min_setup.py -silent %s/aptamer.out -tag aptamer_min -nstruct 100 -out_folder %s/min -out_script %s/min_cmdline ''"%(path, path, path))
if a:
	progress('!No minimization command-lines created')
	exit(1)
a += system("/bin/bash %s/min_cmdline"%path)
if a:
	progress('!Unable to run minimization')
	exit(1)

#Selection of the 5 best
console("Selection of the 5 best")
progress('9')

a += system(exportcmd+"$RNA_TOOLS/silent_util/silent_file_sort_and_select.py %s/min/0/aptamer_min.out -select 1-5 -o %s/aptamer_best.out"%(path, path))
if a:
	progress('!Unable to select the best files')
	exit(1)

#Conversion to PDB
console("Conversion to PDB")
progress('10')

a += system(exportcmd+"$RNA_TOOLS/silent_util/extract_lowscore_decoys.py %s/aptamer_best.out 5"%path)
if a:
	progress('!Cannot convert .out to .pdb')
	exit(1)

#Conversion to DNA
if int(argv[3]):
	console("Conversion to DNA")
	progress('11')
	
	try:
		for k in xrange(1,6):
			fichier = open( "aptamer_best.out.%d.pdb"%k , "r" )
			atomes = fichier.readlines()
			fichier.close()
			output = []
			for atome in atomes:
				if not("O2'" in atome):
					if (atome[-5]=='H' or atome[-4]=='H') and ("U" in atome) and ("H5 " in atome):
						line = atome.split('   ')
						line[1] = line[1][:-2] + 'C7'
						line[-1] = '  C \n'
						atome = '   '.join(line)
					if "U" in atome:
						atome = atome[:19]+'T'+atome[20:]	
				output.append(atome)
			fichier = open( "pre-DNA_aptamer_best.out.%d.pdb"%k, "w" )
			fichier.writelines(output)
			fichier.close()
			a += system("rm aptamer_best.out.%d.pdb"%k)
			if a:
				progress('!%dth minimisation failed'%k)
				exit(1)
	except:
		progress('!DNA conversion failed')
		exit(1)
	
	console("Re-minimize")
	a += system(exportcmd+"$ROSETTA3/bin/score.linuxgccrelease -in:file:s %s/pre-DNA_aptamer_best.out.*.pdb -no_optH false -output"%path)
	if a:
		progress('!Cannot minimize the converted to DNA file')
		exit(1)
	a += system("rm %s/default.sc"%path)
	
	for k in xrange(1,6):
		a += system("rm %s/pre-DNA_aptamer_best.out.%d.pdb"%(path,k))

console("Completed.")
progress('ok')


