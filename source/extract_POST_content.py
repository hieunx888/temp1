import urllib.parse

def extract_input_fields(request):
	request = request.split('\r\n\r\n')[-1].split('\n')
	values = []
	for item in request:
		if len(item) != 0:
			firstEqualSign = item.find("=")
			extractedString = item[firstEqualSign + 1:]
			extractedString.replace("\r","")
			extractedString.replace("\n", "")
			# print(value)
			values.append(extractedString)
	return values
