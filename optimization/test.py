import sys
import json

print(json.dumps([float(sys.argv[1]), 100 + float(sys.argv[2])]))
