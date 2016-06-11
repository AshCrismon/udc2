package org.cicbd.udc2.service.impl;

import java.net.UnknownHostException;
import java.util.List;
import java.util.Map;

import org.cicbd.udc2.config.AbstractTestConfig;
import org.cicbd.udc2.service.HostMetricService;
import org.cicbd.udc2.vo.MetricVo;
import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;

import com.alibaba.fastjson.JSONObject;

public class HostMetricServiceTest extends AbstractTestConfig {

	@Autowired
	private HostMetricService<MetricVo> metricService;

	@Test
	public void testFindMetricData() throws UnknownHostException {
		String collectionName = "ganglia.cloudserver";
		String queryStr = "{metric: 'cpu_aidle', timestamp: {$gte: 1460713845, $lte: 1460723845}}";
		List<MetricVo> metrics = metricService.findMetricData(collectionName, queryStr);
		print("total records: " + metrics.size());
		for (MetricVo metric : metrics) {
			print(metric.toString());
		}
	}
	
	@Test
	public void testFindMetricData2(){
		String collectionName = "ganglia.cloudserver";
		String metricName = "cpu_aidle";
		long beginTime = 1460713845;
		long endTime = 1460723845;
		Map<String, Object> result = metricService.findMetricData(collectionName, metricName, beginTime, endTime);
		print("total records: " + result.size());
		print("hostname : " + result.get("hostname"));
		
		print(JSONObject.toJSONString(result));
	}
}
