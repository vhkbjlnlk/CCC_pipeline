import mysql.connector
import argparse
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
parser=argparse.ArgumentParser()
parser.add_argument('--cccfile',help='cell to cell communication results data csv file path, please make sure that \
sample info was imported into sql sample info table',default='test')

mydb=mysql.connector.connect(
    user='root',
    host='localhost',
    password='',
    database='practice1')
mydb.autocommit = True
mycursor = mydb.cursor(buffered=True)

import pandas as pd
sample_query='insert into sample_info values({});'

def sql(query):
    mycursor.execute(query)
    result=pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)
    return result
def insert_data(sample_path,sample_name): 
    sample_name='\'{}\''.format(sample_name) #sample_name example: " 'brain1_1' "
    query='insert into ccc({}) values({});'
    data=pd.read_csv(sample_path)
    data=data[data.columns.to_list()[1:17]]
    cols='{}'.format(sql('describe ccc;').iloc[1:,:]['Field'].to_string(index=False).replace('\n',','))
    data=data.sort_values('magnitude_rank').sort_index().reset_index(
        names='overall rank').applymap(lambda x : "'{}'".format(x) if isinstance(x,str) else x)
    for x in range(len(data)):
        x=data.iloc[x].to_string(index=False).replace('\n',',').replace('    ','')+','+sample_name
        mycursor.execute(query.format(cols,x))
    pass




x=pd.read_csv('/Users/boyongwei/Documents/shell_ccc/sample_info.csv',index_col=0)

for z in x.index:
    if len(sql('select * from sample_info \
where sample_name=\'{}\';'.format(z))['sample_name'])==0:
        print('{} is not updated into mysql'.format(z))
        mycursor.execute( 'insert into sample_info values({},{});'.format( 
            "\"{}\"".format(z),
            "\"{}\"".format('\",\"'.join(x.loc[z].to_list())) ) 
                        )
    else:
        pass
        





sample_path=parser.parse_args().cccfile
sample_name=sample_path.split('/')[-2]
insert_data(sample_path=sample_path,sample_name=sample_name)
mydb.close()
