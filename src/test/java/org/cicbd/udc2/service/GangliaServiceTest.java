package org.cicbd.udc2.service;

import java.io.IOException;

import org.cicbd.udc2.config.AbstractTestConfig;
import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class GangliaServiceTest extends AbstractTestConfig{
	
	@Autowired
	private GangliaService gangliaService;
	
	@Test
	public void testInstallAgent() throws IOException {
		gangliaService.installAgent("192.168.32.128", "root", "000000");
	}

	@Test
	public void testInstallServer() throws IOException {
		gangliaService.installServer("192.168.32.128", "root", "000000");
	}
	
	@Test
	public void testInstallSinker() throws IOException {
		gangliaService.installSinker("192.168.1.32", "serveradmin", "serveradmin");
	}

}
