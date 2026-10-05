#!/usr/bin/env bash
# Download the 5 SuiteSparse SPD matrices and build the RCM-reordered .rcm.csr files used by all sweeps.
#   ./get_matrices.sh        (~430 MB download; needs src/ built: cd src && make)
set -euo pipefail
cd "$(dirname "$0")"
[[ -x src/rcm ]] || (cd src && make)
mkdir -p matrices
for m in McRae/ecology2 GHS_psdef/apache2 Schmid/thermal2 AMD/G3_circuit Williams/cant; do
    name=$(basename "$m")
    if [[ ! -f matrices/$name/$name.mtx ]]; then
        echo "downloading $name"
        curl -fSL "https://suitesparse-collection-website.herokuapp.com/MM/$m.tar.gz" -o "matrices/$name.tar.gz" \
          || curl -fSL "https://sparse.tamu.edu/MM/$m.tar.gz" -o "matrices/$name.tar.gz"
        tar xzf "matrices/$name.tar.gz" -C matrices && rm "matrices/$name.tar.gz"
    fi
    [[ -f matrices/$name/$name.rcm.csr ]] || src/rcm "matrices/$name/$name.mtx" "matrices/$name/$name.rcm.csr"
done
echo "done: matrices/*/*.rcm.csr"
