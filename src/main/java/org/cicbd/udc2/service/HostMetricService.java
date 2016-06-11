package org.cicbd.udc2.service;

import java.util.Map;

public interface HostMetricService<T> extends MetricService<T>{

	/**
	 * fetch the metric data from the specified collection, 
	 * the time range of the metric data is also specified
	 * @param collectionName
	 * @param metricName
	 * @param beginTime
	 * @param endTime
	 * @return
	 */
	Map<String, Object> findMetricData(String collectionName, String metricName, long beginTime, long endTime);
	
}
