from PIL import Image
from time import time

def image_to_matrix(name):
    start_image = Image.open(name)
    new_img = start_image.convert("1")
    image_matrix = new_img.load()
    img_w, img_h = new_img.size
    real_matrix = []
    for i in range(0,img_h):    
        real_matrix.append([])
        for j in range(0,img_w):
            if image_matrix[j,i] >= 128:
                real_matrix[i].append(1)
            else:
                real_matrix[i].append(0)
    return real_matrix
    
def matrix_to_image(input_matrix, name):
    h_size = len(input_matrix)
    w_size = len(input_matrix[0])
    size = w_size, h_size
    new_image = Image.new("1", size)
    new_image_matrix = new_image.load()
    for i in range(0, h_size):
        for j in range(0, w_size):
            val = input_matrix[i][j]
            if val == 0:
                new_image_matrix[j,i] = val
            else:
                new_image_matrix[j,i] = 255
    new_image.save(name)
    new_image.close()
    return "OK"
    
#           N1 N2 N3
#           N4 XX N5
#           N6 N7 N8
#           n1i = n2i = n3i = i-1
#           n4i = n5i = i
#           n6i = n7i = n8i = i+1
#           n1j = n4j = n6j = j-1
#           n2j = n7j = j
#           n3j = n5j = n8j = j+1
            
def generate_empty_matrix(h,w):
    nm = []
    for i in range(0,h):
        nm.append([])
        for j in range(0,w):
            nm[i].append(0)
    return nm

class game(object):
    def __init__(self, input_matrix):
        self.current_state = input_matrix
    def advance_game(self):
        timeinit = time()
        input_matrix = self.current_state
        h_size = len(input_matrix)
        w_size = len(input_matrix[0])
        new_matrix = []
        for i in range(0, h_size):
            new_matrix.append([])
            for j in range(0, w_size):
                #nsum = 0
                curlife = input_matrix[i][j]
                if i-1 < 0:
                    n1i = n2i = n3i = h_size - 1
                else:
                    n1i = n2i = n3i = i-1
                n4i = n5i = i
                if i+1 > (h_size - 1):
                    n6i = n7i = n8i = 0
                else:
                    n6i = n7i = n8i = i+1
                if j-1 < 0:
                    n1j = n4j = n6j = w_size - 1
                else:
                    n1j = n4j = n6j = j-1
                n2j = n7j = j
                if j+1 > (w_size - 1):
                    n3j = n5j = n8j = 0
                else:
                    n3j = n5j = n8j = j+1
                nsum = input_matrix[n1i][n1j] + input_matrix[n2i][n2j] + input_matrix[n3i][n3j] + input_matrix[n4i][n4j] + input_matrix[n5i][n5j] + input_matrix[n6i][n6j] + input_matrix[n7i][n7j] + input_matrix[n8i][n8j]
                if curlife == 1 and nsum < 2:
                    new_matrix[i].append(0)
                elif curlife == 1 and (nsum == 2 or nsum == 3):
                    new_matrix[i].append(1)
                elif curlife == 1 and nsum > 3:
                    new_matrix[i].append(0)
                elif curlife == 0 and nsum == 3:
                    new_matrix[i].append(1)
                else:
                    new_matrix[i].append(0)
        print("Time to iterate: " + str(time() - timeinit))
        self.current_state = new_matrix


print("Conway's Game of Life r1.0")
print("By fabrizziop")
print("MIT Licence")
file_name = str(input('Enter original file name: '))
game_mode = str(input('1: Iterate X times then save ONCE, 2: Iterate saving X times '))
its = int(input('Times to iterate: '))
matrix = image_to_matrix(file_name)
game = game(matrix)
if game_mode == '1':
    newname = file_name[:-4] + ".output" + file_name[-4:]
    print("Saving to -> " + newname)
    for i in range(0,its):
        print("Iteration " + str(i))
        game.advance_game()
    matrix_to_image(game.current_state, newname)
    print("Done")
        
if game_mode == '2':
    for i in range(0,its):
        nstr = str(i)
        while len(nstr) < len(str(its-1)):
            nstr = '0' + nstr
        newname = file_name[:-4] + ".output" + nstr + file_name[-4:]
        print("Iteration " + str(i))
        game.advance_game()
        matrix_to_image(game.current_state, newname)
