VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "hashicorp/precise64"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 512
    vb.cpus = 2
  end

  config.vm.network "private_network", type: "dhcp"

  config.hostmanager.enabled = true
  config.hostmanager.ip_resolver = proc do |vm, resolving_vm|
	  if vm.id
		`VBoxManage guestproperty get #{vm.id} "/VirtualBox/GuestInfo/Net/1/V4/IP"`.split()[1]
	  end
  end

  config.vm.define :server do |srv|
    srv.vm.hostname = "nagios-server"
    srv.vm.synced_folder "server/", "/usr/local/nagios/etc", create: true
    srv.vm.network "forwarded_port", guest: 80, host: 8080
    srv.vm.provision :fabric do |fabric|
      fabric.fabfile_path = "./fabfile.py"
      fabric.tasks = ["srv", ]
    end
  end

  config.vm.define :client do |cl|
    cl.vm.hostname = "nagios-client"
    cl.vm.synced_folder "client/", "/usr/local/nagios/etc", create: true
    cl.vm.provision :fabric do |fabric|
      fabric.fabfile_path = "./fabfile.py"
      fabric.tasks = ["cl", ]
    end
  end
end
