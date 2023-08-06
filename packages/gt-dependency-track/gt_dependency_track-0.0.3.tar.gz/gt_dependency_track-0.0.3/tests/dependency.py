from gt_dependency_track import DependencyTrack
url = 'http://dependency-track-api-8081'
api_key = '<<change here>>'
dt = DependencyTrack(url, api_key)

print("List of project uuid")
list_projects = dt.list_projects()
for project in list_projects:
    print(project['uuid'])

print("Upload bom")
dt.upload_project_bom('<<change here>>', 'bom.json')
