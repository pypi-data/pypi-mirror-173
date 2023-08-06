#!/bin/bash
# Copyright (c) 2022 Huawei Technologies Co., Ltd.
#
# This software is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#
# http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

USAGE="Usage: deploy-datasystem.sh [-a ACTION] [-c COMPONENT] [-d DATASYSTEM_HOME] [-p CONFIG_PATH] [-h]

Where 'ACTION' is one of:
    pass       \tPass packages to the hosts.
    pass_conf  \tUpdate configures to hosts.
    start      \tStart the datasystem component(s), default ACTION.
    stop       \tStop the datasystem component(s).

Where 'COMPONENT' is one of:
    all        \tStart/Stop all masters, workers and gcs nodes, default COMPONENT.
    master     \tStart/Stop masters on master nodes.
    worker     \tStart/Stop workers on worker nodes.
    gcs        \tStart/Stop gcs on gcs nodes.
    agent      \tStart/Stop agent on agent nodes.
    clusterfs  \tStart/Stop fuse mount dir on clusterfs nodes.

-a    Action for datasystem components.
-c    Specify datasystem component.
-d    Datasystem home, default is $(realpath "../").
-n    Component number.
-p    Specify the config directory.
-w    Number of seconds to wait for result, default is 2s.
-h    Show usage for help."

readonly BASE_DIR=$(dirname "$(readlink -f "$0")")
readonly DEFAULT_CONF_DIR="${BASE_DIR}/../conf"
readonly DEPLOY_LOG="${BASE_DIR}/deploy.log"

ACTION="start"
COMPONENT="all"
DATASYSTEM_HOME="$(realpath "${BASE_DIR}/..")"
BIN_DIR="$(realpath "${BASE_DIR}/..")"
CONF_DIR=$(realpath "${BASE_DIR}/conf")
ALL_IP_LIST=()
COMPONENT_NUM=""
HANDLE_CLUSTERFS="No"
LAUNCHER=("bash")

function get_env()
{
  if [[ -f "${CONF_DIR}/master-env.sh" ]]; then . "${CONF_DIR}/master-env.sh"; fi
  if [[ -f "${CONF_DIR}/worker-env.sh" ]]; then . "${CONF_DIR}/worker-env.sh"; fi
  if [[ -f "${CONF_DIR}/gcs-env.sh" ]]; then . "${CONF_DIR}/gcs-env.sh"; fi
  if [[ -f "${CONF_DIR}/agent-env.sh" ]]; then . "${CONF_DIR}/agent-env.sh"; fi

  # get all ip addresses and remove deduplicate ip address
  local all_addresses
  all_addresses=("${MASTER_ADDRESS[@]}" "${WORKER_ADDRESS[@]}" "${GCS_ADDRESS[@]}" "${AGENT_ADDRESS[@]}")
  for((i=0;i<"${#all_addresses[@]}";i++))
  do
    ALL_IP_LIST+=("$(echo "${all_addresses[i]}" | cut -d : -f 1)")
  done
  ALL_IP_LIST=($(awk -v RS=' ' '!a[$1]++' <<< "${ALL_IP_LIST[@]}"))
}

function pass_package_remote()
{
  local ip="$1"
  local pkg="$2"
  local dst_dir="$3"

  ssh -o NumberOfPasswordPrompts=0 -o ConnectTimeout=5 -o StrictHostKeyChecking=no -tt "${ip}" \
    "mkdir -p ${dst_dir}" 2>&1 | while read -r line; do echo "[$(date '+%F %T')][${ip}] ${line}"; done >> "${DEPLOY_LOG}"
  if [ $? -ne 0 ]; then
    return 1
  fi

  scp -o NumberOfPasswordPrompts=0 -o ConnectTimeout=5 -o StrictHostKeyChecking=no -r "${pkg}"/* "${ip}":"${dst_dir}" 2>&1 |
    while read -r line; do echo "[$(date '+%F %T')][${ip}] ${line}"; done >> "${DEPLOY_LOG}"
  if [[ $? -ne 0 ]]; then
    return 1
  fi
  return 0
}

function pass_package_local()
{
  local ip="$1"
  local pkg="$2"
  local dst_dir="$3"

  if [[ "${pkg}" == "${dst_dir}" ]]; then
    return 0
  fi

  if [[ ! -d "${dst_dir}" ]]; then
    mkdir -p "${dst_dir}" 2>&1 | while read -r line; do echo "[$(date '+%F %T')][${ip}] ${line}"; done >> "${DEPLOY_LOG}"
    if [[ $? -ne 0 ]]; then
      return 1
    fi
  fi

  cp -r "${pkg}"/* "${dst_dir}" 2>&1 | while read -r line; do echo "[$(date '+%F %T')][${ip}] ${line}"; done >> "${DEPLOY_LOG}"
  if [[ $? -ne 0 ]]; then
    return 1
  fi
  return 0
}

function pass_packages()
{
  # if conf dir is not default dir, pass it as well.
  local deafult_path
  if [[ -d "${BASE_DIR}/../conf" ]]; then
    deafult_path=$(realpath "${BASE_DIR}")
  fi
  local dst_path
  if [[ -d "${CONF_DIR}" ]]; then
    dst_path=$(realpath "${CONF_DIR}")
  fi
  if [[ "x${deafult_path}" != "x${dst_path}" ]]; then
    pass_conf
  fi
  echo -e "-- ${CYAN}Starting${NC} to pass the datasystem packages"
  local real_path
  for ip in "${ALL_IP_LIST[@]}"
  do
    real_path=$(realpath "${BASE_DIR}/..")
    if is_local_ip "${ip}"; then
      pass_package_local "${ip}" "${real_path}" "${DATASYSTEM_HOME}"
    else
      pass_package_remote "${ip}" "${real_path}" "${DATASYSTEM_HOME}"
    fi

    if [[ $? -eq 0 ]]; then
      print_ok_msg "pass package" "server" "${ip}"
    else
      print_fail_msg "pass package" "server" "${ip}"
      echo -e "${CYAN}---- $(tail -1 "${DEPLOY_LOG}")${NC}"
    fi
  done
  echo -e "-- Pass the datasystem packages ${GREEN}Complete${NC}!\n"
}

function pass_conf()
{
  echo -e "-- ${CYAN}Starting${NC} to pass the datasystem configure items"
  local real_path
  for ip in "${ALL_IP_LIST[@]}"
  do
    real_path=$(realpath "${CONF_DIR}")
    if is_local_ip "${ip}"; then
      pass_package_local "${ip}" "${real_path}" "${DEFAULT_CONF_DIR}"
    else
      pass_package_remote "${ip}" "${real_path}" "${DEFAULT_CONF_DIR}"
    fi

    if [[ $? -eq 0 ]]; then
      print_ok_msg "pass configure items" "server" "${ip}"
    else
      print_fail_msg "pass configure items" "server" "${ip}"
      echo -e "${CYAN}---- $(tail -1 "${DEPLOY_LOG}")${NC}"
    fi
  done
  echo -e "-- Pass the datasystem configure items ${GREEN}Complete${NC}!\n"
}

# start one master/worker/gcs generate place.

function start_one_worker
{
  local argv_list
  is_array "WORKER_ADDRESS" && worker_address="${WORKER_ADDRESS[$COMPONENT_NUM]}" || worker_address="${WORKER_ADDRESS}"
  [[ -n "${worker_address}" ]] && argv_list+=("-worker_address" "${worker_address}")
  is_array "WORKER_MASTER_ADDRESS" && master_address="${WORKER_MASTER_ADDRESS[$COMPONENT_NUM]}" || master_address="${WORKER_MASTER_ADDRESS}"
  [[ -n "${master_address}" ]] && argv_list+=("-master_address" "${master_address}")
  is_array "WORKER_SHARED_MEMORY_SIZE_MB" && shared_memory_size_mb="${WORKER_SHARED_MEMORY_SIZE_MB[$COMPONENT_NUM]}" || shared_memory_size_mb="${WORKER_SHARED_MEMORY_SIZE_MB}"
  [[ -n "${shared_memory_size_mb}" ]] && argv_list+=("-shared_memory_size_mb" "${shared_memory_size_mb}")
  is_array "WORKER_HEARTBEAT_INTERVAL_MS" && heartbeat_interval_ms="${WORKER_HEARTBEAT_INTERVAL_MS[$COMPONENT_NUM]}" || heartbeat_interval_ms="${WORKER_HEARTBEAT_INTERVAL_MS}"
  [[ -n "${heartbeat_interval_ms}" ]] && argv_list+=("-heartbeat_interval_ms" "${heartbeat_interval_ms}")
  is_array "WORKER_AUTHORIZATION_ENABLE" && authorization_enable="${WORKER_AUTHORIZATION_ENABLE[$COMPONENT_NUM]}" || authorization_enable="${WORKER_AUTHORIZATION_ENABLE}"
  [[ -n "${authorization_enable}" ]] && argv_list+=("-authorization_enable" "${authorization_enable}")
  is_array "WORKER_ENABLE_UDS" && enable_uds="${WORKER_ENABLE_UDS[$COMPONENT_NUM]}" || enable_uds="${WORKER_ENABLE_UDS}"
  [[ -n "${enable_uds}" ]] && argv_list+=("-enable_uds" "${enable_uds}")
  is_array "WORKER_SC_REGULAR_SOCKET_NUM" && worker_sc_regular_socket_num="${WORKER_SC_REGULAR_SOCKET_NUM[$COMPONENT_NUM]}" || worker_sc_regular_socket_num="${WORKER_SC_REGULAR_SOCKET_NUM}"
  [[ -n "${worker_sc_regular_socket_num}" ]] && argv_list+=("-worker_sc_regular_socket_num" "${worker_sc_regular_socket_num}")
  is_array "WORKER_SC_STREAM_SOCKET_NUM" && worker_sc_stream_socket_num="${WORKER_SC_STREAM_SOCKET_NUM[$COMPONENT_NUM]}" || worker_sc_stream_socket_num="${WORKER_SC_STREAM_SOCKET_NUM}"
  [[ -n "${worker_sc_stream_socket_num}" ]] && argv_list+=("-worker_sc_stream_socket_num" "${worker_sc_stream_socket_num}")
  is_array "WORKER_PAGE_SIZE" && page_size="${WORKER_PAGE_SIZE[$COMPONENT_NUM]}" || page_size="${WORKER_PAGE_SIZE}"
  [[ -n "${page_size}" ]] && argv_list+=("-page_size" "${page_size}")
  is_array "WORKER_MAX_STREAM_SIZE_MB" && max_stream_size_mb="${WORKER_MAX_STREAM_SIZE_MB[$COMPONENT_NUM]}" || max_stream_size_mb="${WORKER_MAX_STREAM_SIZE_MB}"
  [[ -n "${max_stream_size_mb}" ]] && argv_list+=("-max_stream_size_mb" "${max_stream_size_mb}")
  is_array "WORKER_REMOTE_SEND_THREAD_NUM" && remote_send_thread_num="${WORKER_REMOTE_SEND_THREAD_NUM[$COMPONENT_NUM]}" || remote_send_thread_num="${WORKER_REMOTE_SEND_THREAD_NUM}"
  [[ -n "${remote_send_thread_num}" ]] && argv_list+=("-remote_send_thread_num" "${remote_send_thread_num}")
  is_array "WORKER_SCAN_REMOTE_SEND_INTERVALS_US" && scan_remote_send_intervals_us="${WORKER_SCAN_REMOTE_SEND_INTERVALS_US[$COMPONENT_NUM]}" || scan_remote_send_intervals_us="${WORKER_SCAN_REMOTE_SEND_INTERVALS_US}"
  [[ -n "${scan_remote_send_intervals_us}" ]] && argv_list+=("-scan_remote_send_intervals_us" "${scan_remote_send_intervals_us}")
  is_array "WORKER_REDIS_ADDRESS" && redis_address="${WORKER_REDIS_ADDRESS[$COMPONENT_NUM]}" || redis_address="${WORKER_REDIS_ADDRESS}"
  [[ -n "${redis_address}" ]] && argv_list+=("-redis_address" "${redis_address}")
  is_array "WORKER_SPILL_DIRECTORIES" && spill_directories="${WORKER_SPILL_DIRECTORIES[$COMPONENT_NUM]}" || spill_directories="${WORKER_SPILL_DIRECTORIES}"
  [[ -n "${spill_directories}" ]] && argv_list+=("-spill_directories" "${spill_directories}")
  is_array "WORKER_SPILL_SIZE_LIMIT" && spill_size_limit="${WORKER_SPILL_SIZE_LIMIT[$COMPONENT_NUM]}" || spill_size_limit="${WORKER_SPILL_SIZE_LIMIT}"
  [[ -n "${spill_size_limit}" ]] && argv_list+=("-spill_size_limit" "${spill_size_limit}")
  is_array "WORKER_REDIS_USERNAME" && redis_username="${WORKER_REDIS_USERNAME[$COMPONENT_NUM]}" || redis_username="${WORKER_REDIS_USERNAME}"
  [[ -n "${redis_username}" ]] && argv_list+=("-redis_username" "${redis_username}")
  is_array "WORKER_REDIS_PASSWD" && redis_passwd="${WORKER_REDIS_PASSWD[$COMPONENT_NUM]}" || redis_passwd="${WORKER_REDIS_PASSWD}"
  [[ -n "${redis_passwd}" ]] && argv_list+=("-redis_passwd" "${redis_passwd}")
  is_array "WORKER_RPC_THREAD_NUM" && rpc_thread_num="${WORKER_RPC_THREAD_NUM[$COMPONENT_NUM]}" || rpc_thread_num="${WORKER_RPC_THREAD_NUM}"
  [[ -n "${rpc_thread_num}" ]] && argv_list+=("-rpc_thread_num" "${rpc_thread_num}")
  is_array "WORKER_UNIX_DOMAIN_SOCKET_DIR" && unix_domain_socket_dir="${WORKER_UNIX_DOMAIN_SOCKET_DIR[$COMPONENT_NUM]}" || unix_domain_socket_dir="${WORKER_UNIX_DOMAIN_SOCKET_DIR}"
  [[ -n "${unix_domain_socket_dir}" ]] && argv_list+=("-unix_domain_socket_dir" "${unix_domain_socket_dir}")
  is_array "WORKER_LOG_DIR" && log_dir="${WORKER_LOG_DIR[$COMPONENT_NUM]}" || log_dir="${WORKER_LOG_DIR}"
  [[ -n "${log_dir}" ]] && argv_list+=("-log_dir" "${log_dir}")
  is_array "WORKER_MAX_LOG_SIZE" && max_log_size="${WORKER_MAX_LOG_SIZE[$COMPONENT_NUM]}" || max_log_size="${WORKER_MAX_LOG_SIZE}"
  [[ -n "${max_log_size}" ]] && argv_list+=("-max_log_size" "${max_log_size}")
  is_array "WORKER_TOTAL_LOG_SIZE_MB" && total_log_size_mb="${WORKER_TOTAL_LOG_SIZE_MB[$COMPONENT_NUM]}" || total_log_size_mb="${WORKER_TOTAL_LOG_SIZE_MB}"
  [[ -n "${total_log_size_mb}" ]] && argv_list+=("-total_log_size_mb" "${total_log_size_mb}")
  is_array "WORKER_LOG_ASYNC" && log_async="${WORKER_LOG_ASYNC[$COMPONENT_NUM]}" || log_async="${WORKER_LOG_ASYNC}"
  [[ -n "${log_async}" ]] && argv_list+=("-log_async" "${log_async}")
  is_array "WORKER_LOG_COMPRESS" && log_compress="${WORKER_LOG_COMPRESS[$COMPONENT_NUM]}" || log_compress="${WORKER_LOG_COMPRESS}"
  [[ -n "${log_compress}" ]] && argv_list+=("-log_compress" "${log_compress}")
  is_array "WORKER_V" && v="${WORKER_V[$COMPONENT_NUM]}" || v="${WORKER_V}"
  [[ -n "${v}" ]] && argv_list+=("-v" "${v}")
  is_array "WORKER_ZMQ_ENABLE_AUTH" && zmq_enable_auth="${WORKER_ZMQ_ENABLE_AUTH[$COMPONENT_NUM]}" || zmq_enable_auth="${WORKER_ZMQ_ENABLE_AUTH}"
  [[ -n "${zmq_enable_auth}" ]] && argv_list+=("-zmq_enable_auth" "${zmq_enable_auth}")
  is_array "WORKER_CURVE_KEY_DIR" && curve_key_dir="${WORKER_CURVE_KEY_DIR[$COMPONENT_NUM]}" || curve_key_dir="${WORKER_CURVE_KEY_DIR}"
  [[ -n "${curve_key_dir}" ]] && argv_list+=("-curve_key_dir" "${curve_key_dir}")
  export LD_LIBRARY_PATH="${BIN_DIR}/lib:$LD_LIBRARY_PATH"
  (nohup "${BIN_DIR}/worker" "${argv_list[@]}" >${BASE_DIR}/worker.out 2>&1) &
  pid=$!
  sleep 5
  [[ -f /proc/$pid/cmdline ]] && cat /proc/$pid/cmdline || ret_code=1
  if [[ $ret_code -ne 0 ]]; then
    cat ${BASE_DIR}/worker.out
  fi
  return $ret_code
}

function stop_one_worker()
{
  is_array "WORKER_ADDRESS" && worker_address="${WORKER_ADDRESS[$COMPONENT_NUM]}" || worker_address="${WORKER_ADDRESS}"
  pid="$(ps ux | grep /worker | grep ${worker_address} | grep -v grep | awk '{print $2}')"
  if ! is_num "${pid}"; then
    echo -e "Cannot found the worker we want: ${worker_address}" >&2
    exit 1
  fi
  kill -15 "$pid"
  while [ -e /proc/$pid ]; do sleep 0.5; done
}

function deploy_one_worker()
{
  . "${CONF_DIR}/worker-env.sh"
  if [ x"${ACTION}" = "xstart" ]; then
    start_one_worker
  else
    stop_one_worker
  fi
}

function deploy_worker()
{
  if [ x"${ACTION}" = "xstart" ]; then
    "${LAUNCHER[@]}" "${BASE_DIR}/worker-launcher.sh" "${BASE_DIR}/deploy-datasystem.sh" "-a" "start" "-c" "worker" "-p" "${CONF_DIR}"
  else
    "${LAUNCHER[@]}" "${BASE_DIR}/worker-launcher.sh" "${BASE_DIR}/deploy-datasystem.sh" "-a" "stop" "-c" "worker" "-p" "${CONF_DIR}"
  fi
}


function start_one_master
{
  local argv_list
  is_array "MASTER_ADDRESS" && master_address="${MASTER_ADDRESS[$COMPONENT_NUM]}" || master_address="${MASTER_ADDRESS}"
  [[ -n "${master_address}" ]] && argv_list+=("-master_address" "${master_address}")
  is_array "MASTER_BACKEND_STORE_DIR" && backend_store_dir="${MASTER_BACKEND_STORE_DIR[$COMPONENT_NUM]}" || backend_store_dir="${MASTER_BACKEND_STORE_DIR}"
  [[ -n "${backend_store_dir}" ]] && argv_list+=("-backend_store_dir" "${backend_store_dir}")
  is_array "MASTER_REDIS_ADDRESS" && redis_address="${MASTER_REDIS_ADDRESS[$COMPONENT_NUM]}" || redis_address="${MASTER_REDIS_ADDRESS}"
  [[ -n "${redis_address}" ]] && argv_list+=("-redis_address" "${redis_address}")
  is_array "MASTER_NODE_TIMEOUT_S" && node_timeout_s="${MASTER_NODE_TIMEOUT_S[$COMPONENT_NUM]}" || node_timeout_s="${MASTER_NODE_TIMEOUT_S}"
  [[ -n "${node_timeout_s}" ]] && argv_list+=("-node_timeout_s" "${node_timeout_s}")
  is_array "MASTER_NODE_DEAD_TIMEOUT_S" && node_dead_timeout_s="${MASTER_NODE_DEAD_TIMEOUT_S[$COMPONENT_NUM]}" || node_dead_timeout_s="${MASTER_NODE_DEAD_TIMEOUT_S}"
  [[ -n "${node_dead_timeout_s}" ]] && argv_list+=("-node_dead_timeout_s" "${node_dead_timeout_s}")
  is_array "MASTER_CHECK_HEARTBEAT_INTERVAL_MS" && check_heartbeat_interval_ms="${MASTER_CHECK_HEARTBEAT_INTERVAL_MS[$COMPONENT_NUM]}" || check_heartbeat_interval_ms="${MASTER_CHECK_HEARTBEAT_INTERVAL_MS}"
  [[ -n "${check_heartbeat_interval_ms}" ]] && argv_list+=("-check_heartbeat_interval_ms" "${check_heartbeat_interval_ms}")
  is_array "MASTER_RPC_THREAD_NUM" && rpc_thread_num="${MASTER_RPC_THREAD_NUM[$COMPONENT_NUM]}" || rpc_thread_num="${MASTER_RPC_THREAD_NUM}"
  [[ -n "${rpc_thread_num}" ]] && argv_list+=("-rpc_thread_num" "${rpc_thread_num}")
  is_array "MASTER_UNIX_DOMAIN_SOCKET_DIR" && unix_domain_socket_dir="${MASTER_UNIX_DOMAIN_SOCKET_DIR[$COMPONENT_NUM]}" || unix_domain_socket_dir="${MASTER_UNIX_DOMAIN_SOCKET_DIR}"
  [[ -n "${unix_domain_socket_dir}" ]] && argv_list+=("-unix_domain_socket_dir" "${unix_domain_socket_dir}")
  is_array "MASTER_LOG_DIR" && log_dir="${MASTER_LOG_DIR[$COMPONENT_NUM]}" || log_dir="${MASTER_LOG_DIR}"
  [[ -n "${log_dir}" ]] && argv_list+=("-log_dir" "${log_dir}")
  is_array "MASTER_MAX_LOG_SIZE" && max_log_size="${MASTER_MAX_LOG_SIZE[$COMPONENT_NUM]}" || max_log_size="${MASTER_MAX_LOG_SIZE}"
  [[ -n "${max_log_size}" ]] && argv_list+=("-max_log_size" "${max_log_size}")
  is_array "MASTER_TOTAL_LOG_SIZE_MB" && total_log_size_mb="${MASTER_TOTAL_LOG_SIZE_MB[$COMPONENT_NUM]}" || total_log_size_mb="${MASTER_TOTAL_LOG_SIZE_MB}"
  [[ -n "${total_log_size_mb}" ]] && argv_list+=("-total_log_size_mb" "${total_log_size_mb}")
  is_array "MASTER_LOG_ASYNC" && log_async="${MASTER_LOG_ASYNC[$COMPONENT_NUM]}" || log_async="${MASTER_LOG_ASYNC}"
  [[ -n "${log_async}" ]] && argv_list+=("-log_async" "${log_async}")
  is_array "MASTER_LOG_COMPRESS" && log_compress="${MASTER_LOG_COMPRESS[$COMPONENT_NUM]}" || log_compress="${MASTER_LOG_COMPRESS}"
  [[ -n "${log_compress}" ]] && argv_list+=("-log_compress" "${log_compress}")
  is_array "MASTER_V" && v="${MASTER_V[$COMPONENT_NUM]}" || v="${MASTER_V}"
  [[ -n "${v}" ]] && argv_list+=("-v" "${v}")
  is_array "MASTER_ZMQ_ENABLE_AUTH" && zmq_enable_auth="${MASTER_ZMQ_ENABLE_AUTH[$COMPONENT_NUM]}" || zmq_enable_auth="${MASTER_ZMQ_ENABLE_AUTH}"
  [[ -n "${zmq_enable_auth}" ]] && argv_list+=("-zmq_enable_auth" "${zmq_enable_auth}")
  is_array "MASTER_CURVE_KEY_DIR" && curve_key_dir="${MASTER_CURVE_KEY_DIR[$COMPONENT_NUM]}" || curve_key_dir="${MASTER_CURVE_KEY_DIR}"
  [[ -n "${curve_key_dir}" ]] && argv_list+=("-curve_key_dir" "${curve_key_dir}")
  export LD_LIBRARY_PATH="${BIN_DIR}/lib:$LD_LIBRARY_PATH"
  (nohup "${BIN_DIR}/master" "${argv_list[@]}" >${BASE_DIR}/master.out 2>&1) &
  pid=$!
  sleep 5
  [[ -f /proc/$pid/cmdline ]] && cat /proc/$pid/cmdline || ret_code=1
  if [[ $ret_code -ne 0 ]]; then
    cat ${BASE_DIR}/master.out
  fi
  return $ret_code
}

function stop_one_master()
{
  is_array "MASTER_ADDRESS" && master_address="${MASTER_ADDRESS[$COMPONENT_NUM]}" || master_address="${MASTER_ADDRESS}"
  pid="$(ps ux | grep /master | grep ${master_address} | grep -v grep | awk '{print $2}')"
  if ! is_num "${pid}"; then
    echo -e "Cannot found the master we want: ${master_address}" >&2
    exit 1
  fi
  kill -15 "$pid"
  while [ -e /proc/$pid ]; do sleep 0.5; done
}

function deploy_one_master()
{
  . "${CONF_DIR}/master-env.sh"
  if [ x"${ACTION}" = "xstart" ]; then
    start_one_master
  else
    stop_one_master
  fi
}

function deploy_master()
{
  if [ x"${ACTION}" = "xstart" ]; then
    "${LAUNCHER[@]}" "${BASE_DIR}/master-launcher.sh" "${BASE_DIR}/deploy-datasystem.sh" "-a" "start" "-c" "master" "-p" "${CONF_DIR}"
  else
    "${LAUNCHER[@]}" "${BASE_DIR}/master-launcher.sh" "${BASE_DIR}/deploy-datasystem.sh" "-a" "stop" "-c" "master" "-p" "${CONF_DIR}"
  fi
}


function start_one_agent
{
  local argv_list
  is_array "AGENT_WORKER_ADDRESS" && worker_address="${AGENT_WORKER_ADDRESS[$COMPONENT_NUM]}" || worker_address="${AGENT_WORKER_ADDRESS}"
  [[ -n "${worker_address}" ]] && argv_list+=("-worker_address" "${worker_address}")
  is_array "AGENT_ADDRESS" && agent_address="${AGENT_ADDRESS[$COMPONENT_NUM]}" || agent_address="${AGENT_ADDRESS}"
  [[ -n "${agent_address}" ]] && argv_list+=("-agent_address" "${agent_address}")
  is_array "AGENT_RPC_THREAD_NUM" && rpc_thread_num="${AGENT_RPC_THREAD_NUM[$COMPONENT_NUM]}" || rpc_thread_num="${AGENT_RPC_THREAD_NUM}"
  [[ -n "${rpc_thread_num}" ]] && argv_list+=("-rpc_thread_num" "${rpc_thread_num}")
  is_array "AGENT_UNIX_DOMAIN_SOCKET_DIR" && unix_domain_socket_dir="${AGENT_UNIX_DOMAIN_SOCKET_DIR[$COMPONENT_NUM]}" || unix_domain_socket_dir="${AGENT_UNIX_DOMAIN_SOCKET_DIR}"
  [[ -n "${unix_domain_socket_dir}" ]] && argv_list+=("-unix_domain_socket_dir" "${unix_domain_socket_dir}")
  is_array "AGENT_LOG_DIR" && log_dir="${AGENT_LOG_DIR[$COMPONENT_NUM]}" || log_dir="${AGENT_LOG_DIR}"
  [[ -n "${log_dir}" ]] && argv_list+=("-log_dir" "${log_dir}")
  is_array "AGENT_MAX_LOG_SIZE" && max_log_size="${AGENT_MAX_LOG_SIZE[$COMPONENT_NUM]}" || max_log_size="${AGENT_MAX_LOG_SIZE}"
  [[ -n "${max_log_size}" ]] && argv_list+=("-max_log_size" "${max_log_size}")
  is_array "AGENT_TOTAL_LOG_SIZE_MB" && total_log_size_mb="${AGENT_TOTAL_LOG_SIZE_MB[$COMPONENT_NUM]}" || total_log_size_mb="${AGENT_TOTAL_LOG_SIZE_MB}"
  [[ -n "${total_log_size_mb}" ]] && argv_list+=("-total_log_size_mb" "${total_log_size_mb}")
  is_array "AGENT_LOG_ASYNC" && log_async="${AGENT_LOG_ASYNC[$COMPONENT_NUM]}" || log_async="${AGENT_LOG_ASYNC}"
  [[ -n "${log_async}" ]] && argv_list+=("-log_async" "${log_async}")
  is_array "AGENT_LOG_COMPRESS" && log_compress="${AGENT_LOG_COMPRESS[$COMPONENT_NUM]}" || log_compress="${AGENT_LOG_COMPRESS}"
  [[ -n "${log_compress}" ]] && argv_list+=("-log_compress" "${log_compress}")
  is_array "AGENT_V" && v="${AGENT_V[$COMPONENT_NUM]}" || v="${AGENT_V}"
  [[ -n "${v}" ]] && argv_list+=("-v" "${v}")
  is_array "AGENT_ZMQ_ENABLE_AUTH" && zmq_enable_auth="${AGENT_ZMQ_ENABLE_AUTH[$COMPONENT_NUM]}" || zmq_enable_auth="${AGENT_ZMQ_ENABLE_AUTH}"
  [[ -n "${zmq_enable_auth}" ]] && argv_list+=("-zmq_enable_auth" "${zmq_enable_auth}")
  is_array "AGENT_CURVE_KEY_DIR" && curve_key_dir="${AGENT_CURVE_KEY_DIR[$COMPONENT_NUM]}" || curve_key_dir="${AGENT_CURVE_KEY_DIR}"
  [[ -n "${curve_key_dir}" ]] && argv_list+=("-curve_key_dir" "${curve_key_dir}")
  export LD_LIBRARY_PATH="${BIN_DIR}/lib:$LD_LIBRARY_PATH"
  (nohup "${BIN_DIR}/agent" "${argv_list[@]}" >${BASE_DIR}/agent.out 2>&1) &
  pid=$!
  sleep 5
  [[ -f /proc/$pid/cmdline ]] && cat /proc/$pid/cmdline || ret_code=1
  if [[ $ret_code -ne 0 ]]; then
    cat ${BASE_DIR}/agent.out
  fi
  return $ret_code
}

function stop_one_agent()
{
  is_array "AGENT_ADDRESS" && agent_address="${AGENT_ADDRESS[$COMPONENT_NUM]}" || agent_address="${AGENT_ADDRESS}"
  pid="$(ps ux | grep /agent | grep ${agent_address} | grep -v grep | awk '{print $2}')"
  if ! is_num "${pid}"; then
    echo -e "Cannot found the agent we want: ${agent_address}" >&2
    exit 1
  fi
  kill -15 "$pid"
  while [ -e /proc/$pid ]; do sleep 0.5; done
}

function deploy_one_agent()
{
  . "${CONF_DIR}/agent-env.sh"
  if [ x"${ACTION}" = "xstart" ]; then
    start_one_agent
  else
    stop_one_agent
  fi
}

function deploy_agent()
{
  if [ x"${ACTION}" = "xstart" ]; then
    "${LAUNCHER[@]}" "${BASE_DIR}/agent-launcher.sh" "${BASE_DIR}/deploy-datasystem.sh" "-a" "start" "-c" "agent" "-p" "${CONF_DIR}"
  else
    "${LAUNCHER[@]}" "${BASE_DIR}/agent-launcher.sh" "${BASE_DIR}/deploy-datasystem.sh" "-a" "stop" "-c" "agent" "-p" "${CONF_DIR}"
  fi
}


function deploy_all()
{
  if [[ x"${ACTION}" = "xstart" ]]; then
    deploy_master
    deploy_worker
    deploy_agent
  else
    deploy_agent
    deploy_worker
    deploy_master
  fi
}

function deploy_components()
{
  echo -e "-- ${CYAN}Starting${NC} to ${ACTION} the datasystem cluster"
  case "${COMPONENT}" in
    all|master|worker|gcs|agent|clusterfs)
      deploy_${COMPONENT}
      ;;
    *)
      echo -e "This command requires a component be specified, your component: \"${COMPONENT}\"." >&2
      echo -e "${USAGE}" >&2
      exit 1
  esac
  echo -e "-- ${ACTION} the datasystem cluster ${GREEN}Complete${NC}!"
}

function main()
{
  # Add -x if debugging is enable.
  if [[ "$-" == *x* ]]; then
    LAUNCHER+=("-x")
  fi

  . "${BASE_DIR}/deploy-common.sh"
  while getopts "hfa:c:d:n:p:w:" OPT; do
    case "${OPT}" in
      a)
        ACTION="${OPTARG}"
        ;;
      c)
        COMPONENT="${OPTARG}"
        ;;
      d)
        DATASYSTEM_HOME="${OPTARG}"
        ;;
      f)
        HANDLE_CLUSTERFS="Yes"
        ;;
      n)
        COMPONENT_NUM="${OPTARG}"
        ;;
      p)
        CONF_DIR=$(realpath "${OPTARG}")
        if [[ ! -d "${CONF_DIR}" ]]; then
          echo -e "No such conf directory: ${OPTARG}" >&2
          exit 1
        fi
        ;;
      h)
        echo -e "${USAGE}"
        exit 0
        ;;
      w)
        echo -e "Deprecated options, no longer used!" >&2
        ;;
      *)
        echo -e "Error: OPTION \"${OPT}\" not recognized\n${USAGE}" >&2
        exit 1
        ;;
    esac
  done

  if [[ -z "${ACTION}" ]]; then
    echo -e "Error: no ACTION specified\n${USAGE}" >&2
    exit 1
  fi

  # deploy or pass packages according to the action.
  case "${ACTION}" in
    pass)
      get_env
      pass_packages
      ;;
    pass_conf)
      get_env
      pass_conf
      ;;
    start|stop)
      if [[ -z "${COMPONENT_NUM}" ]] ; then
        deploy_components
      else
        deploy_one_${COMPONENT}
      fi
      ;;
    *)
      echo -e "Error: ACTION \"${ACTION}\" not recognized\n${USAGE}" >&2
      ;;
  esac
}

main "$@"