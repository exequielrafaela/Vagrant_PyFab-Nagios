# Vagrant_PyFab-Nagios

## Documentation:

http://www.binbash.com.ar/virtualization/vagrant/vagrant-bvox-nagios-linux

http://www.binbash.com.ar/os/gnu-linux/ubuntu-1/nagios-4-ubuntu-14-04

NOTE: Remember to check the "Doc" folder in the repository.

### Useful URLS:

http://nagios-plugins.org/doc/man/check_http.html

### Screenshot

![alt tag](https://github.com/exequielrafaela/Vagrant_PyFab-Nagios/blob/master/images/Nagios_web-admin.png)

### Consider:

  That check_nrpe looks up the command given in it’s argument locally in which is defined the name of the command that should be configured on the remote host in /etc/nagios/nrpe_local.cfg.

  Passing arguments to command defined in /etc/nagios/objects/commands.cfg and passing it as a whole argument to the check_nrpe command won’t work unless the remote host is configured to allow command argument processing in /etc/nagios/nrpe.cfg.
  
  Changing the parameter dont_blame_nrpe=0 to dont_blame_nrpe=1 will do the trick on that!
