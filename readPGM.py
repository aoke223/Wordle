from printTest import*

def readPGM(filename: str) -> list:
    '''This function reads a Pgm file
    parameters: filename - corresponding to the str Pgm filename you want it to read
    returns: A list of strings and ints corresponding to the pgm magic number, comment,  a list of the columns and rows, the max level, and a list correspoding to the pgm'''
    image= open(filename, "r")
    # read header
    magic_num= image.readline().strip()
    comment= image.readline().strip()
    cols_rows= image.readline().strip()
    max_level= int(image.readline().strip())
    # convert string like "9 10" to list ['9', '10']
    cols_rows_list= cols_rows.split()
    # convert str in list to int
    for i in range(len(cols_rows_list)):
        cols_rows_list[i]= int(cols_rows_list[i])
    
    header=[magic_num, comment, cols_rows_list, max_level]


    pixels=[]
    # read line by line without knowing how many lines
    pixel_value= image.readline().strip()
    pixel_int=pixel_value.split()
    while pixel_value != "":
        for i in range(len(pixel_int)):
            pixel_int[i]= int(pixel_int[i])
            pixels.append(pixel_int[i])
        pixel_value= image.readline().strip()
        pixel_int=pixel_value.split()
    image.close()
    return [header, pixels]
    

def writePGM(filename: str, new_list: list[list[str]]) -> None:
    '''This function writes a pgm file
    parameters: filename - corresponding to the str Pgm filename you want to write
    new_list - corresponding to the list returned from readPgm
    returns: None'''
    output_file= open(filename, "w")
    output_file.write(f"{new_list[0][0]}\n")
    output_file.write(f"{new_list[0][1]}\n")
    output_file.write(f"{new_list[0][2][0]} {new_list[0][2][1]}\n")
    output_file.write(f"{new_list[0][3]}\n")
    for i in range(len(new_list[1])):
        output_file.write(f"{new_list[1][i]}\n")
    output_file.close()
    
def main() -> None:
    image_list= readPGM("house.pgm")
    print(image_list)
    printTest(readPGM, "house.pgm", expected=[['P2', '# cute little house', [7, 8], 9], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 9, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 9, 0, 0, 9, 9, 9, 9, 9, 0, 0, 9, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0]])
    printTest(readPGM, "Circle.pgm", expected=[['P2', '# circle', [5, 5], 6], [0, 6, 6, 0, 0, 6, 0, 0, 6, 0, 6, 0, 0, 6, 0, 6, 0, 0, 6, 0, 0, 6, 6, 0, 0]])
    printTest(readPGM, "Stickman.pgm", expected=[['P2', '# stickman', [9, 9], 7], [0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 0, 0, 7, 0]])
    image_list= writePGM("house1.pgm", [['P2', '# cute little house', [7, 8], 9], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 9, 0, 9, 0, 0, 0, 9, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 9, 0, 0, 9, 9, 9, 9, 9, 0, 0, 9, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 9, 0, 0, 9, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0]])
    '''House1.pgm: 
    P2
    # cute little house
    7 8
    9 
    0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 9 0 9 0 0 0 9 0 0 0 9 0 0 9 0 0 0 9 0 0 9 9 9 9 9 0 0 9 0 0 0 9 0 0 9 0 0 0 9 0 0 9 0 0 0 9 0 0 9 0 0 0 9 0 0 0 0 0 0 0 0'''
    image_list= writePGM("Stickman_mom.pgm", [['P2', '# stickman', [9, 9], 7], [0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 0, 0, 7, 0]])
    '''Stickman_mom.pgm:
    P2
    # stickman
    9 9
    7
    0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 7, 0, 0, 0, 0, 0, 7, 0'''

main()