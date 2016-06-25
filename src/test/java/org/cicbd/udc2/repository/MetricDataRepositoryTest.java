package org.cicbd.udc2.repository;

import java.util.List;
import org.cicbd.udc2.config.AbstractTestConfig;
import org.cicbd.udc2.model.MetricData;
import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;

public class MetricDataRepositoryTest extends AbstractTestConfig {

	@Autowired
	private MetricDataRepository metricDataRepository;
	
	@Test
	public void testFindAll(){
		String collectionName = "cloudservers/192.168.1.32";
		List<MetricData> result = metricDataRepository.findAll(collectionName);
		print("total records: " + result.size());
		print(result);
	}
	
	@Test
	public void testFindMetricData(){
		String collectionName = "cloudservers/192.168.1.32";
		long beginTime = System.currentTimeMillis() - 1 * 24 * 3600;
		long endTime = System.currentTimeMillis();
		String queryStr = "{metric: 'cpu_aidle', timestamp: {$gte: " + beginTime + ", $lte: " + endTime + "}}";
		List<MetricData> result = metricDataRepository.findMetricData(collectionName, queryStr);
		print("total records: " + result.size());
		print(result);
		
	}
	
	@Test
	public void testFindMetricData2(){
		String collectionName = "cloudservers/192.168.1.32";
		String metricName = "cpu_aidle";
		long beginTime = System.currentTimeMillis() - 1 * 24 * 3600;
		long endTime = System.currentTimeMillis();
		List<MetricData> result = metricDataRepository.findMetricData(collectionName, metricName, beginTime, endTime);
		print("total records: " + result.size());
		print(result);
	}
	
}
