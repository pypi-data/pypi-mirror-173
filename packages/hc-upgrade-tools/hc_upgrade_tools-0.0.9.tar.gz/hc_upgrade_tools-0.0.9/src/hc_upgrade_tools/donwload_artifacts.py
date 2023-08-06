
import logging
from hc_upgrade_tools import utility as util
import os


# get logger for this file
_logger = util.setup_logging("download_pkg", "hc_upgrade_tools.download.log", logging.DEBUG)

# init sub command parser as subparser of skeleton.py
# subparser add_argument in this file
def init_subparser(subparsers):
    """Init sub command parser as subparser of skeleton.py

    Args:
      subparsers (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    subparser = subparsers.add_parser("dl-pkg", help="sub command help")

    # add argument "--host"
    subparser.add_argument("--host", help="host name or ip address", type=str, metavar="STR", required=True)
    # add argument "--port"
    subparser.add_argument("--port", help="port number", type=int, metavar="INT", required=True)
    # add argument resource-path
    subparser.add_argument("--resource-path",
        help="resource path", type=str, metavar="STR",
        default="/api/githook/request-artifacts"
    )
    # add argument "projectID"
    subparser.add_argument("--projectID", help="project ID", type=str, metavar="STR")

    subparser.set_defaults(func=main_process)

    return subparser

def main_process(args):
    upgrade_porcess_root_dir = "/tmp/hc_upgrade_tools"
    server_host = args.host
    server_port = args.port
    res_path = args.resource_path
    project_id = args.projectID
    target_dir = os.path.join(upgrade_porcess_root_dir, "artifacts")
    artifact_name = "artifact.zip"

    artifacts_path = util.download_artifact(server_host, server_port, res_path, project_id, target_dir, artifact_name)

    if artifacts_path:
        build_dir = os.path.join(upgrade_porcess_root_dir, "build")

        util.handle_artifacts(artifacts_path, build_dir, source_sub_folder="archive/backend/build")