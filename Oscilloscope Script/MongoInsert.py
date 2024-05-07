import pymongo

'''
http://192.168.2.190:8081/
admin/1234

API Mongo

SHOW ALL DATASESE : http://192.168.2.190:5000/databases
SHOW Collections in DATASESE : http://192.168.2.190:5000/collections/ <database_name>
SHOW data : http://192.168.2.190:5000/data/<database_name>/<collections_name>

sample:
http://192.168.2.190:5000/databases
http://192.168.2.190:5000/collections/ocs-data
http://192.168.2.190:5000/data/ocs-data/t4
'''
# ฟังก์ชันสำหรับแปลงข้อมูล TRC เป็น JSON และบันทึกลงใน MongoDB
def insert_file(db_name, col_name, json_file):
    db_url = 'mongodb://root:12345678@192.168.2.190:27017/'
    '''
    db_name = 'ocs-data'
    collection_name = 't10'
    '''

    # แปลงข้อมูลเป็น JSON
    # waveform_json = {"data": list(waveform_data)}

    # เชื่อมต่อ MongoDB
    client = pymongo.MongoClient(db_url)
    db = client[db_name]
    collection = db[col_name]

    try:
        # บันทึกข้อมูลลงใน MongoDB
        with pymongo.timeout(10):
            collection.insert_one(json_file)
        print('C')
    except Exception as e:
        # แสดงข้อความเมื่อไม่สามารถบันทึกข้อมูลได้
        print('E', e)

    # ปิดการเชื่อมต่อ MongoDB
    client.close()


