import requests
from LegendsLIB import *
class VENOM:
  def get_rest(user):
    info = A7X.info(user)
    IDN=info['ID']

    headerros = {
        'Content-Length': '305',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'i.instagram.com',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Instagram 6.12.1 Android (25/7.1.2; 160dpi; 383x680; LENOVO/Android-x86; 4242ED1; x86_64; android_x86_64; en_US)',
        # Requests sorts cookies= alphabetically

        'Accept-Language': 'en-US',
        'X-IG-Connection-Type': 'WIFI',
        'X-IG-Capabilities': 'AQ==',
        'Accept-Encoding': 'gzip',
							}
    datada = {
        'ig_sig_key_version': '4',
        "user_id":IDN
							}
    reso = requests.post('https://i.instagram.com/api/v1/accounts/send_password_reset/',headers=headerros, data=datada).json()
    try:
      resto =str(reso['obfuscated_email'])
      return resto
    except:
      this='YOU BLOCKED'
      return this