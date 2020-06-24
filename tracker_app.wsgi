import sys, os
sys.path.insert (0,'/home/charlie/git/spending-tracker')
print(f"Charlie is figuring out version: {sys.version_info}")

from tracker_app import app as application
