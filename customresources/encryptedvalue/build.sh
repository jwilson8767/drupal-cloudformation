pushd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
rm -rf _build
pip install -r _src/requirements.txt -t _build/
cp _src/* _build/
popd
