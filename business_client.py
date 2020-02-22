import requests
import hashlib
import json


def post_request(headers, json_data, url):
    response = requests.request(
        method="POST", url=url, headers=headers, data=json_data)
    return response


test_server = "https://beta.mypaga.com/"
live_Server = "https://www.mypaga.com/"


class Business_Client(object):

    def __init__(self, principal, apiKey, credential, test):
        self.principal = principal
        self.apiKey = apiKey
        self.credential = credential
        self.test = test

    def register_customer(self, reference_number, customer_phone_number, customer_email, first_name, last_name,
                          customer_date_birth, customer_gender):

        endpoint = "paga-webservices/business-rest/secured/registerCustomer"

        data = {'referenceNumber': reference_number,
                'customerPhoneNumber': customer_phone_number,
                'customerEmail': customer_email,
                'customerFirstName': first_name,
                'customerLastName': last_name,
                'customerDateOfBirth': customer_date_birth,
                'customerGender': customer_gender}

        pattern = reference_number + customer_phone_number + \
            first_name + last_name + self.apiKey

        hash_strings = self.generate_hash(pattern)

        # url = self.url(self.test)
        server_url = self.url(self.test) + endpoint
        headers = {
            'credentials': self.credential,
            'Accept': 'application/json',
            'principal': self.principal,
            'hash': hash_strings,
            'Content-Type': 'multipart/form-data'
        }

        customer = json.dumps(data)
        up = {'customer': (customer, "multipart/form-data")}
        response = requests.request(
            method="POST", url=server_url, headers=headers, data=up)
        return response.text

    def money_transfer(self, reference_number, amount, currency, destination_account, destination_bank,
                       sender_principal,
                       sender_credentials, withdrawal_code, source_of_funds, transaction_reference,
                       suppress_recipient_message, locale, alternate_sender_name, mini_recipient_kyc, holding_period):

        endpoint = "paga-webservices/business-rest/secured/moneyTransfer"

        data = {'referenceNumber': reference_number,
                'amount': amount,
                'currency': currency,
                'destinationAccount': destination_account,
                'destinationBank': destination_bank,
                'senderPrincipal': sender_principal,
                'senderCredentials': sender_credentials,
                'withdrawalCode': withdrawal_code,
                'sourceOfFunds': source_of_funds,
                'transferReference': transaction_reference,
                'suppressRecipientMessage': suppress_recipient_message,
                'locale': locale,
                'alternateSenderName': alternate_sender_name,
                'minRecipientKYCLevel': mini_recipient_kyc,
                'holdingPeriod': holding_period}

        pattern = reference_number + amount + destination_account + self.apiKey

        hash_strings = self.generate_hash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)

        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)
        return response.text

    def get_merchants(self, reference_number, locale):
        endpoint = "paga-webservices/business-rest/secured/getMerchants"
        data = {'referenceNumber': reference_number, 'locale': locale}

        pattern = reference_number + self.apiKey

        hash_strings = self.generate_hash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)

        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)
        return response.text

    def airtime_purchase(self, reference_number, amount, currency, destination_number,
                         purchaser_principal, purchaser_credentials, source_of_funds, locale):
        endpoint = "paga-webservices/business-rest/secured/airtimePurchase"

        data = {'referenceNumber': reference_number,
                'amount': amount,
                'currency': currency,
                'destinationPhoneNumber': destination_number,
                'purchaserPrincipal': purchaser_principal,
                'purchaser_principal': purchaser_credentials,
                'sourceOfFunds': source_of_funds,
                'locale': locale}
        pattern = reference_number + \
            str(amount) + destination_number + self.apiKey

        hash_strings = self.generate_hash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)
        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)
        return response.text

    def validate_deposit_to_bank(self, reference_number, amount, currency, destination_bank_uuid,
                                 destination_bank_acct_no, recipient_phone_number,
                                 recipient_mobile_operator_code, recipient_email, recipient_name, locale):
        endpoint = "paga-webservices/business-rest/secured/validateDepositToBank"

        data = {'referenceNumber': reference_number,
                'amount': amount,
                'currency': currency,
                'destinationBankUUID': destination_bank_uuid,
                'destinationBankAccountNumber': destination_bank_acct_no,
                'recipientPhoneNumber': recipient_phone_number,
                'recipientMobileOperatorCode': recipient_mobile_operator_code,
                'recipientEmail': recipient_email,
                'recipientName': recipient_name,
                'locale': locale}

        pattern = reference_number + \
            str(amount) + destination_bank_uuid + \
            destination_bank_acct_no + self.apiKey

        hash_strings = self.generate_hash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)
        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)
        return response.text

    def deposit_to_bank(self, reference_number, amount, currency, destination_bank_uuid,
                        destination_bank_acct_no, recipient_no, recipient_mobile_operator_code,
                        recipient_email, recipient_name, alt_sender_name, suppress_recipient_msg,
                        remarks, locale):
        endpoint = "paga-webservices/business-rest/secured/depositToBank"

        data = {'referenceNumber': reference_number,
                'amount': amount,
                'currency': currency,
                'destinationBankUUID': destination_bank_uuid,
                'destinationBankAccountNumber': destination_bank_acct_no,
                'recipientPhoneNumber': recipient_no,
                'recipientMobileOperatorCode': recipient_mobile_operator_code,
                'recipientEmail': recipient_email,
                'recipientName': recipient_name,
                'alternateSenderName': alt_sender_name,
                'suppressRecipientMessage': suppress_recipient_msg,
                'remarks': remarks,
                'locale': locale}

        pattern = reference_number + str(
            amount) + destination_bank_uuid + destination_bank_acct_no + self.apiKey

        hash_strings = self.generate_hash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)
        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)
        return response.text

    def get_account_balance(self, reference_number, acct_principal, acct_credentials, source_of_funds, locale):

        endpoint = "paga-webservices/business-rest/secured/accountBalance"

        data = {'referenceNumber': reference_number,
                'accountPrincipal': acct_principal,
                'accountCredentials': acct_credentials,
                'sourceOfFunds': source_of_funds,
                'locale': locale}

        pattern = reference_number + self.apiKey

        hash_strings = self.generate_hash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)
        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)

        return response.text

    def get_transaction_history(self, reference_number, acct_principal, acct_credentials, start_date, end_date, locale):

        endpoint = "paga-webservices/business-rest/secured/transactionHistory"

        data = {'referenceNumber': reference_number,
                'accountPrincipal': acct_principal,
                'accountCredentials': acct_credentials,
                'startDateUTC': start_date,
                'endDateUTC': end_date,
                'locale': locale}

        pattern = reference_number + self.apiKey

        hash_strings = self.generate_hash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)
        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)

        return response.text

    def get_recent_transaction_history(self, reference_number, acct_principal, acct_credentials, locale):
        endpoint = "paga-webservices/business-rest/secured/recentTransactionHistory"

        data = {'referenceNumber': reference_number,
                'accountPrincipal': acct_principal,
                'accountCredentials': acct_credentials,
                'locale': locale}

        pattern = reference_number + self.apiKey

        hash_strings = self.generate_hash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)
        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)

        return response.text

    def get_operation_status(self, reference_number, locale):

        endpoint = "paga-webservices/business-rest/secured/getOperationStatus"

        data = {'referenceNumber': reference_number,
                'locale': locale}

        pattern = reference_number + self.apiKey

        hash_strings = self.generate_hash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)
        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)

        return response.text

    def get_banks(self, reference_number, locale):

        endpoint = "paga-webservices/business-rest/secured/getBanks"

        data = {'referenceNumber': reference_number,
                'locale': locale}

        pattern = reference_number + self.apiKey

        hash_strings = self.generate_hash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)
        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)

        return response.text

    def get_merchant_services(self, reference_number, merchant_public_id, locale):
        endpoint = "paga-webservices/business-rest/secured/getMerchantServices"

        data = {'referenceNumber': reference_number,
                'merchantPublicId': merchant_public_id,
                'locale': locale}

        pattern = reference_number + merchant_public_id + self.apiKey

        hash_strings = self.generate_hash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)
        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)

        return response.text

    def get_mobile_operators(self, reference_number, locale):
        endpoint = "paga-webservices/business-rest/secured/getMobileOperators"

        data = {'referenceNumber': reference_number,
                'locale': locale}

        pattern = reference_number + self.apiKey

        hash_strings = self.generate_hash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)
        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)

        return response.text

    def merchant_payment(self, reference_number, amount, currency, merchant_account, merchant_reference_number,
                         merchant_service, purchaser_principal, purchaser_credentials, source_of_funds, locale):
        endpoint = "paga-webservices/business-rest/secured/merchantPayment"

        data = {'referenceNumber': reference_number,
                'amount': amount,
                'currency': currency,
                'merchantAccount': merchant_account,
                'merchantReferenceNumber': merchant_reference_number,
                'merchantService': merchant_service,
                'purchaserPrincipal': purchaser_principal,
                'purchaserCredentials': purchaser_credentials,
                'sourceOfFunds': source_of_funds,
                'locale': locale}

        pattern = reference_number + \
            str(amount) + merchant_account + \
            merchant_reference_number + self.apiKey

        hash_strings = self.generate_hash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)
        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)

        return response.text

    def build_header(self, hash_strings):
        headers = {
            'credentials': self.credential,
            'Accept': 'application/json',
            'principal': self.principal,
            'hash': hash_strings,
            'Content-Type': 'application/json'
        }

        return headers

    def bulk_money_transfer(self, money_transfer_items, bulk_reference_number):
        endpoint = "paga-webservices/business-rest/secured/moneyTransferBulk"

        data = {'items': money_transfer_items,
                'bulkReferenceNumber': bulk_reference_number}

        pattern = money_transfer_items[0]['referenceNumber'] + str(money_transfer_items[0]['amount']) \
            + money_transfer_items[0]['destinationAccount'] + \
            str(len(money_transfer_items)) + self.apiKey

        hash_strings = self.generate_hash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)
        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)

        return response.text

    def onboard_merchant(self, reference_number, merchant_external_id, name, description, address_line1, address_line2,
                         address_city, address_state, address_zip, address_country, first_name, last_name, date_of_birth,
                         phone, email, established_date, website_url, display_name, type, finance_admin_email):

        endpoint = "paga-webservices/business-rest/secured/onboardMerchant"
        json_data = {}
        merchantInfo = {}
        legalEntity = {}
        legalEntityRepresentative = {}
        additionalParameters = {}
        integration = {}

        legalEntity['name'] = name
        legalEntity['description'] = description
        legalEntity['addressLine1'] = address_line1
        legalEntity['addressLine2'] = address_line2
        legalEntity['addressCity'] = address_city
        legalEntity['addressState'] = address_state
        legalEntity['addressZip'] = address_zip
        legalEntity['addressCountry'] = address_country

        legalEntityRepresentative['firstName'] = first_name
        legalEntityRepresentative['lastName'] = last_name
        legalEntityRepresentative['dateOfBirth'] = date_of_birth
        legalEntityRepresentative['phone'] = phone
        legalEntityRepresentative['email'] = email

        additionalParameters['establishedDate'] = established_date
        additionalParameters['websiteUrl'] = website_url
        additionalParameters['displayName'] = display_name

        integration['type'] = type
        integration['financeAdminEmail'] = finance_admin_email

        merchantInfo['legalEntity'] = legalEntity
        merchantInfo['legalEntityRepresentative'] = legalEntityRepresentative
        merchantInfo['additionalParameters'] = additionalParameters

        json_data['reference'] = reference_number
        json_data['merchantExternalId'] = merchant_external_id
        json_data['integration'] = integration
        json_data['merchantInfo'] = merchantInfo

        print(json.dumps(json_data))

        pattern = reference_number+merchant_external_id+name+phone+email+self.apiKey

        hash_strings = self.generate_hash(pattern)

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)
        data = json.dumps(json_data)

        response = post_request(headers, data, server_url)

        return response.text

    def get_transactions(self, *args):
        list_of_transactions = []

        for transaction_elements in args:

            transactions = {
                "referenceNumber": transaction_elements[0],
                "amount": transaction_elements[1],
                "currency": transaction_elements[2],
                "destinationAccount": transaction_elements[3],
                "destinationBank": transaction_elements[4],
                "transferReference": transaction_elements[5],
                "sourceOfFunds": transaction_elements[6],
                "sendWithdrawalCode": transaction_elements[7],
                "suppressRecipientMessage": transaction_elements[8],
                "minRecipentKYCLevel": transaction_elements[9],
                "holdingPeriod": transaction_elements[10]
            }

            list_of_transactions.append(transactions)

        return list_of_transactions

    @staticmethod
    def url(test):
        if test:
            return test_server
        else:
            return live_Server

    @staticmethod
    def generate_hash(pattern):
        hash = hashlib.sha512()
        hash.update(('%s' % (pattern)).encode('utf-8'))
        generated_hash = hash.hexdigest()
        return generated_hash
