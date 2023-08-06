from gt_dependency_track import DependencyTrack
import argparse

url = 'http://dependency-track.gt.solution:8081'
api_key = "gB8eNGNE0RIloZ4zxC9SpCFOHNWQIEwC"

class Main:
  if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CI/CD integration for Dependency Track')
    parser.add_argument('--host', help="Dependency Track Hostname", required=True)
    parser.add_argument('--api_token', help="API Key", required=True)
    parser.add_argument('--product_uuid', help="Dependency Track Product ID", required=True)
    parser.add_argument('--file', help="Scanner file", required=True)
    

    args = vars(parser.parse_args())
    host = args["host"]
    api_token = args["api_token"]
    product_uuid = args["product_uuid"]
    file = args["file"]
    dt = DependencyTrack(host, api_token)

    dt.upload_project_bom(product_uuid, file)