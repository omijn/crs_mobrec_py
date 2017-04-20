parameters = [{ 
    'reference': 'sMakers',
    'category': 'value',    
    'type': 'csv',
    'identifiers': ['acer', 'alcatel', 'allview', 'amazon', 'amoi', 'apple', 'archos', 'asus', 'at&t', 'benefon', 'benq', 'benq-siemens', 'bird', 'blackberry', 'blu', 'bosch', '8bq', 'casio', 'cat', 'celkon', 'chea', '5coolpad', 'dell', '4ee', 'emporia', '6energizer', 'ericsson', 'eten', 'fujitsusiemens', 'garmin-asus', 'gigabyte', 'gionee', '7google', 'haier', 'hp', 'htc', 'huawei', 'i-mate', 'i-mobile', 'icemobile', 'innostream', 'inq', '2intex', 'jolla', 'karbonn', 'kyocera', 'lava', '9leeco', 'lenovo', 'lg', 'maxon', 'maxwest', 'meizu', 'micromax', 'microsoft', 'mitac', 'mitsubishi', 'modu', 'motorola', 'mwg', 'nec', 'neonode', 'niu', 'nokia', 'nvidia', 'o2', 'oneplus', 'oppo', 'orange', 'palm', 'panasonic', 'pantech', 'parla', 'philips', 'plum', '1posh', 'prestigio', '3qmobile', 'qtek', 'sagem', 'samsung', 'sendo', 'sewon', 'sharp', 'siemens', 'sonim', 'sony', 'sonyericsson', 'spice', 't-mobile', 'tel.me.', 'telit', 'thuraya', 'toshiba', 'unnecto', 'vertu', 'verykool', 'vivo', 'vkmobile', 'vodafone', 'wiko', 'wnd', 'xcute', 'xiaomi', 'xolo', 'yezz', 'yota', '0yu', 'zte'],
    'values': {
        'acer': 59, 'alcatel': 5, 'allview': 88, 'amazon': 76, 'amoi': 28, 'apple': 48, 'archos': 90, 'asus': 46, 'at&t': 57, 'benefon': 15, 'benq': 31, 'benq-siemens': 42, 'bird': 34, 'blackberry': 36, 'blu': 67, 'bosch': 10, '8bq': 10, 'casio': 77, 'cat': 89, 'celkon': 75, 'chea': 24, '5coolpad': 10, 'dell': 61, '4ee': 10, 'emporia': 93, '6energizer': 10, 'ericsson': 2, 'eten': 40, 'fujitsusiemens': 50, 'garmin-asus': 65, 'gigabyte': 47, 'gionee': 92, '7google': 10, 'haier': 33, 'hp': 41, 'htc': 45, 'huawei': 58, 'i-mate': 35, 'i-mobile': 52, 'icemobile': 69, 'innostream': 29, 'inq': 60, '2intex': 10, 'jolla': 84, 'karbonn': 83, 'kyocera': 17, 'lava': 94, '9leeco': 10, 'lenovo': 73, 'lg': 20, 'maxon': 14, 'maxwest': 87, 'meizu': 74, 'micromax': 66, 'microsoft': 64, 'mitac': 25, 'mitsubishi': 8, 'modu': 63, 'motorola': 4, 'mwg': 56, 'nec': 12, 'neonode': 22, 'niu': 79, 'nokia': 1, 'nvidia': 97, 'o2': 30, 'oneplus': 95, 'oppo': 82, 'orange': 71, 'palm': 27, 'panasonic': 6, 'pantech': 32, 'parla': 81, 'philips': 11, 'plum': 72, '1posh': 10, 'prestigio': 86, '3qmobile': 10, 'qtek': 38, 'sagem': 13, 'samsung': 9, 'sendo': 18, 'sewon': 26, 'sharp': 23, 'siemens': 3, 'sonim': 54, 'sony': 7, 'sonyericsson': 19, 'spice': 68, 't-mobile': 55, 'tel.me.': 21, 'telit': 16, 'thuraya': 49, 'toshiba': 44, 'unnecto': 91, 'vertu': 39, 'verykool': 70, 'vivo': 98, 'vkmobile': 37, 'vodafone': 53, 'wiko': 96, 'wnd': 51, 'xcute': 43, 'xiaomi': 80, 'xolo': 85, 'yezz': 78, 'yota': 99, '0yu': 10, 'zte': 62
    }
},
{
    'reference': 'sSIMTypes',
    'category': 'general',
    'reference_identifiers': ['sim'],    
    'type': 'csv',    
    'values': {
        'mini': 1, 'micro': 2, 'nano': 3
    }
},
{
    'reference': 'sNumberSIMs',
    'category': 'general',
    'reference_identifiers': ['sim'],    
    'type': 'csv',
    'values': {
        'dual': 1, 'two': 1, '2': 1,
        'triple': 2, 'three': 2, '3': 2,
        'quad': 3, 'four': 3, '4': 3
    }
},
{
    'reference': 'sOSes',
    'category': 'value',    
    'identifiers': ['android', 'ios', 'windows', 'symbian', 'feature phone', 'rim', 'bada', 'firefox'],
    'type': 'csv',
    'values': {
        'feature phone': 1, 'android': 2, 'ios': 3, 'windows': 4, 'symbian': 5, 'rim': 6, 'bada': 7, 'firefox': 9
    }
},
{
    'reference': 'nCpuMHzMin',
    'category': 'general',
    'reference_identifiers': ['phone', 'processor', 'cpu'],    
    'pos': ['JJ', 'RB'],
    'type': 'integer',
    'pattern': '\d+'
},
{
    'reference': 'nCPUCoresMin',
    'category': 'general',
    'reference_identifiers': ['core', 'cores'],    
    'type': 'integer',
    'values': {
        'single': 1, 'one': 1, '1': 1,
        'dual': 2, 'two': 2, '2': 2,
        'quad': 4, 'four': 4, '4': 4,
        'octa': 8, 'eight': 8, '8': 8
    }
},
{    
    'reference': 'nRamMin',
    'category': 'general',
    'reference_identifiers': ['ram', 'memory', 'main memory'],
    'pos': ['JJ'],
    'type': 'integer',
    'pattern': '\d+'
},
{    
    'reference': 'nIntMemMin',
    'category': 'general',
    'reference_identifiers': ['memory', 'internal memory', 'storage', 'storage space', 'storage size', 'capacity'],
    'pos': ['JJ'],
    'type': 'integer',
    'pattern': '\d+'
},
{
    'reference': 'idCardslot',
    'category': 'general',
    'reference_identifiers': ['card', 'memory card', 'card slot', 'expandable memory'],
    'type': 'radio',
    'values': {
        'yes': 1, 'no': 3
    }
},
{
    'reference': 'nDisplayResMin',
    'category': 'general',
    'reference_identifiers': ['resolution'],    
    'pos': ['JJ'],
    'type': 'integer',
    'pattern': '\d+'
},
{
    'reference': 'fDisplayInchesMin',
    'category': 'general',
    'reference_identifiers': ['screen', 'screen size', 'inch'],
    'pos': ['JJ'],
    'type': 'float',
    'pattern': '\d\.\d'
},
{
    'reference': 'nDisplayDensityMin',
    'category': 'general',
    'reference_identifiers': ['pixel density', 'display density', 'screen density', 'ppi'],
    'pos': ['JJ'],
    'type': 'integer',
    'pattern': '\d+'
},
{
    'reference': 'sDisplayTechs',
    'category': 'value',
    'identifiers': ['ips', 'oled', 'amoled'],
    'type': 'csv',
    'values': {
        'ips': 1,
        'oled': 2, 'amoled': 2
    }
},
{
    'reference': 'idTouchscreen',
    'category': 'value',
    'identifiers': ['touch screen', 'touchscreen'],
    'type': 'radio',
    'values': {
        'yes': 1, 'no': 0
    }
},
{
    'reference': 'nCamPrimMin',
    'category': 'general',
    'reference_identifiers': ['camera', 'primary camera', 'back camera', 'rear camera', 'main camera'],    
    'pos': ['JJ'],
    'type': 'integer',
    'pattern': '\d+'
},
{
    'reference': 'nCamSecMin',
    'category': 'general',
    'reference_identifiers': ['camera', 'secondary camera', 'front camera', 'selfie camera'],
    'pos': ['JJ'],
    'type': 'integer',
    'pattern': '\d+'
},
{
    'reference': 'chkFrontflash',
    'category': 'value',
    'identifiers': ['front flash'],   
    'type': 'check'
},
{
    'reference': 'chkCameraOIS',
    'category': 'value',
    'identifiers': ['ois', 'optical image stabilisation', 'image stabilisation'],    
    'type': 'check'
},
{
    'reference': 'chk35mm',
    'category': 'value',
    'identifiers': ['audio jack', '3.5 mm', '3.5 mm jack', 'audio port', '3.5 mm port', '3.5 millimetre', '3.5 millimeter'],   
    'type': 'check'
},
{
    'reference': 'chkStereoSpk',
    'category': 'value',
    'identifiers': ['stereo speakers', 'speakers', 'speaker'],    
    'type': 'check'
},
{
    'reference': 'chkAccelerometer',
    'category': 'value',
    'identifiers': ['accelerometer'],    
    'type': 'check'
},
{
    'reference': 'chkGyro',
    'category': 'value',
    'identifiers': ['gyro', 'gyroscope'],
    'type': 'check'
},
{
    'reference': 'chkCompass',
    'category': 'value',
    'identifiers': ['compass'],    
    'type': 'check'
},
{
    'reference': 'chkProximity',
    'category': 'value',
    'identifiers': ['proximity', 'proximity sensor'],    
    'type': 'check'
},
{
    'reference': 'chkBarometer',
    'category': 'value',
    'identifiers': ['barometer', 'pressure sensor'],    
    'type': 'check'
},
{
    'reference': 'chkTemperature',
    'category': 'value',
    'identifiers': ['temperature sensor'],    
    'type': 'check'
},
{
    'reference': 'chkHumidity',
    'category': 'value',
    'identifiers': ['humidity sensor'],    
    'type': 'check'
},
{
    'reference': 'chkHeartrate',
    'category': 'value',
    'identifiers': ['heart rate sensor', 'pulse detector', 'heartbeat sensor'],    
    'type': 'check'
},
{
    'reference': 'chkFingerprint',
    'category': 'value',
    'identifiers': ['fingerprint', 'fingerprint scanner', 'fingerprint sensor'],    
    'type': 'check'
},
{
    'reference': 'chkNFC',
    'category': 'value',
    'identifiers': ['nfc', 'near field communication'],    
    'type': 'check'
},
{
    'reference': 'chkInfrared',
    'category': 'value',
    'identifiers': ['infrared'],    
    'type': 'check'
},
{
    'reference': 'chkFMradio',
    'category': 'value',
    'identifiers': ['radio', 'fm radio'],    
    'type': 'check'
},
{
    'reference': 'nBatCapacityMin',
    'category': 'general',
    'reference_identifiers': ['battery', 'battery capacity', 'battery life'],
    'pos': ['JJ'],
    'type': 'integer',
    'pattern': '\d+'
},
{
    'reference': 'idBatRemovable',
    'category': 'value',
    'identifiers': ['removable battery'],    
    'type': 'radio',
    'values': {
        'yes': 1, 'no': 2
    }
}]