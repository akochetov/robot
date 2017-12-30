echo "Setting up service..."
sudo cp robot_btn /etc/init.d/
sudo chmod +x /etc/init.d/robot_btn
sudo update-rc.d robot_btn defaults

echo "Creating logs directory..."
sudo mkdir ./logs
sudo chmod 777 ./logs

echo "Enabling I2C bus..."
sudo sed -i '$ a i2c-bcm2835' /etc/modules
sudo sed -i '$ a i2c-dev' /etc/modules
sudo sed -i -e 's/#dtparam=i2c_arm=on/dtparam=i2c_arm=on/g' /boot/config.txt

echo "Installing I2C tools..."
sudo apt-get install i2c-tools
sudo apt-get install python-smbus 

echo "Installing git..."
sudo apt-get install git

echo "Done."
