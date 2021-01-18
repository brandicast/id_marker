#!/bin/bash
MY_PATH=$PWD
echo $MY_PATH
tmp_dir=$(mktemp -d -t brandicast-XXXXXXXXXX)
mkdir -p  $tmp_dir/usr/bin
mkdir $tmp_dir/DEBIAN
cp control $tmp_dir/DEBIAN/
cp ./dist/id_marker $tmp_dir/usr/bin/
cd $tmp_dir
cd ..
dpkg -b $tmp_dir
rm -rf $tmp_dir
mv "$tmp_dir.deb" $MY_PATH/id_marker.deb





