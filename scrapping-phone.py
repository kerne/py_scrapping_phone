import threading
import time
from mechanize import Browser
from bs4 import BeautifulSoup
from chunk_file import read, divide_chunks


def soup(content, selector):
    soup = BeautifulSoup(content, 'html.parser')
    soup = soup.select_one(selector)
    return soup


def formulario(telefono):
    url = 'http://www.telexplorer.cl'
    br = Browser()
    br.set_handle_robots(False)  # ignore robots
    br.addheaders = [
        ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')]
    br.open(url)
    br.select_form(id="form_res2")
    br.form['area'] = telefono['area']
    br.form['telefono'] = telefono['numero']
    res = br.submit()
    content = res.read()
    data = soup(content, '.resultado')
    return data


def find_lines(telefonos):
    linea = ''
    for t in telefonos:
        print('Thread ID : ' + str(threading.current_thread().ident))
        data = formulario(t)
        if data:
            lineas = []
            for d in data.find_all('p'):
                element = d.text.strip()
                element = element.replace(',', ' ')
                print(element)
                addd = element.split('\t')
                if len(addd) > 1:
                    element = str(addd[0]).strip() + "," + str(addd[1]).strip()
                lineas.append(element)
            linea += ','.join([str(elem) for elem in lineas]) + '\n'
        else:
            print('Data Not Found')
    write(linea)


def create_thread(idx, data):
    return threading.Thread(target=find_lines, name='t'+str(idx), args=(data,))


def write(content):
    file_name = "phone_result"
    with open(file_name, "a") as f:
        f.write(str(content))


def run():
    # read()
    init = 190
    end = init + 10
    for i in range(init, end):
        file_name = 'file_' + str(i)
        file_phones = open(file_name, "r")
        print('Reading File :' + file_name)
        list_phone = []
        for row in file_phones:
            row = row.split(',')
            list_phone.append(
                {'area': row[0].strip(), 'numero': row[1].strip()})
        file_phones.close()
        chunk_list = list(divide_chunks(list_phone, 10))
        threads = []
        for idx, data in enumerate(chunk_list):
            thread = create_thread(idx, data)
            print('Created :' + thread.name)
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()
        import os
        os.remove(file_name)
        time.sleep(5)


if __name__ == "__main__":
    run()
