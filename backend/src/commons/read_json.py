from json import load

def read_json(file_path:str)->dict:
    with open(file_path) as f:
      data = load(f)
    return data