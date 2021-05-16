while True:
    line = input().lower()
    if line == '/exit':
        print('Bye!')
        break
    if line:
        nums = [int(i) for i in line.split()]
        print(sum(nums))
