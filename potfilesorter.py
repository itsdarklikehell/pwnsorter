import sys, os
from shutil import copyfile

potfile_source = '/home/rizzo/wpa-sec.founds.potfile'
dlurl = 'https://wpa-sec.stanev.org/?api&dl=1'

wpa_source = "/etc/wpa_supplicant/wpa_supplicant.conf"
wpa_backup = "/tmp/wpa_supplicant.bak"
wpa_tmp = "/tmp/wpa_supplicant.tmp"

wificonfigstore_source = "/home/rizzo/WiFiConfigStore.xml"
wificonfigstore_backup = "/tmp/wificonfigstore.bak"
wificonfigstore_tmp = "/tmp/wificonfigstore.tmp"

wificonfigstoresoftap_source = "/home/rizzo/WiFiConfigStoreSoftAp.xml"
wificonfigstoresoftap_backup = "/tmp/wificonfigstoresoftap.bak"
wificonfigstoresoftap_tmp = "/tmp/wificonfigstoresoftap.tmp"


def get_potfile():
    print("Download your potfile from: " + dlurl)
    print('To: ' + potfile_source)
    #urllib.request.urlretrieve(dlurl, potfile_source)


def backup_configs():
    if os.path.exists(wpa_tmp):
        os.remove(wpa_tmp)
    else:
        print('Backing up: ' + wpa_source)
        print('To: ' + wpa_backup)
        copyfile(wpa_source, wpa_backup)
        print('Create tempfile to work with in: ' + wpa_tmp)
        copyfile(wpa_source, wpa_tmp)

    if os.path.exists(wificonfigstore_tmp):
        os.remove(wificonfigstore_tmp)
    else:
        print('Backing up: ' + wificonfigstore_source)
        print('To: ' + wificonfigstore_backup)
        copyfile(wificonfigstore_source, wificonfigstore_backup)
        print('Create tempfile to work with in: ' + wificonfigstore_tmp)
        copyfile(wificonfigstore_source, wificonfigstore_tmp)

    if os.path.exists(wificonfigstoresoftap_tmp):
        os.remove(wificonfigstoresoftap_tmp)
    else:
        print('Backing up: ' + wificonfigstoresoftap_source)
        print('To: ' + wificonfigstoresoftap_backup)
        copyfile(wificonfigstoresoftap_source, wificonfigstoresoftap_backup)
        print('Create tempfile to work with in: ' + wificonfigstoresoftap_tmp)
        copyfile(wificonfigstoresoftap_source, wificonfigstoresoftap_tmp)


def copy_config():
    if os.path.exists(wpa_tmp):
        print('Copying new created config to: ' + wpa_source)
        copyfile(wpa_tmp, wpa_source)
        os.remove(wpa_tmp)
    else:
        print('Cannot copy: ' + wpa_tmp + ' to: ' + wpa_source)
        print('Are you ROOT?')
        exit()

    if os.path.exists(wificonfigstore_tmp):
        print('Copying new created config to: ' + wificonfigstore_source)
        copyfile(wificonfigstore_tmp, wificonfigstore_source)
        os.remove(wificonfigstore_tmp)
    else:
        print('Cannot copy: ' + wificonfigstore_tmp + ' to: ' + wificonfigstore_source)
        print('Are you ROOT?')
        exit()

    if os.path.exists(wificonfigstoresoftap_tmp):
        print('Copying new created config to: ' + wificonfigstoresoftap_source)
        copyfile(wificonfigstoresoftap_tmp, wificonfigstoresoftap_source)
        os.remove(wificonfigstoresoftap_tmp)
    else:
        print('Cannot copy: ' + wificonfigstoresoftap_tmp + ' to: ' + wificonfigstoresoftap_source)
        print('Are you ROOT?')
        exit()


def checkwpaconfig(check_file, search_str):
    with open(check_file, 'r') as checklines:
        for line in checklines:
            if search_str in line:
                print(search_str + ' is already in the file: ' + checklines.name)
                return True
    print(search_str + ' is not found in: ' + str(check_file))
    return False


def readpotfiledata():
    network_block = (
        '\n'
        'network={\n'
        '  scan_ssid=1\n'
        '  ssid="{bssid}"\n'
        '  psk="{password}"\n'
        '}\n'
        '\n'
    )
    with open(potfile_source, 'r') as checkpotfile:
        print('Reading: ' + checkpotfile.name + ' Data.')
        for line in checkpotfile:
            potfiledata = line.split(':')
            if len(potfiledata) < 4:
                continue
            latitude, longitude, bssid, wpapassword = (p.rstrip() for p in potfiledata[:4])
            print('FOUND:')
            print('BSSID: ' + bssid)
            print('WpaPassword: ' + wpapassword)
            print('Latitude: ' + latitude)
            print('Longitude: ' + longitude)
            block = network_block.format(bssid=bssid, password=wpapassword)
            if checkwpaconfig(wpa_tmp, bssid):
                print(bssid + ' Found, Skipping.')
                continue
            for tmp in (wpa_tmp, wificonfigstore_tmp, wificonfigstoresoftap_tmp):
                print('Found new network: ' + bssid)
                print('Appending to: ' + tmp)
                with open(tmp, 'a+') as outputfile:
                    outputfile.write(block)


get_potfile()
backup_configs()
readpotfiledata()
copy_config()
print('Done.')
