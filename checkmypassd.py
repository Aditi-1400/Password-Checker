import requests
import hashlib
import sys

def request_api_data(query_char):
	url = 'https://api.pwnedpasswords.com/range/' + query_char
	res = requests.get(url)
	if res.status_code != 200:
		raise RuntimeError(f'Error fetching: {res.status_code}, check')
	return res

def get_password(hashes, to_check):
	hashes = (line.split(':') for line in hashes.text.splitlines())
	for h, count in hashes:
		if h == to_check:
			return count
	return 0

def pwned_api_check(password):
	sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first5char, tail = sha1password[:5], sha1password[5:]
	response = request_api_data(first5char)
	
	return get_password(response, tail)

def main(args):
	for password in args:
		count = pwned_api_check(password)
		if(count):
			print(f'{password} found {count} times')
		else:
			print("password not found")
	return 'done!'

if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))