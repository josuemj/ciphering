#!/bin/bash
set -e
echo 'MediSpft v2.1.0 update'
cp firmware_analizador.bin /opt/medisoft/fw/
cp driver_lab.dll /opt/medisoft/drivers/
systemctl restart medisoft-lab
