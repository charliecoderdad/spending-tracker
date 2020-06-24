def getTableHeadTags(headersList):
	tableHead = "<table border=1 class='table table-sm table-hover'>"
	tableHead += "<thead class='thead-dark'><tr>"
	for item in headersList:
		tableHead += "<th scope='col'>" + item + "</th>"
	tableHead += "</tr></thead>"
	return tableHead;
