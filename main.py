# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print('Hi, {}'.format(name))  # Press Ctrl+F8 to toggle the breakpoint.


def list_mean(p):
    total = 0.0
    for t in p:
        total += t
    mean = total / len(p)
    return mean

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    a = [1, 2, 3, 4]
    print(list_mean(a))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
