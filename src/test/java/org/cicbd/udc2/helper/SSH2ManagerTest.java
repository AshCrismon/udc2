package org.cicbd.udc2.helper;

import java.io.IOException;

import org.cicbd.udc2.helper.SSH2Manager.SSH2Client;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class SSH2ManagerTest {
	
	private SSH2Client client;
	
	@Before
	public void login() throws IOException{
		client = SSH2Manager.connect("192.168.1.113", "serveradmin", "serveradmin");
	}

	@Test
	public void testSSH2Client() throws IOException {
		client.execCommand("ls -l");
		System.out.println(client.getLastExecuteStatus());
	}
	
	@Test
	public void testSCPClient() throws IOException{
		client.putShell("src/main/shell/ganglia_install.sh", "~");
		client.putShell("src/main/shell/ganglia_install.sh", "~");
	}
	
	@Test
	public void testPutShellAndExecute() throws IOException{
//		client.putShell("src/main/shell/ganglia_install.sh", "~");
//		client.put("tar/ganglia.tar.gz", "~");
		client.execCommand("./ganglia_install.sh");
	}
	
	@After
	public void disConnect(){
		client.disConnect();
	}
}
