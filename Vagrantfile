# -*- mode: ruby -*-
# vi: set ft=ruby :

root_bootstrap = <<-EOF
  apt-get update
  apt-get install -y git make python python-dev python-pip libffi-dev
  pip install -U pip
  hash -r
  pip install virtualenv
EOF

user_bootstrap = <<-EOF
  git clone https://github.com/llimllib/limbo
  virtualenv limbo
EOF

Vagrant.configure(2) do |config|
  config.vm.box = "hashicorp/precise64"
  config.vm.provision :shell, inline: root_bootstrap
  config.vm.provision :shell, inline: user_bootstrap, privileged: false
end
