#!/bin/sh

echo "3 feature importance"
echo "angular.js"
python scripts/evaluation_feature_importance/evaluation_ap_feature_3.py angularjs 64
echo "bootstrap"
python scripts/evaluation_feature_importance/evaluation_ap_feature_3.py bootstrap 48
echo "jquery"
python scripts/evaluation_feature_importance/evaluation_ap_feature_3.py jquery 25
echo "rails"
python scripts/evaluation_feature_importance/evaluation_ap_feature_3.py rails 47

