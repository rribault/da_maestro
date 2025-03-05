import openpyxl
from models import TEMPLATE_PATH

wb = openpyxl.load_workbook(TEMPLATE_PATH)
sheet = wb['Analytique']
# Initialize a list to store non-empty values
codes_dict = {}
# Iterate through the cells in the specified column
i=0
for cell in sheet['A']:
    if i>0 :
        if cell.value is not None:
            project_name = cell.value
            code = sheet[f'B{cell.row}'].value
            codes_dict[code] = f'{project_name} {code}'
    i+=1

spending_lines = {}
for cell in sheet['H']:
    if cell.value is not None:
        name = cell.value
        spending_lines[name] = name
