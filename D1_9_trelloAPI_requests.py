import sys
import requests  
  
# Данные авторизации в API Trello  
auth_params = {    
    'key': "", 
    'token': "", }  
  
base_url = "https://api.trello.com/1/{}" 
board_id = "85m59MCb"
idBoard = "5db0a9314f9bcb382a522c16"

def read(show_num = False):      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
    start = 1
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:              
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        print('"{}" [{}]:'.format(column['name'],len(task_data)))   
        
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print("\t#{}\t{}".format(start, task['name']) if show_num else "\t{0}".format(task['name'], start))
            start += 1

def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if task['name'] == name:    
                task_id = task['id']    
                break    
        if task_id:    
            break    
       
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:                
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            break  

def move_num(num, column_name):
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    start = 1
    task_id = None    
    for column in column_data:    
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()    
        for task in column_tasks:    
            if start == num:    
                task_id = task['id']    
                break    
            start += 1
        if task_id:    
            break

    for column in column_data:    
        if column['name'] == column_name:                
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            break    
    read()

def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
        if column['name'] == column_name:
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})      
            break

def newlist(name):
    response = requests.post(base_url.format('lists'), data={'name': name, 'idBoard': idBoard, **auth_params})
    print("OK\n", response.text)


if __name__ == "__main__":
    if len(sys.argv) <= 2:    
        read()    
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move#':    
        read(show_num = True)
        try:
            pos = int(input('\nВведите номер задачи для перемещения в список "%s": ' % sys.argv[2]))
        except:
            print("Что-то не так с вводом.")
        else:
            move_num(pos, sys.argv[2])
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'newlist':
        newlist(sys.argv[2]) 