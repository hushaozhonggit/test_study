import os
import shutil
from utils.project_path import get_path

jmx_path = get_path('jmx_run_template')
jtl_path = get_path('jtl_files')
result_path = get_path('result')


def run():
    thread_numbers = [1, 5, 10, 20]  # 线程数
    ranpup = 1  # 多少时间内启动完
    times = 30  # 运行时间
    cycle = -1  # 迭代次数；-1表示无限；值为非-1时，运行时间无效
    test_name = 'baidu_demo.jmx'
    for threads in thread_numbers:
        if os.system("tasklist | findstr 'java.exe' | findstr 'Console'") != "":
            os.system("taskkill /F /IM java.exe /T")
        else:
            pass
        if os.path.exists(f'jmx_run_template/{test_name.split(".")[0]}_{threads}.jmx'):
            os.remove(f'jmx_run_template/{test_name.split(".")[0]}_{threads}.jmx')
        else:
            shutil.copyfile(f'jmx_files/{test_name}', f'jmx_run_template/{test_name.split(".")[0]}_{threads}.jmx')
        if os.path.exists(f'jtl_files/jtl_{test_name.split(".")[0]}_{threads}.jtl'):
            os.remove(f'jtl_files/jtl_{test_name.split(".")[0]}_{threads}.jtl')
        if os.path.exists(f'result/{test_name.split(".")[0]}_report_{threads}'):
            shutil.rmtree(f'result/{test_name.split(".")[0]}_report_{threads}')
        else:
            os.mkdir(f'result/{test_name.split(".")[0]}_report_{threads}')
            print(f'线程数:{threads}\t|\t压测中...\t|\t运行时长：{times}s')
            os.system(f"jmeter -Jthreads={threads} -Jcycle={cycle} -Jranpup={ranpup} -Jtimes={times} -n -t {jmx_path}/{test_name.split('.')[0]}_{threads}.jmx -l {jtl_path}/jtl_{test_name.split('.')[0]}_{threads}.jtl -e -o {result_path}/{test_name.split('.')[0]}_report_{threads}")


if __name__ == '__main__':
    run()
