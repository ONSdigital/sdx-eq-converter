from app import subscriber, cloud_config

if __name__ == '__main__':
    print('Starting sdx-eq-converter')
    cloud_config()
    subscriber.start()
