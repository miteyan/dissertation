def write_file(file, string):
    with open(file=file, mode='wb') as f:
        f.write(string)
    f.close()