import yaml

yaml_str = """
name: John
age: 30
city: New York
"""

data = yaml.load(yaml_str, Loader=yaml.Loader)
print(data)