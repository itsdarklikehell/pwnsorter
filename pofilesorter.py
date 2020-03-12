import sys, os, subprocess
from shutil import copyfile

wpa_source = "/etc/wpa_supplicant/wpa_supplicant.conf"
wpa_backup = "/tmp/wpa_supplicant.bak"
wpa_tmp = "/tmp/wpa_supplicant.tmp"
potfile_source = '/home/rizzo/Downloads/wpa-sec.founds.potfile'


def backup_configs():
    if os.path.exists(wpa_tmp):
        os.remove(wpa_tmp)
    else:
        print('Backing up: ' + wpa_source)
        print('To: ' + wpa_backup)
        copyfile(wpa_source, wpa_backup)
        print('Create tempfile to work with in: ' + wpa_tmp)
        copyfile(wpa_source, wpa_tmp)

def copy_config():
    print('Copying new created config to: ' + wpa_source)
    if os.path.exists(wpa_tmp):
        copyfile(wpa_tmp, wpa_source)
        os.remove(wpa_tmp)
    else:
        print('Cannot copy: ' + wpa_tmp + ' to: ' + wpa_source)
        print('Are you ROOT?')
        exit()

def checkwpaconfig(wpa_tmp, search_str):
    with open(wpa_tmp, 'r') as checklines:
        for line in checklines:
            if search_str in line:
                print(search_str + ' is already in the file: ' + checklines.name)
                return True
    print(search_str + ' is not found in: ' + checklines.name)
    return False


def readpotfiledata():
    with open(potfile_source, 'r') as checkpotfile:
        print('Reading: ' + checkpotfile.name + ' Data.')
        for line in checkpotfile:
            potfiledata = line.split(':')
            Latitude = potfiledata[0].rstrip()
            Longitude = potfiledata[1].rstrip()
            BSSID = potfiledata[2].rstrip()
            WpaPassword = potfiledata[3].rstrip()
            print('FOUND:')
            print('BSSID: ' + BSSID)
            print('WpaPassword: ' + WpaPassword)
            print('Latitude: ' + Latitude)
            print('Longitude: ' + Longitude)
            if checkwpaconfig(wpa_tmp, BSSID):
                print(BSSID + ' Found, Skipping.')
            else:
                with open(wpa_tmp, 'a+') as outputfile:
                    print('Found new network: ' + BSSID)
                    print('Appending to: ' + outputfile.name)
                    outputfile.writelines('\n')
                    outputfile.writelines('network={' + '\n')
                    outputfile.writelines('  scan_ssid=1' + '\n')
                    outputfile.writelines('  ssid="' + BSSID + '"\n')
                    outputfile.writelines('  psk="' + WpaPassword + '"\n')
                    outputfile.writelines('}\n')
                    outputfile.writelines('\n')


backup_configs()
readpotfiledata()
copy_config()
