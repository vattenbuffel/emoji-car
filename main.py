import numpy as np
import time
import msvcrt
import threading

width = 15
height = 10
p_brick_base = 0.4
p_brick_increase = 0.2
fps_increase_factor = 0.1
fps_increase_interval = 10

w = b'w'
a = b'a'
s = b's'
d = b'd'
q = b'q'


car = "\U0001F697"
# print(car)
tree = "\U0001F333"
# print(tree)
brick = "\U0001F4A7"
# print(brick)
empty = "  "
fast_forward = "\U000023E9"

class Player():
    def __init__(self):
        self.x = width-1
        self.y = np.random.randint(1,height-1)
        self.input = None
        threading.Thread(target=self.read_input).start()

    def read_input(self):
    #   print("start reading input")
        while True:
            self.input = msvcrt.getch()
            # print(f"input: {self.input}")
            if self.input == q:
                exit(0)

    def update_pos(self, road):
        key = self.input
        if key == q:
            print("Good bye!")
            exit(0)
        if key == w:
            old_y = self.y
            self.y = max(1, self.y-1)
            if collision(self, road):
                self.y = old_y

        elif key == a:
            old_x = self.x
            self.x = max(0, self.x-1)
            if collision(self, road):
                self.x = old_x

        elif key == s:
            old_y = self.y
            self.y = min(height-2, self.y+1)
            if collision(self, road):
                self.y = old_y

        elif key == d:
            old_x = self.x
            self.x = min(width-1, self.x+1)
            if collision(self, road):
                self.x = old_x
                
        self.input = None


def remove_blocks(road, prev_clear):
    col = road[1:-1,0]

    # Make sure there exist an empty connecting cell in col to prev_empty
    i_to_check = list(set([prev_clear-1 if prev_clear>0 else prev_clear, prev_clear, prev_clear+1 if prev_clear<height-3 else prev_clear]))

    clear_cell = col[i_to_check] == empty


    if np.sum(clear_cell) == 0:
        # Clear a cell
        prev_clear = np.random.choice(i_to_check)
        road[1+prev_clear, 0] = empty
    else:
        prev_clear = np.array(i_to_check)[clear_cell==True]
        prev_clear = np.random.choice(prev_clear)

    road[1+prev_clear, 1] = empty
        
    return road, prev_clear

def generate_col(p_brick_base, p_brick_increase):
    col = np.zeros((height,1), dtype='object')
    col[:,:] = empty

    # Add trees at the sides
    col[[0,-1]] = tree

    # Add rocks
    n_free = height-2
    p_brick = p_brick_base
    for i in range(n_free):
        if n_free == 1:
            break

        rnd_number = np.random.rand()
        if rnd_number <= p_brick:
            col[i+1,0] = brick 
            n_free -= 1
            p_brick = p_brick_base + p_brick_increase
        else:
            p_brick = p_brick_base 

    return col

def generate_road():
    road = np.zeros((height, width), dtype='object')
    for i in range(width):
        col = generate_col(0,0)
        road[:,i] = col.reshape(-1)

    return road

def print_road(road):
    for row in road[:,2:]:
        for col in row:
            print(col, end="")
        print("")

def add_player(player, road):
    road_player = np.copy(road)
    road_player[player.y, player.x] = car
    return road_player

def collision(player, road):
    if road[player.y, player.x] == brick:
        return True
    else:
        return False

def main():
    fps  = 1
    player = Player()
    score = 0
    frame_counter = 0
    prev_clear = np.random.randint(1,height-3)
    prev_clear = height-3

    road = generate_road()
    road[:,1:] = road[:,:-1]
    new_col = generate_col(p_brick_base, p_brick_increase)
    road[:,0] = new_col.reshape(-1)
    road[:,1:] = road[:,:-1]
    new_col = generate_col(p_brick_base, p_brick_increase)
    road[:,0] = new_col.reshape(-1)

    while True:
        player.update_pos(road)
        road_player = add_player(player, road)
        print_road(road_player)

        dead = collision(player, road)
        if dead:
            print(f"You died!\nYour score was {score}.")
            break
        road[:,1:] = road[:,:-1]
        dead = collision(player, road)

        new_col = generate_col(p_brick_base, p_brick_increase)
        road[:,0] = new_col.reshape(-1)
        road, prev_clear = remove_blocks(road, prev_clear)

        time.sleep(1/fps)
        frame_counter += 1
        if frame_counter % fps_increase_interval == 0:
            fps *= (1+fps_increase_factor)
            for i  in range(width-1): print(fast_forward,end="")
            print()

        score += 1


while True:
    main()



