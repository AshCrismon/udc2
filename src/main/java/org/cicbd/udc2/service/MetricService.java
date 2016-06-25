package org.cicbd.udc2.service;

import java.util.Map;

public interface MetricService {

	/**
	 * Fetch the specified metric data, the data format is just like below:
	 *{
	 * 		cid: "clustername/hostname"
	 * 		metric: {
	 * 			"name": "cpu_idle",
	 * 			"title": "",
	 * 			"desc": "",
	 * 			"group": "",
	 * 			"series": {clock: value, ...},
	 * 		}
	 * }
	 * @param mid metric id
	 * @param beginTime
	 * @param endTime
	 * @return
	 */
	public Map<String, Object> findMetric(String mid, long beginTime, long endTime);
	
	public Map<String, Object> findMetric(String cid, String metricName, long beginTime, long endTime);
}
