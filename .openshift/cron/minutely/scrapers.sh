#!/bin/bash

if [ ! -f $OPENSHIFT_DATA_DIR/last_run ]; then
	touch $OPENSHIFT_DATA_DIR/last_run
fi
if [[ $(find $OPENSHIFT_DATA_DIR/last_run -mmin +1) ]]; then #run every 5 mins
	rm -f $OPENSHIFT_DATA_DIR/last_run
	touch $OPENSHIFT_DATA_DIR/last_run
    python ${OPENSHIFT_REPO_DIR}/wsgi/scrapers.py
fi
