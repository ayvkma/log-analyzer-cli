from datetime import datetime
import sys

# list storing the data extracted from each log
LOGS = []

print("---------------------LOG ANALYZER-------------------------\n")
print('Enter the relative path of your log file:', end=" ")

file_path = input()

with open(file_path) as logs:
    for log in logs:
        log_data = log.split()
        ip = log_data[0]
        date_time = log_data[3].strip('[')
        dt = datetime.strptime(date_time, "%d/%b/%Y:%H:%M:%S")
        method = log_data[5].strip('"')
        endpoint = log_data[6]
        req_type = log_data[7].strip('"')
        status_code = int(log_data[8])
        response_size = int(log_data[9])
        response_time = int(log_data[10][:-2])
        
        LOGS.append({ 
                'ip': ip,
                'date_time': dt,
                'method': method,
                'endpoint': endpoint,
                'req_type': req_type,
                'status_code': status_code,
                'response_size': response_size,
                'response_time': response_time
            })

if len(LOGS) <= 0:
    raise RuntimeError("ERROR WHILE READING LOG FILE")

while True:
    print('What kind of information you want to get from the logs?')
    print("""
    1. Specifc Errors (e.g. 500 errors between 12 Dec and 13 Dec)
    2. Which IP caused the most failed logins (401)?
    3. Average response time across all requests
    4. Which IPs requested more than [number_of_reqs] times over a short duration [duration] seconds?
    5. Fastest and Slowest Endpoints
    """)
    
    print("Which one do you want to select?", end=" ")
    user_input = int(input())
    
    if user_input == 1:
        print("\nEnter error status code:", end=" ")
        status_code = int(input())
        print("Enter start date:", end=" ")
        start_date = input()
        start_date_time = datetime.strptime(start_date, "%Y %d %b")
        print("Enter end date:", end=" ")
        end_date = input()
        end_date_time = datetime.strptime(end_date, "%Y %d %b")
    
        error_count = 0
        
        for log in LOGS:
            if (    log['status_code'] == status_code and 
                    start_date_time <= log['date_time'] <= end_date_time
                ):
                error_count += 1
                
        print('------------------------------------------------------------------------------------\n')
        print(f"===============> {error_count} {status_code} errors happened between {start_date} and {end_date} <===============\n")
        print('------------------------------------------------------------------------------------\n')
        
    elif user_input == 2:
        ip_to_failed_login_freq = {}
        for log in LOGS:
            if log['status_code'] == 401:
                ip = log['ip']
                ip_to_failed_login_freq[ip] = ip_to_failed_login_freq.get(ip, 0) + 1
        
        max_failed_login_ip = max(ip_to_failed_login_freq, key=ip_to_failed_login_freq.get)
        failed_logins = max(ip_to_failed_login_freq.values())
        
        print('------------------------------------------------------------------------------------\n')
        print(f"===============> IP - `{max_failed_login_ip}` caused the most ({failed_logins}) failed logins (401) <===============\n")
        print('------------------------------------------------------------------------------------\n')
    
    elif user_input == 3:
        sum_of_resp_times = sum(log['response_time'] for log in LOGS)
        total = len(LOGS)
        avg_resp_time = round(sum_of_resp_times / total, 3)
        
        print('------------------------------------------------------------------------------------\n')
        print(f"===============> Average response time across all requests is: {avg_resp_time} <===============\n")
        print('------------------------------------------------------------------------------------\n')
        
    elif user_input == 4:
        print("\nEnter number of frequent requests: ")
        number_of_reqs = int(input())
        print("Enter duration in seconds for the requests: ")
        duration = int(input())
        
        ip_to_times = {}
        
        for log in LOGS:
            lst = ip_to_times.get(log['ip'], [])
            lst.append(log['date_time'])
            ip_to_times[log['ip']] = lst
            
        result_ips = []
        
        for ip in ip_to_times:
            times = ip_to_times[ip]
            times.sort()
            
            total_reqs = 1
            
            start = 0
            end = len(times) - 1
            
            while start < end:
                if (times[end] - times[start]).total_seconds() > duration:
                    end -= 1
                else:
                    total_reqs += 1
                    start += 1
          
            if total_reqs >= number_of_reqs:
                result_ips.append(ip)
        
        print("-----------------------------------------------------------------------\n")
        print(f"===============> IPs that requested {number_of_reqs} requests in less than {duration} seconds: \n")
        
        for ip in result_ips:
            print(f"--------- {ip}")
            
        print(f"\n<===============")
        print("-----------------------------------------------------------------------\n")
            
    elif user_input == 5:
        fastest_response_time = sys.maxsize
        slowest_response_time = -1
        
        fastest_endpoint_ip = None
        fastest_endpoint = None
        
        slowest_endpoint_ip = None
        slowest_endpoint = None
        
        for log in LOGS:
            if log['response_time'] < fastest_response_time:
                fastest_response_time = log['response_time']
                fastest_endpoint_ip = log['ip']
                fastest_endpoint = log['endpoint']
            if log['response_time'] > slowest_response_time:
                slowest_response_time = log['response_time']
                slowest_endpoint_ip = log['ip']
                slowest_endpoint = log['endpoint']
                
        print('-------------------------------------------------------------\n')
        print(f"===============> Fastest Endpoint - {fastest_endpoint} from IP - {fastest_endpoint_ip} with response_time: {fastest_response_time} <===============")
        print()
        print(f"===============> Slowest Endpoint - {slowest_endpoint} from IP - {slowest_endpoint_ip} with response_time: {slowest_response_time} <===============")
        print('-------------------------------------------------------------\n')
                

                
                
            
            
        
        
            
        
        