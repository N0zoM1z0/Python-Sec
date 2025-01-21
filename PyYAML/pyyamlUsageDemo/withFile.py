import yaml

print(yaml.__version__) # 3.10
filename = r"data.yaml"
data = {'name': 'John', 'age': 30, 'city': 'New York'}
with open(filename, 'w') as f:
    yaml.dump(data, f)
print("++++++++++++++++++++++++++++++++")
with open(filename, 'r') as f:
    data = yaml.load(f,Loader=yaml.Loader)
print(data)

