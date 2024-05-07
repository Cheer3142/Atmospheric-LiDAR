import requests
from datetime import datetime, timedelta
import time

def download_file_from_nextcloud(server_url, username, password, file_path, local_destination):
    # Authenticate with Nextcloud
    session = requests.Session()
    session.auth = (username, password)

    # Make a request to get the download link for the file
    url = f"https://nc.narit.or.th/nextcloud/remote.php/dav/files/" + \
            f"88B7A53F-2122-4350-BCC3-05C6AB15CC5D/" + file_path  # user


    response = session.request("GET", url)

    if response.status_code == 200:
        # Download the file
        with open(local_destination, "wb") as f:
            f.write(response.content)
        response.close()
        print("File downloaded successfully.")
        return True
    else:
        print("Failed to download file. Status code:", response.status_code)
        response.close()
        return False

def get(path=r"C:\Users\Optics Lab 2\Documents\Cheer\Lidar\MPL_pull\\",
        dateandtime = None):
    # Example usage
    server_url = "https://nc.narit.or.th"
    username = "patcharadanai"
    password = "patcharadanai088413"

    if dateandtime is None:
        now     = datetime.utcnow()
        now     = now.replace(minute = now.minute//5*5) - timedelta(minutes=5)
        now_str = now.strftime("%Y%m%d%H%M")       
    else:
        now_str = str(dateandtime)

    # NC file path
    file_path = "RealTimeLiDARncFiles/MPL_5038_{}.nc".format(now_str)

    # Debug
    # file_path = "RealTimeLiDARncFiles/MPL_5038_202403241215.nc".format(file_name)

    # Local path
    local_destination = path + "/" + "MPL_5038_{}.nc".format(now_str) # print(local_destination)
    # print(now_str)

    while True:
        if (download_file_from_nextcloud(server_url, username, password,
                                 file_path, local_destination)): break
        time.sleep(10)
    return local_destination

if __name__ == '__main__':
    destination = get()