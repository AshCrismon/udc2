package org.cicbd.udc2.helper;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

import org.cicbd.udc2.model.MetricData;
import org.cicbd.udc2.model.MetricInfo;

public abstract class MetricAdaptor {
	
	/**
	 * Input :
	 * {
	 * 		collectionName 	--> cid
	 * 		metricName		-->	metric
	 * 		data			--> [{clock: "", value: ""}, ...]
	 * }
	 * 
	 * Output:
	 * {
	 * 		cid: "clustername/hostname"
	 * 		metric: {
	 * 			"name": "cpu_idle",
	 * 			"title": "",
	 * 			"desc": "",
	 * 			"group": "",
	 * 			"units": "",
	 * 			"series": {clock: value, ...},
	 * 		}
	 * }
	 * @param collectionName
	 * @param metricName
	 * @param metrics
	 * @return
	 */
	public static Map<String, Object> adapt(String collectionName, String metricName, List<MetricData> metricData, MetricInfo metricInfo){
		Map<String, Object> result = new HashMap<>();
		Map<String, Object> metric = new HashMap<>();
		
		Map<Long, String> series = new TreeMap<>();
		for(MetricData md : metricData){
			series.put(md.getClock(), md.getValue());
		}
		
		metric.put("name", metricName);
		metric.put("series", series);
		if(metricInfo != null){
			metric.put("title", metricInfo.getTITLE());
			metric.put("desc", metricInfo.getDESC());
			metric.put("group", metricInfo.getGROUP());
		}
		
		result.put("cid", collectionName);
		result.put("metric", metric);
		return result;
	}
}
