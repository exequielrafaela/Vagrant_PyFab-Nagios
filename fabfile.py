from fabric.api import sudo, run, settings, hide, cd, lcd
from termcolor import colored
import os


# nagios_core = 'nagios-4.1.1'
# nagios_plugins = 'nagios-plugins-2.1.1'
# nagios_nrpe = 'nrpe-2.15'

# IMPORTANT => http://nagios-plugins.org/doc/man/
#vagrant@nagios-server:/usr/local/nagios/libexec$ /usr/local/nagios/libexec/check_ping -H 172.28.128.4 -w 500.0,80% -c 1000.0,100% -p 5
#PING OK - Packet loss = 0%, RTA = 0.95 ms|rta=0.948000ms;500.000000;1000.000000;0.000000 pl=0%;80;100;0


def srv():
    with settings(warn_only=True):
        print colored('##########################', 'blue')
        print colored('##### NAGIOS SERVER ######', 'blue')
        print colored('##########################', 'blue')

        sudo('apt-get update')
        sudo('apt-get -y install build-essential apache2 apache2-utils openssl libapache2-mod-php5 libgd2-xpm-dev libssl-dev xinetd unzip')
        #sudo('apt-get install --reinstall make')
        #unzip

#file="/etc/hosts"
#if [ -f "$file" ]
#then
#	echo "$file found."
#else
#	echo "$file not found."
#fi
        run('if [ ! -f "/home/vagrant/nagios-4.1.1.tar.gz" ]; then '
                'wget https://sourceforge.net/projects/nagios/files/nagios-4.x/nagios-4.1.1/nagios-4.1.1.tar.gz; '
            'fi')

        run('if [ ! -f "/home/vagrant/nagios-plugins-2.1.1.tar.gz" ]; then '
                'wget http://www.nagios-plugins.org/download/nagios-plugins-2.1.1.tar.gz; '
            'fi')

        run('if [ ! -f "/home/vagrant/nrpe-2.15.tar.gz" ]; then '
                'wget https://sourceforge.net/projects/nagios/files/nrpe-2.x/nrpe-2.15/nrpe-2.15.tar.gz; '
            'fi')

        sudo('useradd nagios')
        sudo('groupadd nagcmd')
        sudo('usermod -a -G nagcmd nagios')
        sudo('usermod -G nagcmd www-data')

        run('tar -xzf nagios-4.1.1.tar.gz')
        with cd('/home/vagrant/nagios-4.1.1'):
            # run('ls')  # cd /var/www && ls
            #sudo('./configure --with-command-group=nagcmd --with-httpd-conf=/etc/apache2/sites-available')
            sudo('./configure --with-nagios-group=nagios --with-command-group=nagcmd')


            sudo('make all')
            sudo('make install')
            sudo('make install-commandmode')
            sudo('make install-init')
            sudo('make install-config')
            sudo('/usr/bin/install -c -m 644 sample-config/httpd.conf /etc/apache2/sites-available/nagios.conf')
            #sudo('make install-webconf')

        #sudo('chown nagios:nagios /usr/local/nagios/etc/htpasswd.users')
        #sudo('a2ensite nagios')
        sudo('a2enmod rewrite')
        sudo('a2enmod cgi')
        sudo('htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin nagios')

        sudo('ln -s /etc/apache2/sites-available/nagios.conf /etc/apache2/sites-enabled/')

        sudo('service nagios start')
        sudo('a2enmod version')
        sudo('service apache2 restart')

        # run('cd ..')
        run('tar -xzf nagios-plugins-2.1.1.tar.gz')
        with cd('/home/vagrant/nagios-plugins-2.1.1'):
            # sudo('./configure')
            sudo('./configure --with-nagios-user=nagios --with-nagios-group=nagios --with-openssl')
            sudo('make')
            sudo('make install')

        run('tar -xzf nrpe-2.15.tar.gz')
        with cd('/home/vagrant/nrpe-2.15'):
            sudo('./configure --enable-command-args --with-nagios-user=nagios --with-nagios-group=nagios --with-ssl=/usr/bin/openssl --with-ssl-lib=/usr/lib/x86_64-linux-gnu')
            #sudo('./configure --with-ssl=/usr/bin/openssl --with-ssl-lib=/usr/lib/x86_64-linux-gnu')
            sudo('make all')
            sudo('make install')
            sudo('make install-xinetd')
            sudo('make install-daemon-config')

        #sudo('update-rc.d nagios defaults 99')
        sudo('ln -s /etc/init.d/nagios /etc/rcS.d/S99nagios')
        sudo('service apache2 restart')
        sudo('service xinetd restart')
        sudo('service nagios start')

        print colored('##########################', 'blue')
        print colored('## NETWORK CONFIGURATION #', 'blue')
        print colored('##########################', 'blue')
        with hide('output'):
            netconf = sudo('ip addr show')
        print colored(netconf, 'yellow')

#############################################################################
#############################################################################

def cl():
    # type: () -> object
    with settings(warn_only=True):
        print colored('##########################', 'blue')
        print colored('##### NAGIOS CLIENT ######', 'blue')
        print colored('##########################', 'blue')

        sudo('apt-get update')
        sudo('apt-get install -y libssl-dev vsftpd')
        sudo('apt-get -y install build-essential')

        run('if [ ! -f "/home/vagrant/nagios-plugins-2.1.1.tar.gz" ]; then '
                'wget http://www.nagios-plugins.org/download/nagios-plugins-2.1.1.tar.gz; '
            'fi')

        run('if [ ! -f "/home/vagrant/nrpe-2.15.tar.gz" ]; then '
                'wget https://sourceforge.net/projects/nagios/files/nrpe-2.x/nrpe-2.15/nrpe-2.15.tar.gz; '
            'fi')
        #nagiosdownload()

        sudo('useradd nagios')

        run('tar -xzf nagios-plugins-2.1.1.tar.gz')
        with cd('/home/vagrant/nagios-plugins-2.1.1'):
            sudo('./configure')
            sudo('make')
            sudo('make install')

        run('tar -xzf nrpe-2.15.tar.gz')
        with cd('/home/vagrant/nrpe-2.15'):
            sudo('./configure --with-ssl=/usr/bin/openssl --with-ssl-lib=/usr/lib/x86_64-linux-gnu')
            sudo('make all')
            sudo('make install')
            sudo('make install-daemon-config')
            sudo('cp init-script.debian /etc/init.d/nrpe')

        sudo('chmod 755 /etc/init.d/nrpe')
        sudo('update-rc.d nrpe defaults 99')
        sudo('service nrpe start')

        print colored('##########################', 'blue')
        print colored('## NETWORK CONFIGURATION #', 'blue')
        print colored('##########################', 'blue')
        with hide('output'):
            netconf = sudo('ip addr show')
        print colored(netconf, 'yellow')


#############################################################################
#############################################################################

'''
def nagiosdownload():
    if os.path.exists('/home/vagrant/nagios-plugins-2.1.1.tar.gz'):
        print colored(str(os.path.exists('/home/vagrant/nagios-plugins-2.1.1.tar.gz')), 'blue')
        print colored('##############################################', 'blue')
        print colored('nagios-plugins-2.1.1.tar.gz ALREADY DOWNLOADED', 'blue')
        print colored('##############################################', 'blue')
    else:
        print colored('#######################################', 'blue')
        print colored('##### DOWNLOADING NAGIOS PLUGINS ######', 'blue')
        print colored('#######################################', 'blue')
        print colored(str(os.path.exists('/home/vagrant/nagios-plugins-2.1.1.tar.gz')), 'blue')
        run('wget http://www.nagios-plugins.org/download/nagios-plugins-2.1.1.tar.gz')

    if os.path.exists('/home/vagrant/nrpe-2.15.tar.gz'):
        print colored(str(os.path.exists('/home/vagrant/nagios-plugins-2.1.1.tar.gz')), 'blue')
        print colored('###########################################', 'blue')
        print colored('### nrpe-2.15.tar.gz ALREADY DOWNLOADED ###', 'blue')
        print colored('############################################', 'blue')
    else:
        print colored('####################################', 'blue')
        print colored('##### DOWNLOADING NAGIOS NRPE ######', 'blue')
        print colored('####################################', 'blue')
        print colored(str(os.path.exists('/home/vagrant/nrpe-2.15.tar.gz')), 'blue')
        run('wget https://sourceforge.net/projects/nagios/files/nrpe-2.x/nrpe-2.15/nrpe-2.15.tar.gz')
'''

'''
    if not os.path.exists('/home/vagrant/nagios-4.1.1.tar.gz'):
        print colored(str(os.path.exists('/home/vagrant/nagios-plugins-2.1.1.tar.gz')), 'blue')
        print colored('######################################', 'blue')
        print colored('nagios-4.1.1.tar.gz ALREADY DOWNLOADED', 'blue')
        print colored('######################################', 'blue')
    else:
        print colored('####################################', 'blue')
        print colored('##### DOWNLOADING NAGIOS CORE ######', 'blue')
        print colored('####################################', 'blue')
        print colored(str(os.path.exists('/home/vagrant/nagios-4.1.1.tar.gz')), 'blue')
        run('wget https://sourceforge.net/projects/nagios/files/nagios-4.x/nagios-4.1.1/nagios-4.1.1.tar.gz')

    nagiosdownload()
    '''