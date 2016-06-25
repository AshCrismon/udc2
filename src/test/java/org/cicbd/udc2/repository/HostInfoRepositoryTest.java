package org.cicbd.udc2.repository;

import java.util.List;

import org.cicbd.udc2.config.AbstractTestConfig;
import org.cicbd.udc2.model.HostInfo;
import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class HostInfoRepositoryTest extends AbstractTestConfig {

	@Autowired
	private HostInfoRepository hostInfoRepository;
	
	@Test
	public void testFindAll(){
		List<HostInfo> result = hostInfoRepository.findAll("host_info");
		print("total records: " + result.size());
		print(result);
	}
	
	@Test
	public void testFindByHid(){
		String hid = "cloudservers/192.168.1.32";
		HostInfo result = hostInfoRepository.findHostInfo(hid);
		print("host information");
		print(result);
	}
}
