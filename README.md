# Multithreading-Sort



功能
讀入一個文字檔，裡面有使用者隨機產生的數字 範圍有0~1w, 10w,50w,100w 程式根據使用者所選擇的方法, 將隨機亂數的值 依序排列
並且輸出CPU執行的時間以及完成方法時當下的時間(時區為UTC+8 )
流程

讀取檔案完成後，先根據檔案內容的第一個元素來判斷欲採用何種方法。

方法一，將N個數目字直接進行Bubble Sort，並顯示CPU執行之時間。
方法二，將N個數目字切成k份，由k個threads分別進行Bubble Sort後，再由k-1個threads進行Merge Sort，並顯示CPU執行之時間。
方法三，將N個數目字切成k份，並由k個Processes分別進行Bubble Sort之後，再由k-1個Processes進行Merge Sort，並顯示CPU執行之時間。
方法四，將N個數目字切成k份，在一個Process內對k份資料進行Bubble Sort，再用同一個Process作Merge Sort，同時顯示CPU執行之時間。
