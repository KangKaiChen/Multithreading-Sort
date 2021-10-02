#!/usr/bin/python
# coding=utf-8
import threading as td
import multiprocessing as mp
from multiprocessing import Pool
import time
import string
import math
from queue import Queue
from datetime import datetime, timezone, timedelta


def bubblesort(data, q):
    # 定義資料長度
    n = len(data)
    for i in range(n - 1):  # 有 n 個資料長度，但只要執行 n-1 次
        for j in range(n - i - 1):  # 從第1個開始比較直到最後一個還沒到最終位置的數字
            if data[j] > data[j + 1]:  # 比大小然後互換
                data[j], data[j + 1] = data[j + 1], data[j]

    q.put(data)


def readfile(data, case, filename):
    case = input("請輸入要哪個case: ")
    f = open(filename, "r")
    for line in f.readlines():
        line = line.strip("\n")
        data.append(int(line))
    print(data.__len__())
    f.close()
    return case


def mission2_bubble(dividelist, q):
    bubblesort(dividelist, q)
    # list1.append(dividelist)


#  print( list1 )


def mission3_bubble(dividelist, q):
    bubblesort(dividelist, q)


#  print(dividelist)
# list1.append(dividelist)


def mission2or3_merage(ll, rl, q):
    MergeSort(ll, rl, q)


#  print(dividelist)
# list1.append(dividelist)


def bubble_thread(data, K):
    threads = []
    Lastlist = []
    q = Queue()  # a queue to store several lists which are sorted by Bubblesorv
    K_thd = int(len(data) / K)
    dividelist = [data[i : i + K_thd] for i in range(0, K_thd * K, K_thd)]

    if len(data) % K != 0:  # 是否有餘數
        Lastlist += data[K_thd * K + 1 : len(data)]
        dividelist[K - 1] += Lastlist

    # if( K % 2 != 0 ): # 是否是奇數
    #     again = 1
    #     temp = K_thd*k+1
    #     del dividelist[temp:len(data]
    # for i in range(len(dividelist)):
    #     dividelist1 += dividelist[i]
    # for i in range(len(dividelist1)):
    #     if str(dividelist1[i]) == "8":
    #         print("done")
    for i in range(K):
        threads.append(td.Thread(target=mission2_bubble, args=(dividelist[i], q)))
        threads[i].start()

    for i in range(K):
        threads[i].join()

    return q


def merage_thread(data, K):
    m_threads = []
    list_merage = []
    for i in range(K - 1):

        if data.qsize() >= 0:

            ll = data.get()
            rl = data.get()

            threads = td.Thread(target=mission2or3_merage, args=(ll, rl, data))

            threads.start()
            m_threads.append(threads)

    for m in m_threads:  # wait for all thread are terminated
        m.join()

    list_merage += data.get()
    list_merage.sort()

    return list_merage


def bubble_process(data, K):
    m_processes = []
    pool = mp.Pool()
    Lastlist = []
    K_thd = int(len(data) / K)
    dividelist = [data[i : i + K_thd] for i in range(0, K_thd * K, K_thd)]

    if len(data) % K != 0:  # 是否有餘數
        Lastlist += data[K_thd * K + 1 : len(data)]
        dividelist[K - 1] += Lastlist
    manager = mp.Manager()
    q = manager.Queue(K)
    for i in range(K):
        processes = pool.apply_async(mission3_bubble, args=(dividelist[i], q))
        # processes.start()
        m_processes.append(processes)

    # for processes in m_processes:
    #     processes.join()
    pool.close()
    pool.join()
    return q


def Process_bubble_merge(data, K, q):
    meragedata = []
    K_thd = int(len(data) / K)
    dividelist = [data[i : i + K_thd] for i in range(0, K_thd * K, K_thd)]

    if len(data) % K != 0:  # 是否有餘數
        Lastlist += data[K_thd * K + 1 : len(data)]
        dividelist[K - 1] += Lastlist

    # for i in range(len(dividelist)):
    for l in dividelist:
        bubblesort(l, q)

    while q.qsize() != 1:
        ll = q.get()
        rl = q.get()
        MergeSort(ll, rl, q)


def merage_process(data, K):
    m_processes = []
    list_merage = []
    pool = mp.Pool()
    # dividelist = [data[i:i+K_thd] for i in range(0,len(data),K_thd)]
    for i in range(K - 1):

        if data.qsize() >= 0:

            ll = data.get()
            rl = data.get()
            #   p = mp.Process(target=mission3_merage, args=(dividelist[i], q) )
            processes = pool.apply_async(mission2or3_merage, args=(ll, rl, data))
            #    processes.append(p)
            # processes.start()
            m_processes.append(processes)
    pool.close()
    pool.join()
    # for processes in m_processes:  # wait for all process are terminated
    #     processes.join()

    list_merage += data.get()
    return list_merage


def MergeSort(_ll, _rl, q):  # both _ll and _rl are lists

    l, r = 0, 0
    lenOf_ll = len(_ll)
    lenOf_rl = len(_rl)
    items = []  # sorted list

    while l < lenOf_ll and r < lenOf_rl:  # breaks if one of the list is empty !
        if _ll[l] < _rl[r]:
            items.append(_ll[l])
            l += 1
        else:  # _ll[l] > _rl[r]
            items.append(_rl[r])
            r += 1

    # after the comparison, concat the rest of the ll or rl
    if l == lenOf_ll:
        items.extend(_rl[r:lenOf_rl])
    else:  # r == lenOf_rl
        items.extend(_ll[l:lenOf_ll])

    q.put(items)  # put the sorted list into the queue


def message():
    print("--------------------------------------------------")
    print("- 1.Bubble Sort (1 File, 1 Process)              -")
    print("- 2.Bubble Sort & Merge Sort (K-File, K-Threads) -")
    print("- 3.Bubble Sort & Merge Sort (K-File, K-Process) -")
    print("- 4.Bubble Sort & Merge Sort (K-File, 1 Process) -")
    print("--------------------------------------------------")


def PrintDatatime():
    dt = datetime.utcnow()
    dt = dt.replace(tzinfo=timezone.utc)
    tzutc_8 = timezone(timedelta(hours=8))
    local_dt = dt.astimezone(tzutc_8)
    print("Output time " + str(local_dt))
    return str(local_dt)


if __name__ == "__main__":
    message()
    data = list()  # 建立一個串列
    case = ""
    filename = input("輸入檔名:") + ".txt"
    #    filename = "input1_2.txt"

    case = readfile(data, case, filename)
    if case == "1":
        q = Queue()
        print("題號: ", case)
        start = time.time()
        bubblesort(data, q)
        end = time.time()
        output = filename + "_output1.txt"
        f = open(output, "w")
        f.write("Sort\n")
        for i in range(len(data)):
            f.write(str(data[i]))
            f.write("\n")
        f.write("\n***CPU執行時間: %f" % (end - start) + "sec")
        print("\n***CPU執行時間: %f" % (end - start) + "sec")
        f.write("\nOutput time " + PrintDatatime())
        f.close()
    elif case == "2":
        finallymeragedata = []
        print("題號: ", case)
        K = input("請輸入要切成幾分:")
        K = int(K)
        start = time.time()
        bubbledata = bubble_thread(data, K)

        meragedata = merage_thread(bubbledata, K)
        # finallymeragedata = mission2_merge_sort(meragedata) #將合併的結果在merage 一次
        end = time.time()
        output = filename + "_output2.txt"
        f = open(output, "w")
        f.write("MerageSort(K-File, K-Thread)\n")
        for i in range(len(meragedata)):
            f.write(str(meragedata[i]))
            f.write("\n")
        f.write("\n***CPU執行時間: %f" % (end - start) + "sec")
        print("\n***CPU執行時間: %f" % (end - start) + "sec")
        f.write("\nOutput time " + PrintDatatime())
        f.write("\nThread數(檔案分割數):" + str(K))
        f.close()
    elif case == "3":
        processes = []
        list_bubble = []
        finallymeragedata = []
        print("題號: ", case)
        K = input("請輸入要切成幾分:")
        K = int(K)
        start = time.time()
        bubbledata = bubble_process(data, K)
        # for i in range(bubbledata):
        #     dividelist1 += dividelist[i]
        # for i in range(len(dividelist1)):
        #     if str(dividelist1[i]) == "8":
        #         print("done")
        meragedata = merage_process(bubbledata, K)

        end = time.time()
        output = filename + "_output3.txt"
        f = open(output, "w")
        f.write("MerageSort(K-File, K-Process)\n")
        for i in range(len(meragedata)):
            f.write(str(meragedata[i]))
            f.write("\n")
        f.write("\n***CPU執行時間: %f" % (end - start) + "sec")
        print("\n***CPU執行時間執行時間: %f" % (end - start) + "sec")
        f.write("\nOutput time " + PrintDatatime())
        f.write("\nProcess數(檔案分割數):" + str(K))
        f.close()
    elif case == "4":
        meragedata = []
        processes = []
        pool = Pool()
        print("題號: ", case)
        K = input("請輸入要切成幾分:")
        K = int(K)
        manager = mp.Manager()
        q = manager.Queue(
            K
        )  # a queue to store several lists which are sorted by Bubblesorv
        start = time.time()
        # processes = pool.apply_async(Process_bubble_merge, args=(data, K, q))
        Process_bubble_merge(data, K, q)
        # pool.close()
        # pool.join()

        end = time.time()
        output = filename + "_output4.txt"
        f = open(output, "w")
        f.write("MerageSort(K-File, 1 Process)\n")
        meragedata = q.get()
        for i in range(len(meragedata)):
            f.write(str(meragedata[i]))
            f.write("\n")
        f.write("\n CPU執行時間: %f" % (end - start) + "sec")
        print("\n CPU執行時間: %f" % (end - start) + "sec")
        f.write("\nOutput time " + PrintDatatime())
        f.write("\nProcess數(檔案分割數):" + str(K))
        f.close()