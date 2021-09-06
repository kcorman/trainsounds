while :
do
	echo "Running main python script"
	python3 /home/pi/stuff/trainchug.py > /dev/null
	echo "Script stopped. Restarting it..."
	sleep 5
done
