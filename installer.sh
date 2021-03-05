#!/bin/bash
# This is an installation script for the BT Surveillance Framework
# Eventually we hope to do native packages for the OS, but in the meantime,
# This shell script should set up the application for you.

#Begin Script Constants Declaration
PROG_USERNAME=bluemon
PROG_GROUPNAME=bluemon
PROG_DATA_DIR="/var/lib/bluemon"
PROG_EXEC_DIR="/opt/bluemon"
KISMET_APT_PKGS="kismet"
PIP_APT_PKGNAME=python3-pip
PROG_DEPENDENCIES=curl
KISMET_PIP_PKGNAME=kismetexternal
#End Script Constants Declaration

# cd to script location so file copy commands work
cd "${0%/*}" || exit

# Check to make sure being run with root/sudo perms
if [ `whoami` != root ]; then
	echo "This script must be run as root or with sudo for it to work."
	echo "Please re-run this script as root or with sudo"
	exit
fi

# Check if Kismet and its dependencies are installed, install if not present
dpkg -s $KISMET_APT_PKGS > /dev/null 2>&1
if [ $? != 0 ]; then
	echo "Installing Kismet Packages..."
	apt install -y $KISMET_APT_PKGS
else
	echo "Kismet Packages already installed, continuing..."
fi
dpkg -s $PROG_DEPENDENCIES > /dev/null 2>&1
if [ $? != 0 ]; then
  echo "Installing Program Dependencies..."
  apt install -y $PROG_DEPENDENCIES
else
  echo "Dependencies already installed, continuing..."
fi

# Check if pip3 is installed, install if not present
dpkg -s $PIP_APT_PKGNAME > /dev/null 2>&1
if [ $? != 0 ]; then
	echo "Installing PIP3..."
	apt install -y $PIP_APT_PKGNAME
else
	echo "PIP3 already installed, continuing..."
fi

#Replace this with loading from requirements.txt once specifics of using a venv
#are worked out. For now this should be left commented out since we don't use
#this pip package anymore.
# Check if kismetexternal pip package is installed, install if not present
# If present, update to latest version.
#pip3 show kismetexternal > /dev/null 2>&1
#if [ $? != 0 ]; then
#	echo "Installing kismetexternal python package from pip..."
#	pip3 install kismetexternal
#else
#	echo "Updating installed kismetexernal python package..."
#	pip3 install kismetexternal --upgrade --upgrade-strategy=eager
#fi

# Check if user already exists, create if it does not

getent passwd $PROG_USERNAME > /dev/null 2>&1
if [ $? != 0 ]; then
	echo "Creating user $PROG_USERNAME..."
	useradd -d $PROG_DATA_DIR -r $PROG_USERNAME
	chsh -s /sbin/nologin $PROG_USERNAME
fi

#Check if group already exists, create if it does not

getent group $PROG_GROUPNAME > /dev/null 2>&1
if [ $? != 0 ]; then
	echo "Creating group $PROG_GROUPNAME..."
	groupadd $PROG_GROUPNAME
fi

#Check if user is member of group, add if not
GROUP_MEMS="$(groupmems -g $PROG_GROUPNAME -l)"
if [[ "$GROUP_MEMS" != *"$PROG_USERNAME"* ]]; then
	echo "Adding $PROG_USERNAME to $PROG_GROUPNAME..."
	adduser $PROG_USERNAME $PROG_GROUPNAME
	#groupmems has a weird quirk with PAM on Debian based OSes, so we use
	#adduser now instead. You can uncomment the groupmems line if you want
	#The old behavior, but remember to comment the adduser line first.
	#groupmems -g $PROG_GROUPNAME -a $PROG_USERNAME
fi

GROUP_MEMS="$(groupmems -g kismet -l)"
if [[ "$GROUP_MEMS" != *"$PROG_USERNAME"* ]]; then
	echo "Adding $PROG_USERNAME to kismet group..."
	adduser $PROG_USERNAME kismet
	#groupmems has a weird quirk with PAM on Debian based OSes, so we use
	#adduser now instead. You can uncomment the groupmems line if you want
	#The old behavior, but remember to comment the adduser line first.
	#groupmems -g $PROG_GROUPNAME -a $PROG_USERNAME
fi

#For some capture devices that use a serial interface, kismet needs to be
#in the dialout group on Debian OSes so it can attach to the serial device
#under /dev. This is mainly just the nordic RF right now, but other devices
#might need this as well. This will make sure what we run kismet as will be in
#the right group for this to work properly.
GROUP_MEMS="$(groupmems -g dialout -l)"
if [[ "$GROUP_MEMS" != *"$PROG_USERNAME"* ]]; then
	echo "Adding $PROG_USERNAME to dialout group..."
	adduser $PROG_USERNAME dialout
	#groupmems has a weird quirk with PAM on Debian based OSes, so we use
	#adduser now instead. You can uncomment the groupmems line if you want
	#The old behavior, but remember to comment the adduser line first.
	#groupmems -g $PROG_GROUPNAME -a $PROG_USERNAME
fi

#Check if Kismet data directory exists, create it if not
ls $PROG_DATA_DIR > /dev/null 2>&1
if [ $? != 0 ]; then
	echo "Creating kismet data directory"
	mkdir -p $PROG_DATA_DIR
	chown -R $PROG_USERNAME:$PROG_GROUPNAME $PROG_DATA_DIR
	chmod -R 750 $PROG_DATA_DIR
	mkdir $PROG_DATA_DIR/kismet-logs
	chown -R $PROG_USERNAME:$PROG_GROUPNAME $PROG_DATA_DIR/kismet-logs
	chmod -R 750 $PROG_DATA_DIR/kismet-logs
fi


#Deploy the tmpfiles config and reload systemd's config
cp bluemon.conf.systemd-tmpfiles /lib/tmpfiles.d/bluemon.conf
systemd-tmpfiles --create --remove --boot

#Check if directory where bluemon executables stored exists, create if not
ls $PROG_EXEC_DIR > /dev/null 2>&1
if [ $? != 0 ]; then
  echo "Creating directory $PROG_EXEC_DIR..."
  mkdir -p $PROG_EXEC_DIR
  chown -R $PROG_USERNAME:$PROG_GROUPNAME $PROG_EXEC_DIR
  chmod 750 $PROG_EXEC_DIR
fi

#Install service executables (this will overwrite any existing binary)
cp bluemon-kismet.py $PROG_EXEC_DIR/bluemon-kismet
cp bluemon-unix.py $PROG_EXEC_DIR/bluemon-unix
cp bluemon-ubertooth-scan.sh $PROG_EXEC_DIR/bluemon-ubertooth-scan
cp -r notifications $PROG_EXEC_DIR
chmod +x $PROG_EXEC_DIR/bluemon-kismet
chmod +x $PROG_EXEC_DIR/bluemon-unix
chmod +x $PROG_EXEC_DIR/bluemon-ubertooth-scan
chmod +x $PROG_EXEC_DIR/notifications/notifications.py

#Install the systemd services
cp bluemon-kismet.service /etc/systemd/system/
cp bluemon-unix.service /etc/systemd/system/
cp bluemon-unix.socket /etc/systemd/system
cp bluemon-notify.service /etc/systemd/system
#cp bluemon-notify.socket /etc/systemd/system
systemctl daemon-reload

#Create the config directory and copy the sample configs
mkdir /etc/bluemon
chown $PROG_USERNAME:$PROG_GROUPNAME /etc/bluemon
chmod 550 /etc/bluemon
cp bluemon.conf.example /etc/bluemon
cp zones.conf.example /etc/bluemon

#Configure Kismet Service
sed -i "s/root/$PROG_USERNAME/" /usr/lib/systemd/system/kismet.service
cp kismet_site.conf.example /etc/kismet/kismet_site.conf
systemctl enable kismet
systemctl start kismet
#Sleep for 30 seconds to give kismet time to startup on slow devices.
#Note: replace with curl while loop??
echo "Waiting for kismet startup to complete..."
sleep 30
KISMET_ADMIN_PASSWORD="$(openssl rand -hex 20)"
curl -d "username=admin&password=$KISMET_ADMIN_PASSWORD" http://localhost:2501/session/set_password
API_TOKEN="$(curl -f -d 'json={"name": "bluemon", "role": "readonly", duration: 0}' http://admin:$KISMET_ADMIN_PASSWORD@localhost:2501/auth/apikey/generate.cmd)"
if [ $? != 0 ]; then
  echo "Failed to generate Kismet API token for Bluemon Services."
  echo "Check Kismet's documentation to determine how to do this manually."
  API_TOKEN="error"
fi

#Set kismet password for Bluemon
cp /etc/bluemon/bluemon.conf.example /etc/bluemon/bluemon.conf
#sed -i "s/username = kismet/username=admin/" /etc/bluemon/bluemon.conf
#sed -i "s/password = kismet/password=$KISMET_ADMIN_PASSWORD/" /etc/bluemon/bluemon.conf
#Eventually we'll be using Kismet API tokens instead of the kismet username and password.
#The following line (currently commented out) will do the the config work to
#set the API token in Bluemon's config.
sed -i "s/api_token = none/api_token=$API_TOKEN" /etc/bluemon/bluemon.conf

#Start the Service (Can't do this until config files have been setup).
#systemctl start bluemon-kismet.service

#Install the crontab entry (commented out)
echo "#*/2 * * * *	bluemon	/opt/bluemon/bluemon-ubertooth-scan" >> /etc/crontab

#Install is done, provide post-install instructions to user and exit.
echo "Installation Complete!"
echo "The BT surveillance program has been installed."
echo "Please complete the post-install configuration to finish deployment."
echo "You will need to modify the config files in /etc/bluemon before starting the service."