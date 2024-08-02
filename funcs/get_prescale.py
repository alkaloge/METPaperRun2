import sys
import yaml

def get_value_from_yaml(yaml_path, key1, key2, key3):
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
        try:
            return data[key1][key2][key3]
        except (KeyError, TypeError):
            return None

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print("Usage: python script.py <yaml_path> <key1> <key2> <key3>")
        sys.exit(1)

    yaml_path = sys.argv[1]
    key1 = sys.argv[2]
    key2 = int(sys.argv[3])
    key3 = int(sys.argv[4])

    value = get_value_from_yaml(yaml_path, key1, key2, key3)
    print(value)


