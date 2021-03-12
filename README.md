Rest API Example
================

This application shows simple implementation of a rest API

## Setup

The code can be downloaded from github in terminal by:

    git clone https://github.com/drecker/rest-app.git
    cd rest-app

The server then can be simply started using docker:

    docker build --tag rest-app-docker .
    docker run -p 8080:8000 rest-app-docker

The application can also be run directly:

    pip install -r requirements.txt
    gunicorn -w 4 -b 0.0.0.0:8080 -t 600 --log-level debug "rest_app:create_app()" --preload

## Usage

Once the application is running, following endpoints should be exposed

* `/products/<product-id>/` -- endpoint that follows standard CRUD implementation. That is `GET`
  request will return information of product with given id (or about all of them if no ID is presented),
  `POST` request is used for inserting new product (the required supplied data are `name` and
  `description`). `PUT` request is used for update existing item and `DELETE` for deletion.
* `/offers/product/<product-id>/from/<iso-formatted-date>/to/<iso-formatted-date>/` -- endpoint that
  processes only `GET` requests. It will return all the offers in given time period for given product
  with the price change summary. For example: `/offers/product/1/from/2021-01-01/to/2021-01-01/`
  