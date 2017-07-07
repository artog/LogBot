from WarcraftLogApi import WarcraftLogApi
import configparser


def main():
    print ("Starting LogBot")
    config = configparser.ConfigParser()
    print("Loading config file: config.ini")
    config.read('config.ini')
    try:
        apikey = config['default']['apikey']
        if apikey == "":
            print("Invalid config file.")
            quit()
    except Exception as e:
        print("Error loading config file:"+e)
        quit()
        
    api = WarcraftLogApi(apikey)
    print(api.getFights("kFzACTYJbcmXLGqB"))
    print(api.getReports(1499277098372).json())


if __name__ == "__main__":
    main()