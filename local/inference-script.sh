#!/bin/bash
sleap-track labels.slp --video.index 0 --frames 2126,2385,2664,3172,3640,3860,4030,4928,4977,5365,6924,7086,7354,7384,7481,8246,9296,9425,10012,10028 -m models\250504_183857.centroid -m models\250504_183857.centered_instance --controller_port 9000 --publish_port 9001 -o labels.slp.predictions.slp --verbosity json --no-empty-frames
