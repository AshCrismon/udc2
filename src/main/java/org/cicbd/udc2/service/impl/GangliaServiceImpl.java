package org.cicbd.udc2.service.impl;

import java.io.IOException;

import org.cicbd.udc2.helper.SSH2Manager;
import org.cicbd.udc2.helper.SSH2Manager.SSH2Client;
import org.cicbd.udc2.service.GangliaService;
import org.springframework.stereotype.Service;

@Service
public class GangliaServiceImpl implements GangliaService{

	@Override
	public void installAgent(String host, String user, String password) throws IOException {
		SSH2Client client = SSH2Manager.connect(host, user, password);
		client.put("src/main/install/ganglia-3.7.1.tar.gz", "~");
		client.putShell("src/main/shell/ganglia_install.sh", "~");
		client.execCommand("./ganglia_install.sh gmond");
	}

	@Override
	public void installServer(String host, String user, String password) throws IOException {
		SSH2Client client = SSH2Manager.connect(host, user, password);
		client.put("src/main/install/ganglia-3.7.1.tar.gz", "~");
		client.putShell("src/main/shell/ganglia_install.sh", "~");
		client.execCommand("./ganglia_install.sh gmetad");
		
		client.put("src/main/python/monitor.py", "/usr/local/ganglia");
		client.execCommand("pip install xmpppy");
		client.execCommand("python /usr/local/ganglia/monitor.py");
	}
	
	@Override
	public void installSinker(String host, String user, String password) throws IOException {
		SSH2Client client = SSH2Manager.connect(host, user, password);
		client.put("src/main/python/sinker.py", "~");
//		client.execCommand("pip install xmpppy");
		client.execCommand("pwd");
		client.execCommand("python sinker.py --mongodb 192.168.1.13:27017");
	}

}
