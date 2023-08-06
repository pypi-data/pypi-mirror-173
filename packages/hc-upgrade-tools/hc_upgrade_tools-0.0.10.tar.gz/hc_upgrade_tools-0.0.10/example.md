## download artifacts backend for auda-data-center

```
python3 src/hc_upgrade_tools/skeleton.py dl-pkg \
--host=10.0.20.115 \
--port=7070 \
--projectID=196 \
--target-sub-folder-in-artifact=archive \
--project-dir=/Users/shixukai/Downloads/S004/data_center \
--extra-symbolics "current/dock-compose.yml:shared/dock-compose.yml" \
"current/backend/config.js:shared/config.js" \
"current/backend/public:shared/public/"

```