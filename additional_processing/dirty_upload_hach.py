import subprocess

a = subprocess.Popen("aws s3 ls s3://ds-ajm-videos | grep ee6cd078-e786-4e76-98a0-a89dd86652f1")