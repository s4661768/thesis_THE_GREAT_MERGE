import pandas as pd

def read_data(filename: str) -> tuple[list, list]:
    df = pd.read_csv(filename)
    
    rtc_seconds = [ float(rtc_val.split(":")[0]) * 360 + float(rtc_val.split(":")[1]) * 60 + float(rtc_val.split(":")[2]) for rtc_val in df['RTC_TIME'].values ]
    
    offset = float((df['SYS_TIME'].values)[0]) - rtc_seconds[0]
    sys_offset_seconds = [ float(value) - offset for value in df['SYS_TIME'].values ]
    
    return rtc_seconds, sys_offset_seconds;


def read_bt_data(filename: str) -> tuple[list, list, list, list]:
    df = pd.read_csv(filename)

    return df['RUN_TIME'].values, df['MSGS_PER_SEC'].values, df['BITS_PER_SEC'].values, df['BYTES_PER_SEC'].values

# if __name__ == '__main__':
#     # filename = '.\\temp.csv'
#     # read_data(filename)

#     filename = '.\\bt_test_0.csv'
#     read_bt_data(filename)

    # offset = sys - rtc
    # offset - sys = -rtc
    # -offset + sys = rtc
    # sys - offset = rtc