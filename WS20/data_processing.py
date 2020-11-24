import pandas as pd 

data =pd.read_excel('../Ws20_data/WS20_masterclass_data.xlsx', sheet_name = None )


tracks = data['TRACK']
content = data['Content review Title & descript']
final = data['Final schedule']
joined = pd.merge(final, tracks, left_on = 'Title', right_on = 'Masterclass content title (do not edit)')

out_cols = joined.columns
blah = ['Masterclass content title (do not edit)', 'Title', 'Description',  'UUID folder']

out = joined[blah]