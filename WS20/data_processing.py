import pandas as pd 

data =pd.read_excel('../Ws20_data/WS20_masterclass_data.xlsx', sheet_name = None )


tracks = data['TRACK']
content = data['Content review Title & descript']
