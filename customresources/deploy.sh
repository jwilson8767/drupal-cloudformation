#!/usr/bin/env bash
#Builds and deploys lambda function bundles. Requires Kappa already be installed.

for i in */; do
echo building $i
pushd $i
./build.sh
kappa deploy
popd
done;


