#!/bin/bash
#
#### job name
#PBS -N TriD_analysis
#
#### select resources
#PBS -l walltime=72:02:00
#PBS -l nodes=1:ppn=10
##PBS -l mem=128gb
#PBS -M m.gonzalezrivero@aims.gov.au
#PBS -m abe
#
#### redirect error & output files
#PBS -e /export/home/l-p/mgonzale/matlab_logs/errorlog
#
#### load matlab module (setup environment)
module load MATLAB/R2018a
#### change to current working directory
cd /export/home/l-p/mgonzale/Desktop/gits/reef3D/data_analyses
#### execute program

matlab -nodisplay -nodesktop -nosplash -r "summary_transect '/net/138.7.48.21/3d_ltmp/exports/pointsXYZ/OK/' '/net/138.7.48.21/3d_ltmp/exports/cameras/OK/' '/export/home/l-p/mgonzale/Desktop/gits/reef3D/' '/net/138.7.48.21/3d_ltmp/exports/'"

