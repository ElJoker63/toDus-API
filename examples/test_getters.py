import os
from todus.client import ToDusClient2

PHONE = os.getenv("TODUS_PHONE")
PASSWORD = os.getenv("TODUS_PASSWORD")

client = ToDusClient2(PHONE, PASSWORD)
client.login()

print("1. Profile Privacy:")
try:
    print(client.get_profile_privacy())
except Exception as e:
    print(e)

print("2. Group Privacy:")
try:
    print(client.get_group_privacy())
except Exception as e:
    print(e)

print("3. Near Status:")
try:
    print(client.get_near_status())
except Exception as e:
    print(e)

print("4. Block List:")
try:
    print(client.get_block_list())
except Exception as e:
    print(e)

print("5. Followers:")
try:
    print(client.get_followers())
except Exception as e:
    print(e)
