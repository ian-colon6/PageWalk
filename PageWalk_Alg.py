import sys
import csv


def get_indexes(vAddress: int):
    return (
        (vAddress & 0x0000FF8000000000) >> 39,  # PML4E
        (vAddress & 0x0000007FC0000000) >> 30,  # PDPTE
        (vAddress & 0x000000003FE00000) >> 21,  # PDE
        (vAddress & 0x00000000001FF000) >> 12,  # PTE
    )


def get_offset(vAddress: int):
    return vAddress & 0xFFF


def PageWalk(BaseTblAddress, Offset, level, host_level):

    if level > 3:
        print(hex(int(BaseTblAddress, 16) | Offset))
        return
    try:

        Data = load_data(table_file)

        for row in Data:
            if BaseTblAddress in row.keys():
                # HIT
                vals = Data[indexes[level]].get(BaseTblAddress)
                BaseTblAddress = vals
                return PageWalk(BaseTblAddress, Offset, level + 1, host_level)
            else:
                # MISS
                host_index = get_indexes(int(BaseTblAddress, 16))
                #print(host_index)
                host_offset = get_offset(int(BaseTblAddress, 16))
                return PageWalk_Host(ept_pointer, host_index, host_offset, level, host_level)

    except OverflowError:
        print("Overflow!!!")


def PageWalk_Host(BaseTblAdd, h_index, h_offset, level, host_level):

    if host_level > 3:
        BaseTblAdd = hex(int(BaseTblAdd, 16) | h_offset)

        return PageWalk(BaseTblAdd, offset, level + 1, host_level)

    Data = load_data(table_file)
    for row in Data:
        if BaseTblAdd in row.keys():
            vals = Data[h_index[host_level]].get(BaseTblAdd)
            BaseTblAdd = vals
            return PageWalk_Host(BaseTblAdd, h_index, h_offset, level, host_level + 1)

        else:
            print("Page Fault")
            return


def load_data(filepath: str):
    data = []
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)  # Get the headers from the first row
        for row in reader:
            row_dict = {}
            for i, header in enumerate(headers):
                row_dict[header] = row[i]
            data.append(row_dict)
    return data


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cr3 = sys.argv[1]
        ept_pointer = sys.argv[2]
        table_file = sys.argv[3]
        vAddress = int(sys.argv[4], 16)
        offset = get_offset(vAddress)
        indexes = get_indexes(vAddress)

        PageWalk(cr3, offset, 0, 0)
