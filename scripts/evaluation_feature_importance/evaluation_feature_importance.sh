#!/bin/sh

echo "feature importance"
echo "angular.js"
python scripts/evaluation_feature_importance/evaluation_feature_importance.py angularjs
echo "bootstrap"
python scripts/evaluation_feature_importance/evaluation_feature_importance.py bootstrap
echo "jquery"
python scripts/evaluation_feature_importance/evaluation_feature_importance.py jquery
echo "rails"
python scripts/evaluation_feature_importance/evaluation_feature_importance.py rails
