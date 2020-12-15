import glob, os
os.chdir("./output_data")
download_files = []
for total_files in glob.glob("*.csv"):
    download_files.append(files)

out_data
for files in total_files:
    with open(files,'r') as f:
        data = f.read()
        out_data.append(data)

with open('Tuesday_Christmas_out.csv','a') as f:
    for data in out_data:
        f.write(data + '/n')



         