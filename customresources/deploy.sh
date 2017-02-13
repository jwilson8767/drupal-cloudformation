#!/usr/bin/env bash
#Builds and deploys lambda function bundles. Requires Kappa already be installed.
pushd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
for i in */; do
echo building $i
pushd $i
./build.sh
kappa deploy
popd
done;
popd

