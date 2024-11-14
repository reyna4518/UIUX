import csv

def read_csv(filename):
    with open(filename,mode='r') as file:
        reader=csv.DictReader(file)
        rows=list(reader)
    return rows

filename='../5_t-wt_d-wt/sales_data.csv'
rows=read_csv(filename)
# print(rows)
headers=list(rows[0].keys())
# print(headers)
numeric_headers=[header for header in headers if header!='Region']

v_total={header:sum(int(row[header]) for row in rows) for header in numeric_headers}

for row in rows:
    region=row['Region']
    h_total=sum(int(row[header]) for header in numeric_headers)
    twt={header:(int(row[header])/h_total)*100 for header in numeric_headers}
    dwt={header:(int(row[header])/v_total[header])*100 for header in numeric_headers}
    print(f"For {region}")
    print(f"T-Weights are {twt}")
    print(f"D-weights are {dwt}")
    
