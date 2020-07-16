import json
import logging
from random import randrange

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)

region = "eu-central-1"
organisations = boto3.client("organizations")


def create_aws_account(emailAddress, accountName):
    response = organisations.create_account(
        Email=emailAddress,
        AccountName=accountName
    )
    return response['CreateAccountStatus']


def get_create_aws_account_status(create_account_request_id):
    response = organisations.describe_create_account_status(
        CreateAccountRequestId=create_account_request_id
    )
    return response['CreateAccountStatus']


def get_root_organisational_id():
    response = organisations.list_roots()
    return response['Roots'][0]['Id']


def check_ou(root_organisational_unit, organisational_unit_name):
    response = organisations.list_organizational_units_for_parent(
        ParentId=root_organisational_unit
    )
    ou_exists = False
    ou_exists_response = {"ou_exists": ou_exists}
    organisational_units = response['OrganizationalUnits']
    if len(organisational_units) > 0:
        for ou in organisational_units:

            if ou['Name'] == organisational_unit_name:
                ou_exists = True
                ou_exists_response["ou_exists"] = ou_exists
                ou_exists_response["id"] = ou['Id']
                break
    return ou_exists_response


# Create organisational unit
def create_ou(parentId, ouName):
    print("Organisational Unit created")
    response = organisations.create_organizational_unit(
        ParentId=parentId,
        Name=ouName
    )
    return response['OrganizationalUnit']['Id']


# Move Organisational Unit
def move_ou(account_id, root_organisational_id, organisational_unit_id):
    response = organisations.move_account(
        AccountId=account_id,
        SourceParentId=root_organisational_id,
        DestinationParentId=organisational_unit_id
    )
    return response


def check_account(requestId):
    print("Checking requestId " + requestId)
    if requestId is None:
        ClientError


def function(object):
    try:
        # Step 1: A request to the Organisations API is made with the required information
        organisations_account_response = create_aws_account(object['rootEmailAddress'], object['accountName'])
        state = organisations_account_response['State']
        # Step 2: Check if the request to create an account was valid. Retry if necessary
        check_account(organisations_account_response['Id'])
        # Step 3: Wait until the request is completed
        while state != 'SUCCEEDED':
            response = get_create_aws_account_status(organisations_account_response['Id'])
            state = response['State']
            if state == 'FAILED':
                ClientError
        # Step 4: Retrieve the account id
        response = get_create_aws_account_status(organisations_account_response['Id'])
        account_id = response['AccountId']
        # Step 5: Get the organisational root id
        root_organisational_id = get_root_organisational_id()
        # Step 6: Create an organisational unit based on the business Unit, if the organisational unit does not exist
        check_ou_response = check_ou(root_organisational_id, object['organisationalUnit'])
        if check_ou_response['ou_exists']:
            # Get the requesters ou id
            requester_ou_id = check_ou_response['id']
        else:
            # Organisational unit does not exist, lets create it
            requester_ou_id = create_ou(root_organisational_id, object['organisationalUnit'])
        # Step 7: Move the created account to the created organisational unit
        move_ou_response = move_ou(account_id, root_organisational_id, requester_ou_id)

    except ClientError as e:
        logging.error(e)


if __name__ == '__main__':
    create_account = {
        "emailAddress": "example@example.com",
        "accountName": "Test Account",
        "organisationalUnit": "Test Business Unit"
    }
    function(create_account)
