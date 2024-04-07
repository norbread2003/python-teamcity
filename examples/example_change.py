from examples.example_const import *
from teamcity import TeamCity

# Initialize the TeamCity object with your server and tokens
tc = TeamCity(server=TEAMCITY_SERVER, tokens=TEAMCITY_TOKENS)  # Recommended method

# Get changes of a specific build_type_id
changes = tc.get_all_changes(build_type_id=EX_BUILD_TYPE_ID)
print(changes)

# Get pending changes of a specific build_type_id
pending_changes = tc.get_pending_changes(build_type_id=EX_BUILD_TYPE_ID)
print(pending_changes)
