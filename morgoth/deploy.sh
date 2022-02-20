#!/usr/bin/env bash
set -euo pipefail


check_if_kind_exist(){
    # echo "checking kind exist or not"
    result=$(kind version) || echo 'Kind can not be in the system path'
}

check_cluster_exist(){
if [ "$(kind get clusters)" == "kind" ]
then
    echo>&2 "Kubernetes cluster exist bypassing cluster creation"
    isClusterExist="true"
else
    echo>&2 "creating cluster"
    isClusterExist="false"

fi
echo $isClusterExist
}

launch_kind_cluster(){
    pushd local_cluster
    ./launch_cluster.sh
    popd
}


main(){
check_if_kind_exist
source ./deployment_variables.sh
isClusterExist=$(check_cluster_exist)
if [[ "${isClusterExist}" == "false" ]]; then
    launch_kind_cluster
fi

}

main