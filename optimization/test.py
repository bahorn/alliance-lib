import sys
import json

a = float(sys.argv[2]) + float(sys.argv[1])
b = float(sys.argv[1])**2 + float(sys.argv[2])

res = [a, b]

print(json.dumps(res))
