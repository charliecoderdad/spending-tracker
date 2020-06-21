import json

catTable = {
	"category1": {
		"total": 0,
		"percent": 5
	},
	"category2": {
		"total": 0,
		"percent": 5
	},
	"category3": {
		"total": 0,
		"percent": 5
	}
}

for cat in sorted(catTable.keys()):
	print(cat)
	print(catTable[cat]['total'])
	
