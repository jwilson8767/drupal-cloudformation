#!/usr/bin/env bash
#Builds and deploys lambda function bundles. Requires Kappa already be installed.
if ! type "kappa" > /dev/null; then
  echo "Kappa not install. Exiting."
  exit 1
fi

pushd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
    pushd customresources
        for i in */; do
            echo building $i
            pushd $i
                ./build.sh
                kappa deploy
            popd
        done;
    popd
popd
