import python_code
import cython_code
import time

begin = time.perf_counter()
res = python_code.fact(100000)
end = time.perf_counter()
print(f'Python result: {res}')
python_time = end - begin

begin = time.perf_counter()
res = cython_code.fact(100000)
end = time.perf_counter()
print(f'Cython result: {res}')
cython_time = end - begin

print(f'Cython is {python_time / cython_time}X faster')
