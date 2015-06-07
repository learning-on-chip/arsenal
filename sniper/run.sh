#!/bin/bash

set -e

if [ -z "${SNIPER_ROOT}" ]; then
  echo 'Please set SNIPER_ROOT'
  exit 1
fi

if [ -z "${BENCHMARKS_ROOT}" ]; then
  echo 'Please set BENCHMARKS_ROOT'
  exit 1
fi

if [ -z "${BULLET_ROOT}" ]; then
  echo 'Please set BULLET_ROOT'
  exit 1
fi

root=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
sniper=${BENCHMARKS_ROOT}/run-sniper
benchmark=${BENCHMARK:=blackscholes}
output=${OUTPUT:=${PWD}/${benchmark}}

options=
options+=" -p parsec-${benchmark}"
options+=" -i small"
options+=" -n 16"
options+=" -c gainestown"
options+=" -c --general/total_cores=1"
options+=" -c --general/output_dir=${output}"
options+=" -s ${root}/scripts/bullet.py"

if [ ! -d ${output} ]; then
  mkdir -p ${output}
fi

redis-server ${root}/configs/redis.conf
redis-cli DEL bullet-queue > /dev/null

export TOOLS_ROOT="${root}/tools"

echo "Running ${benchmark}..."
${sniper} ${options}
