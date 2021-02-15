#!/bin/sh

echo "平均適合率"
echo "時系列の考慮なし"
echo "angular.js"
python scripts/evaluation_ap/evaluation_ap_no_series.py angularjs 64
echo "bootstrap"
python scripts/evaluation_ap/evaluation_ap_no_series.py bootstrap 48
echo "jquery"
python scripts/evaluation_ap/evaluation_ap_no_series.py jquery 25
echo "rails"
python scripts/evaluation_ap/evaluation_ap_no_series.py rails 47
