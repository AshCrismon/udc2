package org.cicbd.udc2.service;

import java.util.Map;

import org.cicbd.udc2.config.AbstractTestConfig;
import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class MetricServiceTest extends AbstractTestConfig {
	
	@Autowired
	private MetricService metricService;
	
	@Test
	public void testFindMetric(){
		String mid = "cloudservers/192.168.1.32/cpu_aidle";
		long beginTime = System.currentTimeMillis() - 1 * 24 * 3600;
		long endTime = System.currentTimeMillis();
		Map<String, Object> result = metricService.findMetric(mid, beginTime, endTime);
		print("total records: " + result.size());
		print(result.entrySet());
	}
	
	@Test
	public void testFindMetric2(){
		String cid = "cloudservers/192.168.1.32";
		String metricName = "cpu_aidle";
		long beginTime = System.currentTimeMillis() - 1 * 24 * 3600;
		long endTime = System.currentTimeMillis();
		Map<String, Object> result = metricService.findMetric(cid, metricName, beginTime, endTime);
		print("total records: " + result.size());
		print(result.entrySet());
	}
}
