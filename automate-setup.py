import mechanize
import os
import time 
import requests
import re

psql_host = os.environ['DB_HOST']
psql_user = "root"
psql_pass = os.environ['DB_PASS']
psql_db   = os.environ['DB_NAME']

confluence_title = "Automated Confluence Initial Setup"
confluence_key = os.environ['KEY']

confluence_admin_email = os.environ['ADMIN_EMAIL']
confluence_admin_user  = os.environ['ADMIN_USERNAME']
confluence_admin_pass  = os.environ['ADMIN_PASSWORD']
confluence_admin_firstname = os.environ['ADMIN_FIRST_NAME']
confluence_admin_lastname = os.environ['ADMIN_LAST_NAME']


url='https://confluence.shs-dev.dsa-notprod.homeoffice.gov.uk'

# Set up mechanize browser
br = mechanize.Browser()
br.set_handle_robots(False)
br.open(url)

# Choose setup mode = Production Installation
br.select_form(nr=0)
br.form.find_control('setupType').readonly = False
br.form['setupType'] = 'custom'
res = br.submit()
print("Submitted install type OK")

# Fill in the license key
br.select_form(nr=0)
br.form['confLicenseString']=confluence_key
br.submit()
print("Submitted license OK")


# Select Own DB 
br.select_form(nr=0)
br.submit()
print("Chose DB OK")


# # Fill in the PSQL data
br.select_form(nr=0)
br.form['dbConfigInfo.hostname'] = psql_host
br.form['dbConfigInfo.port'] = '5432'
br.form['dbConfigInfo.databaseName'] = psql_db
br.form['dbConfigInfo.userName'] = psql_user
br.form['dbConfigInfo.password'] = psql_pass
br.submit()
print("Submitted PostgreSQL host OK")

# Checking status of website - pods can go down 
stat=str(requests.get(url).status_code)
time.sleep(60)
print("Waiting for pods")
if re.search('50.',stat):
    time.sleep(60)
    print("Still waiting for pods")
else:
    print("Confluence up")

# Select the type of site as an empty site

br.select_form(nr=1)
br.submit()
print("Set up as empty site OK")


# Manage users internally
br.select_form(nr=0)
br.submit()
print("Set up user management OK")


# Create the admin user
br.select_form(nr=0)
br.form['fullName'] = "{}".format(confluence_admin_firstname)
br.form['email'] = confluence_admin_email
br.form['username'] = confluence_admin_user
br.form['password'] = confluence_admin_pass
br.form['confirm'] = confluence_admin_pass
br.submit()

print("Set up admin OK")

print("DONE")

