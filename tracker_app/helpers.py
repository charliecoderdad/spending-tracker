def getTableHeadTags(headersList):
	tableHead = "<table border=1 class='table table-sm table-hover js-sort-table'>"
	tableHead += "<thead class='thead-dark'><tr>"
	for item in headersList:
		# If item is a monetary unit we need to add js-sort-number class to the th element
		if (item == "Total" or item == "Min. Spending" or item == "Discretionary" or item == "Amount" or item == "Percent"):
			tableHead += "<th scope='col' class='js-sort-number'>" + item + "</th>"
		elif (item == "Date"):
			tableHead += "<th scope='col' class='js-sort-date'>" + item + "</th>"
		elif (item == "Month"):
			tableHead += "<th scope='col' class='js-sort-month'>" + item + "</th>"
		else:
			tableHead += "<th scope='col'>" + item + "</th>"
	tableHead += "</tr></thead>"
	return tableHead;
