while True:
    line = input().lower()
    if line == '/exit':
        print('Bye!')
        break
    if line == '/help':
        print('The program calculates the sum of numbers')
        continue
    if line:
        nums = [int(i) for i in line.split()]
        print(sum(nums))
