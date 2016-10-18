APTAMER 3D STRUCTURE COMPUTATION TOOL
=====================================

WHAT TO FO FOR ?
----------------

- Want to see what the aptamer you designed looks like ?
- Want to prepare a PDB structure for docking with your target/biomarker ?
- Want to see how a polymorphism in the chain influences interaction with the target ?

Then use our tool.

We found a simple method to compute the structure of aptamers, copying the protocol to compute RNA 3D-foldings with Rosetta. The trick is to convert the aptamer to RNA, then compute its structure, re-convert to DNA and minimize the free energy to adjust atom coordinates.
See how.pdf to have more info.
This is not made to give precise energy computation results. This gives you the most probable 3D structures in PDB file format.



RECOMMENDED HARDWARE
--------------------

You may have a better experience of modelling on a computer with a strong CPU.
I recommend using a multi-core processor (8 threads seems good), and at least 8 GB of RAM.



INSTALL
-------
1) First, download the source of Rosetta 3.7 at https://www.rosettacommons.org/software/license-and-download .
   The version number matters.
   
2) Put your downloaded archive rosetta_src_3.7_bundle.tgz in the same folder than INSTALL and the other files. Please chose a safe place: you need at least 10 GB of storage.

3) Edit the file 3daptamers.py : at line 22, you need to modifiy the path to the directory.
   For example, i put my rosetta_src_3.7_bundle.tgz in /home/lbecquey/Aptamers
   
4) Optional: Edit the file INSTALL : at line 22 again, replace -j2 by -jX where X is the number
of processors you have on your machine. This step is only to compile Rosetta, it will not affect your computations.

5) Open a terminal, and execute install.sh with admin rights:
   sudo ./INSTALL
   
   The installation and compilation may take several hours.
   
6) You can delete the files rosetta_src_3.7_bundle.tgz, install.py and INSTALL




HOW TO USE
----------

Open a terminal in the folder and type the following command:

   ./3daptamers.py APTAMERSEQ JOBNUM RETURNDNA? SECSTRUCT NCYCLES
   
where the arguments are the following:

APTAMERSEQ
The primary sequence of the DNA or RNA you want to model. For example, AAAAGTGTGCGA.

JOBNUM
A number to identify you job. A folder will be created with this number and contain the files.
If you run several computations at one time, use different numbers to have different separated folders.

RETURNDNA?
Put 1 if you use a DNA sequence, 0 if you use a RNA.


SECSTRUCT
If you know the secondary structure of your sequence, you can force the software to use it.
This is highly recommended if your aptamer contains pseudoknots or G-quadruplexes, because we are
unable to predict them.
Give the structure in dot-bracket format: "..((((((((((.......)))))))))).....(( ......))...."

NCYCLES
The number of cycles to run. The recommended value is 20000, especially if your sequence is long.
But as it is very long, you can reduce the numbers of cycles, down to 5000 if you want to earn some time.

At the end of the computation, you get some PDB files in the folder with the JOBNUM you entered.



ATTRIBUTIONS
------------

- ViennnaRNA is a free software developped by the University of Vienna (see https://github.com/ViennaRNA/ViennaRNA/blob/master/COPYING )
- Rosetta is a structural bioinformatics suite that you can modify, but only for non commercial purposes (see https://els.comotion.uw.edu/licenses/86 )
- this script is freely distributed under the MIT licence: https://opensource.org/licenses/MIT

It has been developped by Louis Becquey, Julien Orlans and Etienne Fachaux for the 2016 iGEM Contest, as a part of the Team INSA-Lyon's project.