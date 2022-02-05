def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def write(content, idx):
    file_name = "file_" + str(idx)
    with open(file_name, "w") as f:
        f.write(str(content))


def read():
    file_phones = open("telefonos_buin.csv", "r")
    list_phone = ''
    for row in file_phones:
        row = row.split(',')
        list_phone += row[0].strip()+","+row[1].strip() + "\n"
    row = divide_chunks(list_phone, 1000)
    for i , line in enumerate(row):
        write(line, i)
