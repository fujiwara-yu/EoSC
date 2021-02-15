#!/bin/sh

echo "平均適合率"
echo "時系列の考慮あり"
echo "angular.js"
python scripts/evaluation_ap/pickle_ap_first_user.py angularjs 64
echo "bootstrap"
python scripts/evaluation_ap/pickle_ap_first_user.py bootstrap 48
echo "jquery"
python scripts/evaluation_ap/pickle_ap_first_user.py jquery 25
echo "rails"
python scripts/evaluation_ap/pickle_ap_first_user.py rails 47
