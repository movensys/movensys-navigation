MOVENSYS_NAVIGATION_CONTAINER="${MOVENSYS_NAVIGATION_CONTAINER:-movensys_navigation_container}"
MOVENSYS_NAVIGATION_WORKSPACE="${MOVENSYS_NAVIGATION_WORKSPACE:-/home/admin/workspaces/movensys_ws}"

nros() {
  local flags=(-i)
  [ -t 0 ] && flags=(-it)

  local setup='source /opt/ros/${ROS_DISTRO}/setup.bash'
  setup="${setup} && source ${MOVENSYS_NAVIGATION_WORKSPACE}/install/setup.bash"

  if [ $# -eq 0 ]; then
    docker exec "${flags[@]}" -u admin "${MOVENSYS_NAVIGATION_CONTAINER}" \
      bash -lc "${setup} && exec bash -i"
  else
    docker exec "${flags[@]}" -u admin "${MOVENSYS_NAVIGATION_CONTAINER}" \
      bash -lc "${setup} && \"\$@\"" nros "$@"
  fi
}
