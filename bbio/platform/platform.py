

def detect_platform():
  """ Attempt to detect the current platform. Returns one of: 'BeagleBone 3.2',
      'BeagleBone >=3.8'. """
  platform = ''
  with open('/proc/cpuinfo', 'rb') as f:
    cpuinfo = f.read().lower() 
  if ('armv7' in cpuinfo and 
     ('am335x' in cpuinfo or 'am33xx' in cpuinfo)):
    platform = 'BeagleBone'

  import commands
  uname_status, uname = commands.getstatusoutput('uname -a')
  if uname_status > 0:
    exit('uname failed, cannot detect kernel version! uname output:\n %s' % uname)
  if ('3.2' in uname):
    platform += ' 3.2'
  else:
    platform += ' >=3.8'

  return platform
