#!/bin/bash
for i in $(seq 10 10 840); do
    text=$(printf %03d $i)
    base="base"
    if (($i < 70)); then
        base="uturn"
    elif ((($i < 430) && ($i % 20 == 10))); then
        base="rotleft"
    elif ((i < 430)); then
        base="rotright"
    elif ((i < 540)); then
        base="backup"
    elif ((i < 670)); then
        base="move1"
    elif ((i < 790)); then
        base="move2"
    elif ((i < 850)); then
        base="move3"
    fi
    convert -pointsize 15 -fill yellow -draw "text 51,23 \"$text\"" $base.png $i.png
done
