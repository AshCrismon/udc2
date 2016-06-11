package org.cicbd.udc2.helper;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.cicbd.udc2.vo.MetricVo;

public abstract class HostDataSinker {
	
	/**
	 * the formatted data is like below:
	 * {
	 * 		hostname: "hostname",
	 * 		metrics: [
	 * 			{
	 * 				"metric": "cpu_idle",
	 * 				"data": [{clock: "", value: ""}, ...],
	 * 			},
	 * 			...
	 * 		]
	 * }
	 * @param collectionName
	 * @param metricName
	 * @param metrics
	 * @return
	 */
	public static Map<String, Object> sink(String collectionName, String metricName, List<MetricVo> data){
		List<Map<String, Object>> metricList = new ArrayList<>();
		Map<String, Object> metricInfo = new HashMap<>();
		metricInfo.put("metric", metricName);
		metricInfo.put("data", data);
		metricList.add(metricInfo);
		
		Map<String, Object> result = new HashMap<>();
		result.put("hostname", collectionName);
		result.put("metrics", metricList);
		return result;
	}
}
