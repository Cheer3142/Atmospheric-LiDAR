import pymongo

# ฟังก์ชันสำหรับแปลงข้อมูล TRC เป็น JSON และบันทึกลงใน MongoDB
def read_json(db_name, col_name):
    db_url = 'mongodb://root:12345678@192.168.2.190:27017/'
    '''
    db_name = 'ocs-data'
    collection_name = 't10'

    ans = col.find_one()
    x = col.find({},{'_id': 0, 'appliance': 1, 
                 'rating': 1, 'company': 1})
                 
    '''

    # แปลงข้อมูลเป็น JSON
    # waveform_json = {"data": list(waveform_data)}

    # เชื่อมต่อ MongoDB
    client  = pymongo.MongoClient(db_url)
    db      = client[db_name]
    col     = db[col_name]

    ans = col.find_one({}, {'_id':0,
                            'range_raw': 1,
                            "copol_raw" : 1, 
                            "crosspol_raw" : 1, })
    ans = col.find_one()
    # ปิดการเชื่อมต่อ MongoDB
    client.close()

    return ans

if __name__ == '__main__':
    db_name     = 'raw-mpl'
    col_name    = 'MPL_5038_202403010001'

    r = read_json(db_name, col_name)
    print(r) # r['range_raw']
