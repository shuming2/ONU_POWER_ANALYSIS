
def generate_column_name():
    f = open('format.txt', 'r')
    lines = f.readlines()
    lsts = []
    for line in lines:
        lst = line.split()
        lsts.append(lst[0])
    print(lsts)
    str1 = ', '.join(lsts)
    print(str1)
    f.close()


def generate_create_sql():
    f = open('format.txt', 'r')
    lines = f.readlines()
    lsts = []
    for line in lines:
        lst = line.split()
        lst.pop()
        datatype = lst[1]
        if datatype == 'VARCHAR2':
            lst[1] = 'VARCHAR'
        elif datatype == 'NUMBER':
            lst[1] = 'DOUBLE'
        elif datatype == 'DATE':
            lst[1] = 'DATETIME'
        if len(lst) == 3:
            lst[1] += '({})'.format(lst[2])
            lst.pop()

        lsts.append(lst)

    strlst = []
    for lst in lsts:
        strlst.append(' '.join(lst))
    sql = ',\n'.join(strlst)
    print(sql)
    f.close()


if __name__ == '__main__':
    # generate_create_sql()
    generate_column_name()
