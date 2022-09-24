#coding=utf-8
#!/usr/bin/python
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Lists all the apks for a given app."""

import argparse

import apiclient

# from apiclient.discovery import build
import httplib2
import time
from googleapiclient.discovery import build
from oauth2client import client
from oauth2client.service_account import ServiceAccountCredentials

K_P12 = '/Users/gan/Downloads/lustrous-camera-327609-2898732a6732.p12'
SERVICE_ACCOUNT_EMAIL = ('gama-gsservice-refund@lustrous-camera-327609.iam.gserviceaccount.com')
package_namae_11 = 'com.gamamobi.iktw'

# K_P12 = '/Users/gan/Downloads/pc-api-6907385374250876574-272-f0c45adebfca.p12'
# SERVICE_ACCOUNT_EMAIL = ('id-newgama-gs-server-refund01@pc-api-6907385374250876574-272.iam.gserviceaccount.com')
# package_namae_11 = 'com.gamamobi.twsm'

def main():
  # Load the key in PKCS 12 format that you downloaded from the Google APIs
  # Console when you created your Service account.
  f = file(K_P12, 'rb')
  key = f.read()
  f.close()

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with the Credentials. Note that the first parameter, service_account_name,
  # is the Email address created for the Service account. It must be the email
  # address associated with the key that was created.
  # credentials = client.SignedJwtAssertionCredentials(
  #     SERVICE_ACCOUNT_EMAIL,
  #     key,
  #     scope='https://www.googleapis.com/auth/androidpublisher')

  credentials = ServiceAccountCredentials.from_p12_keyfile(service_account_email=SERVICE_ACCOUNT_EMAIL, filename=K_P12, scopes='https://www.googleapis.com/auth/androidpublisher')
  http = httplib2.Http()
  http = credentials.authorize(http)

  service = build('androidpublisher', 'v3', http=http)

  package_name = package_namae_11

  # try:
  #
  #   edit_request = service.edits().insert(body={}, packageName=package_name)
  #   result = edit_request.execute()
  #   edit_id = result['id']
  #
  #   apks_result = service.edits().apks().list(
  #     editId=edit_id, packageName=package_name).execute()
  #
  #   for apk in apks_result['apks']:
  #     print 'versionCode: %s, binary.sha1: %s' % (
  #       apk['versionCode'], apk['binary']['sha1'])
  #
  # except client.AccessTokenRefreshError:
  #   print ('The credentials have been revoked or expired, please re-run the '
  #          'application to re-authorize')


  try:
    # pay_result = service.purchases().voidedpurchases().list(packageName=package_name, startTime=format_2_timestamp('2020-02-6 00:00:00') * 1000, endTime=format_2_timestamp('2020-02-7 00:00:00')* 1000).execute()
    pay_result = service.purchases().voidedpurchases().list(packageName=package_name).execute()
    print pay_result
    print u'长度：' + str(len(pay_result['voidedPurchases']))
    for paymm in pay_result['voidedPurchases']:
      print 'orderId: %s, voidedSource: %s , voidedReason: %s , purchaseTime: %s , voidedTime: %s' % (
          paymm['orderId'], paymm['voidedSource'], paymm['voidedReason'], makeTime(paymm['purchaseTimeMillis']), makeTime(paymm['voidedTimeMillis']))

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')


def makeTime(timestamp):
  # timestamp = 1462451334

  # change to localtime
  time_local = time.localtime(long(timestamp) / 1000)
  # change to sample(2016-05-05 20:28:54)
  dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
  return dt

def format_2_timestamp(format_time):
  ts = time.strptime(format_time, "%Y-%m-%d %H:%M:%S")
  aaa=time.mktime(ts)
  print aaa
  print int(aaa)
  return int(aaa)


if __name__ == '__main__':
  main()
  # aaa = format_2_timestamp('2019-10-1 00:00:00')
