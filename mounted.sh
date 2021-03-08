#!/bin/bash

if (mount | grep $1)
then 
	echo "Mounted"
else
	echo "Not Mounted"
fi
