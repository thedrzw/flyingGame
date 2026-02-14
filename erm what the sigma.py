# test_tuple = (10)
# test_list = [10]

# for item in test_tuple:
#     print(item)

# for item in test_list:
#     print(item)


# def update_player_data(value, update):
#     print(value)
#     value = update(value)
#     print(value)

# update_player_data(['a', 'b', 'c'], lambda list: list.append('d'))


# strings = ['the quick brown fox jumped over the lazy river ahhhhhhhhh please add line breaks']
# print(' testing testing 1 2 3 '.split(' '))


# tuple1 = (100, 200)
# tuple1[0], tuple1[1] += 300, 400
# print(tuple1)


# if 'a' in ['a', 'b', 'c']:
#     print('yes')
# if ['a', 'b', 'c'] in 'a':
#     print('yes')


# def wrapper(func, *args):
#     print('wrapper function!')
#     print(*args)
#     return func(*args)

# def mulitplication(term1: float | int, term2: float | int):
#     return term1 * term2

# print(wrapper(mulitplication, 1, 4))


# a = 0x100
# print(a)


# class Object:
#     def __init__(self, name) -> None:
#         self.name = name

# mouse = Object('mouse')

# print(hasattr(mouse, 'name'))


# a = 0
# b = 0
# conditional = a == b
# a = 1
# print(conditional)


# a = 0
# b = 0
# if a is 0:
#     print('yes')


# from typing import Any

# class Coordinates:

#     def __init__(self, x1, y1, x2, y2) -> None:
#         self.x1 = x1
#         self.y1 = y1
#         self.x2 = x2
#         self.y2 = y2

#         self.width = x2 - x1
#         self.height = y2 - y1
    
#     def __setattr__(self, name: str, value: Any):
#         super().__setattr__(name, value)

#         if name == 'x1':
#             self.width = self.x2 - self.x1

#         if name == 'width':
#             self.x2 = self.x1 + self.width

# coordinates = Coordinates(1, 1, 10, 10)
# print(coordinates.width) # should return 9

# coordinates.x1 = 4
# print(coordinates.width) # should return 6

# coordinates.width = 100
# print(coordinates.x2) # should return 101


import pygame
from time import process_time_ns

loops = 100_000_000

t1 = process_time_ns()

for _ in range(loops):
    pygame.Rect(1.1, 1.1, 102, 203)

t2 = process_time_ns()

print(f'took {(t2 - t1) / loops} nanoseconds per loop')

# in conclusion, the pygame rect constructor is pretty damn fast because its written in c