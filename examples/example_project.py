from examples.example_const import *
from teamcity import TeamCity

# Initialize the TeamCity object with your server and tokens
tc = TeamCity(server=TEAMCITY_SERVER, tokens=TEAMCITY_TOKENS)  # Recommended method

# Get detailed build types of a specific project_id
build_types = tc.get_project_build_types(project_id=EX_PROJECT_ID)
print(build_types)

# Get  build type list of a specific project_id
build_types = tc.get_project_build_types(project_id=EX_PROJECT_ID, details=False)
print(build_types)
