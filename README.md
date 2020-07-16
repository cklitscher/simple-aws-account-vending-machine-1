## Description: Simple AWS Account Vending Machine 

This repository contains a solution for the creation of an AWS Account within an AWS organisation. It is a simple solution meaning, it creates one account and one account only. The code 
is written in python and is written with the intention of being run locally.

### Arguments

The Account Vending machine takes a simple JSON object consisting of arguments. They are


* emailAddress - The root email address of the AWS account
* accountName - The name of the account
* organisationalUnit - The organisational unit you wish to place the account in

#### Language: Python

#### Repository Structure:

* [README.md](README.md)
* [function.py](function.py)
* [requirements.txt](requirements.txt)