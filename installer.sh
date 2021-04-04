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
PIP_APT_PKGNAME="python3-pip"
PROG_DEPENDENCIES="curl wget python3-venv python3-wheel python3-setuptools ubertooth ubertooth-firmware"
#End Script Constants Declaration

# cd to script location so file copy commands work
cd "${0%/*}" || exit

# Check to make sure being run with root/sudo perms
if [ $(whoami) != root ]; then
	echo "This script must be run as root or with sudo for it to work."
	echo "Please re-run this script as root or with sudo"
	exit
fi

#Try to determine what Debian based distro we're running so we can add the
#proper APT repository for kismet.
DISTRO_NAME=$(cat /etc/os-release | grep -e ^NAME | cut -d \" -f 2)
DISTRO_VERSION_ID=$(cat /etc/os-release | grep -e ^VERSION_ID | cut -d \" -f 2)
DISTRO_VERSION_NAME=$(cat /etc/os-release | grep -e ^VERSION_CODENAME | cut -d \" -f 2)

if [ ! -f /etc/apt/sources.list.d/kismet.list ]; then
  case $DISTRO_NAME in
    "Ubuntu")
      case $DISTRO_VERSION_ID in
        "20.04") #Ubuntu 20.04 (latest LTS version as of right now)
          echo "Ubuntu 20.04 Detected. Installing Kismet APT repository..."

          wget -O - https://www.kismetwireless.net/repos/kismet-release.gpg.key | apt-key add -
          echo 'deb https://www.kismetwireless.net/repos/apt/release/focal focal main' | tee /etc/apt/sources.list.d/kismet.list
          apt update
          ;;
        "18.04" | "16.04")
          echo "This Ubuntu version is not supported for bluemon. Aborting installation..."
          exit 1
          ;;
        *) #versions of Ubuntu newer than 20.04, i.e. 20.10
          echo "Detected an Ubuntu Release version which does not have a Kismet APT Repository."
          echo "Defaulting to the Kismet APT Repository for Kali, this may cause issues..."
          wget -O - https://www.kismetwireless.net/repos/kismet-release.gpg.key | apt-key add -
	  echo 'deb https://www.kismetwireless.net/repos/apt/release/kali kali main' | tee /etc/apt/sources.list.d/kismet.list
          ;;
      esac
      ;;

    "Debian" | "Raspbian")
      case $DISTRO_VERSION_NAME in
        "buster" | "Buster")
          wget -O - https://www.kismetwireless.net/repos/kismet-release.gpg.key | apt-key add -
          echo 'deb https://www.kismetwireless.net/repos/apt/release/buster buster main' | tee /etc/apt/sources.list.d/kismet.list
          apt update
          ;;
        *) #Don't even try to proceed for something that's not Debian Buster.
          echo "This Debian/Raspbian version is not supported for bluemon. Aborting installation..."
          exit 1
          ;;
      esac
      ;;

    "Kali GNU/Linux")
      wget -O - https://www.kismetwireless.net/repos/kismet-release.gpg.key | apt-key add -
      echo 'deb https://www.kismetwireless.net/repos/apt/release/kali kali main' | tee /etc/apt/sources.list.d/kismet.list
      apt update
      ;;

    *) #Fail for distros that are not any of the previous.
      echo "This OS is not supported for bluemon. Aborting installation..."
      exit 1
      ;;
  esac
fi
# Update the APT package lists before we go further, in case user hasn't
# pulled updated package manifests in a while.
apt update

# Check if Kismet and its dependencies are installed, install if not present
if ! dpkg -s $KISMET_APT_PKGS > /dev/null 2>&1; then
	echo "Installing Kismet Packages..."
	apt install -y $KISMET_APT_PKGS
else
	echo "Kismet Packages already installed, continuing..."
fi

if ! dpkg -s "$PROG_DEPENDENCIES" > /dev/null 2>&1; then
  echo "Installing Program Dependencies..."
  apt install -y $PROG_DEPENDENCIES
else
  echo "Dependencies already installed, continuing..."
fi

# Check if pip3 is installed, install if not present
if ! dpkg -s $PIP_APT_PKGNAME > /dev/null 2>&1; then
	echo "Installing PIP3..."
	apt install -y $PIP_APT_PKGNAME
else
	echo "PIP3 already installed, continuing..."
fi

#Create the venv and load the dependencies
python3 -m venv $PROG_EXEC_DIR/venv
source $PROG_EXEC_DIR/venv/bin/activate
pip3 install -r requirements.txt
deactivate

# Check if user already exists, create if it does not
if ! getent passwd $PROG_USERNAME > /dev/null 2>&1; then
	echo "Creating user $PROG_USERNAME..."
	useradd -d $PROG_DATA_DIR -r $PROG_USERNAME
	chsh -s /sbin/nologin $PROG_USERNAME
fi

#Check if group already exists, create if it does not
if ! getent group $PROG_GROUPNAME > /dev/null 2>&1; then
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
if ! ls $PROG_DATA_DIR > /dev/null 2>&1; then
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
if ! ls $PROG_EXEC_DIR > /dev/null 2>&1; then
  echo "Creating directory $PROG_EXEC_DIR..."
  mkdir -p $PROG_EXEC_DIR
  chown -R $PROG_USERNAME:$PROG_GROUPNAME $PROG_EXEC_DIR
  chmod 750 $PROG_EXEC_DIR
fi

#Install service executables (this will overwrite any existing binary)
cp bluemon-kismet.py $PROG_EXEC_DIR/bluemon-kismet.py
cp bluemon-unix.py $PROG_EXEC_DIR/bluemon-unix.py
cp bluemon-ubertooth-scan.sh $PROG_EXEC_DIR/bluemon-ubertooth-scan
cp -r notifications $PROG_EXEC_DIR
chmod +x $PROG_EXEC_DIR/bluemon-kismet.py
chmod +x $PROG_EXEC_DIR/bluemon-unix.py
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
cp devices.conf.example /etc/bluemon
cp notifications.conf.example /etc/bluemon

#Configure Kismet Service
sed -i "s/root/$PROG_USERNAME/" /usr/lib/systemd/system/kismet.service
cp kismet_site.conf.example /etc/kismet/kismet_site.conf
cp kismet_site.conf.example /etc/kismet
systemctl enable kismet
systemctl start kismet
echo "Waiting for kismet startup to complete..."
#Loop until we can hit Kismet's API (should return a 401 when kismet is up)
#Note that curl will return 0 here even though an HTTP error code is received.
while true; do
  curl http://localhost:2501/system/status.json > /dev/null 2>&1 && break
  sleep 0.5
done
#Wait a few more seconds to make sure kismet's ready.
sleep 5
KISMET_ADMIN_PASSWORD="$(openssl rand -hex 20)"
curl -d "username=admin&password=$KISMET_ADMIN_PASSWORD" http://localhost:2501/session/set_password
API_TOKEN="$(curl -f -d 'json={"name": "bluemon", "role": "readonly", duration: 0}' http://admin:$KISMET_ADMIN_PASSWORD@localhost:2501/auth/apikey/generate.cmd)"
if [ $? != 0 ]; then
  echo "Failed to generate Kismet API token for Bluemon Services."
  echo "Check Kismet's documentation to determine how to do this manually."
  API_TOKEN="error"
fi

#Create default config files from sample configs
cp /etc/bluemon/bluemon.conf.example /etc/bluemon/bluemon.conf
cp /etc/bluemon/zones.conf.example /etc/bluemon/zones.conf
cp /etc/bluemon/devices.conf.example /etc/bluemon/devices.conf
cp /etc/bluemon/notifications.conf.example /etc/bluemon/notifications.conf

#set the API token in Bluemon's config.
sed -i "s/api_token = none/api_token=$API_TOKEN/" /etc/bluemon/bluemon.conf

#Start the Service (Can't do this until config files have been setup).
#systemctl start bluemon-kismet.service

#Enable the bluemon-unix socket so its listening if user sets up ubertooth
systemctl enable bluemon-unix.socket
systemctl start bluemon-unix.socket

#Install the crontab entry (commented out) if its not already present
CRONTAB_ENTRY="#*/2 * * * *	bluemon	/opt/bluemon/bluemon-ubertooth-scan"
if ! grep -Fxq "$CRONTAB_ENTRY" /etc/crontab; then
  echo "$CRONTAB_ENTRY" >> /etc/crontab
fi
#Install is done, provide post-install instructions to user and exit.
echo "Installation Complete!"
echo "The BT surveillance program has been installed."
echo "Please complete the post-install configuration to finish deployment."
echo "You will need to modify the config files in /etc/bluemon before starting the service."
echo "You can access kismet by going to http://localhost:2501 in your browser."
echo "Your kismet login is:"
echo -e "\tUsername: admin"
echo -e "\tPassword: $KISMET_ADMIN_PASSWORD\n"
echo "You may need to adjust your firewall to access kismet from other devices."
echo "After completing post-install configuration, you will need to activate"
echo "and start the needed bluemon services for your deployment using the"
echo "following steps run with sudo or as root:"
echo -e "\n1. Kismet events processor:"
echo -e "\ta. systemctl enable bluemon-kismet"
echo -e "\tb. systemctl start bluemon-kismet\n"
echo -e "2. Ubertooth events processing:"
echo -e "\ta. Uncomment the bluemon-ubertooth-scan line in /etc/crontab"
echo -e "\tb. tsystemctl start bluemon-unix.socket\n"
echo -e "3. Notification Server:"
echo -e "\ta. systemctl enable bluemon-notify.service"
echo -e "\tb. systemctl start bluemon-notify.service"