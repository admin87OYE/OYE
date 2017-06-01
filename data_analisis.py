import pandas as pd
import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import numpy as np
import truncate
import random
import time


def mean(num_set):
    """ Calculates the mean of numbers in a list """
    result = 0
    for num in num_set:
        result += num
    result /= len(num_set)
    return result


def median(num_set):
    """ Calculates the median of numbers in a list """
    num_set = sorted(num_set)
    if len(num_set) % 2 == 0:
        result = mean([num_set[int(len(num_set)/2)], num_set[int(len(num_set)/2-1)]])
    else:
        result = num_set[int((len(num_set)-1)/2)]
    return result


def median_list(nums):
    medians = []
    temp = []
    for num in nums:
        temp.append(num)
        medians.append(median(temp))
    return medians


def mean_list(nums):
    means = []
    temp = []
    for num in nums:
        temp.append(num)
        means.append(mean(temp))
    return means


def plot_nums(nums):
    plt.plot(range(len(nums)), nums, label='Numbers')
    plt.plot(range(len(nums)), mean_list(nums), label='Mean')
    plt.plot(range(len(nums)), median_list(nums), label='Median')
    plt.xlabel('Next Number')
    plt.ylabel('Number Value')
    plt.title('Numbers')
    plt.legend()
    plt.show()


def bar_freq(day):
    freq = get_num_freq(day)
    freq = [sorted(freq, key=freq.get), sorted(freq.values())]
    plt.bar(freq[0], freq[1])
    plt.ylabel('Frequency')
    plt.xlabel('Number')
    plt.show()


def log_to_list(directory, file):
    """ Takes only the numbers from the log file and puts them in a list which it returns"""
    num_list = []
    num_dict = log_to_dict(directory, file)
    for current_round in num_dict:
        for num in current_round['nums']:
            num_list.append(num)
    return num_list


def log_to_excel(directory, file):
    """ Takes in an OYE_MB log file and converts it to an excel spreadsheet """
    log_to_df(directory, file).to_csv(directory + file[:-4] + '.xls')


def log_to_html(directory, file):
    """ Takes in an OYE_MB log file and converts it to an html table """
    log_to_df(directory, file).to_html(directory + file[:-4] + '.html')


def log_to_dict(directory, file):
    """ Takes in an OYE_MB log file and converts it to a dictionary with values for:
        date, time, winning numbers, round number """
    date = ""
    for num in file[11:].split('_'):
        date = date + num + '-'
    date = date[:-5]
    with open(directory + file, 'r') as log:
        day = []
        current_round = 1
        for single_round in log:
            time = single_round.split('|')[0][7:-1]
            nums = []
            for num in single_round.split('|')[1][18:].split(', '):
                nums.append(int(num))
            day.append({"date": date, "time": time, "nums": nums, "round": current_round})
            current_round += 1
        return day


def log_to_df(directory, file):
    """ Takes in an OYE_MB log file and converts it to a pandas dataframe """
    day = log_to_dict(directory, file)
    df = pd.DataFrame(day)
    df.set_index('round', inplace=True)
    return df


def print_num_freq(day):
    """ Prints the data returned by get_num_freq() in a table-like fashion """
    nums = get_num_freq(day)
    nums = [sorted(nums, key=nums.get), sorted(nums.values())]
    for num in range(0, 48):
        print("Number " + str(nums[0][num]) + " ------------ " + str(nums[1][num]) + " times")


def get_num_freq(day):
    """ Takes in a dictionary (you can get one from a file using log_to_dict()) and returns
        two lists. The first list contains numbers sorted by their frequency and the second
        list contains the sorted frequencies """
    nums = {}
    for i in range(1, 49):
        nums.update({i: 0})
    for current_round in day:
        for num in current_round['nums']:
            nums[num] += 1
    return nums


def generate_round(size=35):
    """ Generates a list of 35 random numbers in a range of 1-48 """
    return random.sample(range(1, 49), size)


def generate_nums(size):
    """ Generates a list of a specific size with random numbers in the range of 1-48 """
    nums = []
    full_rounds = int(size/35)
    for _ in range(full_rounds):
        for num in generate_round():
            nums.append(num)
    if (size - (full_rounds * 35)) > 0:
        for num in generate_round(size - (full_rounds * 35)):
            nums.append(num)
    return nums


def create_artificial_log(directory, file_name="OYE_MB_ALOG_" + time.strftime("%y_%m_%d") + ".txt", length=256):
    """ Creates a log file just like the real one but with python's random generated numbers """
    temp = open(directory + file_name, 'w')
    temp.close()
    for current_round in range(length):
        with open(directory + file_name, 'a') as alog:
            alog.write("TIME - " + time.strftime("%H:%M:%S") + " | WINNING NUMBERS - ")
            for number in sorted(generate_round()):
                alog.write(str(number) + ", ")
        truncate.truncate_utf8_chars(directory + file_name, 2)
        with open(directory + file_name, 'a') as alog:
            alog.write("\n")


def create_artificial_dlog(directory, file_name="OYE_MB_ADLOG.CSV", length=256*35):
    temp = open(directory + file_name, 'w')
    temp.close()
    date = []
    for _ in range(length):
        date.append(time.strftime("%d-%m-%y"))
    _time = []
    for _ in range(length):
        _time.append(time.strftime("%H:%M:%S"))
    nums = generate_nums(length)
    nums2 = []
    for num in nums:
        nums2.append(float(num))
    means = mean_list(nums)
    medians = median_list(nums)
    pct_change = [0]
    for i in range(1, len(nums)):
        pct_change.append((nums[i] - nums[i-1]) / nums[i-1] * 100)
    with open(directory + file_name, 'a') as adlog:
        adlog.write("date,time,value,mean,median,pct_change\n")
        for curr_num in range(length):
            adlog.write(str(date[curr_num]) + ',' + str(_time[curr_num]) + ',' +
                        str(nums2[curr_num]) + ',' + str(means[curr_num]) + ',' +
                        str(medians[curr_num]) + ',' + str(pct_change[curr_num]) + '\n')
