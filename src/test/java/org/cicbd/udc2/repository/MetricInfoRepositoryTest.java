package org.cicbd.udc2.repository;

import java.util.List;

import org.cicbd.udc2.config.AbstractTestConfig;
import org.cicbd.udc2.model.MetricInfo;
import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class MetricInfoRepositoryTest extends AbstractTestConfig {

	@Autowired
	private MetricInfoRepository metricInfoRepository;
	
	@Test
	public void testFindAll(){
		String collectionName = "metric_info";
		List<MetricInfo> result = metricInfoRepository.findAll(collectionName);
		print("total records: " + result.size());
		print(result.toString());
	}
	
	@Test
	public void testFindByMid(){
		String mid = "cloudservers/192.168.1.32/cpu_aidle";
		MetricInfo result = metricInfoRepository.findMetricInfo(mid);
		print("metric information");
		print(result);
	}
}
