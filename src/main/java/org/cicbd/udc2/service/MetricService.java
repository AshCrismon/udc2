package org.cicbd.udc2.service;

import java.util.List;

public interface MetricService<T> {

	/**
	 * fetch the metric data from the specified collection according to the query string 
	 * such as "{metric: 'cpu_aidle', clock: {$gte: beginTime, $lte: endTime}}"
	 * @param collectionName
	 * @param query
	 * @return
	 */
	List<T> findMetricData(String collectionName, String query);
	
	/**
	 * fetch the metric data from the specified collection according to the query string 
	 * such as "{metric: 'cpu_aidle', clock: {$gte: beginTime, $lte: endTime}}", and
	 * return the specified fields
	 * @param collectionName
	 * @param query
	 * @param fields
	 * @return
	 */
	List<T> findMetricData(String collectionName, String query, String fields);

}
