import urllib
import urllib2

config = None

def configure(publisher_key, scoring_key, ws_host='ws.areyouahuman.com'):
    """
    Sets the publisher key and scoring key needed to make subsequent calls to the areyouahuman API. Call this function
    once when your application initializes.

    publisher_key
        Identifies you and your application to areyouahuman.com.
    scoring_key
        Used to retrieve pass or fail results from areyouahuman.com.
    ws_host
        Web service host for areyouahuman calls (no trailing slash). Defaults to 'ws.areyouahuman.com'.
    """
    publisher_url = ''.join([
        'https://',
        ws_host,
        '/ws/script/',
        urllib2.quote(publisher_key, safe='')])
    publisher_html = ''.join([
        '<div id="AYAH"></div><script type="text/javascript" src="',
        publisher_url,
        '"></script>'])
    scoring_url = ''.join([
        'https://',
        ws_host,
        '/ws/scoreGame'])
    global config
    config = { 'publisher_key': publisher_key,
               'scoring_key': scoring_key,
               'ws_host': ws_host,
               'publisher_url': publisher_url,
               'publisher_html': publisher_html,
               'scoring_url': scoring_url }

def check_configuration():
    if config == None:
        raise Exception('You must call ayah.configure() before using this API.')

def get_publisher_html():
    """
    Gets the HTML markup that displays the PlayThru content to the alleged human. When the alleged human finishes
    the PlayThru challenge, pass the value of the hidden input field with id='session_secret' to score_result().
    """
    check_configuration()
    return config['publisher_html']

def score_result(session_secret):
    """
    Returns True or False indicating whether the alleged human succeeded in satisfying the PlayThru challenge.

    session_secret
        Pass in the value of the hidden input field with id='session_secret'.
    """
    check_configuration()
    data = { 'scoring_key': config['scoring_key'],
             'session_secret': session_secret }
    values = urllib.urlencode(data)
    response = urllib2.urlopen(config['scoring_url'], values)
    result = False
    if response.code == 200:
        content = response.readline()
        dict = eval(content)
        result = (int(dict['status_code']) == 1)
    return result

def record_conversion(session_secret):
	"""
	Returns the HTML needed to be embedded in the confirmation page after a form submission.
	Once the code loads on the page it will record a conversion with our system.
	
	session_secret
		Pass in the value of the hidden input field with id='session_secret'
	"""
	check_configuration()
	conversion_url = ''.join([
	'<iframe style="border: none;" height="0" width="0" src="https://',
	ws_host,
	'/ws/recordConversion/',
	session_secret,
	'"></iframe>'])
	return conversion_url