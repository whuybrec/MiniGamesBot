
def creat_table(*lists):
    PADDING = 2
    column_sizes = [0 for e in lists[0]]
    for i in range(len(lists)):
        for j in range(len(lists[i])):
            if column_sizes[j] < len(str(lists[i][j])):
                column_sizes[j] = len(str(lists[i][j]))

    table = ""
    for lst in lists:
        for i in range(len(lst)):
            table += str(lst[i]).ljust(column_sizes[i]+PADDING)
        table += "\n"
    return table
