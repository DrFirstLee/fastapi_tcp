
STX = bytes([2])
ETX = bytes([3])


HOST = '0.0.0.0'  # 서버 IP 주소
PORT = 9900  # 서버 포트 번호

def check_sendingData_validity(input_data):
    if input_data[-1:] !=  '\x03' :
        return {'result' : False, 'result_detail' : 'data end error'}   
    elif input_data[:1] != '\x02':
        return {'result' : False, 'result_detail' : 'data start error'}        
        
    return {'result' : True, 'result_detail' : 'success'}        


def check_ack(input_data):
    if (len(input_data)!=6) :
        return {'result' : False, 'result_detail' : 'data Length error'}
    elif input_data[-1:] !=  '\x03' :
        return {'result' : False, 'result_detail' : 'data end error'}   
    elif input_data[:1] != '\x02':
        return {'result' : False, 'result_detail' : 'data start error'}        
    elif input_data[1:-1] != 'ACK0':
        return {'result' : False, 'result_detail' : 'data ack error'}           
    return {'result' : True, 'result_detail' : 'success'}        

def check_polling(input_data):
    if (len(input_data)!=6) :
        return {'result' : False, 'result_detail' : 'data Length error'}
    elif input_data[-1:] != '\x03' :
        return {'result' : False, 'result_detail' : 'data end error'}   
    elif input_data[:1] != '\x02':
        return {'result' : False, 'result_detail' : 'data start error'}        
    elif input_data[1:-1] != 'POLL':
        return {'result' : False, 'result_detail' : 'data ack error'}           
    return {'result' : True, 'result_detail' : 'success'}        

def make_title_udp(datacode, procbit, job_date, job_time, outerkey, apinews_key, category, title, img_url, stdcnt, STX, ETX):
    send_data= datacode+ procbit+ job_date+ job_time+ outerkey+ apinews_key+ category+ title+ img_url+ stdcnt
    send_data_encoded = STX +  send_data.encode(encoding='euc-kr', errors='ignore') + ETX
    return {'result' : True,'result_detail' : 'success' , 'result_content' : send_data_encoded }        


def make_content_udp(datacode, job_date, job_time, page_no, contents ):
    end_sect = '1'
    send_data_header = datacode+ job_date+ job_time ### + page_no+ contents 
    if len(contents) >= 2048:
        send_data_encoded_l = []
        end_sect = '0'
        for split_data in range( int(len(contents)/ 2048 + 1)):
            contents_text = contents[split_data*2048:2048*(split_data+1)]
            page_no = str(split_data+1)
            
            if split_data == int(len(contents)/ 2048) :
                end_sect = '1'
                contents_text = contents_text.ljust(2048)
            
            fin_data = send_data_header + page_no+ contents_text+ end_sect
            send_data_encoded = STX +  fin_data.encode(encoding='euc-kr', errors='ignore') + ETX
            send_data_encoded_l.append(send_data_encoded)
        
    else:
        contents_text = contents.ljust(2048)
        page_no = '1'
        fin_data = send_data_header + page_no+ contents_text+ end_sect
        send_data_encoded = STX +  fin_data.encode(encoding='euc-kr', errors='ignore') + ETX
        send_data_encoded_l = [send_data_encoded]
    
    
    return {'result' : True,'result_detail' : send_data_encoded_l , 'result_content' : send_data_encoded_l }        
    