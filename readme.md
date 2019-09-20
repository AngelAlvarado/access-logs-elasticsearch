# Batch Apache access log files into ElasticSearch

This repo let's you setup a data pipeline to stream access log files into ElasticSearch. The pipeline is automated using Docker, Streamsets, Geolite, Elasticsearch and Kibana. 

## Requirements:

* Docker
* Docker compose

## Instructions:

Access Kibana via http://localhost:5601.

A [Dashboard](http://localhost:5601/app/kibana#/dashboard/ApacheWeblog-Dashboard) and individual visualizations will be created automatically during the docker build.

[![dashboard](images/dashboard.png?raw=true)](images/dashboard.png)

### ToDos
 airflow instructions
 create ES index using a DAG
 insert data into ES using a DAG 