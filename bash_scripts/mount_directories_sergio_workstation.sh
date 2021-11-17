#!/bin/bash


#TODO: create script for un-mounting
mount_dir="/home/alberto/mounted_directories"

mount_directory () {
  # 1: name of mounting directory
  # 2: path to mount on login node
  # 3: directory where to create the link on sergio machine
  #Mount scratch directory, creating a new directory
  for i in {1..1000}
  do
    candidate_dir="$mount_dir/$1_$i"
     if [ ! -d "$candidate_dir" ]; then
        mkdir -p "$candidate_dir"
        sshfs bailoni@login.cluster.embl.de:"$2" "$candidate_dir/"
        #Create link, remove previous one if existing:
        if [ -L "$3" ]; then
            rm "$3"
        fi
        echo ln -sf "$candidate_dir/" "$3"
        ln -sf "$candidate_dir/" "$3"
        break
     fi
  done
}

mount_directory scratch /scratch/bailoni /scratch/bailoni
#mount_directory g_shared /scratch/bailoni /scratch/bailoni
mount_directory conda /scratch/bailoni/miniconda3 /home/alberto/miniconda3
