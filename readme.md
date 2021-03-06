# Streaming Apache access log files into ElasticSearch

This repo let's you setup a data pipeline to stream access log files into ElasticSearch. The pipeline is automated using Docker, Streamsets, Geolite, Elasticsearch and Kibana. 

## Requirements:

* Docker
* Docker compose

## Instructions:

Once this repo has been cloned, open your command line and initialize the docker containers using: $ docker-compose up. This can take a while.

Once the containers are up and running you’ll to execute only one step manually to kick off the datacollector and have the whole pipeline working.

1.-Import the [pipeline](access_log_elasticsearch_pipeline.json) into streamsets by going to http://localhost:18630

[![importing-pipeline](images/import-pipeline-streamsets.png?raw=true)](images/import-pipeline-streamsets.png) 

* You can use a custom name and description.

You should see the following pipeline

[![pipeline](images/complete-pipeline-streamsets.png?raw=true)](images/complete-pipeline-streamsets.png)

Preview or Start the pipeline right away.

[![start-pipeline](images/preview-start-pipeline.png?raw=true)](images/preview-start-pipeline.png)


Access Kibana via http://localhost:5601.

A [Dashboard](http://localhost:5601/app/kibana#/dashboard/ApacheWeblog-Dashboard) and individual visualizations will be created automatically during the docker build.

[![dashboard](images/dashboard.png?raw=true)](images/dashboard.png)
