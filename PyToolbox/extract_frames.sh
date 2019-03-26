#!/usr/bin/env bash


cd $1

for fname in *; do
    for vname in $fname/*.MP4; do
        if [ -d "$fname" ]; then
            vname=${vname##*/}
            ffmpeg -i "$vname" -qscale:v 2 -ss 6 -movflags use_metadata_tags -vf "fps=4" "${vname:0:2}"_"$fname"_V"${vname:9:2}"_%04d.jpg
        fi
    done
done 


