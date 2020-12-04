import glob, os
os.chdir("./output_data")
for file in glob.glob("*.csv"):
    print(file)