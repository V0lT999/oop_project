"""first lab"""
import random


def quicksort(nums):
    """function of sorting"""
    if len(nums) <= 1:
        return nums
    else:
        q = random.choice(nums)
    l_nums = [n for n in nums if n > q]

    e_nums = [q] * nums.count(q)
    b_nums = [n for n in nums if n < q]
    return quicksort(l_nums) + e_nums + quicksort(b_nums)


def main():
    """main of program"""
    mas = [i for i in range(1, 11)]
    print(mas)
    mas = quicksort(mas)
    print(mas)


if __name__ == "__main__":
    main()