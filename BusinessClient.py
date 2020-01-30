import demjson
import requests
import hashlib
import json

from MoneyTransferItem import MoneyTransferItems


def post_request(headers, json_data, url):
    response = requests.request(method="POST", url=url, headers=headers, data=json_data)
    return response


test_server = "https://beta.mypaga.com/"
live_Server = "https://www.mypaga.com/"


class BusinessClient(object):

    def __init__(self, principal, apiKey, credential, test):
        self.principal = principal
        self.apiKey = apiKey
        self.credential = credential
        self.test = test

    def register_customer(self, reference_number, customer_phone_number, customer_email, first_name, last_name,
                          customer_date_birth, customer_gender):
        """ Register Customer

                Parameters
                ----------
                reference_number : string
                    A unique reference number for this request. This same reference number will be returned in the response
                customer_phone_number : string
                    customer_phone_number The phone number of the new customer. This number must not belong to an existing registered customer
                customer_email : string
                    customer_email The email of the new customer
                first_name : string
                    first_name The first name of the customer
                last_name : string
                    last_name The Last name of the customer      
                customer_date_birth : string
                    customer_date_birth Birth date of the customer
                customer_gender : string
                    customer_gender The gender of the new customer. Must be either (FEMALE, MALE)       
                Returns
                 -------
           RegisterCustomerResponse
        """
        endpoint = "paga-webservices/business-rest/secured/registerCustomer"

        data = {'referenceNumber': reference_number,
                'customerPhoneNumber': customer_phone_number,
                'customerEmail': customer_email,
                'customerFirstName': first_name,
                'customerLastName': last_name,
                'customerDateOfBirth': customer_date_birth,
                'customerGender': customer_gender}

        pattern = reference_number + customer_phone_number + first_name + last_name + self.apiKey
        print pattern

        hash_strings = self.generate_hash(pattern)

        # url = self.url(self.test)
        server_url = self.url(self.test) + endpoint
        print server_url
        headers = {
            'credentials': self.credential,
            'Accept': 'application/json',
            'principal': self.principal,
            'hash': hash_strings,
            'Content-Type': 'multipart/form-data'
        }

        customer = json.dumps(data)
        up = {'customer': (customer, "multipart/form-data")}
        print customer
        response = requests.request(method="POST", url=server_url, headers=headers, data=up)
        return response.text

    def money_transfer(self, reference_number, amount, currency, destination_account, destination_bank,
                       sender_principal,
                       sender_credentials, withdrawal_code, source_of_funds, transaction_reference,
                       suppress_recipient_message, locale, alternate_sender_name, mini_recipient_kyc, holding_period):
        """ Money Transfer

                Parameters
                ----------
                reference_number : string
                    A unique reference number for this request. This same reference number will be returned in the response
                amount : double
                    amount The amount of money to transfer to the recipient
                currency : string
                    currency The currency of the operation, if being executed in a foreign currency
                destination_account : string
                    destination_account The account identifier for the recipient receiving the money transfer. 
                    This account identifier may be a phone number, account nickname, or any other unique account identifier supported by the Paga platform. 
                    If destinationBank is specified, this is the bank account number
                destination_bank : string
                    destination_bank For money transfers to a bank account, this is the destination bank code     
                sender_principal : string
                    sender_principal The authentication principal for the user sending money if the money is being sent on behalf of a user.
                     If null, the money transfer will be processed from the 3rd parties own account.
                sender_credentials : string
                    sender_credentials The authentication credentials for the user sending money if the money is being sent on behalf of a user.       
                withdrawal_code : Boolean
                    withdrawal_code If the cash is being sent on behalf of the third party itself (i.e. sender principal is null), 
                    then this indicates whether confirmation messages for funds sent to non Paga customers will include the withdrawal code in the message (true) or omit it (false). 
                    If false, then the withdrawal code will be returned in the withdrawalCode response parameter.
                     For funds sent to Paga customers, the funds are deposited directly into the customer's account so no withdrawal code is necessary. Defaults to true
                source_of_funds : string
                    source_of_funds The name of a source account for funds. If null, the source sender's Paga account will be used as the funding source.
                transaction_reference : string
                    transaction_reference The name of a source account for funds. If null, the source sender's Paga account will be used as the funding source.
                suppress_recipient_message : Boolean
                    suppress_recipient_message Whether to prevent sending an SMS to the recipient of the money transfer. 
                    This can be used in cases where the business wishes to perform their own messaging. Defaults to false, meaning that messages are NOT suppressed.     
                locale : string
                    locale 	The language/locale to be used in messaging. If provided, this must conform to the IETF language tag standard
                alternate_sender_name : string
                    alternate_sender_name The gender of the new customer. Must be either (FEMALE, MALE)
                mini_recipient_kyc : string
                    mini_recipient_kyc The minimum target KYC level the money transfer transaction recipient's paga account must have, can be one of KYC1, KYC2, and KYC3
                holding_period : Integer
                    sender_credentials The number of days with which the recipient's KYC must have before it is reverted back to the sender. 
                    It is only valid if the minKYCLevel is set and it's default to 120 days. If minKYCLevel is set and the recipient?s KYC is below it, 
                    then this will be the number of days it should wait to meet the minKYC Level provided. 
                    If the target KYC is not upgraded within this period the fund will be returned back to the sender?s account.                                                            
                Returns
                 -------
           MoneyTransferResponse
        """

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
        """ Get Merchants

                Parameters
                ----------
                reference_number : string
                    A unique reference number for this request. This same reference number will be returned in the response
                locale : string
                    locale The language/locale to be used in messaging. If provided, this must conform to the IETF language tag standard 
                Returns
                 -------
           GetMerchantResponse
        """

        endpoint = "paga-webservices/business-rest/secured/getMerchants"
        data = {'referenceNumber': reference_number, 'locale': locale}

        pattern = reference_number + self.apiKey

        hash_strings = self.generate_hash(pattern)
        print hash_strings

        url = self.url(self.test)
        server_url = url + endpoint

        headers = self.build_header(hash_strings)

        json_data = json.dumps(data)
        response = post_request(headers, json_data, server_url)
        return response.text

    def airtime_purchase(self, reference_number, amount, currency, destination_number,
                         purchaser_principal, purchaser_credentials, source_of_funds, locale):
        """ Airtime Purchase

                Parameters
                ----------
                reference_number : string
                    A unique reference number for this request. This same reference number will be returned in the response
                amount : double
                    amount The amount of airtime to purchase
                currency : string
                    The currency of the operation, if being executed in a foreign currency
                destination_number : string
                    destination_number The first name of the customer
                purchaser_principal : string
                    purchaser_principal The Last name of the customer      
                purchaser_credentials : string
                    purchaser_credentials Birth date of the customer
                source_of_funds : string
                    source_of_funds The gender of the new customer. Must be either (FEMALE, MALE)   
                locale : string
                    locale The language/locale to be used in messaging. If provided, this must conform to the IETF language tag standard         
                Returns
                 -------
           Airtime Purchase Response
        """

        endpoint = "paga-webservices/business-rest/secured/airtimePurchase"

        data = {'referenceNumber': reference_number,
                'amount': amount,
                'currency': currency,
                'destinationPhoneNumber': destination_number,
                'purchaserPrincipal': purchaser_principal,
                'purchaser_principal': purchaser_credentials,
                'sourceOfFunds': source_of_funds,
                'locale': locale}
        pattern = reference_number + str(amount) + destination_number + self.apiKey

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
        """ Validate Deposit to Bank

                Parameters
                ----------
                reference_number : string
                    A unique reference number for this request. This same reference number will be returned in the response
                amount : double
                    amount The amount of airtime to purchase
                currency : string
                    The currency of the operation, if being executed in a foreign currency
                destination_bank_uuid : string
                    destination_bank_uuid The Paga bank UUID identifying the bank to which the deposit will be made. 
                    In order to get the list of supported banks and bank UUIDs, execute the getBanks operation defined in this document. 
                    Bank codes will not change though additional banks may be added to the list in the future.
                destination_bank_acct_no : string
                    destination_bank_acct_no The ten digit NUBAN bank account number for the account to which the deposit will be made. 
                    This number should be a valid account number for the destination bank as specified by the destinationBankCode parameter above. 
                    Executing operation will validate this number and if valid, return the account holder name as stored at the bank for this account.     
                recipient_phone_number : string
                    recipient_phone_number The mobile phone number of the recipient of the deposit to bank transaction. 
                    Either one or both of this parameter and the recipientEmail parameter must be provided. 
                    If this parameter is provided, this operation will validate that it is a valid phone number.
                recipient_mobile_operator_code : string
                    recipient_mobile_operator_code Ignored if recipientPhoneNumber parameter is not provided. 
                    This describes the mobile operator that the recipientPhoneNumber belongs to. 
                    If recipientPhoneNumber is provided, but this parameter is not, a default mobile operator will selected based on the phone number pattern, 
                    but this may not be correct due to number portability of mobile phone numbers and may result in delayed or failed delivery of any SMS messages to the recipient.
                recipient_email : string
                    recipient_email The email address of the recipient of the deposit to bank transaction.
                     Either one or both of this parameter and the recipientPhoneNumber parameter must be provided.
                     If this parameter is provided, this operation will validate that it is a valid email address format.
                recipient_name : string
                    recipient_name The name of the recipient. This parameter is currently bot validated.         
                locale : string
                    locale The language/locale to be used in messaging. If provided, this must conform to the IETF language tag standard         
                Returns
                 -------
           ValidateDepositBankResponse
        """

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

        pattern = reference_number + str(amount) + destination_bank_uuid + destination_bank_acct_no + self.apiKey

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
        """ Deposit to Bank

                Parameters
                ----------
                reference_number : string
                    A unique reference number for this request. This same reference number will be returned in the response
                amount : double
                    amount The amount of airtime to purchase
                currency : string
                    The currency of the operation, if being executed in a foreign currency
                destination_bank_uuid : string
                    destination_bank_uuid The Paga bank UUID identifying the bank to which the deposit will be made. 
                    In order to get the list of supported banks and bank UUIDs, execute the getBanks operation defined in this document. 
                    Bank codes will not change though additional banks may be added to the list in the future.
                destination_bank_acct_no : string
                    destination_bank_acct_no The ten digit NUBAN bank account number for the account to which the deposit will be made. 
                    This number should be a valid account number for the destination bank as specified by the destinationBankCode parameter above. 
                    Executing operation will validate this number and if valid, return the account holder name as stored at the bank for this account.     
                recipient_phone_number : string
                    recipient_phone_number The mobile phone number of the recipient of the deposit to bank transaction. 
                    Either one or both of this parameter and the recipientEmail parameter must be provided. 
                    If this parameter is provided, this operation will validate that it is a valid phone number.
                recipient_mobile_operator_code : string
                    recipient_mobile_operator_code Ignored if recipientPhoneNumber parameter is not provided. 
                    This describes the mobile operator that the recipientPhoneNumber belongs to. 
                    If recipientPhoneNumber is provided, but this parameter is not, a default mobile operator will selected based on the phone number pattern, 
                    but this may not be correct due to number portability of mobile phone numbers and may result in delayed or failed delivery of any SMS messages to the recipient.
                recipient_email : string
                    recipient_email The email address of the recipient of the deposit to bank transaction.
                     Either one or both of this parameter and the recipientPhoneNumber parameter must be provided.
                     If this parameter is provided, this operation will validate that it is a valid email address format.
                recipient_name : string
                    recipient_name The name of the recipient. This parameter is currently bot validated.   
                alt_sender_name : string
                    alt_sender_name In notifications sent to the recipient, your business display name (if set), or business name (if display name not set) is included. 
                    If you wish notifications to indicate the deposit to bank as coming from an alternate name, you may set the alternate name in this parameter. 
                    This parameter length is limited to 20 characters and will be truncated if longer. 
                suppress_recipient_msg : Boolean
                    suppress_recipient_msg If this field is set to true, no notification message (SMS or email) will be sent to the recipient. 
                    IF omitted or set to false, an email or SMS will be sent to recipient as described above.
                remarks : string
                    remarks Additional bank transfer remarks that you may wish to appear on your bank statement record for this transaction. 
                    Remarks are limited to 30 characters and will be truncated if longer.                   
                locale : string
                    locale The language/locale to be used in messaging. If provided, this must conform to the IETF language tag standard         
                Returns
                 -------
           DepositBankResponse
        """

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
        """ Get Account Balance

                Parameters
                ----------
                reference_number : string
                    A unique reference number for this request. This same reference number will be returned in the response
                acct_principal : string
                    acct_principal The authentication principal for the user who's balance is being inquired, if the inquiry is being made on behalf of a user.
                     If null, the balance inquiry will be processed from the 3rd parties own account.     
                acct_credentials : string
                    acct_credentials Birth date of the customer
                source_of_funds : string
                    source_of_funds The authentication credentials for the user who's balance is being inquired, if the inquiry is being made on behalf of a user.   
                locale : string
                    locale The language/locale to be used in messaging. If provided, this must conform to the IETF language tag standard         
                Returns
                 -------
           Account Balance Response
        """

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
        """ Get Transaction History

                Parameters
                ----------
                reference_number : string
                    A unique reference number for this request. This same reference number will be returned in the response
                acct_principal : string
                    acct_principal The authentication principal for the user who's balance is being inquired, if the inquiry is being made on behalf of a user.
                     If null, the balance inquiry will be processed from the 3rd parties own account.     
                acct_credentials : string
                    acct_credentials Birth date of the customer
                start_date : string
                    start_date The start date of the interval for which transaction history results should be returned. 
                    The results are inclusive of this date and it should include hour, minute and second values in addition to the date. 
                end_date : string
                    end_date The start date of the interval for which transaction history results should be returned. 
                    The results are exclusive of this date and it should include hour, minute and second values in addition to the date.      
                locale : string
                    locale The language/locale to be used in messaging. If provided, this must conform to the IETF language tag standard         
                Returns
                 -------
           Get Transaction History Response
        """

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
        """ Get Recent Transaction History

                Parameters
                ----------
                reference_number : string
                    A unique reference number for this request. This same reference number will be returned in the response
                acct_principal : string
                    acct_principal The authentication principal for the user who's balance is being inquired, if the inquiry is being made on behalf of a user.
                     If null, the balance inquiry will be processed from the 3rd parties own account.     
                acct_credentials : string
                    acct_credentials Birth date of the customer      
                locale : string
                    locale The language/locale to be used in messaging. If provided, this must conform to the IETF language tag standard         
                Returns
                 -------
           Get Recent Transaction History Response
        """

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
        """ Get Operation Status

                Parameters
                ----------
                reference_number : string
                    A unique reference number for this request. This same reference number will be returned in the response      
                locale : string
                    locale The language/locale to be used in messaging. If provided, this must conform to the IETF language tag standard         
                Returns
                 -------
           Get Operation Status
        """

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
        """ Get Bank

                Parameters
                ----------
                reference_number : string
                    A unique reference number for this request. This same reference number will be returned in the response      
                locale : string
                    locale The language/locale to be used in messaging. If provided, this must conform to the IETF language tag standard         
                Returns
                 -------
           Get Bank Response
        """

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
        """ Get Merchant Services

                Parameters
                ----------
                reference_number : string
                    A unique reference number for this request. This same reference number will be returned in the response 
                merchant_public_id : string
                    merchant_public_id The identifier which uniquely identifies the merchant on the Paga platform. i.e Merchant Public Id         
                locale : string
                    locale The language/locale to be used in messaging. If provided, this must conform to the IETF language tag standard         
                Returns
                 -------
           Get Merchant Services Response
        """

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
        """ Get Mobile Operators

               Parameters
               ----------
               reference_number : string
                   A unique reference number for this request. This same reference number will be returned in the response
               locale : string
                   locale The language/locale to be used in messaging. If provided, this must conform to the IETF language tag standard
               Returns
                -------
          Get Mobile Operators Response
       """

        endpoint = "paga-webservices/business-rest/secured/getMobileOperators"

        data = {'referenceNumber': reference_number,'locale': locale}

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
    """ Merchant Payment

            Parameters
            ----------
            reference_number : string
                A unique reference number for this request. This same reference number will be returned in the response
            amount : double
                amount The amount of airtime to purchase
            currency : string
                The currency of the operation, if being executed in a foreign currency
            merchant_account : string
               The account number identifying the merchant (eg. merchant Id, UUID)
            merchant_reference_number : string
                merchant_reference_number The account/reference number identifying the customer on the merchant's system
            merchant_service : string
                merchant_service The list of merchant service codes specifying which of the merchant's services are being paid for
            purchaser_principal : string
                purchaser_principal The authentication principal for the user paying the merchant if the payment is being made on behalf of a user.
                If null, the airtime will be processed from the 3rd parties own account.
            purchaser_credentials : string
                purchaser_credentials The authentication credentials for the user paying the merchant if the payment is being made on behalf of a user.
            source_of_funds : string
                source_of_funds The name of a source account for funds. If null, the source purchaser's Paga account will be used as the funding source.
            locale : string
                locale The language/locale to be used in messaging. If provided, this must conform to the IETF language tag standard
            Returns
             -------
       Merchant Payment Response
    """

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

    pattern = reference_number + str(amount) + merchant_account + merchant_reference_number + self.apiKey

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
    """ Bulk Money Transfer
           The Bulk Money Transfer operation enables an integrated 3rd party to utilize the Paga
           platform to execute the money transfer operation described  above to multiple recipients
           simultaneously. This is limited to 300 payment items per bulk operation.
           Returns
            -------
      Bulk Money Transfer Response
   """


    endpoint = "paga-webservices/business-rest/secured/moneyTransferBulk"

    data = {'items': money_transfer_items,
        'bulkReferenceNumber': bulk_reference_number}


    pattern = money_transfer_items[0]['referenceNumber'] + str(money_transfer_items[0]['amount']) \
          + money_transfer_items[0]['destinationAccount'] + str(len(money_transfer_items)) + self.apiKey

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
    """ Onboard Merchant

            The  Onboard Merchant operation, allows Aggregator Organizations to create sub organizations on the paga platform.
             -------
       Onboard Merchant
    """

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

    pattern = reference_number + merchant_external_id + name + phone + email + self.apiKey
    print pattern

    hash_strings = self.generate_hash(pattern)

    print hash_strings

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

    print len(list_of_transactions)
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
